from io import BytesIO


# --- AI Model ---
AUDIO_TRANSCRIBE_MODEL = "whisper-1"


# def transcribe_audio_to_words(audio_bytes, language=st.session_state['language_iso']):
#     openai_client = get_openai_client()
#     audio_file = BytesIO(audio_bytes)
#     audio_file.name = "audio.mp3"
#     transcript = openai_client.audio.transcriptions.create(
#         file=audio_file,
#         model=AUDIO_TRANSCRIBE_MODEL,
#         language=language,
#         response_format="srt",  # tu se mogę zmienić na SRT ale trzeba usunąć TEXT z RETURNA I NA DOLE rzzy zapisie zamias txt też SRT !!!!! ONEONEONE
#     )

#     return transcript

def transcribe_audio_to_words(audio_bytes, openai_client, language, response_format):
    openai_client=openai_client
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "audio.mp3"
    transcript = openai_client.audio.transcriptions.create(
        file=audio_file,
        model=AUDIO_TRANSCRIBE_MODEL,
        language=language,
        response_format=response_format,
    )
    return transcript