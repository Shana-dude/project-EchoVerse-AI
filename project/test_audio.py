"""
Test script to verify audio generation functionality
"""

import streamlit as st
from ai_models import AIModelManager

def test_audio_generation():
    """Test the audio generation functionality"""
    st.title("🎧 Audio Generation Test")
    
    # Initialize AI manager
    ai_manager = AIModelManager()
    
    # Test text
    test_text = st.text_area(
        "Enter test text:",
        value="Hello, this is a test of the EchoVerse audio generation system. The quick brown fox jumps over the lazy dog.",
        height=100
    )
    
    if st.button("🎵 Generate Test Audio"):
        if test_text.strip():
            with st.spinner("Generating audio..."):
                # Generate audio using fallback method
                audio_result = ai_manager._generate_speech_fallback(test_text)
                
                if audio_result:
                    st.success("✅ Audio generated successfully!")
                    
                    # Display audio info
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Duration", f"{audio_result['duration']:.1f} min")
                    
                    with col2:
                        file_size_mb = audio_result['file_size'] / (1024 * 1024)
                        st.metric("File Size", f"{file_size_mb:.2f} MB")
                    
                    with col3:
                        st.metric("Format", audio_result.get('format', 'mp3').upper())
                    
                    # Audio player
                    st.audio(audio_result['audio_data'], format=f"audio/{audio_result.get('format', 'mp3')}")
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Audio",
                        data=audio_result['audio_data'],
                        file_name=f"test_audio.{audio_result.get('format', 'mp3')}",
                        mime=f"audio/{audio_result.get('format', 'mp3')}"
                    )
                else:
                    st.error("❌ Failed to generate audio")
        else:
            st.warning("Please enter some text to generate audio")

if __name__ == "__main__":
    test_audio_generation()
