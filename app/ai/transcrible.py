from io import BytesIO

# --- AI Model ---
from config.settings import AUDIO_AI_MODEL_WHISPER_1

def detect_audio_language(audio_bytes, openai_client) -> str:
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "audio.mp3"

    transcript = openai_client.audio.transcriptions.create(
        file=audio_file,
        model=AUDIO_AI_MODEL_WHISPER_1,
         response_format="verbose_json",
    )

    return transcript.language


def transcribe_audio_to_words(audio_bytes, openai_client, language, response_format):
    openai_client=openai_client
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "audio.mp3"
    transcript = openai_client.audio.transcriptions.create(
        file=audio_file,
        model=AUDIO_AI_MODEL_WHISPER_1,
        language=language,
        response_format=response_format,
    )
    return transcript