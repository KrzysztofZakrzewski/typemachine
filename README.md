# typemachine
The application for generating subtitles from short videos.

## Instructions:
After entering your OpenAI key, you (the user) can: 
1. In the "Upload Video" field, upload the video from which you want to extract text.
2. Then press the "Generate Audio" button and check if the audio was generated correctly.
3. Next, press the "Audio Transcription" button — the text from the uploaded video will appear.
4. You can modify it, but remember to press CTRL + ENTER to confirm your changes.
5. Enter the language you want to translate the script into (by default, it will be Polish).
6. Press the "Translate" button to generate a translation in SRT file format.
7. The translated text can also be modified and confirmed with CTRL + ENTER.
8. You can download both the translated version and the original.

## quick-spec:
Python 3.11.11

##Name                    Version                   Build  Channel

1. streamlit                 1.42.0          py311haa95532_0         
2. streamlit-audiorecorder   0.0.6                    pypi_0    pypi
3. pydub                     0.25.1             pyhd8ed1ab_1    conda-forge
4. python-dotenv             0.21.0          py311haa95532_0       
5. openai                    1.47.0             pyhd8ed1ab_0    conda-forge
6. ffmpeg                    6.1.1                hc79a5da_2           
7. ffmpeg-python             0.2.0                    pypi_0    pypi

Also in use:
- io,
- BytesIO,
- hashlib, 
- md5
- os


# In the future, the application will be expanded with new functionalities and its usability and performance will be improved.

# Project Structure
=================
```
app/
│
├── ai/
│   └── transcrible.py  --> all function needed for recognition the langue of text, transcrible and translate of text
│
├── audio/
│   └── extract.py  --> function needed for extract mp3 format from Video
│
├── config/
│   └── settings.py  --> hardcode the AI model used in project
│
└── main.py  --> main code of the app.
```