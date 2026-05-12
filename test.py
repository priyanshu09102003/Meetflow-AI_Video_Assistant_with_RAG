from utils.audio_processor import process_input
from core.transcriber import transcribe_all

source = "https://youtu.be/Lg-meK5IU8Q?si=3cCwR10vggNN-qYB"

chunks = process_input(source)

print(transcribe_all(chunks))