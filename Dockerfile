# Wybierz bazowy obraz z Pythonem
FROM python:3.11-slim

# Zainstaluj ffmpeg
RUN apt update && apt install -y ffmpeg

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki do obrazu
COPY . .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Ustaw port Streamlit
EXPOSE 8501

# Uruchom Streamlit
CMD ["streamlit", "run", "typemachine.py", "--server.port=8501", "--server.enableCORS=false"]
