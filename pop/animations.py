"""
EchoVerse Animation Components
Custom animations and visual effects for the application
"""

import streamlit as st
import time

def show_loading_animation(message="Processing...", duration=3):
    """Show a custom loading animation"""
    
    # Create loading animation HTML
    loading_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; padding: 2rem;">
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <div class="loading-text">{message}</div>
        </div>
    </div>
    
    <style>
    .loading-container {{
        text-align: center;
        animation: fadeIn 0.5s ease-in;
    }}
    
    .loading-spinner {{
        width: 60px;
        height: 60px;
        border: 4px solid #e9ecef;
        border-top: 4px solid #28a745;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem auto;
        box-shadow: 0 0 20px rgba(40, 167, 69, 0.3);
    }}
    
    .loading-text {{
        font-size: 1.2rem;
        color: #28a745;
        font-weight: 600;
        animation: pulse 2s ease-in-out infinite;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.6; }}
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>
    """
    
    # Display the animation
    placeholder = st.empty()
    placeholder.markdown(loading_html, unsafe_allow_html=True)
    
    # Simulate processing time
    time.sleep(duration)
    
    # Clear the animation
    placeholder.empty()

def show_success_animation(message="Success!"):
    """Show a success animation"""
    
    success_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; padding: 1rem;">
        <div class="success-container">
            <div class="success-icon">✅</div>
            <div class="success-text">{message}</div>
        </div>
    </div>
    
    <style>
    .success-container {{
        text-align: center;
        animation: successBounce 0.6s ease-out;
    }}
    
    .success-icon {{
        font-size: 3rem;
        animation: iconBounce 0.8s ease-out;
        margin-bottom: 0.5rem;
    }}
    
    .success-text {{
        font-size: 1.1rem;
        color: #28a745;
        font-weight: 600;
        animation: textSlide 0.5s ease-out 0.3s both;
    }}
    
    @keyframes successBounce {{
        0% {{ transform: scale(0.3) rotate(-10deg); opacity: 0; }}
        50% {{ transform: scale(1.1) rotate(5deg); }}
        100% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
    }}
    
    @keyframes iconBounce {{
        0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
        40% {{ transform: translateY(-10px); }}
        60% {{ transform: translateY(-5px); }}
    }}
    
    @keyframes textSlide {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    </style>
    """
    
    st.markdown(success_html, unsafe_allow_html=True)

def show_progress_animation(progress, message="Processing..."):
    """Show an animated progress bar"""
    
    progress_html = f"""
    <div class="progress-container">
        <div class="progress-text">{message}</div>
        <div class="progress-bar-container">
            <div class="progress-bar" style="width: {progress}%"></div>
        </div>
        <div class="progress-percentage">{progress}%</div>
    </div>
    
    <style>
    .progress-container {{
        padding: 1rem;
        text-align: center;
        animation: fadeIn 0.5s ease-in;
    }}
    
    .progress-text {{
        font-size: 1.1rem;
        color: #28a745;
        font-weight: 600;
        margin-bottom: 1rem;
        animation: pulse 2s ease-in-out infinite;
    }}
    
    .progress-bar-container {{
        width: 100%;
        height: 20px;
        background-color: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }}
    
    .progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, #28a745, #20c997, #28a745);
        background-size: 200% 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
        animation: progressShine 2s linear infinite;
        box-shadow: 0 0 10px rgba(40, 167, 69, 0.5);
    }}
    
    .progress-percentage {{
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
    }}
    
    @keyframes progressShine {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>
    """
    
    return progress_html

def show_audio_wave_animation():
    """Show an audio wave animation"""
    
    wave_html = """
    <div class="audio-wave-container">
        <div class="wave-text">🎵 Generating Audio...</div>
        <div class="audio-wave">
            <div class="wave-bar"></div>
            <div class="wave-bar"></div>
            <div class="wave-bar"></div>
            <div class="wave-bar"></div>
            <div class="wave-bar"></div>
        </div>
    </div>
    
    <style>
    .audio-wave-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem;
        animation: fadeIn 0.5s ease-in;
    }
    
    .wave-text {
        font-size: 1.2rem;
        color: #28a745;
        font-weight: 600;
        margin-bottom: 1rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .audio-wave {
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .wave-bar {
        width: 6px;
        height: 20px;
        background: linear-gradient(180deg, #28a745, #20c997);
        border-radius: 3px;
        animation: waveAnimation 1.5s ease-in-out infinite;
    }
    
    .wave-bar:nth-child(1) { animation-delay: 0s; }
    .wave-bar:nth-child(2) { animation-delay: 0.1s; }
    .wave-bar:nth-child(3) { animation-delay: 0.2s; }
    .wave-bar:nth-child(4) { animation-delay: 0.3s; }
    .wave-bar:nth-child(5) { animation-delay: 0.4s; }
    
    @keyframes waveAnimation {
        0%, 100% { height: 20px; }
        50% { height: 40px; }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """
    
    return wave_html

def show_typing_animation(text, speed=0.05):
    """Show a typing animation effect"""
    
    placeholder = st.empty()
    displayed_text = ""
    
    for char in text:
        displayed_text += char
        placeholder.markdown(f"""
        <div style="font-family: 'Courier New', monospace; font-size: 1.1rem; color: #28a745; padding: 1rem; background: #f8f9fa; border-radius: 10px; border-left: 4px solid #28a745;">
            {displayed_text}<span style="animation: blink 1s infinite;">|</span>
        </div>
        
        <style>
        @keyframes blink {{
            0%, 50% {{ opacity: 1; }}
            51%, 100% {{ opacity: 0; }}
        }}
        </style>
        """, unsafe_allow_html=True)
        time.sleep(speed)
    
    # Remove cursor after typing is complete
    placeholder.markdown(f"""
    <div style="font-family: 'Courier New', monospace; font-size: 1.1rem; color: #28a745; padding: 1rem; background: #f8f9fa; border-radius: 10px; border-left: 4px solid #28a745;">
        {displayed_text}
    </div>
    """, unsafe_allow_html=True)
