"""
EchoVerse Audio Generation Pipeline
Complete pipeline for text processing and audio generation
"""

import streamlit as st
import time
import json
from datetime import datetime
from ai_models import AIModelManager
from animations import show_progress_animation, show_success_animation, show_audio_wave_animation
from config import *

class AudioPipeline:
    def __init__(self):
        self.ai_manager = AIModelManager()
        self.current_job = None
        
    def show_generation_interface(self):
        """Display the audio generation interface"""
        if not st.session_state.get('original_text'):
            st.warning("⚠️ Please input text first before generating audio.")
            st.info("💡 Go to **Text Input** page to add content or generate from a topic using AI!")
            return

        st.markdown("## 🎛️ Audio Generation Settings")
        st.info("🎯 **Workflow**: Choose settings → Generate → See text comparison → Listen to audio → Download results")
        
        # Settings columns
        col1, col2 = st.columns(2)
        
        with col1:
            self._show_tone_settings()
        
        with col2:
            self._show_voice_settings()
        
        # Advanced settings
        with st.expander("🔧 Advanced Settings"):
            self._show_advanced_settings()
        
        # Text preview
        st.markdown("---")
        st.markdown("### 📖 Text Preview")

        col1, col2 = st.columns(2)

        with col1:
            with st.expander("👀 Preview Original Text", expanded=False):
                original_text = st.session_state.get('original_text', '')
                st.text_area("Original Text Preview", original_text[:500] + "..." if len(original_text) > 500 else original_text,
                            height=150, disabled=True, key="preview_original", label_visibility="collapsed")
                st.caption(f"Total length: {len(original_text):,} characters, {len(original_text.split()):,} words")

        with col2:
            with st.expander("✨ Preview Rewritten Text", expanded=False):
                rewritten_text = st.session_state.get('rewritten_text', '')
                if rewritten_text:
                    st.text_area("Rewritten Text Preview", rewritten_text[:500] + "..." if len(rewritten_text) > 500 else rewritten_text,
                                height=150, disabled=True, key="preview_rewritten", label_visibility="collapsed")
                    st.caption(f"Total length: {len(rewritten_text):,} characters, {len(rewritten_text.split()):,} words")
                else:
                    st.info("Generate audiobook first to see rewritten text preview")
                    st.text_area("Rewritten Text Preview", "No rewritten text available yet...",
                                height=150, disabled=True, key="preview_rewritten_empty", label_visibility="collapsed")

        # Show what will happen
        tone = st.session_state.get('selected_tone', 'Neutral')
        intensity = st.session_state.get('selected_intensity', 'Medium')
        if tone != 'Neutral':
            st.info(f"🎭 **Preview**: Your text will be rewritten with **{tone}** tone at **{intensity}** intensity, then converted to audio.")

        # Generation button
        st.markdown("---")
        if st.button("🎵 Generate Audiobook", type="primary", use_container_width=True):
            self._start_generation()
    
    def _show_tone_settings(self):
        """Show tone and intensity settings"""
        st.markdown("### 🎭 Tone & Style")
        
        # Tone selection
        tone = st.selectbox(
            "Select Tone",
            list(TONE_OPTIONS.keys()),
            index=0,
            help="Choose the emotional tone for your audiobook"
        )
        
        # Show tone description
        if tone in TONE_OPTIONS:
            st.info(f"📝 {TONE_OPTIONS[tone]['description']}")
        
        # Intensity level
        intensity = st.select_slider(
            "Intensity Level",
            options=list(INTENSITY_LEVELS.keys()),
            value="Medium",
            help="Adjust how pronounced the tone should be"
        )
        
        # Store in session state
        st.session_state.selected_tone = tone
        st.session_state.selected_intensity = intensity
    
    def _show_voice_settings(self):
        """Show voice and language settings"""
        st.markdown("### 🎤 Voice & Language")
        
        # Voice selection
        voice = st.selectbox(
            "Select Voice",
            list(VOICE_OPTIONS.keys()),
            index=0,
            help="Choose the narrator voice"
        )
        
        # Language selection
        language = st.selectbox(
            "Select Language",
            list(LANGUAGE_OPTIONS.keys()),
            index=0,
            help="Choose the output language"
        )
        
        # Voice preview (simulated)
        if st.button(f"🔊 Preview {voice} Voice", key="voice_preview"):
            st.audio("https://www.soundjay.com/misc/sounds/bell-ringing-05.wav")  # Placeholder
            st.success(f"Playing {voice} voice sample...")
        
        # Store in session state
        st.session_state.selected_voice = voice
        st.session_state.selected_language = language
    
    def _show_advanced_settings(self):
        """Show advanced generation settings"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Chapter processing
            process_chapters = st.checkbox(
                "Process Chapters Separately",
                value=True,
                help="Generate audio for each chapter individually"
            )
            
            # Add pauses
            add_pauses = st.checkbox(
                "Add Chapter Pauses",
                value=True,
                help="Add brief pauses between chapters"
            )
            
            # Background music
            background_music = st.checkbox(
                "Add Background Music",
                value=False,
                help="Add subtle background music (coming soon)"
            )
        
        with col2:
            # Speed control
            speech_speed = st.slider(
                "Speech Speed",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="Adjust narration speed"
            )
            
            # Pitch control
            speech_pitch = st.slider(
                "Speech Pitch",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="Adjust voice pitch"
            )
            
            # Audio quality
            audio_quality = st.selectbox(
                "Audio Quality",
                ["Standard", "High", "Premium"],
                index=1,
                help="Choose audio quality level"
            )
        
        # Store advanced settings
        st.session_state.advanced_settings = {
            "process_chapters": process_chapters,
            "add_pauses": add_pauses,
            "background_music": background_music,
            "speech_speed": speech_speed,
            "speech_pitch": speech_pitch,
            "audio_quality": audio_quality
        }
    
    def _start_generation(self):
        """Start the audio generation process"""
        # Get settings from session state
        tone = st.session_state.get('selected_tone', 'Neutral')
        intensity = st.session_state.get('selected_intensity', 'Medium')
        voice = st.session_state.get('selected_voice', 'Lisa')
        language = st.session_state.get('selected_language', 'English')
        original_text = st.session_state.get('original_text', '')
        
        if not original_text:
            st.error("No text available for processing")
            return
        
        # Create animated progress containers
        progress_container = st.container()
        comparison_container = st.container()

        with progress_container:
            st.markdown("### 🔄 Generation Progress")
            progress_placeholder = st.empty()
            status_placeholder = st.empty()

        # Create live text comparison container with styling
        with comparison_container:
            st.markdown("### 📝 Live Text Comparison")

            # Add custom CSS for live comparison
            st.markdown("""
            <style>
            .live-comparison {
                border: 2px solid #28a745;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
            }
            .processing-indicator {
                animation: pulse 2s infinite;
                border: 2px dashed #ffc107;
                background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            }
            @keyframes pulse {
                0% { opacity: 0.7; }
                50% { opacity: 1; }
                100% { opacity: 0.7; }
            }
            </style>
            """, unsafe_allow_html=True)

            comparison_placeholder = st.empty()

        try:
            # Step 1: Show original text first
            with comparison_placeholder:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown('<div class="live-comparison">', unsafe_allow_html=True)
                    st.markdown("#### 📄 Original Text")
                    st.text_area("Original", original_text, height=250, disabled=True, key="live_original", label_visibility="collapsed")
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="live-comparison processing-indicator">', unsafe_allow_html=True)
                    st.markdown("#### ⏳ Rewriting in Progress...")
                    processing_text = f"""🎭 Applying {tone} tone with {intensity} intensity...

🔄 Step 1: Applying tone adaptation...
✨ Step 2: Gemini AI enhancing content...
📝 Adding details and context...
🎯 Optimizing for audio narration...

AI processing in progress!"""
                    st.text_area("Processing", processing_text, height=250, disabled=True, key="live_processing", label_visibility="collapsed")
                    st.markdown('</div>', unsafe_allow_html=True)

            # Step 1: Text Rewriting with Local + Gemini AI
            with status_placeholder:
                st.markdown(show_progress_animation(10, "🎭 Rewriting text with Local + Gemini AI..."), unsafe_allow_html=True)

            time.sleep(0.5)  # Faster animation

            rewritten_text = self.ai_manager.rewrite_text_with_tone(
                original_text, tone, intensity, language
            )

            # Update progress
            with progress_placeholder:
                st.markdown(show_progress_animation(60, "✅ Text enhanced and rewritten with AI!"), unsafe_allow_html=True)

            # Store rewritten text
            st.session_state.rewritten_text = rewritten_text

            # Update comparison with rewritten text
            with comparison_placeholder:
                st.success("🎉 Text rewriting completed successfully!")
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown('<div class="live-comparison">', unsafe_allow_html=True)
                    st.markdown("#### 📄 Original Text")
                    st.text_area("Original", original_text, height=250, disabled=True, key="live_original_final", label_visibility="collapsed")
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="live-comparison" style="border-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);">', unsafe_allow_html=True)
                    st.markdown("#### ✨ Rewritten Text")
                    st.text_area("Rewritten", rewritten_text, height=250, disabled=True, key="live_rewritten_final", label_visibility="collapsed")
                    st.markdown('</div>', unsafe_allow_html=True)

                # Show quick comparison stats
                st.markdown("#### 📊 Quick Comparison")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Original Words", f"{len(original_text.split()):,}")
                with col2:
                    st.metric("Rewritten Words", f"{len(rewritten_text.split()):,}")
                with col3:
                    change_pct = ((len(rewritten_text.split()) - len(original_text.split())) / len(original_text.split()) * 100) if len(original_text.split()) > 0 else 0
                    st.metric("Change", f"{change_pct:+.1f}%")
                with col4:
                    st.metric("Applied Tone", f"{tone} ({intensity})")

            time.sleep(1)  # Faster comparison view

            # Step 2: Audio Generation with wave animation
            with status_placeholder:
                st.markdown(show_audio_wave_animation(), unsafe_allow_html=True)

            with progress_placeholder:
                st.markdown(show_progress_animation(70, "🎤 Generating audio narration..."), unsafe_allow_html=True)

            audio_data = self.ai_manager.generate_speech(rewritten_text, voice, language)

            # Store audio data
            st.session_state.audio_data = audio_data

            # Complete with success animation
            with progress_placeholder:
                st.markdown(show_progress_animation(100, "✅ Generation complete!"), unsafe_allow_html=True)

            time.sleep(1)

            with status_placeholder:
                show_success_animation("🎉 Audiobook generated successfully!")

            # Show audio player immediately after generation
            st.markdown("---")
            self._show_audio_player()

            # Add to history
            try:
                from history_manager import HistoryManager
                history_manager = HistoryManager()
                history_manager.add_generation_to_history(
                    original_text, rewritten_text, tone, voice, language
                )
                st.info("💾 Generation saved to history!")
            except Exception as e:
                pass  # Don't break if history fails

            # Show generation summary
            st.markdown("---")
            self._show_generation_summary(rewritten_text, audio_data)

            # Guide user to Results page
            st.markdown("---")
            st.success("🎉 **Generation Complete!** Go to the **📋 Results** page to see full comparison, download files, and access all features.")

        except Exception as e:
            st.error(f"❌ Generation failed: {str(e)}")
    
    def _show_generation_summary(self, rewritten_text, audio_data):
        """Show summary of generated content"""
        st.markdown("### 📊 Generation Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            original_words = len(st.session_state.get('original_text', '').split())
            st.metric("Original Words", f"{original_words:,}")
        
        with col2:
            rewritten_words = len(rewritten_text.split())
            st.metric("Rewritten Words", f"{rewritten_words:,}")
        
        with col3:
            if isinstance(audio_data, dict) and 'total_duration' in audio_data:
                duration = audio_data['total_duration']
                st.metric("Audio Duration", f"{duration:.1f} min")
            else:
                st.metric("Audio Duration", "~5 min")
        
        with col4:
            if isinstance(audio_data, dict) and 'total_chunks' in audio_data:
                chunks = audio_data['total_chunks']
                st.metric("Audio Segments", chunks)
            else:
                st.metric("Audio Segments", "1")
    
    def show_results_interface(self):
        """Display the results interface with text comparison and audio player"""
        if not st.session_state.get('rewritten_text'):
            st.info("Generate an audiobook to see results here.")
            return
        
        st.markdown("## 📋 Results")
        
        # Text comparison
        self._show_text_comparison()
        
        # Audio player
        self._show_audio_player()
        
        # Download options
        self._show_download_options()
    
    def _show_text_comparison(self):
        """Show side-by-side text comparison"""
        st.markdown("### 📝 Text Comparison")

        # Add custom CSS for better text comparison styling
        st.markdown("""
        <style>
        .text-comparison {
            border: 2px solid #28a745;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background-color: #f8f9fa;
        }
        .text-comparison h4 {
            color: #28a745;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="text-comparison">', unsafe_allow_html=True)
            st.markdown("#### 📄 Original Text")
            original_text = st.session_state.get('original_text', '')
            st.text_area("Original Text", original_text, height=300, disabled=True, key="original_display", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="text-comparison">', unsafe_allow_html=True)
            st.markdown("#### ✨ Rewritten Text")
            rewritten_text = st.session_state.get('rewritten_text', '')
            st.text_area("Rewritten Text", rewritten_text, height=300, disabled=True, key="rewritten_display", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Text statistics and tone information
        st.markdown("#### 📊 Comparison Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            original_words = len(original_text.split())
            st.metric("Original Words", f"{original_words:,}")

        with col2:
            rewritten_words = len(rewritten_text.split())
            st.metric("Rewritten Words", f"{rewritten_words:,}")

        with col3:
            change_pct = ((rewritten_words - original_words) / original_words * 100) if original_words > 0 else 0
            st.metric("Word Count Change", f"{change_pct:+.1f}%")

        with col4:
            tone = st.session_state.get('selected_tone', 'Neutral')
            intensity = st.session_state.get('selected_intensity', 'Medium')
            st.metric("Applied Tone", f"{tone} ({intensity})")
        
        with col3:
            intensity = st.session_state.get('selected_intensity', 'Medium')
            st.metric("Intensity Level", intensity)
    
    def _show_audio_player(self):
        """Show audio player interface"""
        st.markdown("### 🎧 Audio Player")

        audio_data = st.session_state.get('audio_data')

        if audio_data and isinstance(audio_data, dict):
            # Check if we have actual audio data
            if audio_data.get("audio_data") or audio_data.get("audio_file"):
                st.success("🎵 Audio Ready for Playback!")

                # Display audio info
                col1, col2, col3 = st.columns(3)

                with col1:
                    duration = audio_data.get("total_duration", audio_data.get("duration", 0))
                    st.metric("Duration", f"{duration:.1f} min")

                with col2:
                    file_size = audio_data.get("file_size", 0)
                    if file_size > 0:
                        st.metric("File Size", f"{file_size / 1024:.1f} KB")
                    else:
                        st.metric("File Size", "Unknown")

                with col3:
                    voice = audio_data.get("voice", "Unknown")
                    st.metric("Voice", voice)

                # Audio player
                if audio_data.get("audio_file"):
                    try:
                        # Read audio file and display player
                        with open(audio_data["audio_file"], "rb") as audio_file:
                            audio_bytes = audio_file.read()
                            # Determine format based on file extension or metadata
                            audio_format = audio_data.get("format", "wav")
                            if audio_format == "mp3":
                                st.audio(audio_bytes, format="audio/mp3")
                            else:
                                st.audio(audio_bytes, format="audio/wav")
                    except Exception as e:
                        st.error(f"Error loading audio file: {str(e)}")
                elif audio_data.get("audio_data"):
                    # Direct audio data
                    audio_format = audio_data.get("format", "wav")
                    if audio_format == "mp3":
                        st.audio(audio_data["audio_data"], format="audio/mp3")
                    else:
                        st.audio(audio_data["audio_data"], format="audio/wav")

                # Chapter navigation if available
                chapters = st.session_state.get('chapters', [])
                if chapters and audio_data.get("chunks"):
                    st.markdown("#### 📚 Chapter Navigation")
                    chapter_names = [f"Chapter {i+1}: {ch['title']}" for i, ch in enumerate(chapters)]
                    selected_chapter = st.selectbox("Jump to Chapter", chapter_names)

                    if st.button("🔄 Go to Chapter"):
                        st.info(f"Jumping to {selected_chapter}")

            else:
                st.warning("Audio data is incomplete. Please regenerate the audiobook.")
        else:
            st.warning("No audio generated yet. Please generate an audiobook first.")
    
    def _show_download_options(self):
        """Show download options"""
        st.markdown("### 💾 Download Options")

        audio_data = st.session_state.get('audio_data')
        rewritten_text = st.session_state.get('rewritten_text', '')

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 🎵 Audio Download")
            if audio_data and audio_data.get("audio_data"):
                # Provide real audio download
                audio_bytes = audio_data["audio_data"]
                audio_format = audio_data.get("format", "wav")

                if audio_format == "mp3":
                    filename = f"echoverse_audio_{int(time.time())}.mp3"
                    mime_type = "audio/mp3"
                    label = "📥 Download Audio (MP3)"
                else:
                    filename = f"echoverse_audio_{int(time.time())}.wav"
                    mime_type = "audio/wav"
                    label = "📥 Download Audio (WAV)"

                st.download_button(
                    label=label,
                    data=audio_bytes,
                    file_name=filename,
                    mime=mime_type,
                    use_container_width=True
                )

                # Show file info
                file_size_mb = len(audio_bytes) / (1024 * 1024)
                st.caption(f"File size: {file_size_mb:.2f} MB | Format: {audio_format.upper()}")
            else:
                st.button("📥 Download Audio", disabled=True, use_container_width=True)
                st.caption("Generate audio first")

        with col2:
            st.markdown("#### 📄 Text Download")
            if rewritten_text:
                st.download_button(
                    label="📄 Download Rewritten Text",
                    data=rewritten_text,
                    file_name=f"echoverse_rewritten_{int(time.time())}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

                # Original text download
                original_text = st.session_state.get('original_text', '')
                if original_text:
                    st.download_button(
                        label="📝 Download Original Text",
                        data=original_text,
                        file_name=f"echoverse_original_{int(time.time())}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            else:
                st.button("📄 Download Text", disabled=True, use_container_width=True)
                st.caption("Process text first")

        with col3:
            st.markdown("#### 📦 Complete Package")
            if audio_data and rewritten_text:
                # Create a complete package
                if st.button("📦 Create Package", use_container_width=True):
                    self._create_complete_package()
            else:
                st.button("📦 Download Package", disabled=True, use_container_width=True)
                st.caption("Complete generation first")

    def _create_complete_package(self):
        """Create a complete downloadable package"""
        import zipfile
        import io
        import json

        # Create ZIP file in memory
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add audio file
            audio_data = st.session_state.get('audio_data')
            if audio_data and audio_data.get("audio_data"):
                audio_format = audio_data.get("format", "wav")
                audio_filename = f"audiobook.{audio_format}"
                zip_file.writestr(audio_filename, audio_data["audio_data"])

            # Add texts
            original_text = st.session_state.get('original_text', '')
            rewritten_text = st.session_state.get('rewritten_text', '')

            if original_text:
                zip_file.writestr("original_text.txt", original_text)
            if rewritten_text:
                zip_file.writestr("rewritten_text.txt", rewritten_text)

            # Add settings/metadata
            metadata = {
                "tone": st.session_state.get('selected_tone', 'Unknown'),
                "intensity": st.session_state.get('selected_intensity', 'Unknown'),
                "voice": st.session_state.get('selected_voice', 'Unknown'),
                "language": st.session_state.get('selected_language', 'Unknown'),
                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "word_count": len(rewritten_text.split()) if rewritten_text else 0,
                "estimated_duration": audio_data.get("total_duration", 0) if audio_data else 0
            }

            zip_file.writestr("metadata.json", json.dumps(metadata, indent=2))

            # Add README
            readme_content = """# EchoVerse Audiobook Package

This package contains:
- audiobook.wav: Generated audio file
- original_text.txt: Original input text
- rewritten_text.txt: AI-rewritten text with tone adaptation
- metadata.json: Generation settings and information

Generated by EchoVerse - AI Audiobook Creator
"""
            zip_file.writestr("README.txt", readme_content)

        zip_buffer.seek(0)

        # Provide download
        st.download_button(
            label="📦 Download Complete Package (ZIP)",
            data=zip_buffer.getvalue(),
            file_name=f"echoverse_package_{int(time.time())}.zip",
            mime="application/zip",
            use_container_width=True
        )


        st.success("📦 Package created successfully!")
        st.balloons()
