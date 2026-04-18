# AttentionX - Automated Content Repurposing Engine

## Problem Statement
Long-form educational, mentorship, and workshop videos contain valuable information, but modern audiences usually prefer short-form content. Finding important moments manually, converting videos into vertical format, and adding captions takes time and effort.

## Solution
AttentionX is a prototype that takes a long-form video and automatically:
- transcribes the speech
- finds highlight moments
- extracts short clips
- converts them into vertical format
- adds captions for short-form platforms

## Features
- Upload long video
- Automatic speech transcription
- Highlight detection
- Short clip generation
- Vertical video formatting
- Caption overlay

## Tech Stack
- Python
- Streamlit
- OpenAI Whisper
- MoviePy
- OpenCV
- FFmpeg

## How to Run
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py