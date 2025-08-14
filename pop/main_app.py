"""
EchoVerse Main Application
Streamlit-based web interface for the audiobook creation system
"""

import streamlit as st
from streamlit_option_menu import option_menu
import time

# Import all modules
from config import *
from auth import *
from landing_page import show_landing_page
from text_processor import TextProcessor
from audio_pipeline import AudioPipeline
from advanced_features import AdvancedFeatures


# Configure Streamlit page
st.set_page_config(**PAGE_CONFIG)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    if 'show_auth' not in st.session_state:
        st.session_state.show_auth = False

def show_sidebar():
    """Display sidebar navigation"""
    with st.sidebar:
        # User info
        if is_authenticated():
            st.markdown(f"### 👋 Welcome, {get_current_user()}!")

            # Navigation menu with improved styling
            selected = option_menu(
                "EchoVerse",
                ["🏠 Home", "📝 Text Input", "🎛️ Generate", "📋 Results", "🔖 Bookmarks", "📦 Batch", "📊 Summary", "📚 Chapters"],
                icons=['house', 'file-text', 'gear', 'list-task', 'bookmark', 'archive', 'bar-chart', 'book'],
                menu_icon="headphones",
                default_index=st.session_state.get('nav_index', 0),
                styles={
                    "container": {"padding": "0!important", "background-color": "#f8f9fa"},
                    "icon": {"color": "#28a745", "font-size": "18px"},
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#e9ecef", "color": "#212529"},
                    "nav-link-selected": {"background-color": "#28a745", "color": "white"},
                }
            )

            # Store selected index
            if selected:
                nav_options = ["🏠 Home", "📝 Text Input", "🎛️ Generate", "📋 Results", "🔖 Bookmarks", "📦 Batch", "📊 Summary", "📚 Chapters"]
                st.session_state.nav_index = nav_options.index(selected)

            # Logout button
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                logout()

            return selected
        else:
            st.markdown("### 🎧 EchoVerse")
            st.markdown("Please login to access the application.")
            return None

def show_main_content(page):
    """Display main content based on selected page"""
    # Initialize components
    text_processor = TextProcessor()
    audio_pipeline = AudioPipeline()
    advanced_features = AdvancedFeatures()
    
    if page == "🏠 Home":
        show_home_dashboard()
    
    elif page == "📝 Text Input":
        text_processor.show_text_input_interface()
        st.markdown("---")
        text_processor.show_text_preview()
    
    elif page == "🎛️ Generate":
        audio_pipeline.show_generation_interface()
    
    elif page == "📋 Results":
        audio_pipeline.show_results_interface()
    
    elif page == "🔖 Bookmarks":
        advanced_features.show_bookmarks_interface()
    
    elif page == "📦 Batch":
        advanced_features.show_batch_processing_interface()
    
    elif page == "📊 Summary":
        advanced_features.show_summary_generator()
    
    elif page == "📚 Chapters":
        advanced_features.show_chapter_navigator()

def show_home_dashboard():
    """Display home dashboard"""
    st.markdown("# 🎧 EchoVerse Dashboard")
    st.markdown("### Transform your text into captivating audiobooks with AI")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Audiobooks Created", "0", delta="0")
    
    with col2:
        st.metric("⏱️ Total Audio Time", "0 min", delta="0")
    
    with col3:
        st.metric("📝 Words Processed", "0", delta="0")
    
    with col4:
        st.metric("🔖 Bookmarks", len(st.session_state.get('bookmarks', [])))
    
    # Quick actions
    st.markdown("## 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Start New Project", use_container_width=True, type="primary"):
            st.success("🚀 Starting new project...")
            st.session_state.nav_index = 1  # Text Input page
            st.rerun()

    with col2:
        if st.button("📦 Batch Process", use_container_width=True):
            st.success("📦 Opening batch processor...")
            st.session_state.nav_index = 5  # Batch page
            st.rerun()

    with col3:
        if st.button("📊 Generate Summary", use_container_width=True):
            st.success("📊 Opening summary generator...")
            st.session_state.nav_index = 6  # Summary page
            st.rerun()
    
    # Recent activity
    st.markdown("## 📈 Recent Activity")
    
    if st.session_state.get('original_text'):
        st.success("✅ Text loaded and ready for processing")
        
        if st.session_state.get('rewritten_text'):
            st.success("✅ Text rewritten with tone adaptation")
        
        if st.session_state.get('audio_data'):
            st.success("✅ Audio generated successfully")
    else:
        st.info("👋 Welcome! Start by uploading text or pasting content in the Text Input section.")
    
    # Tips and tutorials
    st.markdown("## 💡 Tips & Tutorials")
    
    with st.expander("🎭 How to Choose the Right Tone"):
        st.markdown("""
        - **Neutral**: Best for educational content, news articles, and factual material
        - **Suspenseful**: Perfect for mystery stories, thrillers, and dramatic content
        - **Inspiring**: Great for motivational content, speeches, and self-help material
        - **Educational**: Ideal for textbooks, tutorials, and instructional content
        - **Storytelling**: Perfect for novels, short stories, and narrative content
        """)
    
    with st.expander("🎤 Voice Selection Guide"):
        st.markdown("""
        - **Lisa**: Clear, professional female voice - great for business content
        - **Michael**: Warm, authoritative male voice - perfect for educational material
        - **Allison**: Friendly, conversational female voice - ideal for casual content
        - **Emma**: Youthful, energetic female voice - great for children's content
        - **Brian**: Deep, resonant male voice - perfect for dramatic content
        """)
    
    with st.expander("🔖 Using Bookmarks Effectively"):
        st.markdown("""
        - Highlight important concepts or quotes
        - Add personal notes for better understanding
        - Use different bookmark types to organize content
        - Enable "read aloud" for important notes during narration
        - Create chapter summaries with bookmarks
        """)

def main():
    """Main application function"""
    init_session_state()
    
    # Custom CSS for better styling with green theme and animations
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    .main > div {
        padding-top: 2rem;
        font-family: 'Poppins', sans-serif;
    }

    /* Animated background */
    .stApp {
        background: linear-gradient(-45deg, #e8f5e8, #f0f8f0, #e8f5e8, #f5f9f5);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Floating animation elements */
    .floating-icons {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }

    .floating-icon {
        position: absolute;
        opacity: 0.1;
        animation: float 8s ease-in-out infinite;
        font-size: 2rem;
    }

    .floating-icon:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
    .floating-icon:nth-child(2) { top: 20%; right: 10%; animation-delay: 2s; }
    .floating-icon:nth-child(3) { top: 60%; left: 5%; animation-delay: 4s; }
    .floating-icon:nth-child(4) { top: 70%; right: 15%; animation-delay: 6s; }
    .floating-icon:nth-child(5) { top: 40%; left: 80%; animation-delay: 1s; }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }

    /* Green button styling */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #28a745, #20c997, #28a745);
        background-size: 200% 200%;
        color: white;
        transition: all 0.4s ease;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        animation: buttonGlow 2s ease-in-out infinite alternate;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
        background-position: 100% 0;
        animation: none;
    }

    .stButton > button:active {
        transform: translateY(-1px) scale(0.98);
    }

    @keyframes buttonGlow {
        0% { box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3); }
        100% { box-shadow: 0 6px 20px rgba(40, 167, 69, 0.5); }
    }

    /* Primary button special styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #198754, #20c997, #0d6efd);
        animation: primaryPulse 3s ease-in-out infinite;
    }

    @keyframes primaryPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    /* Metrics styling */
    .stMetric {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border: 2px solid #28a745;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        animation: metricFloat 4s ease-in-out infinite;
    }

    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.2);
    }

    @keyframes metricFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-3px); }
    }

    /* Success messages */
    .success-message {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border: 2px solid #28a745;
        color: #155724;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        animation: successSlide 0.5s ease-out;
    }

    @keyframes successSlide {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    /* Info messages */
    .info-message {
        background: linear-gradient(135deg, #d1ecf1, #bee5eb);
        border: 2px solid #17a2b8;
        color: #0c5460;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        animation: infoFade 0.5s ease-in;
    }

    @keyframes infoFade {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa, #e9ecef);
        border-right: 3px solid #28a745;
    }

    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #28a745, #20c997);
        animation: progressGlow 2s ease-in-out infinite alternate;
    }

    @keyframes progressGlow {
        0% { box-shadow: 0 0 5px rgba(40, 167, 69, 0.5); }
        100% { box-shadow: 0 0 15px rgba(40, 167, 69, 0.8); }
    }

    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #28a745 !important;
        animation: spinGlow 1s linear infinite;
    }

    @keyframes spinGlow {
        0% { filter: drop-shadow(0 0 5px rgba(40, 167, 69, 0.5)); }
        50% { filter: drop-shadow(0 0 10px rgba(40, 167, 69, 0.8)); }
        100% { filter: drop-shadow(0 0 5px rgba(40, 167, 69, 0.5)); }
    }

    /* Audio player styling */
    audio {
        width: 100%;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
    }

    /* Text area styling */
    .stTextArea > div > div > textarea {
        border: 2px solid #28a745;
        border-radius: 10px;
        transition: all 0.3s ease;
        color: #212529 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        background-color: #ffffff !important;
    }

    .stTextArea > div > div > textarea:focus {
        box-shadow: 0 0 15px rgba(40, 167, 69, 0.3);
        border-color: #20c997;
        color: #000000 !important;
    }

    /* Text input styling */
    .stTextInput > div > div > input {
        border: 2px solid #28a745;
        border-radius: 8px;
        color: #212529 !important;
        font-weight: 500 !important;
        background-color: #ffffff !important;
    }

    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 10px rgba(40, 167, 69, 0.3);
        border-color: #20c997;
        color: #000000 !important;
    }

    /* Selectbox styling */
    .stSelectbox > div > div > select {
        border: 2px solid #28a745;
        border-radius: 8px;
        color: #212529 !important;
        font-weight: 500 !important;
    }

    /* Make all text darker and more visible */
    .stMarkdown, .stText, p, span, div {
        color: #212529 !important;
    }

    /* Placeholder text styling */
    .stTextArea > div > div > textarea::placeholder,
    .stTextInput > div > div > input::placeholder {
        color: #6c757d !important;
        font-weight: 400 !important;
    }
    </style>

    <!-- Floating animation elements -->
    <div class="floating-icons">
        <div class="floating-icon">🎧</div>
        <div class="floating-icon">📚</div>
        <div class="floating-icon">🎵</div>
        <div class="floating-icon">🎙️</div>
        <div class="floating-icon">📖</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check authentication
    if not is_authenticated():
        # Show landing page or auth
        if st.session_state.get('show_auth'):
            st.markdown("# 🎧 EchoVerse")
            show_auth_page()
        else:
            show_landing_page()
    else:
        # Show main application
        selected_page = show_sidebar()

        if selected_page:
            show_main_content(selected_page)
        else:
            show_home_dashboard()





if __name__ == "__main__":
    main()
