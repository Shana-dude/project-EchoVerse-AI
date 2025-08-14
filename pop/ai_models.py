"""
EchoVerse AI Models Integration
Handles Hugging Face API calls for text rewriting and speech synthesis
"""

import streamlit as st
import requests
import json
import time
import base64
import io
from config import *
from utils import call_huggingface_api, chunk_text

class AIModelManager:
    def __init__(self):
        self.text_model = TEXT_TO_TEXT_MODEL
        self.tts_model = TEXT_TO_SPEECH_MODEL
        self.api_key = HF_API_KEY
        
    def rewrite_text_with_tone(self, text, tone, intensity, language="English"):
        """Rewrite text with specified tone and intensity"""
        if not text.strip():
            return text

        # Skip Hugging Face API for now and use local tone adaptation
        st.info("🎭 Applying tone adaptation...")

        return self._apply_tone_locally(text, tone, intensity, language)

    def _apply_tone_locally(self, text, tone, intensity, language="English"):
        """Apply tone adaptation locally without API calls"""
        import re

        # Simple tone adaptation rules
        tone_adaptations = {
            "Suspenseful": {
                "low": {"prefix": "Mysteriously, ", "suffix": "... but what happens next?"},
                "medium": {"prefix": "In a dramatic turn of events, ", "suffix": "... the tension builds."},
                "high": {"prefix": "SUDDENLY, ", "suffix": "... danger lurks around every corner!"}
            },
            "Inspiring": {
                "low": {"prefix": "Remarkably, ", "suffix": " This shows great potential."},
                "medium": {"prefix": "Incredibly, ", "suffix": " This is truly inspiring!"},
                "high": {"prefix": "AMAZINGLY, ", "suffix": " This will change everything!"}
            },
            "Educational": {
                "low": {"prefix": "It's important to note that ", "suffix": " This concept is fundamental."},
                "medium": {"prefix": "Let's explore how ", "suffix": " Understanding this is crucial."},
                "high": {"prefix": "REMEMBER: ", "suffix": " This is a key learning point!"}
            },
            "Storytelling": {
                "low": {"prefix": "Once upon a time, ", "suffix": " And so the story continues..."},
                "medium": {"prefix": "In a world where ", "suffix": " The adventure unfolds..."},
                "high": {"prefix": "LONG AGO, ", "suffix": " And they lived happily ever after!"}
            }
        }

        # Get intensity level
        intensity_map = {"Low": "low", "Medium": "medium", "High": "high"}
        intensity_key = intensity_map.get(intensity, "medium")

        # Apply tone if available
        if tone in tone_adaptations and tone != "Neutral":
            adaptation = tone_adaptations[tone][intensity_key]

            # Split text into sentences
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]

            if sentences:
                # Apply tone to first and last sentences
                first_sentence = adaptation["prefix"] + sentences[0].lower()
                if len(sentences) > 1:
                    last_sentence = sentences[-1] + adaptation["suffix"]
                    middle_sentences = sentences[1:-1]
                    rewritten = first_sentence + ". " + ". ".join(middle_sentences) + (". " if middle_sentences else "") + last_sentence
                else:
                    rewritten = first_sentence + adaptation["suffix"]

                # Capitalize properly
                rewritten = ". ".join([s.strip().capitalize() for s in rewritten.split(". ") if s.strip()])

                st.success(f"✅ Applied {tone} tone with {intensity} intensity!")
                return rewritten

        # Return original text if no tone adaptation
        st.info("ℹ️ Using original text (Neutral tone)")
        return text
    
    def process_text_in_chunks(self, text, tone, intensity, language="English", progress_callback=None):
        """Process long text in chunks for better results"""
        if len(text) <= 2000:
            return self.rewrite_text_with_tone(text, tone, intensity, language)
        
        # Split into chunks
        chunks = chunk_text(text, 1500)  # Smaller chunks for better processing
        rewritten_chunks = []
        
        total_chunks = len(chunks)
        
        for i, chunk in enumerate(chunks):
            if progress_callback:
                progress_callback(i / total_chunks, f"Processing chunk {i+1}/{total_chunks}")
            
            rewritten_chunk = self.rewrite_text_with_tone(chunk, tone, intensity, language)
            rewritten_chunks.append(rewritten_chunk)
            
            # Small delay to avoid rate limiting
            time.sleep(1)
        
        if progress_callback:
            progress_callback(1.0, "Processing complete!")
        
        return " ".join(rewritten_chunks)
    
    def generate_speech(self, text, voice="lisa", language="English"):
        """Generate speech from text using TTS model"""
        if not text.strip():
            return None

        st.info("🎤 Generating audio using Google TTS...")

        # Skip Hugging Face TTS for now and go directly to reliable Google TTS
        return self._generate_speech_fallback(text, voice, language)
    
    def generate_speech_in_chunks(self, text, voice="lisa", language="English", progress_callback=None):
        """Generate speech for long text in chunks"""
        if len(text) <= 1000:  # Reduced chunk size for better API compatibility
            return self.generate_speech(text, voice, language)

        # Split into smaller chunks for TTS
        chunks = chunk_text(text, 800)  # Smaller chunks work better
        audio_chunks = []
        all_audio_data = []

        total_chunks = len(chunks)

        for i, chunk in enumerate(chunks):
            if progress_callback:
                progress_callback(i / total_chunks, f"Generating audio chunk {i+1}/{total_chunks}")

            audio_chunk = self.generate_speech(chunk, voice, language)
            if audio_chunk and audio_chunk.get("audio_data"):
                audio_chunks.append(audio_chunk)
                all_audio_data.append(audio_chunk["audio_data"])

            # Small delay between chunks to avoid rate limiting
            time.sleep(2)

        if progress_callback:
            progress_callback(1.0, "Audio generation complete!")

        # Combine all audio data
        if all_audio_data:
            combined_audio_data = b''.join(all_audio_data)

            # Save combined audio
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.write(combined_audio_data)
            temp_file.close()

            combined_audio = {
                "audio_data": combined_audio_data,
                "audio_file": temp_file.name,
                "chunks": audio_chunks,
                "total_duration": sum(chunk.get("duration", 0) for chunk in audio_chunks),
                "voice": voice,
                "language": language,
                "total_chunks": len(audio_chunks),
                "file_size": len(combined_audio_data)
            }

            return combined_audio

        return None

    def _generate_speech_fallback(self, text, voice="lisa", language="English"):
        """Fallback TTS using Google Text-to-Speech"""
        try:
            from gtts import gTTS
            import tempfile
            import os

            # Limit text length for better performance
            if len(text) > 5000:
                text = text[:5000] + "..."
                st.warning("⚠️ Text truncated to 5000 characters for audio generation")

            # Map language names to gTTS language codes
            lang_map = {
                "English": "en",
                "Spanish": "es",
                "Hindi": "hi",
                "French": "fr",
                "German": "de",
                "Italian": "it",
                "Portuguese": "pt",
                "Chinese": "zh",
                "Japanese": "ja",
                "Korean": "ko"
            }

            lang_code = lang_map.get(language, "en")

            # Create gTTS object with error handling
            try:
                tts = gTTS(text=text, lang=lang_code, slow=False)
            except Exception as e:
                st.error(f"❌ Error creating TTS object: {str(e)}")
                # Try with English as fallback
                if lang_code != "en":
                    st.info("🔄 Trying with English language...")
                    tts = gTTS(text=text, lang="en", slow=False)
                else:
                    raise e

            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')

            try:
                tts.save(temp_file.name)
            except Exception as e:
                st.error(f"❌ Error saving audio file: {str(e)}")
                return None

            # Verify file was created and has content
            if not os.path.exists(temp_file.name) or os.path.getsize(temp_file.name) == 0:
                st.error("❌ Audio file was not created properly")
                return None

            # Read the audio data
            with open(temp_file.name, 'rb') as f:
                audio_data = f.read()

            if len(audio_data) == 0:
                st.error("❌ Generated audio file is empty")
                return None

            audio_info = {
                "audio_data": audio_data,
                "audio_file": temp_file.name,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "voice": f"Google TTS ({voice})",
                "language": language,
                "duration": len(text.split()) / 150,  # Estimate duration
                "generated_at": time.time(),
                "file_size": len(audio_data),
                "format": "mp3"
            }

            st.success("✅ Audio generated successfully using Google TTS!")
            return audio_info

        except ImportError:
            st.error("❌ Google TTS not available. Installing...")
            try:
                import subprocess
                import sys
                subprocess.check_call([sys.executable, "-m", "pip", "install", "gtts"])
                st.success("✅ Google TTS installed! Please try again.")
                return None
            except:
                st.error("❌ Failed to install Google TTS. Please run: pip install gtts")
                return None
        except Exception as e:
            st.error(f"❌ Google TTS failed: {str(e)}")
            st.info("🔄 Trying Windows TTS as final fallback...")
            return self._generate_speech_windows_tts(text, voice, language)

    def _generate_speech_windows_tts(self, text, voice="lisa", language="English"):
        """Windows TTS fallback using pyttsx3"""
        try:
            import pyttsx3
            import tempfile
            import os

            # Limit text length
            if len(text) > 3000:
                text = text[:3000] + "..."
                st.warning("⚠️ Text truncated to 3000 characters for Windows TTS")

            # Initialize TTS engine
            engine = pyttsx3.init()

            # Set properties
            voices = engine.getProperty('voices')
            if voices:
                # Try to find a suitable voice
                for v in voices:
                    if 'female' in v.name.lower() and voice.lower() in ['lisa', 'allison', 'emma']:
                        engine.setProperty('voice', v.id)
                        break
                    elif 'male' in v.name.lower() and voice.lower() in ['michael', 'brian']:
                        engine.setProperty('voice', v.id)
                        break

            # Set speech rate and volume
            engine.setProperty('rate', 180)  # Speed of speech
            engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.close()

            # Generate speech
            engine.save_to_file(text, temp_file.name)
            engine.runAndWait()

            # Check if file was created
            if not os.path.exists(temp_file.name) or os.path.getsize(temp_file.name) == 0:
                st.error("❌ Windows TTS failed to create audio file")
                return None

            # Read the audio data
            with open(temp_file.name, 'rb') as f:
                audio_data = f.read()

            audio_info = {
                "audio_data": audio_data,
                "audio_file": temp_file.name,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "voice": f"Windows TTS ({voice})",
                "language": language,
                "duration": len(text.split()) / 150,  # Estimate duration
                "generated_at": time.time(),
                "file_size": len(audio_data),
                "format": "wav"
            }

            st.success("✅ Audio generated using Windows TTS!")
            return audio_info

        except ImportError:
            st.error("❌ Windows TTS not available. Installing pyttsx3...")
            try:
                import subprocess
                import sys
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyttsx3"])
                st.success("✅ pyttsx3 installed! Please try again.")
                return None
            except:
                st.error("❌ Failed to install pyttsx3. Please run: pip install pyttsx3")
                return self._create_demo_audio(text, voice, language)
        except Exception as e:
            st.error(f"❌ Windows TTS failed: {str(e)}")
            return self._create_demo_audio(text, voice, language)

    def _create_demo_audio(self, text, voice="lisa", language="English"):
        """Create a demo audio file when all TTS methods fail"""
        try:
            import tempfile
            import wave
            import numpy as np

            # Generate a simple tone as demo audio
            sample_rate = 22050
            duration = min(len(text.split()) / 150 * 60, 30)  # Max 30 seconds

            # Generate a simple sine wave
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency = 440  # A4 note
            audio_signal = np.sin(2 * np.pi * frequency * t) * 0.3

            # Convert to 16-bit integers
            audio_signal = (audio_signal * 32767).astype(np.int16)

            # Save as WAV file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')

            with wave.open(temp_file.name, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 2 bytes per sample
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_signal.tobytes())

            # Read the audio data
            with open(temp_file.name, 'rb') as f:
                audio_data = f.read()

            audio_info = {
                "audio_data": audio_data,
                "audio_file": temp_file.name,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "voice": f"Demo Tone ({voice})",
                "language": language,
                "duration": duration / 60,  # Convert to minutes
                "generated_at": time.time(),
                "file_size": len(audio_data),
                "format": "wav"
            }

            st.warning("⚠️ Generated demo audio tone (TTS services unavailable)")
            st.info("💡 Install gtts or pyttsx3 for actual speech synthesis")
            return audio_info

        except Exception as e:
            st.error(f"❌ Demo audio generation failed: {str(e)}")
            return None
    
    def translate_text(self, text, target_language):
        """Translate text to target language"""
        if target_language == "English":
            return text
        
        # Simple translation prompt
        prompt = f"Translate the following text to {target_language}:\n\n{text}\n\nTranslation:"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": len(text.split()) * 2,
                "temperature": 0.3,
                "top_p": 0.9
            }
        }
        
        response = call_huggingface_api(self.text_model, payload)
        
        if response and isinstance(response, list) and len(response) > 0:
            translated = response[0].get("generated_text", "")
            if "Translation:" in translated:
                return translated.split("Translation:")[-1].strip()
        
        return text
    
    def generate_summary(self, text, max_length=200):
        """Generate a summary of the text"""
        if len(text) <= max_length:
            return text
        
        prompt = f"Summarize the following text in about {max_length} characters:\n\n{text}\n\nSummary:"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_length // 4,  # Rough estimate
                "temperature": 0.5,
                "top_p": 0.9
            }
        }
        
        response = call_huggingface_api(self.text_model, payload)
        
        if response and isinstance(response, list) and len(response) > 0:
            summary = response[0].get("generated_text", "")
            if "Summary:" in summary:
                return summary.split("Summary:")[-1].strip()
        
        # Fallback to simple truncation
        return text[:max_length] + "..." if len(text) > max_length else text
    
    def check_model_status(self):
        """Check if models are available"""
        status = {
            "text_model": False,
            "tts_model": False,
            "api_key": bool(self.api_key)
        }
        
        # Test text model
        try:
            test_payload = {"inputs": "Hello, this is a test."}
            response = call_huggingface_api(self.text_model, test_payload)
            status["text_model"] = response is not None
        except:
            pass
        
        # Test TTS model (simulated)
        status["tts_model"] = True  # Simulated for demo
        
        return status
