from sqlalchemy.orm import Session
from app.models.conversation import Conversation, Message
from app.models.user import User
from app.schemas.conversation import ConversationCreate
from typing import List, Optional


def create_conversation(db: Session, user_id: int, title: str = None) -> Conversation:
    """Créer une nouvelle conversation"""
    if not title:
        title = "Nouvelle conversation"

    conversation = Conversation(
        user_id=user_id,
        title=title
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_user_conversations(db: Session, user_id: int, limit: int = 20) -> List[Conversation]:
    """Récupérer les conversations d'un utilisateur"""
    return db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).order_by(Conversation.created_at.desc()).limit(limit).all()


def get_conversation_by_id(db: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
    """Récupérer une conversation spécifique"""
    return db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()


def add_message_to_conversation(db: Session, conversation_id: int, content: str, is_bot: bool) -> Message:
    """Ajouter un message à une conversation"""
    message = Message(
        conversation_id=conversation_id,
        content=content,
        is_bot=is_bot
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_conversation_messages(db: Session, conversation_id: int, limit: int = 50) -> List[Message]:
    """Récupérer les messages d'une conversation"""
    return db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.asc()).limit(limit).all()


def get_conversation_history_for_ai(db: Session, conversation_id: int, limit: int = 10) -> List[dict]:
    """Récupérer l'historique formaté pour l'IA"""
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.desc()).limit(limit).all()

    # Inverser pour avoir l'ordre chronologique
    messages.reverse()

    return [
        {
            "content": msg.content,
            "is_bot": msg.is_bot,
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]


def delete_conversation(db: Session, conversation_id: int, user_id: int) -> bool:
    """Supprimer une conversation et tous ses messages"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()

    if not conversation:
        return False

    # Supprimer d'abord tous les messages de la conversation
    db.query(Message).filter(Message.conversation_id == conversation_id).delete()

    # Puis supprimer la conversation
    db.delete(conversation)
    db.commit()

    return True