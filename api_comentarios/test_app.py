import unittest
import json
from app import app, comments, save_comments

class CommentAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.token = self.get_auth_token()

    def get_auth_token(self):
        # Faz login para obter o token de autenticação
        response = self.app.post('/login', json={'username': 'admin', 'password': 'senha'})
        data = json.loads(response.data)
        return data['token']

    def test_create_comment(self):
        response = self.app.post('/comments', json={'author': 'Test', 'content': 'Comentario teste!'}, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', json.loads(response.data))

    def test_get_comments(self):
        response = self.app.get('/comments')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(json.loads(response.data)), 1)

    def test_update_comment(self):
        # Adiciona um comentário primeiro
        self.app.post('/comments', json={'author': 'Test', 'content': 'Comentario teste!'}, headers={'Authorization': f'Bearer {self.token}'})
        
        # Atualiza o comentário
        response = self.app.put('/comments/1', json={'author': 'Test', 'content': 'Comentario atualizado!'}, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['content'], 'Comentario atualizado!')

    def test_delete_comment(self):
        # Adiciona um comentário primeiro
        self.app.post('/comments', json={'author': 'Test', 'content': 'Comentario teste!'}, headers={'Authorization': f'Bearer {self.token}'})
        
        # Deleta o comentário
        response = self.app.delete('/comments/1', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('author', json.loads(response.data))

    def test_login(self):
        response = self.app.post('/login', json={'username': 'admin', 'password': 'senha'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', json.loads(response.data))

    def test_login_failed(self):
        response = self.app.post('/login', json={'username': 'admin', 'password': 'senha_errada'})
        self.assertEqual(response.status_code, 401)
        self.assertIn('message', json.loads(response.data))

if __name__ == '__main__':
    unittest.main()
