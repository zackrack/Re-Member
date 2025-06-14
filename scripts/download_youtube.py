import os
import sys
import yt_dlp

VIDEO_DIR = os.path.join(os.path.dirname(__file__), "..", "video")
os.makedirs(VIDEO_DIR, exist_ok=True)

def download_youtube_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': os.path.join(VIDEO_DIR, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': False,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"🎬 Downloading video from: {url}")
        ydl.download([url])
        print(f"✅ Download complete. Saved to: {VIDEO_DIR}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_youtube.py <youtube_url>")
        sys.exit(1)

    youtube_url = sys.argv[1]
    download_youtube_video(youtube_url)
