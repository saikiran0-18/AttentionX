import os
import textwrap
from moviepy import VideoFileClip, TextClip, CompositeVideoClip


def ensure_folder(path: str):
    os.makedirs(path, exist_ok=True)


def center_crop_to_vertical(clip, target_w=1080, target_h=1920):
    original_w, original_h = clip.size
    target_ratio = target_w / target_h
    original_ratio = original_w / original_h

    if original_ratio > target_ratio:
        new_w = int(original_h * target_ratio)
        x1 = (original_w - new_w) // 2
        cropped = clip.cropped(x1=x1, y1=0, x2=x1 + new_w, y2=original_h)
    else:
        new_h = int(original_w / target_ratio)
        y1 = (original_h - new_h) // 2
        cropped = clip.cropped(x1=0, y1=y1, x2=original_w, y2=y1 + new_h)

    return cropped.resized((target_w, target_h))


def create_caption_clip(text: str, width: int, height: int, duration: float):
    wrapped = "\n".join(textwrap.wrap(text, width=28))

    txt = TextClip(
        text=wrapped,
        font_size=28,
        color="white",
        method="caption",
        size=(int(width * 0.88), None)
    ).with_duration(duration)

    y_pos = int(height * 0.72)
    txt = txt.with_position(("center", y_pos))

    return txt


def export_highlight_clip(video_path: str, start: float, end: float, caption: str, output_path: str):
    with VideoFileClip(video_path) as clip:
        sub = clip.subclipped(start, end)
        vertical = center_crop_to_vertical(sub, 1080, 1920)

        caption_clip = create_caption_clip(
            text=caption,
            width=1080,
            height=1920,
            duration=(end - start)
        )

        final = CompositeVideoClip([vertical, caption_clip])
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=24
        )