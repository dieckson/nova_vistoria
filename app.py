from flask import Flask, request, jsonify
import redis
import uuid
import json

app = Flask(__name__)
redis_client = redis.Redis(host='seu-redis-host', port=6379, decode_responses=True)

@app.route("/nova-vistoria", methods=["POST"])
def nova_vistoria():
    data = request.json
    tarefa_id = str(uuid.uuid4())
    redis_client.lpush('fila', json.dumps({'id': tarefa_id, 'video_url': data['video_url']}))
    return jsonify({"message": "Tarefa adicionada na fila", "tarefa_id": tarefa_id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
