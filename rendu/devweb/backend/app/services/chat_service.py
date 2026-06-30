"""
Service pour la gestion des conversations
"""
from app.models import db, Session, Message
from app.services.ollama_service import OllamaService
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class ChatService:
    """Service pour gérer les conversations et messages"""
    
    @staticmethod
    def create_session(session_id: str) -> Session:
        """Créer une nouvelle session"""
        session = Session(id=session_id)
        db.session.add(session)
        db.session.commit()
        logger.info(f"Created session: {session_id}")
        return session
    
    @staticmethod
    def get_or_create_session(session_id: str) -> Session:
        """Récupérer une session ou la créer si elle n'existe pas"""
        session = Session.query.get(session_id)
        if not session:
            session = ChatService.create_session(session_id)
        return session
    
    @staticmethod
    def add_message(session_id: str, role: str, content: str) -> Message:
        """Ajouter un message à une session"""
        session = ChatService.get_or_create_session(session_id)
        message = Message(session_id=session_id, role=role, content=content)
        db.session.add(message)
        db.session.commit()
        return message
    
    @staticmethod
    def get_history(session_id: str, limit: int = None):
        """Récupérer l'historique des messages"""
        session = Session.query.get(session_id)
        if not session:
            return []
        
        query = Message.query.filter_by(session_id=session_id).order_by(Message.timestamp.asc())
        
        if limit:
            query = query.limit(limit)
        
        return [msg.to_dict() for msg in query.all()]
    
    @staticmethod
    def process_message(session_id: str, user_message: str) -> dict:
        """
        Traiter un message utilisateur et générer une réponse
        
        Returns:
            {
                'success': bool,
                'user_message': str,
                'bot_response': str,
                'error': str (si applicable)
            }
        """
        try:
            # Sauvegarder le message utilisateur
            ChatService.add_message(session_id, 'user', user_message)
            
            # Générer la réponse
            bot_response = OllamaService.generate(user_message)
            
            # Sauvegarder la réponse
            ChatService.add_message(session_id, 'assistant', bot_response)
            
            return {
                'success': True,
                'user_message': user_message,
                'bot_response': bot_response
            }
        
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                'success': False,
                'user_message': user_message,
                'bot_response': None,
                'error': str(e)
            }
    
    @staticmethod
    def delete_session(session_id: str) -> bool:
        """Supprimer une session et tous ses messages"""
        try:
            session = Session.query.get(session_id)
            if session:
                db.session.delete(session)
                db.session.commit()
                logger.info(f"Deleted session: {session_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting session: {str(e)}")
            return False
    
    @staticmethod
    def get_all_sessions():
        """Récupérer toutes les sessions"""
        sessions = Session.query.order_by(Session.updated_at.desc()).all()
        return [s.to_dict() for s in sessions]
