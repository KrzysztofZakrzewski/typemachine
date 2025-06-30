# typemachine
The application for generating subtitles from short videos.

## Instructions:
After entering your OpenAI key, you (the user) can: 
1. Choose the target language for translation by entering the ISO language code.
2. Upload a video file in the “Upload video file” field — this is the video from which you want to extract text.
3. Click the “Generate Audio” button and check if the audio was generated correctly.
4. The extracted text from the uploaded video will appear.
5. You can modify the text, but remember to press CTRL+ENTER to confirm any changes. 6. After clicking the “Download transcription as .srt file” button, the file will be saved to your drive.

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