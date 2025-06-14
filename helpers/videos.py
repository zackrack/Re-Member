import cv2
import os

def extract_frames_from_video(video_path, output_dir="frames", interval_sec=5, resize_width=None):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_sec)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_num = 0
    saved_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_num % frame_interval == 0:
            if resize_width:
                height = int(frame.shape[0] * resize_width / frame.shape[1])
                frame = cv2.resize(frame, (resize_width, height))

            frame_filename = os.path.join(output_dir, f"frame_{saved_frames:03d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frames += 1

        frame_num += 1

    cap.release()
    print(f"✅ Extracted {saved_frames} frames to: {output_dir}")
