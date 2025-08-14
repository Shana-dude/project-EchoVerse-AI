"""
EchoVerse History Manager
Manages user's past audiobook generations and interactions like ChatGPT
"""

import streamlit as st
import json
import time
from datetime import datetime
import os

class HistoryManager:
    def __init__(self):
        self.history_file = "user_history.json"
        self.load_history()
    
    def load_history(self):
        """Load user history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    st.session_state.user_history = json.load(f)
            else:
                st.session_state.user_history = []
        except Exception as e:
            st.session_state.user_history = []
    
    def save_history(self):
        """Save user history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(st.session_state.user_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Failed to save history: {str(e)}")
    
    def add_generation_to_history(self, original_text, rewritten_text, tone, voice, language):
        """Add a new audiobook generation to history"""
        if not hasattr(st.session_state, 'user_history'):
            st.session_state.user_history = []
        
        history_entry = {
            "id": f"gen_{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "type": "audiobook_generation",
            "title": self._generate_title(original_text),
            "original_text": original_text[:500] + "..." if len(original_text) > 500 else original_text,
            "rewritten_text": rewritten_text[:500] + "..." if len(rewritten_text) > 500 else rewritten_text,
            "full_original": original_text,
            "full_rewritten": rewritten_text,
            "settings": {
                "tone": tone,
                "voice": voice,
                "language": language
            },
            "stats": {
                "original_words": len(original_text.split()),
                "rewritten_words": len(rewritten_text.split()),
                "characters": len(rewritten_text)
            }
        }
        
        st.session_state.user_history.insert(0, history_entry)  # Add to beginning
        
        # Keep only last 50 entries to avoid file getting too large
        if len(st.session_state.user_history) > 50:
            st.session_state.user_history = st.session_state.user_history[:50]
        
        self.save_history()
        return history_entry["id"]
    
    def add_topic_generation_to_history(self, topic, generated_text, content_type, word_count):
        """Add AI topic generation to history"""
        if not hasattr(st.session_state, 'user_history'):
            st.session_state.user_history = []
        
        history_entry = {
            "id": f"topic_{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "type": "topic_generation",
            "title": f"Generated: {topic}",
            "topic": topic,
            "generated_text": generated_text[:500] + "..." if len(generated_text) > 500 else generated_text,
            "full_text": generated_text,
            "settings": {
                "content_type": content_type,
                "word_count": word_count
            },
            "stats": {
                "words": len(generated_text.split()),
                "characters": len(generated_text)
            }
        }
        
        st.session_state.user_history.insert(0, history_entry)
        
        if len(st.session_state.user_history) > 50:
            st.session_state.user_history = st.session_state.user_history[:50]
        
        self.save_history()
        return history_entry["id"]
    
    def _generate_title(self, text):
        """Generate a short title from text"""
        words = text.split()[:8]  # First 8 words
        title = " ".join(words)
        if len(text.split()) > 8:
            title += "..."
        return title
    
    def show_history_interface(self):
        """Show the history interface like ChatGPT"""
        st.markdown("## 📚 Your EchoVerse History")
        st.markdown("Track all your past audiobook generations and AI interactions")
        
        if not hasattr(st.session_state, 'user_history') or not st.session_state.user_history:
            st.info("🌟 No history yet! Start creating audiobooks to see your history here.")
            return
        
        # Search and filter options
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_term = st.text_input("🔍 Search history", placeholder="Search by title, topic, or content...")
        
        with col2:
            filter_type = st.selectbox("Filter by type", ["All", "Audiobook Generation", "Topic Generation"])
        
        with col3:
            if st.button("🗑️ Clear History", type="secondary"):
                if st.button("⚠️ Confirm Clear", type="secondary"):
                    st.session_state.user_history = []
                    self.save_history()
                    st.success("History cleared!")
                    st.rerun()
        
        # Filter history
        filtered_history = self._filter_history(st.session_state.user_history, search_term, filter_type)
        
        if not filtered_history:
            st.info("No items match your search criteria.")
            return
        
        # Display history items
        st.markdown(f"### 📋 Found {len(filtered_history)} items")
        
        for item in filtered_history:
            self._display_history_item(item)
    
    def _filter_history(self, history, search_term, filter_type):
        """Filter history based on search and type"""
        filtered = history
        
        # Filter by type
        if filter_type == "Audiobook Generation":
            filtered = [item for item in filtered if item["type"] == "audiobook_generation"]
        elif filter_type == "Topic Generation":
            filtered = [item for item in filtered if item["type"] == "topic_generation"]
        
        # Filter by search term
        if search_term:
            search_lower = search_term.lower()
            filtered = [
                item for item in filtered
                if search_lower in item["title"].lower() or
                   search_lower in item.get("topic", "").lower() or
                   search_lower in item.get("original_text", "").lower() or
                   search_lower in item.get("generated_text", "").lower()
            ]
        
        return filtered
    
    def _display_history_item(self, item):
        """Display a single history item"""
        # Create expandable item
        timestamp = datetime.fromisoformat(item["timestamp"]).strftime("%Y-%m-%d %H:%M")
        
        if item["type"] == "audiobook_generation":
            icon = "🎧"
            type_label = "Audiobook"
        else:
            icon = "🤖"
            type_label = "AI Generation"
        
        with st.expander(f"{icon} {item['title']} - {timestamp} ({type_label})"):
            if item["type"] == "audiobook_generation":
                self._display_audiobook_item(item)
            else:
                self._display_topic_item(item)
    
    def _display_audiobook_item(self, item):
        """Display audiobook generation item"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📄 Original Text")
            st.text_area("Original", item["original_text"], height=150, disabled=True, key=f"orig_{item['id']}")
        
        with col2:
            st.markdown("#### ✨ Rewritten Text")
            st.text_area("Rewritten", item["rewritten_text"], height=150, disabled=True, key=f"rewrite_{item['id']}")
        
        # Settings and stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Tone", item["settings"]["tone"])
        with col2:
            st.metric("Voice", item["settings"]["voice"])
        with col3:
            st.metric("Original Words", f"{item['stats']['original_words']:,}")
        with col4:
            st.metric("Rewritten Words", f"{item['stats']['rewritten_words']:,}")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Reuse Original", key=f"reuse_orig_{item['id']}"):
                st.session_state.original_text = item["full_original"]
                st.success("✅ Original text loaded! Go to Generate page.")
        
        with col2:
            if st.button("🔄 Reuse Rewritten", key=f"reuse_rewrite_{item['id']}"):
                st.session_state.original_text = item["full_rewritten"]
                st.success("✅ Rewritten text loaded! Go to Generate page.")
        
        with col3:
            if st.button("📥 Download", key=f"download_{item['id']}"):
                st.download_button(
                    "📄 Download Text",
                    item["full_rewritten"],
                    file_name=f"echoverse_{item['id']}.txt",
                    mime="text/plain",
                    key=f"dl_btn_{item['id']}"
                )
    
    def _display_topic_item(self, item):
        """Display topic generation item"""
        st.markdown(f"**Topic:** {item['topic']}")
        st.markdown(f"**Content Type:** {item['settings']['content_type']}")
        
        st.markdown("#### 🤖 Generated Content")
        st.text_area("Generated", item["generated_text"], height=150, disabled=True, key=f"gen_{item['id']}")
        
        # Stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Words", f"{item['stats']['words']:,}")
        with col2:
            st.metric("Characters", f"{item['stats']['characters']:,}")
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Reuse Content", key=f"reuse_topic_{item['id']}"):
                st.session_state.original_text = item["full_text"]
                st.success("✅ Generated content loaded! Go to Generate page.")
        
        with col2:
            if st.button("📥 Download", key=f"download_topic_{item['id']}"):
                st.download_button(
                    "📄 Download Text",
                    item["full_text"],
                    file_name=f"echoverse_topic_{item['id']}.txt",
                    mime="text/plain",
                    key=f"dl_topic_btn_{item['id']}"
                )
    
    def get_history_stats(self):
        """Get statistics about user history"""
        if not hasattr(st.session_state, 'user_history'):
            return {"total": 0, "audiobooks": 0, "topics": 0}
        
        history = st.session_state.user_history
        audiobooks = len([item for item in history if item["type"] == "audiobook_generation"])
        topics = len([item for item in history if item["type"] == "topic_generation"])
        
        return {
            "total": len(history),
            "audiobooks": audiobooks,
            "topics": topics
        }
