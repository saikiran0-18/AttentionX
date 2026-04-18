import whisper


def transcribe_video(video_path: str, model_size: str = "base") -> dict:
    model = whisper.load_model(model_size)
    result = model.transcribe(video_path, verbose=False, task="translate")
    return result


def get_segments(result: dict) -> list:
    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "start": float(seg["start"]),
            "end": float(seg["end"]),
            "text": seg["text"].strip()
        })
    return segments