# AttentionX - Automated Content Repurposing Engine

## Problem
Long-form mentorship, lecture, and workshop videos contain valuable moments, but users consume content in short-form format.

## Solution
This app:
- uploads a long video
- transcribes it
- finds top highlight moments
- cuts short clips
- converts them into vertical format
- adds captions

## Tech Stack
- Python
- Streamlit
- Whisper
- MoviePy
- OpenCV

## How to Run
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py