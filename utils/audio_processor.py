import os
import yt_dlp
from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

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


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from any YouTube URL format."""
    import re
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})",
        r"(?:embed\/)([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from URL: {url}")


def get_transcript_via_api(url: str) -> str:
    """
    Fetch transcript directly via YouTube Transcript API.
    No downloading, no bot detection, works on all cloud servers.
    """
    video_id = extract_video_id(url)
    print(f"Fetching transcript for video ID: {video_id}")

    try:
        # Try English first, then any available language
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Prefer manually created English transcript
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except Exception:
            try:
                # Fall back to auto-generated English
                transcript = transcript_list.find_generated_transcript(['en'])
            except Exception:
                # Fall back to any available transcript and translate to English
                transcript = transcript_list.find_generated_transcript(
                    [t.language_code for t in transcript_list]
                ).translate('en')

        data = transcript.fetch()
        full_text = " ".join([entry['text'] for entry in data])
        print(f"Transcript fetched successfully ({len(full_text)} chars)")
        return full_text

    except TranscriptsDisabled:
        raise RuntimeError(
            "Transcripts are disabled for this video. "
            "Please download the video and use Upload File instead."
        )
    except NoTranscriptFound:
        raise RuntimeError(
            "No transcript found for this video. "
            "Please download the video and use Upload File instead."
        )


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
        "http_headers":    _YT_HEADERS,
        "extractor_args":  _YT_EXTRACTOR_ARGS,
        "retries":         5,
        "fragment_retries": 5,
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


def process_input(source: str, language: str = "english") -> tuple:
    """
    Returns (chunks_or_none, transcript_or_none)
    - For YouTube URLs: returns (None, transcript_text) — skip Whisper entirely
    - For local files: returns (chunks, None) — use Whisper as before
    """
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Fetching transcript via API...")
        transcript = get_transcript_via_api(source)
        return None, transcript
    else:
        print("Local file detected. Converting to .wav ...")
        wav_path = convert_to_wav(source)
        print("Chunking audio...")
        chunks = chunk_audio(wav_path)
        print(f"Audio ready - {len(chunks)} chunk(s) created.")
        return chunks, None