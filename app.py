import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from helpers.videos import extract_frames_from_video
from helpers.images import process_images_with_transcript
from helpers.whisperx_chunker import transcribe_with_whisperx

UPLOAD_FOLDER = "static/uploads"
FRAMES_FOLDER = "frames"
TRANSCRIPT_FILE = "transcript_chunks.txt"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure required directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FRAMES_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check file input
        if "video" not in request.files:
            return "No video file provided", 400

        file = request.files["video"]
        if file.filename == "":
            return "No selected file", 400

        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)

        # Step 1: Extract frames from video
        extract_frames_from_video(video_path, output_dir=FRAMES_FOLDER, interval_sec=5, resize_width=640)

        # Step 2: Transcribe using WhisperX and align to frames
        frame_count = len([f for f in os.listdir(FRAMES_FOLDER) if f.lower().endswith(".jpg")])
        transcribe_with_whisperx(video_path, frame_count, output_file=TRANSCRIPT_FILE)

        # Step 3: Process frame + transcript pairs with GPT-4V
        results = process_images_with_transcript(FRAMES_FOLDER, TRANSCRIPT_FILE)
        return render_template("results.html", results=results)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
