import streamlit as st
from pydub import AudioSegment
# from IPython.display import Audio
from dotenv import dotenv_values
from openai import OpenAI
# from audiorecorder import audiorecorder 
from io import BytesIO
from hashlib import md5
# import tempfile
# import subprocess
# import tempfile
import os
# import io
# from IPython.display import Markdown


env = dotenv_values(".env")

AUDIO_TRANSCRIBE_MODEL = "whisper-1"

# openai_client = OpenAI(api_key=env["OPENAI_API_KEY"])


def get_openai_client():
    return OpenAI(api_key=st.session_state["openai_api_key"])
# @st.cache_resource


if not st.session_state.get("openai_api_key"):
    if "OPENAI_API_KEY" in env:
        st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]

    else:
        st.info("Dodaj swój klucz API OpenAI aby móc korzystać z tej aplikacji")
        st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
        if st.session_state["openai_api_key"]:
            st.rerun()

if not st.session_state.get("openai_api_key"):
    st.stop()

# # ### # #
# Obsługa st.session_state

if 'audio_as_bytes_md_5_check' not in st.session_state:
    st.session_state['audio_as_bytes_md_5_check'] = None

if 'audio_as_bytes' not in st.session_state:
    st.session_state['audio_as_bytes'] = None

if 'audio_as_text' not in st.session_state:
    st.session_state['audio_as_text'] = ''

# Obsługa języka
if 'language_iso' not in st.session_state:
    st.session_state['language_iso'] = 'pl'

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
    
#
# WHISPER-1 
#

def transcribe_audio_to_words(audio_bytes, language=st.session_state['language_iso']):
    openai_client = get_openai_client()
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "audio.mp3"
    transcript = openai_client.audio.transcriptions.create(
        file=audio_file,
        model=AUDIO_TRANSCRIBE_MODEL,
        language=language,
        response_format="srt",  # tu se mogę zmienić na SRT ale trzeba usunąć TEXT z RETURNA I NA DOLE rzzy zapisie zamias txt też SRT !!!!! ONEONEONE
    )

    return transcript

#
# MAIN
#
st.set_page_config(page_title="TypeMachine", layout="centered")
st.title("Apka do generowania napisów: TypeMachine 📄🖋️")


with st.expander("📖 Instrukcja (kliknij, aby rozwinąć)"):
    st.write("""
             Po wpisaniu klucza od OpenAI, użytkownik (ty):
    1. Może wybrać język na jaki zostanie przetłumaczony tekst z filmiku wpisująć kod ISO języka.
    2. W polu "wgraj plik wideo" wrzuć filmik, z którego chcesz wyekstrachować tekst.
    3. Następnie wciśnij przycisk "Wygeneruj Audio" i sprawdź wy wygenerowało się poprawnie.
    4. Następnie wciśnij przycisk "Transkrypcja audio", pojawi się tekst z filmu, który został zauplodowany.
    5. Możesz go zmodyfikować, ale pamiętaj aby wcisnąć CRTL+ENTER aby zatwierdzić zmiany.
    6. Po wciścięciu przycsku "Pobierz transkrypcję jako plik .srt" plik zostanie zapisany na twoim dysku.
    """)


# Pole do wpisywania interesującego języka
# language_iso = st.text_input("Wprowadź kod ISO języka na który chcesz przetłumaczyć(np. 'pl', 'en', 'de'):", value='pl')
st.session_state['language_iso'] = st.text_input(
    "Wprowadź kod ISO języka na który chcesz przetłumaczyć (np. 'pl', 'en', 'de'):",
    value=st.session_state['language_iso']
)


uploaded_file = st.file_uploader("Wgraj plik wideo", type=['flac', 'm4a', 'mp3', 'mp4', 'wav', 'ogg', 'aac', 'mpga', 'avi', 'mov', 'wmv', 'webm', 'mkv'])



if uploaded_file is not None:
    # Wyświetlenie odtwarzanego wideo
    st.video(uploaded_file)
        # Pobranie pełnej nazwy pliku
    file_name = uploaded_file.name  # np. "moj_film.mp4"
    
    # Usunięcie rozszerzenia
    file_name_without_ext = os.path.splitext(file_name)[0]

    # Interface do generowania audio
    if st.button("Wygeneruj audio"):
        generate_audio(uploaded_file)
        # !!!!! NIE mam pojęcia dlaczego to nie działało w funcji !!!!! #
        current_md5 = md5(st.session_state["audio_as_bytes"]).hexdigest()
        if st.session_state["audio_as_bytes_md_5_check"] != current_md5:
            st.session_state["audio_as_text"] = ""
            st.session_state["audio_as_bytes_md_5_check"] = current_md5


    # Wyświetlenie playera audio w stałym miejscu (jeśli dane istnieją)
    if st.session_state['audio_as_bytes']:
        st.audio(st.session_state['audio_as_bytes'], format='audio/mp3')

    # Przyciski transkrypcji
    if st.session_state['audio_as_bytes']:
        if st.button("Transkrybuj audio"):
            st.session_state["audio_as_text"] = transcribe_audio_to_words(st.session_state["audio_as_bytes"])

    # Wyświetlenie transkrypcji
    if st.session_state["audio_as_text"]:
        edited_text = st.text_area(
            "Transkrypcja audio",
            value=st.session_state["audio_as_text"],
            # disabled=True,
        )
            # Dodanie przycisku do pobrania tekstu jako plik .srt
    st.download_button(
        label="Pobierz transkrypcję jako plik .srt",
        data= edited_text if 'edited_text' in locals() else st.session_state["audio_as_text"], #st.session_state["audio_as_text"],  # Zawartość do zapisania
        # Wykorzystanie nazwy pliku do tworzenia liter
        file_name=f"{file_name_without_ext}.srt",  # Nazwa pliku   # Można też jako SRT
        mime="text/plain",  # Typ MIME dla pliku tekstowego
    )

else:
    st.write("Wgraj wideo, aby je obejrzeć.")