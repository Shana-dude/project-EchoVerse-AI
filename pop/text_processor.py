"""
EchoVerse Text Processing Module
Handles text input, file uploads, and text preprocessing
"""

import streamlit as st
import PyPDF2
import io
import re
from utils import extract_text_from_pdf, chunk_text, detect_chapters, generate_summary
from config import MAX_FILE_SIZE, ALLOWED_FILE_TYPES, MAX_TEXT_LENGTH

class TextProcessor:
    def __init__(self):
        self.original_text = ""
        self.processed_text = ""
        self.chapters = []
        self.summary = ""
        
    def show_text_input_interface(self):
        """Display the text input interface"""
        st.markdown("## 📝 Text Input")
        
        # Create tabs for different input methods
        tab1, tab2 = st.tabs(["✍️ Paste Text", "📁 Upload File"])
        
        with tab1:
            self._show_text_paste_interface()
        
        with tab2:
            self._show_file_upload_interface()
        
        # Display text statistics if text is available
        if self.original_text:
            self._show_text_statistics()
    
    def _show_text_paste_interface(self):
        """Show text paste interface"""
        st.markdown("### Paste Your Text")
        
        # Sample text button
        col1, col2 = st.columns([3, 1])

        with col2:
            if st.button("📝 Load Sample Text", type="secondary"):
                sample_text = """Chapter 1: The Beginning

Once upon a time, in a small village nestled between rolling hills and whispering forests, there lived a young girl named Luna. She had always been fascinated by the stars that danced across the night sky, their twinkling light filling her with wonder and curiosity.

Every evening, Luna would climb to the highest tower of her family's cottage and gaze upward, dreaming of adventures beyond the clouds. Little did she know that her life was about to change in the most extraordinary way.

Chapter 2: The Discovery

One particularly clear night, as Luna watched the constellations, she noticed something unusual. A shooting star seemed to be falling directly toward her village. But as it grew closer, she realized it wasn't a star at all—it was something far more magical.

The mysterious object landed softly in the meadow behind her house, glowing with an ethereal blue light. Luna's heart raced with excitement and curiosity as she made her way toward the strange visitor from the sky."""

                st.session_state.sample_loaded = True
                return sample_text

        # Text area for pasting content
        with col1:
            initial_text = ""
            if st.session_state.get('sample_loaded'):
                initial_text = """Chapter 1: The Beginning

Once upon a time, in a small village nestled between rolling hills and whispering forests, there lived a young girl named Luna. She had always been fascinated by the stars that danced across the night sky, their twinkling light filling her with wonder and curiosity.

Every evening, Luna would climb to the highest tower of her family's cottage and gaze upward, dreaming of adventures beyond the clouds. Little did she know that her life was about to change in the most extraordinary way.

Chapter 2: The Discovery

One particularly clear night, as Luna watched the constellations, she noticed something unusual. A shooting star seemed to be falling directly toward her village. But as it grew closer, she realized it wasn't a star at all—it was something far more magical.

The mysterious object landed softly in the meadow behind her house, glowing with an ethereal blue light. Luna's heart raced with excitement and curiosity as she made her way toward the strange visitor from the sky."""
                st.session_state.sample_loaded = False

        pasted_text = st.text_area(
            "Enter your text here:",
            value=initial_text,
            height=300,
            placeholder="Paste your text content here...\n\nExample:\nChapter 1: Introduction\nThis is the beginning of my story...\n\nChapter 2: The Adventure\nThe journey continues...\n\nSupports up to 50,000 characters.",
            help="You can paste any text content including articles, stories, educational material, etc. Use clear chapter headings for better navigation."
        )
        
        if pasted_text:
            if len(pasted_text) > MAX_TEXT_LENGTH:
                st.error(f"Text is too long. Maximum allowed length is {MAX_TEXT_LENGTH:,} characters. Current length: {len(pasted_text):,}")
            else:
                self.original_text = pasted_text
                st.success(f"Text loaded successfully! ({len(pasted_text):,} characters)")
                self._process_text()
    
    def _show_file_upload_interface(self):
        """Show file upload interface"""
        st.markdown("### Upload Text File")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=ALLOWED_FILE_TYPES,
            help=f"Supported formats: {', '.join(ALLOWED_FILE_TYPES)}. Maximum file size: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
        
        if uploaded_file is not None:
            # Check file size
            if uploaded_file.size > MAX_FILE_SIZE:
                st.error(f"File is too large. Maximum size allowed: {MAX_FILE_SIZE // (1024*1024)}MB")
                return
            
            # Process based on file type
            file_type = uploaded_file.name.split('.')[-1].lower()
            
            try:
                if file_type == 'txt':
                    # Read text file
                    text_content = uploaded_file.read().decode('utf-8')
                elif file_type == 'pdf':
                    # Extract text from PDF
                    text_content = extract_text_from_pdf(uploaded_file)
                    if text_content is None:
                        st.error("Failed to extract text from PDF")
                        return
                else:
                    st.error(f"Unsupported file type: {file_type}")
                    return
                
                if len(text_content) > MAX_TEXT_LENGTH:
                    st.error(f"File content is too long. Maximum allowed length is {MAX_TEXT_LENGTH:,} characters.")
                    return
                
                self.original_text = text_content
                st.success(f"File '{uploaded_file.name}' loaded successfully! ({len(text_content):,} characters)")
                self._process_text()
                
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    def _process_text(self):
        """Process the loaded text"""
        if not self.original_text:
            return
        
        # Clean and preprocess text
        self.processed_text = self._clean_text(self.original_text)
        
        # Detect chapters
        self.chapters = detect_chapters(self.processed_text)
        
        # Generate summary
        self.summary = generate_summary(self.processed_text)
        
        # Store in session state
        st.session_state.original_text = self.original_text
        st.session_state.processed_text = self.processed_text
        st.session_state.chapters = self.chapters
        st.session_state.summary = self.summary
    
    def _clean_text(self, text):
        """Clean and preprocess text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might interfere with TTS
        text = re.sub(r'[^\w\s\.,!?;:\-\'"()\[\]{}]', '', text)
        
        # Ensure proper sentence endings
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        return text.strip()
    
    def _show_text_statistics(self):
        """Display text statistics"""
        st.markdown("### 📊 Text Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Characters", f"{len(self.original_text):,}")
        
        with col2:
            word_count = len(self.original_text.split())
            st.metric("Words", f"{word_count:,}")
        
        with col3:
            # Estimate reading time (average 200 words per minute)
            reading_time = max(1, word_count // 200)
            st.metric("Est. Reading Time", f"{reading_time} min")
        
        with col4:
            # Estimate audio duration (average 150 words per minute for TTS)
            audio_time = max(1, word_count // 150)
            st.metric("Est. Audio Time", f"{audio_time} min")
        
        # Show chapters if detected
        if self.chapters:
            st.markdown("### 📚 Detected Chapters")
            for i, chapter in enumerate(self.chapters):
                st.write(f"**Chapter {i+1}:** {chapter['title']}")
        
        # Show summary
        if self.summary:
            st.markdown("### 📋 Quick Summary")
            st.info(self.summary)
    
    def show_text_preview(self):
        """Show text preview with highlighting options"""
        if not self.original_text:
            st.warning("No text loaded. Please input text first.")
            return
        
        st.markdown("### 👀 Text Preview")
        
        # Preview options
        col1, col2 = st.columns([3, 1])
        
        with col2:
            preview_length = st.selectbox(
                "Preview Length",
                ["First 500 chars", "First 1000 chars", "Full text"],
                index=0
            )
            
            show_chapters = st.checkbox("Highlight Chapters", value=True)
        
        with col1:
            # Determine preview text
            if preview_length == "First 500 chars":
                preview_text = self.original_text[:500] + ("..." if len(self.original_text) > 500 else "")
            elif preview_length == "First 1000 chars":
                preview_text = self.original_text[:1000] + ("..." if len(self.original_text) > 1000 else "")
            else:
                preview_text = self.original_text
            
            # Display preview
            if show_chapters and self.chapters:
                # Highlight chapter titles
                highlighted_text = preview_text
                for chapter in self.chapters:
                    if chapter['title'] in highlighted_text:
                        highlighted_text = highlighted_text.replace(
                            chapter['title'],
                            f"**🔖 {chapter['title']}**"
                        )
                st.markdown(highlighted_text)
            else:
                st.text_area("Text Preview", preview_text, height=300, disabled=True)
    
    def get_text_chunks(self, max_chunk_size=2000):
        """Get text chunks for processing"""
        if not self.processed_text:
            return []
        
        return chunk_text(self.processed_text, max_chunk_size)
    
    def get_original_text(self):
        """Get original text"""
        return self.original_text
    
    def get_processed_text(self):
        """Get processed text"""
        return self.processed_text
    
    def get_chapters(self):
        """Get detected chapters"""
        return self.chapters
    
    def get_summary(self):
        """Get text summary"""
        return self.summary
