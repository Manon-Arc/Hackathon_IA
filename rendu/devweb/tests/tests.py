"""
Tests unitaires pour les services
"""
import unittest
from app import create_app
from app.models import db, Session, Message

class TestChatService(unittest.TestCase):
    """Tests du service Chat"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_health_endpoint(self):
        """Tester l'endpoint health"""
        response = self.client.get('/api/health')
        self.assertIn(response.status_code, [200, 503])
    
    def test_message_endpoint_missing_data(self):
        """Tester endpoint message sans données"""
        response = self.client.post(
            '/api/chat/message',
            json={"session_id": "test"}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_message_endpoint_invalid_content_type(self):
        """Tester avec mauvais Content-Type"""
        response = self.client.post(
            '/api/chat/message',
            data="not json",
            content_type='text/plain'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_sessions_list(self):
        """Tester la liste des sessions"""
        response = self.client.get('/api/chat/sessions')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('sessions', data)

class TestModels(unittest.TestCase):
    """Tests des modèles"""
    
    def setUp(self):
        """Initialisation"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Nettoyage"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_session(self):
        """Tester la création d'une session"""
        session = Session(id="test_session_1")
        db.session.add(session)
        db.session.commit()
        
        retrieved = Session.query.get("test_session_1")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, "test_session_1")
    
    def test_create_message(self):
        """Tester la création d'un message"""
        # Créer une session
        session = Session(id="test_session_2")
        db.session.add(session)
        db.session.commit()
        
        # Créer un message
        message = Message(
            session_id="test_session_2",
            role="user",
            content="Test message"
        )
        db.session.add(message)
        db.session.commit()
        
        # Vérifier
        retrieved = Message.query.first()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.content, "Test message")
        self.assertEqual(retrieved.role, "user")

if __name__ == '__main__':
    unittest.main()
