from io import BytesIO

# --- AI Models ---
from config.settings import (AUDIO_AI_MODEL_WHISPER_1,
                             TRANSLATE_AI_MODEL_4o_MINI)

# --- Lnaguage detection ---
def detect_audio_language(audio_bytes, openai_client) -> str:
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "audio.mp3"

    transcript = openai_client.audio.transcriptions.create(
        file=audio_file,
        model=AUDIO_AI_MODEL_WHISPER_1,
         response_format="verbose_json",
    )

    return transcript.language

# --- transcribe_audio_to_words ---
def transcribe_audio_to_words(audio_bytes, openai_client, response_format):
    openai_client=openai_client
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "audio.mp3"
    
    transcript = openai_client.audio.transcriptions.create(
        file=audio_file,
        model=AUDIO_AI_MODEL_WHISPER_1,
        response_format=response_format,
    )
    return transcript

# --- Script translation function with GPT-4o-mini- ---
def translate_script(openai_client, language_iso: str, script: str, language_recognition: str) -> str:

    prompt = f"""
    Translate the following SRT subtitle file from {language_recognition} to {language_iso}.
    Preserve all timestamps and subtitle indices exactly.
    """

    response = openai_client.chat.completions.create(
        model=TRANSLATE_AI_MODEL_4o_MINI,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": script},
        ],
    )

    return response.choices[0].message.content.strip()