# 🎧 EchoVerse - AI Audiobook Creator

Transform your text into captivating audiobooks with AI-powered tone adaptation and natural voice synthesis.

## ✨ Features

### Core Features
- **🎭 Tone-Adaptive Text Rewriting**: Transform text with Neutral, Suspenseful, Inspiring, Educational, or Storytelling tones
- **🎤 High-Quality Voice Narration**: Choose from multiple AI voices (Lisa, Michael, Allison, Emma, Brian)
- **📱 User-Friendly Interface**: Intuitive Streamlit-based web interface
- **📥 Multiple Input Methods**: Support for text paste and file uploads (TXT, PDF)
- **🔄 Side-by-Side Comparison**: View original and rewritten text together

### Advanced Features
- **🌍 Multi-Language Support**: Generate audiobooks in 10+ languages
- **📚 Smart Chapter Detection**: Automatic chapter/section identification
- **🔖 Interactive Bookmarks**: Highlight text, add notes, and audio annotations
- **📊 Auto-Summary Generation**: Create quick summaries with audio previews
- **📦 Batch Processing**: Convert multiple files simultaneously
- **⚙️ Intensity Control**: Fine-tune emotional impact (Low, Medium, High)
- **🎵 Audio Controls**: Play, pause, skip chapters, adjust speed/pitch

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Hugging Face API key

### Installation

1. **Clone or download the project**
   ```bash
   cd pop
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL manually

## 🎯 How to Use

### 1. **Landing Page**
- View the animated landing page with feature overview
- Click "Get Started Now" to access the application

### 2. **Authentication**
- Sign up for a new account or login with existing credentials
- All user data is stored locally for privacy

### 3. **Text Input**
- **Paste Text**: Copy and paste your content directly
- **Upload Files**: Support for .txt and .pdf files up to 10MB
- View text statistics and chapter detection

### 4. **Generate Audiobook**
- **Choose Tone**: Select from 5 different tone styles
- **Set Intensity**: Adjust emotional impact level
- **Select Voice**: Pick your preferred narrator
- **Choose Language**: Support for multiple languages
- **Advanced Settings**: Control speed, pitch, and quality

### 5. **Results & Playback**
- **Text Comparison**: View original vs. rewritten text side-by-side
- **Audio Player**: Play, pause, and navigate through chapters
- **Download Options**: Get MP3 audio and text files

### 6. **Advanced Features**
- **Bookmarks**: Highlight important sections and add notes
- **Batch Processing**: Convert multiple files at once
- **Summary Generator**: Create automatic summaries
- **Chapter Navigator**: Jump between detected chapters

## 🛠️ Technical Details

### AI Models Used
- **Text Rewriting**: IBM Granite 3.0-2B Instruct
- **Text-to-Speech**: Microsoft SpeechT5 TTS
- **API Provider**: Hugging Face Inference API

### Architecture
- **Frontend**: Streamlit with custom CSS animations
- **Backend**: Python with modular design
- **Authentication**: Local JSON-based user management
- **File Processing**: PyPDF2 for PDF extraction
- **Audio Processing**: Simulated TTS pipeline (demo mode)

### File Structure
```
pop/
├── app.py                 # Main entry point
├── main_app.py           # Core application logic
├── config.py             # Configuration and settings
├── auth.py               # Authentication system
├── landing_page.py       # Animated landing page
├── text_processor.py     # Text input and processing
├── ai_models.py          # AI model integrations
├── audio_pipeline.py     # Audio generation pipeline
├── advanced_features.py  # Advanced functionality
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🎨 Customization

### Adding New Voices
Edit `config.py` to add new voice options:
```python
VOICE_OPTIONS = {
    "Your Voice": "voice_id",
    # ... existing voices
}
```

### Adding New Tones
Extend the tone options in `config.py`:
```python
TONE_OPTIONS = {
    "Your Tone": {
        "description": "Your description",
        "prompt_modifier": "Your prompt modification"
    }
}
```

### Styling
Modify the CSS in `main_app.py` and `landing_page.py` to customize the appearance.

## 🔧 Configuration

### API Keys
- Set your Hugging Face API key in `config.py`
- The current key is included for demo purposes

### File Limits
- Maximum file size: 10MB
- Maximum text length: 50,000 characters
- Supported formats: TXT, PDF

### Audio Settings
- Sample rate: 22,050 Hz
- Output format: MP3
- Quality levels: Standard, High, Premium

## 🚨 Important Notes

### Demo Mode
- This is a demonstration version
- Audio generation is simulated for demo purposes
- Real implementation would require actual TTS model deployment

### Privacy
- All user data is stored locally
- No data is sent to external servers except for AI processing
- Users can delete their accounts and data at any time

### Performance
- Processing time depends on text length and complexity
- Batch processing may take several minutes for large files
- Internet connection required for AI model access

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install --upgrade streamlit
   ```

2. **API Errors**
   - Check your internet connection
   - Verify Hugging Face API key
   - Try again after a few minutes (rate limiting)

3. **File Upload Issues**
   - Ensure file size is under 10MB
   - Check file format (TXT or PDF only)
   - Try converting PDF to text first

4. **Performance Issues**
   - Close other browser tabs
   - Restart the Streamlit application
   - Check system memory usage

## 📞 Support

For issues or questions:
1. Check this README for common solutions
2. Review the error messages in the application
3. Ensure all dependencies are properly installed

## 🎉 Features Coming Soon

- Real audio generation with actual TTS models
- Cloud deployment options
- Mobile app version
- Advanced voice cloning
- Background music integration
- Social sharing features

---

**EchoVerse** - Transform your reading experience with AI-powered audiobooks! 🎧📚
