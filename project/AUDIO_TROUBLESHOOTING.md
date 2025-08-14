# 🎧 EchoVerse Audio Troubleshooting Guide

## 🔧 Audio Generation Issues

### Problem: "API Error: 404 - Not Found"

**Cause:** The Hugging Face TTS model endpoint is not available or the model name is incorrect.

**Solution:** EchoVerse now automatically uses Google TTS as the primary method, which is more reliable.

### Problem: "Google TTS failed"

**Possible Causes:**
1. No internet connection
2. Google TTS service temporarily unavailable
3. Text is too long

**Solutions:**
1. **Check Internet Connection**
   ```
   - Ensure you have a stable internet connection
   - Try refreshing the page
   ```

2. **Reduce Text Length**
   ```
   - Try with shorter text (under 1000 characters)
   - Break long text into smaller chunks
   ```

3. **Use Windows TTS Fallback**
   ```
   - The app will automatically try Windows TTS if Google TTS fails
   - This works offline but requires pyttsx3 library
   ```

### Problem: "Windows TTS not available"

**Solution:** Install the required library:
```bash
pip install pyttsx3
```

### Problem: "All TTS methods failed"

**Fallback:** The app will generate a demo audio tone as a placeholder.

## 🚀 Recommended Solutions

### 1. **Primary Method: Google TTS (Recommended)**
- **Pros:** Reliable, high quality, multiple languages
- **Cons:** Requires internet connection
- **Best for:** Most users, production use

### 2. **Fallback Method: Windows TTS**
- **Pros:** Works offline, fast
- **Cons:** Limited voices, Windows only
- **Best for:** Offline use, testing

### 3. **Demo Method: Audio Tone**
- **Pros:** Always works
- **Cons:** Not actual speech
- **Best for:** Testing the audio pipeline

## 🔍 Debugging Steps

### Step 1: Check Dependencies
```bash
pip install gtts pyttsx3 scipy numpy
```

### Step 2: Test Audio Generation
1. Go to the EchoVerse app
2. Navigate to "Text Input"
3. Enter a short test text: "Hello, this is a test."
4. Go to "Generate" and click "Generate Audiobook"
5. Check the Results section for audio player

### Step 3: Check Error Messages
- **Green Success Message:** Audio generated successfully
- **Yellow Warning:** Fallback method used
- **Red Error:** Generation failed, check internet/dependencies

### Step 4: Manual Testing
Run the test script:
```bash
streamlit run test_audio.py
```

## 📋 Common Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| "API Error: 404" | HF model not found | Use Google TTS (automatic) |
| "Request timeout" | Slow internet | Try shorter text |
| "Google TTS not available" | Missing gtts | `pip install gtts` |
| "Windows TTS failed" | Missing pyttsx3 | `pip install pyttsx3` |
| "Demo audio generated" | All TTS failed | Check internet & dependencies |

## 🎯 Best Practices

### For Best Audio Quality:
1. **Use shorter sentences** (under 1000 characters)
2. **Check internet connection** before generating
3. **Use simple punctuation** (avoid special characters)
4. **Choose appropriate language** settings

### For Reliability:
1. **Keep text under 5000 characters** for Google TTS
2. **Use English language** for best compatibility
3. **Have backup internet connection**
4. **Install all TTS libraries** for fallback options

## 🔄 Recovery Steps

If audio generation completely fails:

1. **Restart the application**
   ```bash
   # Stop current app (Ctrl+C)
   streamlit run app.py
   ```

2. **Clear browser cache**
   - Refresh the page (F5)
   - Clear browser cache and cookies

3. **Reinstall dependencies**
   ```bash
   pip uninstall gtts pyttsx3
   pip install gtts pyttsx3
   ```

4. **Check system requirements**
   - Windows 10/11 for Windows TTS
   - Python 3.8+ 
   - Stable internet connection

## 📞 Support

If you continue to experience issues:

1. **Check the console output** for detailed error messages
2. **Try the test script** (`test_audio.py`) to isolate the problem
3. **Verify all dependencies** are installed correctly
4. **Test with minimal text** first

## 🎉 Success Indicators

You'll know audio generation is working when you see:
- ✅ "Audio generated successfully using Google TTS!"
- 🎵 Audio player appears in the Results section
- 📥 Download button is enabled
- 🔊 Audio plays when clicked

---

**Note:** EchoVerse now prioritizes reliability over advanced features. Google TTS is used as the primary method because it's more stable than experimental Hugging Face TTS models.
