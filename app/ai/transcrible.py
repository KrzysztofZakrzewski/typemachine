from io import BytesIO

# --- AI Models ---
from config.settings import (AUDIO_AI_MODEL_WHISPER_1,
                             TRANSLATE_AI_MODEL_4o_MINI)

def detect_audio_language(audio_bytes, openai_client) -> str:
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "audio.mp3"

    transcript = openai_client.audio.transcriptions.create(
        file=audio_file,
        model=AUDIO_AI_MODEL_WHISPER_1,
         response_format="verbose_json",
    )

    return transcript.language


def transcribe_audio_to_words(audio_bytes, openai_client, response_format):
    openai_client=openai_client
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "audio.mp3"
    transcript = openai_client.audio.transcriptions.create(
        file=audio_file,
        model=AUDIO_AI_MODEL_WHISPER_1,
        # language=language,
        response_format=response_format,
    )
    return transcript

def translate_script(openai_client, language_iso: str, script: str, ) -> str:

    prompt = f"""
    Chcę abyś przełożył na język {language_iso} scenariusz w konwencji srt, pochodzący z krótkiego filmiku.
    NIE WOLNO zmieniać timestampów i numerów.
    """

    response = openai_client.chat.completions.create(
        model=TRANSLATE_AI_MODEL_4o_MINI,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": script},
        ],
    )

    return response.choices[0].message.content.strip()

# def translate_text(text, source_lang, target_lang, client) -> str:
#     prompt = f"""
#     Translate the following text from {source_lang} to {target_lang}.
#     Preserve meaning and punctuation.
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": prompt},
#             {"role": "user", "content": text},
#         ]
#     )

#     return response.choices[0].message.content.strip()