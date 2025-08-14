"""
Modern Navigation Component for EchoVerse
ChatGPT-style navigation and layout
"""

import streamlit as st

def show_modern_navigation():
    """Display modern navigation bar like ChatGPT"""
    
    # Modern navigation CSS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide default Streamlit elements */
    .stApp > header {
        display: none;
    }
    
    #MainMenu {
        display: none;
    }
    
    footer {
        display: none;
    }
    
    .stApp > .main > div {
        padding-top: 0;
    }
    
    /* Modern Navigation */
    .modern-nav {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'Inter', sans-serif;
    }
    
    .nav-brand {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a1a;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .nav-menu {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-item {
        color: #666;
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background: #f8f9fa;
        color: #007bff;
    }
    
    .nav-item.active {
        background: #007bff;
        color: white;
    }
    
    .nav-user {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .user-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #007bff, #0056b3);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .user-name {
        font-weight: 500;
        color: #1a1a1a;
    }
    
    /* Main Content */
    .main-content {
        margin-top: 80px;
        min-height: calc(100vh - 80px);
        background: #f8fafc;
    }
    
    /* Sidebar */
    .modern-sidebar {
        position: fixed;
        left: 0;
        top: 80px;
        width: 280px;
        height: calc(100vh - 80px);
        background: white;
        border-right: 1px solid rgba(0, 0, 0, 0.1);
        padding: 2rem 0;
        overflow-y: auto;
        z-index: 999;
    }
    
    .sidebar-section {
        padding: 0 1.5rem;
        margin-bottom: 2rem;
    }
    
    .sidebar-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }
    
    .sidebar-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 8px;
        color: #374151;
        text-decoration: none;
        transition: all 0.2s ease;
        cursor: pointer;
        font-weight: 500;
    }
    
    .sidebar-item:hover {
        background: #f3f4f6;
        color: #007bff;
    }
    
    .sidebar-item.active {
        background: #eff6ff;
        color: #007bff;
        border-left: 3px solid #007bff;
    }
    
    .sidebar-icon {
        font-size: 1.25rem;
        width: 20px;
        text-align: center;
    }
    
    /* Content Area */
    .content-area {
        margin-left: 280px;
        padding: 2rem;
        min-height: calc(100vh - 80px);
    }
    
    .content-header {
        margin-bottom: 2rem;
    }
    
    .content-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    
    .content-subtitle {
        color: #6b7280;
        font-size: 1.1rem;
    }
    
    /* Responsive */
    @media (max-width: 1024px) {
        .modern-sidebar {
            transform: translateX(-100%);
            transition: transform 0.3s ease;
        }
        
        .content-area {
            margin-left: 0;
        }
        
        .nav-menu {
            display: none;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def show_navigation_bar(current_user=None, current_page="Home"):
    """Show the top navigation bar"""
    
    nav_items = [
        {"name": "Home", "icon": "🏠"},
        {"name": "Create", "icon": "✨"},
        {"name": "Library", "icon": "📚"},
        {"name": "Settings", "icon": "⚙️"}
    ]
    
    nav_html = f"""
    <nav class="modern-nav">
        <div class="nav-brand">
            🎧 EchoVerse
        </div>
        <div class="nav-menu">
    """
    
    for item in nav_items:
        active_class = "active" if item["name"] == current_page else ""
        nav_html += f"""
            <div class="nav-item {active_class}" onclick="navigateTo('{item["name"]}')">
                {item["icon"]} {item["name"]}
            </div>
        """
    
    nav_html += f"""
        </div>
        <div class="nav-user">
            <span class="user-name">{current_user or "User"}</span>
            <div class="user-avatar">{(current_user or "U")[0].upper()}</div>
        </div>
    </nav>
    """
    
    st.markdown(nav_html, unsafe_allow_html=True)

def show_sidebar_navigation(current_page="Home"):
    """Show the sidebar navigation"""
    
    sidebar_sections = [
        {
            "title": "Create",
            "items": [
                {"name": "Text Input", "icon": "📝", "key": "text_input"},
                {"name": "Generate Audio", "icon": "🎵", "key": "generate"},
                {"name": "Results", "icon": "📋", "key": "results"}
            ]
        },
        {
            "title": "Organize",
            "items": [
                {"name": "Bookmarks", "icon": "🔖", "key": "bookmarks"},
                {"name": "Chapters", "icon": "📚", "key": "chapters"},
                {"name": "Summary", "icon": "📊", "key": "summary"}
            ]
        },
        {
            "title": "Tools",
            "items": [
                {"name": "Batch Process", "icon": "📦", "key": "batch"},
                {"name": "Settings", "icon": "⚙️", "key": "settings"}
            ]
        }
    ]
    
    sidebar_html = """
    <div class="modern-sidebar">
    """
    
    for section in sidebar_sections:
        sidebar_html += f"""
        <div class="sidebar-section">
            <div class="sidebar-title">{section["title"]}</div>
        """
        
        for item in section["items"]:
            active_class = "active" if item["key"] == current_page else ""
            sidebar_html += f"""
            <div class="sidebar-item {active_class}" onclick="navigateToPage('{item["key"]}')">
                <span class="sidebar-icon">{item["icon"]}</span>
                {item["name"]}
            </div>
            """
        
        sidebar_html += "</div>"
    
    sidebar_html += "</div>"
    
    st.markdown(sidebar_html, unsafe_allow_html=True)

def show_content_area(title, subtitle=""):
    """Show the main content area"""
    
    content_html = f"""
    <div class="content-area">
        <div class="content-header">
            <h1 class="content-title">{title}</h1>
            {f'<p class="content-subtitle">{subtitle}</p>' if subtitle else ''}
        </div>
        <div class="content-body">
    """
    
    st.markdown(content_html, unsafe_allow_html=True)

def close_content_area():
    """Close the content area"""
    st.markdown("</div></div>", unsafe_allow_html=True)

def add_navigation_javascript():
    """Add JavaScript for navigation functionality"""
    
    st.markdown("""
    <script>
    function navigateTo(page) {
        // Handle top navigation
        console.log('Navigating to:', page);
        // You can add Streamlit navigation logic here
    }
    
    function navigateToPage(pageKey) {
        // Handle sidebar navigation
        console.log('Navigating to page:', pageKey);
        // You can add Streamlit navigation logic here
    }
    
    // Add smooth scrolling and interactions
    document.addEventListener('DOMContentLoaded', function() {
        // Add any additional JavaScript functionality here
    });
    </script>
    """, unsafe_allow_html=True)
