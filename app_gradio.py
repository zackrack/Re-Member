import gradio as gr
import os
import shutil
import json
import base64

from helpers.whisperx_chunker import transcribe_with_whisperx
from helpers.images import load_transcript_chunks, process_images_with_transcript

UPLOAD_DIR = "uploads"
TRANSCRIPT_FILE = "transcript_chunks.txt"

os.makedirs(UPLOAD_DIR, exist_ok=True)

from helpers.whisperx_chunker import transcribe_with_whisperx
from helpers.images import load_transcript_chunks, process_images_with_transcript

UPLOAD_DIR = "uploads"
TRANSCRIPT_FILE = "transcript_chunks.txt"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_video(video_path):
    filename = os.path.basename(video_path)
    final_path = os.path.join(UPLOAD_DIR, filename)
    shutil.copy(video_path, final_path)

    # Step 1: Transcribe
    transcribe_with_whisperx(final_path, num_frames=30, output_file=TRANSCRIPT_FILE)

    # Step 2: Load and generate AI questions
    transcript_chunks = load_transcript_chunks(TRANSCRIPT_FILE)
    transcript_chunks = process_images_with_transcript("frames", transcript_chunks)

    # Step 3: Extract time + text
    events = []
    for chunk in transcript_chunks:
        if "ai_question" in chunk:
            events.append({
                "time": round(chunk["start"], 2),
                "text": f"<b>🗣️ {chunk['text']}</b><br><b>🧠 {chunk['ai_question']}</b>"
            })

    events_json = json.dumps(events)

    # Step 4: Base64 encode video
    with open(final_path, "rb") as f:
        video_data = f.read()
    video_b64 = base64.b64encode(video_data).decode("utf-8")
    video_src = f"data:video/mp4;base64,{video_b64}"

    # Step 5: HTML for video player
    video_html = f"""
    <div style="width: 100%;">
        <video id="video" width="100%" controls>
            <source src="{video_src}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    """

    # Step 6: HTML for AI questions display
    questions_html = f"""
    <div id="qa-box" style="
        background: #f9f9f9;
        color: #111;
        padding: 15px;
        font-size: 16px;
        line-height: 1.5;
        min-height: 4em;
        border-left: 4px solid #444;
    ">⏱️ Waiting for video to start...</div>

    <script>
        const events = {events_json};
        const video = document.getElementById("video");
        const qaBox = document.getElementById("qa-box");

        let lastEventTime = null;
        let pauseTimeout = null;

        video.addEventListener("timeupdate", () => {{
            const current = video.currentTime;
            let evt = null;
            for (let i = events.length - 1; i >= 0; i--) {{
                if (current >= events[i].time) {{
                    evt = events[i];
                    break;
                }}
            }}

            if (evt && evt.time !== lastEventTime) {{
                lastEventTime = evt.time;
                qaBox.innerHTML = evt.text;

                if (!video.paused) {{
                    video.pause();
                    clearTimeout(pauseTimeout);
                    pauseTimeout = setTimeout(() => {{
                        video.play();
                    }}, 5000);  // 5 seconds
                }}
            }}
        }});
    </script>
    """
    print(json.dumps(events, indent=2))

    return video_html, questions_html

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the Gradio Simulated High School Student.")
    parser.add_argument("--share", action="store_true", help="Enable public Gradio link")
    args = parser.parse_args()

    with gr.Blocks(title="Simulated High School Student") as demo:
        gr.Markdown("## 🧪 Upload a Ray-Ban Video\nThe AI will analyze the experiment and ask questions like a curious student.")

        with gr.Row():
            video_output = gr.HTML(label="Video")
            questions_output = gr.HTML(label="AI Student Questions")

        video_input = gr.File(
            label="🎥 Upload Ray-Ban Video (.mp4, .mov)",
            type="filepath",
            file_types=[".mp4", ".mov"]
        )

        submit_button = gr.Button("Analyze Video")

        submit_button.click(
            fn=lambda: gr.update(value="Analyzing Video..."),
            inputs=None,
            outputs=submit_button
        ).then(
            fn=process_video,
            inputs=video_input,
            outputs=[video_output, questions_output]
        ).then(
            fn=lambda: gr.update(value="Analyze Video"),
            inputs=None,
            outputs=submit_button
        )


    demo.launch(share=args.share)
