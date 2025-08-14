"""
EchoVerse Landing Page
Animated landing page with educational theme
"""

import streamlit as st
import time
from streamlit_lottie import st_lottie
import requests

def load_lottie_url(url):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def show_landing_page():
    """Display the animated landing page"""

    # Custom CSS for animations and styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease infinite;
        margin-bottom: 1rem;
    }

    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out;
    }

    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transform: translateY(0);
        transition: all 0.3s ease;
        animation: slideInLeft 0.8s ease-out;
    }

    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }

    .cta-button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
    }

    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }

    .stat-item {
        text-align: center;
        animation: countUp 2s ease-out;
    }

    .stat-number {
        font-size: 3rem;
        font-weight: bold;
        color: #4ECDC4;
    }

    .stat-label {
        font-size: 1rem;
        color: #666;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    @keyframes countUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .floating-elements {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }

    .floating-element {
        position: absolute;
        opacity: 0.1;
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }

    .hero-bg {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><radialGradient id="a" cx="50%" cy="50%"><stop offset="0%" stop-color="%23ffffff" stop-opacity="0.1"/><stop offset="100%" stop-color="%23ffffff" stop-opacity="0"/></radialGradient></defs><circle cx="200" cy="200" r="100" fill="url(%23a)"/><circle cx="800" cy="300" r="150" fill="url(%23a)"/><circle cx="400" cy="700" r="120" fill="url(%23a)"/></svg>');
        animation: float 20s ease-in-out infinite;
    }

    .hero-content {
        position: relative;
        z-index: 2;
        max-width: 800px;
        margin: 0 auto;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        animation: fadeInUp 1s ease-out;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        margin-bottom: 2rem;
        opacity: 0.9;
        animation: fadeInUp 1s ease-out 0.2s both;
        line-height: 1.6;
    }

    .hero-cta {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: white;
        color: #667eea;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        animation: fadeInUp 1s ease-out 0.4s both;
    }

    .hero-cta:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        color: #667eea;
    }
    
    /* Features Section */
    .features-section {
        padding: 6rem 2rem;
        background: #f8fafc;
    }

    .features-container {
        max-width: 1200px;
        margin: 0 auto;
    }

    .features-header {
        text-align: center;
        margin-bottom: 4rem;
    }

    .features-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }

    .features-subtitle {
        font-size: 1.1rem;
        color: #666;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }

    .feature-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }

    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: block;
    }

    .feature-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }

    .feature-description {
        color: #666;
        line-height: 1.6;
        font-size: 1rem;
    }

    /* Stats Section */
    .stats-section {
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }

    .stat-item {
        padding: 1rem;
    }

    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        animation: countUp 2s ease-out;
    }

    .stat-label {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* CTA Section */
    .cta-section {
        padding: 6rem 2rem;
        background: #1a1a1a;
        color: white;
        text-align: center;
    }

    .cta-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .cta-subtitle {
        font-size: 1.1rem;
        opacity: 0.8;
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .cta-button {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white;
        padding: 1.25rem 2.5rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0, 123, 255, 0.3);
    }

    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0, 123, 255, 0.4);
        color: white;
    }
    
    /* Animations */
    @keyframes slideDown {
        from { transform: translateY(-100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    @keyframes fadeInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }

    @keyframes countUp {
        from { transform: scale(0.5); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .navbar {
            padding: 1rem;
        }

        .navbar-nav {
            display: none;
        }

        .hero-title {
            font-size: 2.5rem;
        }

        .hero-section {
            padding: 6rem 1rem 3rem 1rem;
        }

        .features-grid {
            grid-template-columns: 1fr;
        }

        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    /* Hide Streamlit elements */
    .stApp > header {
        display: none;
    }

    .stApp > .main > div {
        padding-top: 0;
    }

    #MainMenu {
        display: none;
    }

    footer {
        display: none;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .stat-item {
        text-align: center;
        animation: countUp 2s ease-out;
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: bold;
        color: #4ECDC4;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #666;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes countUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .floating-elements {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .floating-element {
        position: absolute;
        opacity: 0.1;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Floating background elements
    st.markdown("""
    <div class="floating-elements">
        <div class="floating-element" style="top: 10%; left: 10%; font-size: 2rem;">🎧</div>
        <div class="floating-element" style="top: 20%; right: 15%; font-size: 1.5rem;">📚</div>
        <div class="floating-element" style="top: 60%; left: 5%; font-size: 1.8rem;">🎵</div>
        <div class="floating-element" style="top: 70%; right: 10%; font-size: 2.2rem;">🎙️</div>
        <div class="floating-element" style="top: 40%; left: 80%; font-size: 1.6rem;">📖</div>
    </div>
    """, unsafe_allow_html=True)

    # Main header
    st.markdown('<h1 class="main-header">🎧 EchoVerse</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform Your Text into Captivating Audiobooks with AI</p>', unsafe_allow_html=True)

    # Get Started button below website name
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started Now", key="header_get_started", type="primary", use_container_width=True):
            st.session_state.show_auth = True
            st.rerun()

    # Hero section with animation placeholder
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Placeholder for Lottie animation (educational theme)
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin: 2rem 0;">
            <div style="font-size: 5rem; animation: pulse 2s infinite;">📚➡️🎧</div>
            <p style="color: white; font-size: 1.2rem; margin-top: 1rem;">AI-Powered Text to Audio Transformation</p>
        </div>
        """, unsafe_allow_html=True)



    # Statistics section
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-number">5+</div>
            <div class="stat-label">Voice Options</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-number">10+</div>
            <div class="stat-label">Languages</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-number">5</div>
            <div class="stat-label">Tone Styles</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-number">∞</div>
            <div class="stat-label">Possibilities</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Features section
    st.markdown("## ✨ Key Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎭 Tone-Adaptive Rewriting</h3>
            <p>Transform your text with AI-powered tone adaptation. Choose from Neutral, Suspenseful, Inspiring, Educational, or Storytelling styles with adjustable intensity levels.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>🌍 Multi-Language Support</h3>
            <p>Generate audiobooks in multiple languages including English, Spanish, Hindi, French, German, and more with regional accent options.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>📑 Smart Chapter Detection</h3>
            <p>Automatically detect chapters and sections, allowing you to navigate, skip, or replay specific parts of your audiobook.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎤 Premium Voice Options</h3>
            <p>Choose from high-quality AI voices including Lisa, Michael, Allison, Emma, and Brian for natural-sounding narration.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>📝 Interactive Bookmarks</h3>
            <p>Highlight text sections, add personal notes, and create bookmarks that are read aloud during narration for enhanced learning.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>⚡ Batch Processing</h3>
            <p>Convert multiple text files into audiobooks simultaneously with offline processing capabilities for maximum efficiency.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <h2 style="color: #333; margin-bottom: 1rem;">Ready to Transform Your Reading Experience?</h2>
            <p style="font-size: 1.1rem; color: #666; margin-bottom: 2rem;">Join thousands of users who have revolutionized their learning with EchoVerse</p>
        </div>
        """, unsafe_allow_html=True)





    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>© 2024 EchoVerse - Powered by IBM Watsonx & Hugging Face AI</p>
        <p>🎧 Transform • 🎭 Adapt • 🌍 Share</p>
    </div>
    """, unsafe_allow_html=True)
    

