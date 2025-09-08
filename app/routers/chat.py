from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.routers.auth import get_current_user
from app.schemas.user import UserResponse
from app.schemas.conversation import (
    ChatRequest, ChatResponse, ConversationResponse,
    ConversationCreate, MessageResponse
)
from app.services import conversation_service
from app.services.openai_service import OpenAIService

router = APIRouter()
openai_service = OpenAIService()


@router.post("/send", response_model=ChatResponse)
def send_message(
        chat_request: ChatRequest,
        current_user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Envoyer un message et recevoir une réponse du bot"""

    # Créer ou récupérer la conversation
    if chat_request.conversation_id:
        conversation = conversation_service.get_conversation_by_id(
            db, chat_request.conversation_id, current_user.id
        )
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Créer une nouvelle conversation
        conversation = conversation_service.create_conversation(
            db, current_user.id, "Nouvelle conversation"
        )

    # Ajouter le message de l'utilisateur
    user_message = conversation_service.add_message_to_conversation(
        db, conversation.id, chat_request.message, is_bot=False
    )

    # Récupérer l'historique pour l'IA
    conversation_history = conversation_service.get_conversation_history_for_ai(
        db, conversation.id, limit=10
    )

    # Générer la réponse du bot
    bot_response_content = openai_service.generate_response(
        message=chat_request.message,
        user_level=current_user.java_level,
        conversation_history=conversation_history
    )

    # Ajouter la réponse du bot
    bot_message = conversation_service.add_message_to_conversation(
        db, conversation.id, bot_response_content, is_bot=True
    )

    return ChatResponse(
        message=MessageResponse.from_orm(user_message),
        bot_response=MessageResponse.from_orm(bot_message),
        conversation_id=conversation.id
    )


@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
        current_user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Récupérer toutes les conversations de l'utilisateur"""
    conversations = conversation_service.get_user_conversations(db, current_user.id)
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
        conversation_id: int,
        current_user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Récupérer une conversation spécifique avec ses messages"""
    conversation = conversation_service.get_conversation_by_id(
        db, conversation_id, current_user.id
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return conversation


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
        conversation_id: int,
        current_user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Supprimer une conversation"""
    success = conversation_service.delete_conversation(
        db, conversation_id, current_user.id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return {"message": "Conversation deleted successfully"}