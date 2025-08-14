"""
EchoVerse Utility Functions
Contains helper functions for text processing, API calls, and file handling
"""

import requests
import json
import base64
import io
import time
import PyPDF2
import streamlit as st
from config import *

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def chunk_text(text, max_length=2000):
    """Split text into chunks for processing"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_length:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                chunks.append(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def call_huggingface_api(model_name, payload, max_retries=3):
    """Make API call to Hugging Face with retry logic"""
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    
    url = f"{HF_API_BASE}/{model_name}"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 503:
                # Model is loading, wait and retry
                time.sleep(10)
                continue
            elif response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            st.warning(f"Request timeout, retrying... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(5)
        except Exception as e:
            st.error(f"API call failed: {str(e)}")
            return None
    
    st.error("Failed to get response after multiple attempts")
    return None

def rewrite_text_with_tone(text, tone, intensity):
    """Rewrite text with specified tone and intensity using IBM Granite model"""
    if not text.strip():
        return text
    
    tone_config = TONE_OPTIONS.get(tone, TONE_OPTIONS["Neutral"])
    intensity_desc = INTENSITY_LEVELS.get(intensity, "moderate and balanced")
    
    prompt = f"""
    {tone_config['prompt_modifier']} 
    
    Apply a {intensity_desc} level of {tone.lower()} tone to the rewrite.
    
    Original text:
    {text}
    
    Rewritten text:
    """
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": len(text.split()) * 2,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True
        }
    }
    
    response = call_huggingface_api(TEXT_TO_TEXT_MODEL, payload)
    
    if response and isinstance(response, list) and len(response) > 0:
        generated_text = response[0].get("generated_text", "")
        # Extract only the rewritten part
        if "Rewritten text:" in generated_text:
            rewritten = generated_text.split("Rewritten text:")[-1].strip()
            return rewritten if rewritten else text
    
    return text

def generate_audio_from_text(text, voice="lisa"):
    """Generate audio from text using Microsoft SpeechT5 TTS"""
    if not text.strip():
        return None
    
    # For demo purposes, we'll simulate audio generation
    # In a real implementation, you would use the actual TTS model
    payload = {
        "inputs": text,
        "parameters": {
            "voice": voice
        }
    }
    
    # Simulate API call delay
    time.sleep(2)
    
    # Return a placeholder audio data (in real implementation, this would be actual audio)
    return f"Audio generated for: {text[:50]}..." if len(text) > 50 else f"Audio generated for: {text}"

def detect_chapters(text):
    """Detect chapters or sections in the text"""
    lines = text.split('\n')
    chapters = []
    current_pos = 0
    
    for i, line in enumerate(lines):
        line = line.strip()
        # Look for chapter indicators
        if (line.startswith(('Chapter', 'CHAPTER', 'Section', 'SECTION', 'Part', 'PART')) or
            (len(line) < 100 and line.isupper() and len(line) > 5)):
            chapters.append({
                'title': line,
                'start_line': i,
                'start_pos': current_pos
            })
        current_pos += len(line) + 1
    
    return chapters

def generate_summary(text, max_length=200):
    """Generate a summary of the text"""
    if len(text) <= max_length:
        return text
    
    # Simple extractive summary - take first and last sentences of each paragraph
    paragraphs = text.split('\n\n')
    summary_parts = []
    
    for para in paragraphs[:3]:  # First 3 paragraphs
        sentences = para.split('.')
        if len(sentences) > 1:
            summary_parts.append(sentences[0] + '.')
    
    summary = ' '.join(summary_parts)
    return summary[:max_length] + "..." if len(summary) > max_length else summary

def create_download_link(audio_data, filename):
    """Create a download link for audio file"""
    if isinstance(audio_data, str):
        # For demo purposes, create a text file
        b64 = base64.b64encode(audio_data.encode()).decode()
        href = f'<a href="data:text/plain;base64,{b64}" download="{filename}.txt">Download Audio File</a>'
        return href
    return None
