import json
import requests
import os
import time
from moviepy.editor import VideoFileClip
import openai

# Configurações
FILA_ARQUIVO = '/tmp/fila_vistorias.json'
WHISPER_API_KEY = os.getenv('WHISPER_API_KEY')

if not WHISPER_API_KEY:
    raise ValueError("Erro: variável WHISPER_API_KEY não definida!")

# Função para processar uma tarefa
def processar_tarefa(tarefa):
    video_url = tarefa["video_url"]
    tarefa_id = tarefa["id"]

    print(f"Processando tarefa {tarefa_id}...")

    try:
        # 1. Baixar o vídeo
        video_response = requests.get(video_url)
        video_path = f'/tmp/{tarefa_id}.mp4'
        with open(video_path, 'wb') as f:
            f.write(video_response.content)

        # 2. Extrair o áudio
        clip = VideoFileClip(video_path)
        audio_path = f'/tmp/{tarefa_id}.mp3'
        clip.audio.write_audiofile(audio_path)

        # 3. Enviar para o Whisper
        openai.api_key = WHISPER_API_KEY
        with open(audio_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

        texto_transcrito = transcript["text"]

        print(f"Tarefa {tarefa_id} transcrita com sucesso!")
        print(f"Texto:\n{texto_transcrito}")

        # Salvar a transcrição num arquivo
        with open(f'/tmp/{tarefa_id}_transcricao.txt', 'w', encoding='utf
