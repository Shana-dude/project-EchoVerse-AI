"""
Quick Test for EchoVerse Audio Generation
Simple test to verify the audio generation works
"""

import streamlit as st
from ai_models import AIModelManager

def main():
    st.set_page_config(page_title="EchoVerse Quick Test", page_icon="🎧")
    
    # Add green styling
    st.markdown("""
    <style>
    .stButton > button {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(40, 167, 69, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎧 EchoVerse Quick Test")
    st.markdown("### Test the audio generation functionality")
    
    # Test text
    test_text = st.text_area(
        "Enter test text:",
        value="Hello! Welcome to EchoVerse. This is a test of our audio generation system. The quick brown fox jumps over the lazy dog.",
        height=100
    )
    
    # Tone selection
    tone = st.selectbox("Select Tone:", ["Neutral", "Suspenseful", "Inspiring", "Educational", "Storytelling"])
    intensity = st.selectbox("Select Intensity:", ["Low", "Medium", "High"])
    
    if st.button("🎵 Generate Test Audio", type="primary"):
        if test_text.strip():
            # Initialize AI manager
            ai_manager = AIModelManager()
            
            # Step 1: Test tone rewriting
            st.info("🎭 Testing tone rewriting...")
            rewritten_text = ai_manager.rewrite_text_with_tone(test_text, tone, intensity)
            
            # Show comparison
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Original Text")
                st.text_area("", test_text, height=150, disabled=True, key="orig", label_visibility="collapsed")
            
            with col2:
                st.markdown("#### Rewritten Text")
                st.text_area("", rewritten_text, height=150, disabled=True, key="rewrite", label_visibility="collapsed")
            
            # Step 2: Test audio generation
            st.info("🎤 Testing audio generation...")
            
            with st.spinner("Generating audio..."):
                audio_result = ai_manager.generate_speech(rewritten_text)
            
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
                st.markdown("### 🎧 Audio Player")
                audio_format = audio_result.get('format', 'mp3')
                st.audio(audio_result['audio_data'], format=f"audio/{audio_format}")
                
                # Download button
                st.download_button(
                    label="📥 Download Audio",
                    data=audio_result['audio_data'],
                    file_name=f"echoverse_test.{audio_format}",
                    mime=f"audio/{audio_format}",
                    type="primary"
                )
                
                st.balloons()
            else:
                st.error("❌ Failed to generate audio")
        else:
            st.warning("Please enter some text to test")
    
    # Instructions
    st.markdown("---")
    st.markdown("### 📋 How to Test")
    st.markdown("""
    1. **Enter text** in the text area above
    2. **Select tone and intensity** for the rewrite
    3. **Click "Generate Test Audio"** to start the process
    4. **Listen to the result** using the audio player
    5. **Download the audio** if generation is successful
    
    **Expected Results:**
    - ✅ Text should be rewritten with the selected tone
    - ✅ Audio should be generated (MP3 format)
    - ✅ Audio player should appear
    - ✅ Download button should work
    """)
    
    st.markdown("---")
    st.markdown("**🔧 Troubleshooting:** If audio generation fails, check your internet connection and try with shorter text.")

if __name__ == "__main__":
    main()
