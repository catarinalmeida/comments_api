from flask import Flask, request, jsonify
import json
import jwt
import datetime
from functools import wraps
from prometheus_flask_exporter import PrometheusMetrics, Counter
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # Adicionando Prometheus

# Senha para codificar os tokens
SECRET_KEY = "api_comentarios"

# Contadores para novas métricas
new_comments_total = Counter('new_comments_total', 'Total de novos comentários')
deleted_comments_total = Counter('deleted_comments_total', 'Total de comentários deletados')

# Carregar e salvar comentários
def save_comments():
    with open('comments.json', 'w') as f:
        json.dump(comments, f)

def load_comments():
    if os.path.exists('comments.json'):
        with open('comments.json', 'r') as f:
            return json.load(f)
    return []

comments = load_comments()

# Decorador para proteger rotas
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'O token é necessário!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user']
        except Exception as e:
            return jsonify({'message': 'Token inválido!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Deleta os comentários testes
@app.route('/comments', methods=['DELETE'])
@token_required
def delete_all_comments(current_user):
    global comments
    deleted_comments_total.inc(len(comments))
    comments = []
    save_comments()  # Salva os comentários após deletar todos
    return jsonify({'message': 'Todos os comentários foram deletados'}), 200

@app.route('/comments', methods=['GET'])
def get_comments():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    start = (page - 1) * per_page
    end = start + per_page
    return jsonify(comments[start:end])

# Endpoint para gerar o token
@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not 'username' in auth or not 'password' in auth:
        return jsonify({'message': 'Login e senha são obrigatorios!'}), 401

    if auth['username'] == 'admin' and auth['password'] == 'senha':
        token = jwt.encode({
            'user': auth['username'],
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({'token': token})

    return jsonify({'message': 'Credenciais inválidas!'}), 401

@app.route('/comments', methods=['POST'])
@token_required
def add_comment(current_user):
    new_comment = request.json
    comment_id = len(comments) + 1  # Gerando novo ID
    new_comment['id'] = comment_id  # Adicionando o ID ao comentário
    comments.append(new_comment)
    save_comments()  # Salva os comentários novos
    new_comments_total.inc()  # Incrementa o contador de novos comentários
    return jsonify(new_comment), 201

@app.route('/comments/<int:comment_id>', methods=['PUT'])
@token_required
def update_comment(current_user, comment_id):
    if comment_id < len(comments):
        comments[comment_id] = request.json
        save_comments()  # Salva após atualizar
        return jsonify(comments[comment_id])
    return jsonify({'error': 'Comment not found'}), 404

@app.route('/comments/<int:comment_id>', methods=['DELETE'])
@token_required
def delete_comment(current_user, comment_id):
    if comment_id < len(comments):
        deleted_comment = comments.pop(comment_id)
        deleted_comments_total.inc()  # Incrementa o contador de comentários deletados
        save_comments()  # Salva após deletar
        return jsonify(deleted_comment)
    return jsonify({'error': 'Comment not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
