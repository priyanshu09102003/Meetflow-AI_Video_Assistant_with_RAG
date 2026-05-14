import os
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# YouTube blocks known cloud server IPs (AWS, GCP etc.) with 403.
# Using the iOS player client + its User-Agent bypasses this detection.
_YT_HEADERS = {
    "User-Agent": (
        "com.google.ios.youtube/19.29.1 CFNetwork/1220.1 Darwin/20.3.0"
    ),
}
_YT_EXTRACTOR_ARGS = {
    "youtube": {
        "player_client": ["ios", "web"],   
    }
}


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        # ── Cloud 403 bypass ──────────────────────────────────────────────
        "http_headers":    _YT_HEADERS,
        "extractor_args":  _YT_EXTRACTOR_ARGS,
        "retries":         5,
        "fragment_retries": 5,
        # ── EJS: JS runtime for YouTube challenge solving (2025 required) ─  ← ADD FROM HERE
        "js_runtimes":       {"node": {}},
        "remote_components": {"ejs:github"},
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = (
            ydl.prepare_filename(info)
            .replace(".webm", ".wav")
            .replace(".m4a", ".wav")
        )
    return filename


def convert_to_wav(input_path: str) -> str:
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000
    chunks = []
    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start: start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks


def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Local file detected. Converting to .wav ...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready - {len(chunks)} chunk(s) created.")
    return chunks