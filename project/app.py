"""
EchoVerse - AI Audiobook Creator
Main entry point for the Streamlit application
"""

import streamlit as st
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import main application
from main_app import main

if __name__ == "__main__":
    main()
