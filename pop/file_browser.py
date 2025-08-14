"""
EchoVerse File Browser
Simple file browser to view the pop folder contents
"""

import streamlit as st
import os
import mimetypes
from pathlib import Path

def show_file_browser():
    """Display file browser for the pop folder"""
    
    st.set_page_config(
        page_title="EchoVerse - File Browser",
        page_icon="📁",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .file-browser {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .file-item {
        display: flex;
        align-items: center;
        padding: 0.5rem;
        border-bottom: 1px solid #eee;
        transition: background 0.3s ease;
    }
    
    .file-item:hover {
        background: #f8f9fa;
    }
    
    .file-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
        width: 30px;
    }
    
    .file-name {
        flex: 1;
        font-weight: 500;
    }
    
    .file-size {
        color: #666;
        font-size: 0.9rem;
    }
    
    .folder-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="folder-header">
        <h1>📁 EchoVerse Project Files</h1>
        <p>Browse and explore the pop folder contents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current directory
    current_dir = Path(".")
    
    # Show folder info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_files = len([f for f in current_dir.iterdir() if f.is_file()])
        st.metric("📄 Total Files", total_files)
    
    with col2:
        python_files = len([f for f in current_dir.glob("*.py")])
        st.metric("🐍 Python Files", python_files)
    
    with col3:
        md_files = len([f for f in current_dir.glob("*.md")])
        st.metric("📝 Documentation", md_files)
    
    # File categories
    st.markdown("## 📂 File Categories")
    
    # Categorize files
    categories = {
        "🐍 Python Files": [],
        "📝 Documentation": [],
        "⚙️ Configuration": [],
        "📁 Other Files": []
    }
    
    for file_path in current_dir.iterdir():
        if file_path.is_file():
            file_name = file_path.name
            file_size = file_path.stat().st_size
            
            if file_name.endswith('.py'):
                categories["🐍 Python Files"].append((file_name, file_size))
            elif file_name.endswith('.md'):
                categories["📝 Documentation"].append((file_name, file_size))
            elif file_name.endswith(('.json', '.txt', '.yml', '.yaml')):
                categories["⚙️ Configuration"].append((file_name, file_size))
            else:
                categories["📁 Other Files"].append((file_name, file_size))
    
    # Display categories
    for category, files in categories.items():
        if files:
            with st.expander(f"{category} ({len(files)} files)"):
                for file_name, file_size in sorted(files):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        # Get file icon
                        icon = get_file_icon(file_name)
                        st.markdown(f"{icon} **{file_name}**")
                    
                    with col2:
                        st.write(f"{file_size:,} bytes")
                    
                    with col3:
                        if st.button("👁️ View", key=f"view_{file_name}"):
                            show_file_content(file_name)
    
    # Quick access to main files
    st.markdown("## 🚀 Quick Access")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎧 Run EchoVerse", type="primary", use_container_width=True):
            st.code("streamlit run app.py", language="bash")
            st.info("Copy this command to your terminal to run EchoVerse")
    
    with col2:
        if st.button("📖 View README", use_container_width=True):
            show_file_content("README.md")
    
    with col3:
        if st.button("🔧 View Config", use_container_width=True):
            show_file_content("config.py")

def get_file_icon(filename):
    """Get appropriate icon for file type"""
    ext = filename.split('.')[-1].lower()
    
    icons = {
        'py': '🐍',
        'md': '📝',
        'txt': '📄',
        'json': '⚙️',
        'yml': '⚙️',
        'yaml': '⚙️',
        'html': '🌐',
        'css': '🎨',
        'js': '⚡',
        'png': '🖼️',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'gif': '🖼️',
        'mp3': '🎵',
        'wav': '🎵',
        'pdf': '📕'
    }
    
    return icons.get(ext, '📄')

def show_file_content(filename):
    """Display file content"""
    try:
        file_path = Path(filename)
        
        if file_path.exists():
            st.markdown(f"### 📄 {filename}")
            
            # Read file content
            if filename.endswith(('.py', '.md', '.txt', '.json', '.yml', '.yaml')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Determine language for syntax highlighting
                if filename.endswith('.py'):
                    st.code(content, language='python')
                elif filename.endswith('.md'):
                    st.markdown(content)
                elif filename.endswith('.json'):
                    st.code(content, language='json')
                else:
                    st.code(content)
            else:
                st.info(f"Cannot preview {filename} - binary file or unsupported format")
        else:
            st.error(f"File {filename} not found")
    
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")

def main():
    """Main function"""
    show_file_browser()

if __name__ == "__main__":
    main()
