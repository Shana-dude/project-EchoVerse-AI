"""
EchoVerse Authentication System
Handles user login, signup, and session management
"""

import streamlit as st
import bcrypt
import json
import os
from datetime import datetime

# User database file
USER_DB_FILE = "users.json"

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USER_DB_FILE):
        try:
            with open(USER_DB_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(username, email, password):
    """Register a new user"""
    users = load_users()
    
    if username in users:
        return False, "Username already exists"
    
    # Check if email already exists
    for user_data in users.values():
        if user_data.get('email') == email:
            return False, "Email already registered"
    
    # Create new user
    users[username] = {
        'email': email,
        'password': hash_password(password),
        'created_at': datetime.now().isoformat(),
        'last_login': None
    }
    
    save_users(users)
    return True, "User registered successfully"

def authenticate_user(username, password):
    """Authenticate user login"""
    users = load_users()
    
    if username not in users:
        return False, "Username not found"
    
    if verify_password(password, users[username]['password']):
        # Update last login
        users[username]['last_login'] = datetime.now().isoformat()
        save_users(users)
        return True, "Login successful"
    
    return False, "Invalid password"

def show_login_form():
    """Display login form"""
    st.markdown("### 🔐 Login to EchoVerse")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
        
        if submit_button:
            if username and password:
                success, message = authenticate_user(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")

def show_signup_form():
    """Display signup form"""
    st.markdown("### 📝 Create EchoVerse Account")
    
    with st.form("signup_form"):
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        submit_button = st.form_submit_button("✨ Create Account", use_container_width=True, type="primary")
        
        if submit_button:
            if username and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    success, message = register_user(username, email, password)
                    if success:
                        st.success(message)
                        st.info("Please login with your new account")
                    else:
                        st.error(message)
            else:
                st.error("Please fill in all fields")

def show_auth_page():
    """Display authentication page with login/signup options"""

    # Add custom styling for auth page
    st.markdown("""
    <style>
    /* Auth page specific styling */
    .auth-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid #28a745;
    }

    .auth-title {
        text-align: center;
        color: #28a745;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        animation: titleGlow 2s ease-in-out infinite alternate;
    }

    @keyframes titleGlow {
        0% { text-shadow: 0 0 10px rgba(40, 167, 69, 0.3); }
        100% { text-shadow: 0 0 20px rgba(40, 167, 69, 0.6); }
    }

    /* Form styling */
    .stForm {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid #28a745;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(90deg, #28a745, #20c997);
        border-radius: 10px;
        padding: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.2);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #28a745 !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    # Auth page header
    st.markdown('<div class="auth-title">🎧 EchoVerse</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #6c757d; margin-bottom: 2rem; font-size: 1.1rem;">AI-Powered Audiobook Creator</div>', unsafe_allow_html=True)

    # Create tabs for login and signup
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab1:
        show_login_form()

    with tab2:
        show_signup_form()

def logout():
    """Logout user and clear session"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user():
    """Get current logged in username"""
    return st.session_state.get('username', None)
