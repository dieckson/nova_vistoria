from flask import Flask, request, jsonify
import redis
import uuid
import json
import os

# Criação do app Flask
app = Flask(__name__)

# Conexão com o Redis (ajuste se necessário)
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'), 
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

@app.route("/nova-vistoria", methods=["POST"])
def nova_vistoria():
    try:
        data = request.get_json()
        video_url = data.get('video_url')

        if not video_url:
            return jsonify({"error": "O campo 'video_url' é obrigatório."}), 400

        tarefa_id = str(uuid.uuid4())

        redis_client.lpush('fila', json.dumps({
            'id': tarefa_id,
            'video_url': video_url
        }))

        return jsonify({
            "message": "Tarefa adicionada na fila",
            "tarefa_id": tarefa_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rodando o app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
