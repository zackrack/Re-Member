import whisperx
import os
import torch
import json
import ffmpeg

device = "cuda"

def transcribe_with_whisperx(video_path, num_frames, output_file="transcript_chunks.txt"):
    model = whisperx.load_model("base", device, compute_type="int8")
    print("🔍 Transcribing with WhisperX...")
    result = model.transcribe(video_path)

    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result_aligned = whisperx.align(result["segments"], model_a, metadata, video_path, device)

    duration = float(ffmpeg.probe(video_path)["format"]["duration"])
    interval = duration / num_frames

    chunks = []
    for i in range(num_frames):
        start = round(i * interval, 2)
        end = round((i + 1) * interval, 2)
        words = [
            word["word"] for word in result_aligned["word_segments"]
            if start <= word["start"] < end
        ]
        text = " ".join(words).strip() or "[no speech]"
        chunks.append({"start": start, "end": end, "text": text})

    with open(output_file, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk) + "\n")

    print(f"✅ Wrote {len(chunks)} aligned transcript chunks to {output_file}")
    return output_file
