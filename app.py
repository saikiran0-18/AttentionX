import os
import shutil
import streamlit as st

from transcribe import transcribe_video, get_segments
from highlights import find_top_highlights
from video_utils import ensure_folder, export_highlight_clip


TEMP_DIR = "temp"
OUTPUT_DIR = os.path.join(TEMP_DIR, "outputs")
UPLOAD_PATH = os.path.join(TEMP_DIR, "uploaded_video.mp4")


def reset_temp():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    ensure_folder(TEMP_DIR)
    ensure_folder(OUTPUT_DIR)


st.set_page_config(page_title="AttentionX MVP", layout="wide")

st.title("AttentionX - Automated Content Repurposing Engine")
st.write("Upload a long video, extract top moments, and generate short vertical clips.")

uploaded_file = st.file_uploader(
    "Upload a video",
    type=["mp4", "mov", "mkv", "avi"]
)

top_k = st.slider("How many short clips?", min_value=1, max_value=5, value=3)
model_size = st.selectbox("Whisper model size", ["tiny", "base", "small"], index=1)

if uploaded_file is not None:
    reset_temp()

    with open(UPLOAD_PATH, "wb") as f:
        f.write(uploaded_file.read())

    st.video(UPLOAD_PATH)

    if st.button("Process Video"):
        with st.spinner("Transcribing video..."):
            result = transcribe_video(UPLOAD_PATH, model_size=model_size)
            segments = get_segments(result)

        st.success("Transcription complete.")

        full_text = result.get("text", "").strip()
        with st.expander("See transcript"):
            st.write(full_text if full_text else "No transcript found.")

        with st.spinner("Finding best moments..."):
            highlights = find_top_highlights(segments, top_k=top_k)

        if not highlights:
            st.error("No strong highlights found. Try a longer or clearer video.")
        else:
            st.subheader("Selected Highlights")

            for i, h in enumerate(highlights, start=1):
                st.markdown(f"**Clip {i}**")
                st.write(f"Start: {h['start']} sec")
                st.write(f"End: {h['end']} sec")
                st.write(f"Score: {h['score']}")
                st.write(h["text"])
                st.write("---")

            st.subheader("Generating short clips")

            output_files = []
            progress = st.progress(0)

            for i, h in enumerate(highlights, start=1):
                out_path = os.path.join(OUTPUT_DIR, f"clip_{i}.mp4")
                caption = h["text"][:35]

                export_highlight_clip(
                    video_path=UPLOAD_PATH,
                    start=h["start"],
                    end=h["end"],
                    caption=caption,
                    output_path=out_path
                )

                output_files.append(out_path)
                progress.progress(i / len(highlights))

            st.success("Clips generated successfully.")

            for i, path in enumerate(output_files, start=1):
                st.markdown(f"### Output Clip {i}")
                st.video(path)

                with open(path, "rb") as f:
                    st.download_button(
                        label=f"Download Clip {i}",
                        data=f,
                        file_name=f"clip_{i}.mp4",
                        mime="video/mp4"
                    )