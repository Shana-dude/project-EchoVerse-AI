"""
EchoVerse Runner Script
Simple script to launch the Streamlit application
"""

import subprocess
import sys
import os

def main():
    """Launch the EchoVerse application"""
    print("🎧 Starting EchoVerse - AI Audiobook Creator...")
    print("=" * 50)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit found")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    
    # Launch the application
    try:
        print("🚀 Launching application...")
        print("📱 Opening browser at http://localhost:8501")
        print("🛑 Press Ctrl+C to stop the application")
        print("=" * 50)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "false",
            "--server.runOnSave", "true",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")

if __name__ == "__main__":
    main()
