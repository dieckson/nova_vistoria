import json
import requests
import os
import time
from moviepy.editor import VideoFileClip
import openai

# Configurações
FILA_ARQUIVO = '/tmp/fila_vistorias.json'
WHISPER_API_KEY = 'OPEN_AI_Key'

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

        # Aqui você pode:
        # - Salvar o texto no S3
        # - Enviar para o Make
        # - Salvar em outro local
        # Exemplo básico: salvar localmente
        with open(f'/tmp/{tarefa_id}_transcricao.txt', 'w', encoding='utf-8') as f:
            f.write(texto_transcrito)

        return True

    except Exception as e:
        print(f"Erro ao processar tarefa {tarefa_id}: {str(e)}")
        return False

# Função para ler a fila
def ler_fila():
    if not os.path.exists(FILA_ARQUIVO):
        with open(FILA_ARQUIVO, 'w') as f:
            json.dump([], f)
    with open(FILA_ARQUIVO, 'r') as f:
        fila = json.load(f)
    return fila

# Função para salvar a fila
def salvar_fila(fila):
    with open(FILA_ARQUIVO, 'w') as f:
        json.dump(fila, f)

# Loop principal do Worker
def worker_loop():
    while True:
        fila = ler_fila()
        if fila:
            print(f"Fila com {len(fila)} tarefas. Processando...")
            tarefa = fila.pop(0)  # Pega a primeira tarefa
            sucesso = processar_tarefa(tarefa)
            if sucesso:
                salvar_fila(fila)
        else:
            print("Fila vazia. Aguardando novas tarefas...")
        time.sleep(10)  # Espera 10 segundos antes de checar novamente

if __name__ == "__main__":
    worker_loop()
