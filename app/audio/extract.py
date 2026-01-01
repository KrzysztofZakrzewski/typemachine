import typing
from pydub import AudioSegment
from io import BytesIO
import streamlit as st

def generate_audio(uploaded_file):
    try:
        # Tworzenie obiektu AudioSegment z pliku wideo
        audio_from_video_file = AudioSegment.from_file(uploaded_file)

        # Eksport audio_from_video_file do formatu MP3 jako BytesIO
        audio = BytesIO()
        audio_from_video_file.export(audio, format="mp3")
        audio.seek(0)  # Cofnij wskaźnik do początku bufora
        # audio_as_bytes = audio.getvalue()

        # Przechowaj dane audio w st.session_state
        st.session_state['audio_as_bytes'] = audio.getvalue()  # Zapisz tylko dane bajtowe


        # st.audio(st.session_state['audio_as_bytes'], format='audio/mp3')

        return True
    except Exception as e:
        st.error(f"Błąd podczas przetwarzania audio: {e}")
        return False