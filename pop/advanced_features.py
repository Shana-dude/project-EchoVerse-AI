"""
EchoVerse Advanced Features
Multi-language support, bookmarks, batch processing, and more
"""

import streamlit as st
import json
import time
import zipfile
import io
from datetime import datetime
from config import *
from ai_models import AIModelManager

class AdvancedFeatures:
    def __init__(self):
        self.ai_manager = AIModelManager()
        
    def show_bookmarks_interface(self):
        """Display bookmarks and notes interface"""
        st.markdown("## 🔖 Bookmarks & Notes")
        
        # Initialize bookmarks in session state
        if 'bookmarks' not in st.session_state:
            st.session_state.bookmarks = []
        
        if 'notes' not in st.session_state:
            st.session_state.notes = {}
        
        # Add new bookmark
        with st.expander("➕ Add New Bookmark"):
            self._show_add_bookmark_form()
        
        # Display existing bookmarks
        self._show_bookmarks_list()
    
    def _show_add_bookmark_form(self):
        """Show form to add new bookmark"""
        original_text = st.session_state.get('original_text', '')
        
        if not original_text:
            st.warning("Please load text first to add bookmarks.")
            return
        
        with st.form("add_bookmark"):
            # Text selection
            start_pos = st.number_input("Start Position (character)", min_value=0, max_value=len(original_text), value=0)
            end_pos = st.number_input("End Position (character)", min_value=start_pos, max_value=len(original_text), value=min(start_pos + 100, len(original_text)))
            
            # Preview selected text
            if start_pos < end_pos:
                selected_text = original_text[start_pos:end_pos]
                st.text_area("Selected Text Preview", selected_text, height=100, disabled=True)
            
            # Bookmark details
            bookmark_title = st.text_input("Bookmark Title", placeholder="Enter bookmark title")
            bookmark_note = st.text_area("Note (optional)", placeholder="Add your notes here...")
            
            # Bookmark type
            bookmark_type = st.selectbox("Bookmark Type", ["Important", "Question", "Summary", "Quote", "Custom"])
            
            # Audio note option
            read_aloud = st.checkbox("Read this note aloud during narration", value=False)
            
            if st.form_submit_button("Add Bookmark"):
                if bookmark_title and start_pos < end_pos:
                    bookmark = {
                        "id": len(st.session_state.bookmarks) + 1,
                        "title": bookmark_title,
                        "start_pos": start_pos,
                        "end_pos": end_pos,
                        "selected_text": selected_text,
                        "note": bookmark_note,
                        "type": bookmark_type,
                        "read_aloud": read_aloud,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    st.session_state.bookmarks.append(bookmark)
                    st.success(f"Bookmark '{bookmark_title}' added successfully!")
                    st.rerun()
                else:
                    st.error("Please provide a title and valid text selection.")
    
    def _show_bookmarks_list(self):
        """Display list of bookmarks"""
        bookmarks = st.session_state.get('bookmarks', [])
        
        if not bookmarks:
            st.info("No bookmarks added yet. Add your first bookmark above!")
            return
        
        st.markdown(f"### 📚 Your Bookmarks ({len(bookmarks)})")
        
        for bookmark in bookmarks:
            with st.expander(f"🔖 {bookmark['title']} ({bookmark['type']})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Selected Text:**")
                    st.text(bookmark['selected_text'][:200] + "..." if len(bookmark['selected_text']) > 200 else bookmark['selected_text'])
                    
                    if bookmark['note']:
                        st.markdown(f"**Note:** {bookmark['note']}")
                    
                    st.caption(f"Position: {bookmark['start_pos']}-{bookmark['end_pos']} | Created: {bookmark['created_at'][:10]}")
                
                with col2:
                    if bookmark['read_aloud']:
                        st.success("🔊 Audio Note")
                    
                    if st.button("🗑️ Delete", key=f"delete_{bookmark['id']}"):
                        st.session_state.bookmarks = [b for b in bookmarks if b['id'] != bookmark['id']]
                        st.rerun()
    
    def show_batch_processing_interface(self):
        """Display batch processing interface"""
        st.markdown("## 📦 Batch Processing")
        
        st.info("Upload multiple text files to convert them into audiobooks simultaneously.")
        
        # File upload for batch processing
        uploaded_files = st.file_uploader(
            "Upload Multiple Files",
            type=ALLOWED_FILE_TYPES,
            accept_multiple_files=True,
            help="Select multiple text or PDF files for batch processing"
        )
        
        if uploaded_files:
            st.markdown(f"### 📁 Selected Files ({len(uploaded_files)})")
            
            # Display file list
            for i, file in enumerate(uploaded_files):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"📄 {file.name}")
                
                with col2:
                    st.write(f"{file.size / 1024:.1f} KB")
                
                with col3:
                    st.write(file.type)
            
            # Batch settings
            st.markdown("### ⚙️ Batch Settings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                batch_tone = st.selectbox("Tone for All Files", list(TONE_OPTIONS.keys()), key="batch_tone")
                batch_intensity = st.selectbox("Intensity for All Files", list(INTENSITY_LEVELS.keys()), index=1, key="batch_intensity")
            
            with col2:
                batch_voice = st.selectbox("Voice for All Files", list(VOICE_OPTIONS.keys()), key="batch_voice")
                batch_language = st.selectbox("Language for All Files", list(LANGUAGE_OPTIONS.keys()), key="batch_language")
            
            # Processing options
            col1, col2 = st.columns(2)
            
            with col1:
                create_zip = st.checkbox("Create ZIP package", value=True)
                include_text = st.checkbox("Include rewritten text files", value=True)
            
            with col2:
                parallel_processing = st.checkbox("Parallel processing (faster)", value=True)
                send_notification = st.checkbox("Send completion notification", value=False)
            
            # Start batch processing
            if st.button("🚀 Start Batch Processing", type="primary", use_container_width=True):
                self._process_batch_files(uploaded_files, {
                    "tone": batch_tone,
                    "intensity": batch_intensity,
                    "voice": batch_voice,
                    "language": batch_language,
                    "create_zip": create_zip,
                    "include_text": include_text,
                    "parallel": parallel_processing
                })
    
    def _process_batch_files(self, files, settings):
        """Process multiple files in batch"""
        st.markdown("### 🔄 Batch Processing Progress")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        results_container = st.container()
        
        total_files = len(files)
        processed_files = []
        
        for i, file in enumerate(files):
            status_text.text(f"Processing {file.name}... ({i+1}/{total_files})")
            
            try:
                # Extract text from file
                if file.name.endswith('.txt'):
                    text_content = file.read().decode('utf-8')
                elif file.name.endswith('.pdf'):
                    from utils import extract_text_from_pdf
                    text_content = extract_text_from_pdf(file)
                else:
                    continue
                
                # Process with AI
                rewritten_text = self.ai_manager.rewrite_text_with_tone(
                    text_content, settings['tone'], settings['intensity'], settings['language']
                )
                
                # Generate audio (simulated)
                audio_data = self.ai_manager.generate_speech(
                    rewritten_text, settings['voice'], settings['language']
                )
                
                processed_files.append({
                    "filename": file.name,
                    "original_text": text_content,
                    "rewritten_text": rewritten_text,
                    "audio_data": audio_data,
                    "status": "success"
                })
                
            except Exception as e:
                processed_files.append({
                    "filename": file.name,
                    "status": "error",
                    "error": str(e)
                })
            
            progress_bar.progress((i + 1) / total_files)
            time.sleep(1)  # Simulate processing time
        
        status_text.text("✅ Batch processing complete!")
        
        # Show results
        with results_container:
            self._show_batch_results(processed_files, settings)
    
    def _show_batch_results(self, results, settings):
        """Show batch processing results"""
        st.markdown("### 📊 Batch Processing Results")
        
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'error']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Files", len(results))
        
        with col2:
            st.metric("Successful", len(successful), delta=len(successful))
        
        with col3:
            st.metric("Failed", len(failed), delta=-len(failed) if failed else 0)
        
        # Detailed results
        if successful:
            st.markdown("#### ✅ Successfully Processed")
            for result in successful:
                with st.expander(f"📄 {result['filename']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Original Text (preview):**")
                        st.text(result['original_text'][:200] + "...")
                    
                    with col2:
                        st.write("**Rewritten Text (preview):**")
                        st.text(result['rewritten_text'][:200] + "...")
                    
                    # Download options
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.download_button(
                            "📥 Download Rewritten Text",
                            result['rewritten_text'],
                            file_name=f"rewritten_{result['filename']}",
                            mime="text/plain"
                        )
                    
                    with col2:
                        if st.button(f"🎵 Download Audio", key=f"audio_{result['filename']}"):
                            st.success("Audio download started! (Demo mode)")
        
        if failed:
            st.markdown("#### ❌ Failed to Process")
            for result in failed:
                st.error(f"📄 {result['filename']}: {result['error']}")
        
        # Create ZIP package
        if settings.get('create_zip') and successful:
            if st.button("📦 Download All as ZIP", type="primary"):
                st.success("ZIP package download started! (Demo mode)")
                st.balloons()
    
    def show_summary_generator(self):
        """Show automatic summary generation"""
        st.markdown("## 📋 Smart Summary Generator")
        
        original_text = st.session_state.get('original_text', '')
        
        if not original_text:
            st.warning("Please load text first to generate summary.")
            return
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            summary_length = st.selectbox(
                "Summary Length",
                ["Short (100 words)", "Medium (250 words)", "Long (500 words)"],
                index=1
            )
            
            summary_style = st.selectbox(
                "Summary Style",
                ["Bullet Points", "Paragraph", "Key Highlights", "Q&A Format"],
                index=0
            )
            
            include_audio = st.checkbox("Generate audio summary", value=True)
        
        with col1:
            if st.button("🔍 Generate Summary", type="primary"):
                with st.spinner("Generating summary..."):
                    # Extract word count from selection
                    word_count = int(summary_length.split('(')[1].split(' ')[0])
                    
                    # Generate summary
                    summary = self.ai_manager.generate_summary(original_text, word_count * 6)  # Rough character estimate
                    
                    st.session_state.generated_summary = summary
                    
                    st.success("Summary generated successfully!")
        
        # Display generated summary
        if st.session_state.get('generated_summary'):
            st.markdown("### 📄 Generated Summary")
            
            summary = st.session_state.generated_summary
            st.text_area("Summary", summary, height=200, disabled=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    "📥 Download Summary",
                    summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )
            
            with col2:
                if st.button("🎵 Generate Audio Summary"):
                    st.success("Audio summary generated! (Demo mode)")
            
            with col3:
                if st.button("📧 Share Summary"):
                    st.info("Sharing options coming soon!")
    
    def show_chapter_navigator(self):
        """Show chapter navigation interface"""
        st.markdown("## 📚 Chapter Navigator")

        chapters = st.session_state.get('chapters', [])
        original_text = st.session_state.get('original_text', '')

        if not chapters and not original_text:
            st.info("📖 No text loaded yet. Please upload text first to detect chapters.")

            # Demo chapters for illustration
            st.markdown("### 🎯 Demo Chapter Structure")
            demo_chapters = [
                {"title": "Introduction", "description": "Opening chapter with background information"},
                {"title": "Chapter 1: The Beginning", "description": "Story starts here with character introduction"},
                {"title": "Chapter 2: The Journey", "description": "Main plot development and conflicts"},
                {"title": "Chapter 3: The Resolution", "description": "Climax and conclusion of the story"}
            ]

            for i, chapter in enumerate(demo_chapters):
                with st.expander(f"📖 {chapter['title']}"):
                    st.write(f"**Description:** {chapter['description']}")
                    st.write("**Status:** Demo chapter")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.button(f"🎵 Play Demo", key=f"demo_play_{i}", disabled=True)
                    with col2:
                        st.button(f"📥 Download Demo", key=f"demo_download_{i}", disabled=True)

            st.markdown("---")
            st.markdown("**💡 Tip:** Upload text with clear chapter headings like 'Chapter 1', 'Section A', etc. for automatic detection.")
            return

        elif not chapters and original_text:
            st.warning("⚠️ No chapters detected in your text. Try adding clear chapter headings.")

            # Offer to create manual chapters
            st.markdown("### ✂️ Create Manual Chapters")

            if st.button("🔍 Auto-detect Chapters", type="primary"):
                # Try to detect chapters from the text
                from utils import detect_chapters
                detected = detect_chapters(original_text)

                if detected:
                    st.session_state.chapters = detected
                    st.success(f"✅ Detected {len(detected)} chapters!")
                    st.rerun()
                else:
                    st.info("No clear chapter markers found. You can create manual chapters below.")

            # Manual chapter creation
            with st.expander("➕ Create Manual Chapter"):
                chapter_title = st.text_input("Chapter Title", placeholder="e.g., Chapter 1: Introduction")
                start_pos = st.number_input("Start Position (character)", min_value=0, max_value=len(original_text), value=0)
                end_pos = st.number_input("End Position (character)", min_value=start_pos, max_value=len(original_text), value=min(start_pos + 500, len(original_text)))

                if st.button("➕ Add Chapter"):
                    if chapter_title:
                        new_chapter = {
                            "title": chapter_title,
                            "start_pos": start_pos,
                            "end_pos": end_pos,
                            "start_line": 0
                        }

                        if 'chapters' not in st.session_state:
                            st.session_state.chapters = []

                        st.session_state.chapters.append(new_chapter)
                        st.success(f"✅ Added chapter: {chapter_title}")
                        st.rerun()
            return
        
        st.markdown(f"### Found {len(chapters)} chapters")
        
        for i, chapter in enumerate(chapters):
            with st.expander(f"📖 Chapter {i+1}: {chapter['title']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Title:** {chapter['title']}")
                    st.write(f"**Position:** Line {chapter.get('start_line', 'Unknown')}")
                    
                    # Show chapter preview
                    original_text = st.session_state.get('original_text', '')
                    if original_text and 'start_pos' in chapter:
                        chapter_text = original_text[chapter['start_pos']:chapter['start_pos'] + 300]
                        st.text_area("Preview", chapter_text, height=100, disabled=True, key=f"chapter_preview_{i}")
                
                with col2:
                    if st.button(f"🎵 Play Chapter {i+1}", key=f"play_chapter_{i}"):
                        st.success(f"Playing Chapter {i+1}...")
                    
                    if st.button(f"📥 Download Chapter {i+1}", key=f"download_chapter_{i}"):
                        st.success(f"Downloading Chapter {i+1}...")
        
        # Chapter-specific settings
        st.markdown("### ⚙️ Chapter Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            auto_pause = st.checkbox("Auto-pause between chapters", value=True)
            chapter_announcements = st.checkbox("Announce chapter titles", value=True)
        
        with col2:
            pause_duration = st.slider("Pause duration (seconds)", 1, 10, 3)
            chapter_tone_variation = st.checkbox("Vary tone by chapter", value=False)
