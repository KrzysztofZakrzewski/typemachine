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

from audio.extract import generate_audio
from ai.transcrible import transcribe_audio_to_words

# ======================
# CONFIGURATION
# ======================

# --- Reading keys from env file ---
env = dotenv_values("../.env")

# --- AI Model ---
# AUDIO_TRANSCRIBE_MODEL = "whisper-1"

# openai_client = OpenAI(api_key=env["OPENAI_API_KEY"])

# --- Load keys from env file ---
def get_openai_client():
    return OpenAI(api_key=st.session_state["openai_api_key"])
# openai_client = get_openai_client()
# @st.cache_resource

# --- Handling missing .env key ---
if not st.session_state.get("openai_api_key"):
    if "OPENAI_API_KEY" in env:
        st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]
    
    # Adding a key manually
    else:
        st.info("Dodaj swój klucz API OpenAI aby móc korzystać z tej aplikacji")
        st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
        if st.session_state["openai_api_key"]:
            st.rerun()

# STOP app if the is no key
if not st.session_state.get("openai_api_key"):
    st.stop()

# ======================
# Handling session state
# ======================

if 'audio_as_bytes_md_5_check' not in st.session_state:
    st.session_state['audio_as_bytes_md_5_check'] = None

if 'audio_as_bytes' not in st.session_state:
    st.session_state['audio_as_bytes'] = None

if 'audio_as_text' not in st.session_state:
    st.session_state['audio_as_text'] = ''

# Obsługa języka
if 'language_iso' not in st.session_state:
    st.session_state['language_iso'] = 'pl'

# ======================
# MAIN
# ======================

# --- Title ---
st.set_page_config(page_title="TypeMachine", layout="centered")
st.title("Apka do generowania napisów: TypeMachine 📄🖋️")

# --- Instrucrion ---
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

# --- Input field for entering the language of interest ---
st.session_state['language_iso'] = st.text_input(
    "Wprowadź kod ISO języka na który chcesz przetłumaczyć (np. 'pl', 'en', 'de'):",
    value=st.session_state['language_iso']
)

uploaded_file = st.file_uploader("Wgraj plik wideo", type=['flac', 'm4a', 'mp3', 'mp4', 'wav', 'ogg', 'aac', 'mpga', 'avi', 'mov', 'wmv', 'webm', 'mkv'])

# ======================
# INTERFACE AND DISPLAY
# ======================
if uploaded_file is not None:
    # --- Display the video being played ---
    st.video(uploaded_file)
    # Getting the full video name
    file_name = uploaded_file.name  # exemp. "moj_film.mp4"
    
    # Removing the extension from the name of the loaded video
    file_name_without_ext = os.path.splitext(file_name)[0]

    # --- Interface for generating audio ---
    if st.button("Wygeneruj audio"):
        generate_audio(uploaded_file)
        # !!!!! NIE mam pojęcia dlaczego to nie działało w funcji !!!!! #
        current_md5 = md5(st.session_state["audio_as_bytes"]).hexdigest()
        if st.session_state["audio_as_bytes_md_5_check"] != current_md5:
            st.session_state["audio_as_text"] = ""
            st.session_state["audio_as_bytes_md_5_check"] = current_md5


    # --- Display audio player in fixed location (if data exists) ---
    if st.session_state['audio_as_bytes']:
        st.audio(st.session_state['audio_as_bytes'], format='audio/mp3')

    # --- Transcription buttons ---
    if st.session_state['audio_as_bytes']:
        if st.button("Transkrybuj audio"):
            # --- Call the "transcribe audio_to_words" function with "get_openai_client" as an argument to load the key --- 
            st.session_state["audio_as_text"] = transcribe_audio_to_words(
                                                st.session_state["audio_as_bytes"],
                                                get_openai_client(),
                                                language=st.session_state['language_iso'],
                                                response_format='srt')

    # --- Transcript display ---
    if st.session_state["audio_as_text"]:
        edited_text = st.text_area(
            "Transkrypcja audio",
            value=st.session_state["audio_as_text"],
            # disabled=True,
        )
    # --- Button to download the text as an SRT file ---
    st.download_button(
        label="Pobierz transkrypcję jako plik .srt",
        data= edited_text if 'edited_text' in locals() else st.session_state["audio_as_text"],  # Zawartość do zapisania
        # --- Using the filename to create the translation filename ---
        file_name=f"{file_name_without_ext}.srt",  # file name
        mime="text/plain",  # MIME type for text file
    )

else:
    st.write("Wgraj wideo, aby je obejrzeć.")