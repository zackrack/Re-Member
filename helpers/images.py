import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers.openai_handlers import ask_ai_student

import json

def load_transcript_chunks(transcript_file):
    with open(transcript_file, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def process_images_with_transcript(frames_dir, transcript_chunks):
    frame_files = sorted([
        f for f in os.listdir(frames_dir)
        if f.lower().endswith(".jpg") or f.lower().endswith(".jpeg")
    ])

    min_len = min(len(frame_files), len(transcript_chunks))
    frame_files = frame_files[:min_len]
    transcript_chunks = transcript_chunks[:min_len]

    for i, (frame_file, chunk) in enumerate(zip(frame_files, transcript_chunks)):
        image_path = os.path.join(frames_dir, frame_file)
        transcript = chunk["text"]
        print(f"📷 Frame {frame_file} — Transcript: {transcript}")
        try:
            question = ask_ai_student(transcript, image_path)
            print(f"🧠 AI Student: {question}\n")
            chunk["ai_question"] = question
        except Exception as e:
            print(f"⚠️ Error on frame {frame_file}: {e}")
            chunk["ai_question"] = f"[Error]: {e}"

    return transcript_chunks

