from sqlalchemy.orm import Session
from ..models.chat import Usuario, Chat
from ..schemas.chat_schemas import UsuarioCreate, ChatCreate, ChatUpdate, MessageRequest, MessageResponse
from ..utils.gemini_sentiment import analizar_sentimiento_gemini
from ..utils.gemini_chat import GeminiChatService
from datetime import datetime
import json
import os

# Función para obtener una instancia actualizada del servicio de Gemini
def get_gemini_service():
    """Obtiene una instancia actualizada del servicio de Gemini con la API key más reciente"""
    return GeminiChatService()

def create_usuario_y_chat(db: Session, doc_id: int):
    chat = Chat()
    db.add(chat)
    db.flush()
    usuario = Usuario(doc_id=doc_id, chat_id=chat.id)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    db.refresh(chat)
    return usuario

def get_usuario_y_chat(db: Session, doc_id: int):
    return db.query(Usuario).filter(Usuario.doc_id == doc_id).first()

def process_message(db: Session, chat_id: str, message_request: MessageRequest) -> MessageResponse:
    """
    Procesa un mensaje completo: genera respuesta con Gemini, analiza sentimiento y guarda en BD
    """
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise ValueError("Chat no encontrado")
    
    # Obtener historial de conversación actual
    conversation_history = chat.mensajes if chat.mensajes else []
    
    # Generar respuesta con Gemini (usando instancia actualizada)
    gemini_service = get_gemini_service()
    bot_response = gemini_service.generate_response(
        message_request.message, 
        conversation_history
    )
    
    # Analizar sentimiento del mensaje del usuario
    try:
        sentiment_result = analizar_sentimiento_gemini(message_request.message)
        # Convertir sentimiento a score numérico
        sentiment_score = convert_sentiment_to_score(sentiment_result)
    except Exception as e:
        print(f"Error en análisis de sentimiento: {e}")
        sentiment_score = 5.0  # Neutral por defecto
    
    # Crear timestamp
    timestamp = datetime.now().isoformat()
    
    # Crear objeto de mensaje completo con la estructura especificada
    new_message = {
        "message": message_request.message,
        "score": sentiment_score,
        "timestamp": timestamp,
        "response": bot_response
    }
    
    # APPEND: Agregar el nuevo mensaje al historial
    if conversation_history is None or not isinstance(conversation_history, list):
        # Si no hay historial o no es una lista, crear nueva lista
        chat.mensajes = [new_message]
    else:
        # Hacer append del nuevo mensaje al historial existente
        updated_messages = conversation_history.copy()
        updated_messages.append(new_message)
        chat.mensajes = updated_messages
    
    # Actualizar el score general del chat con el último sentimiento
    chat.score = sentiment_score
    
    # Forzar actualización en SQLAlchemy para campos JSON
    # Marcar explícitamente que el campo mensajes ha sido modificado
    chat.mensajes = list(chat.mensajes) if chat.mensajes else []
    
    db.commit()
    db.refresh(chat)
    
    return MessageResponse(
        message=message_request.message,
        score=sentiment_score,
        timestamp=timestamp,
        response=bot_response
    )

def convert_sentiment_to_score(sentiment: str) -> float:
    """
    Convierte el resultado de sentimiento de texto a score numérico
    """
    sentiment_map = {
        "positivo": 8.0,
        "neutral": 5.0,
        "neutro": 5.0,
        "negativo": 2.0
    }
    return sentiment_map.get(sentiment.lower(), 5.0)

def update_chat(db: Session, chat_id: str, chat_update: ChatUpdate):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        return None
    # Lógica para hacer append de mensajes si es una lista
    mensaje_nuevo = None
    if chat_update.mensajes is not None:
        if chat.mensajes is None:
            chat.mensajes = [chat_update.mensajes] if not isinstance(chat_update.mensajes, list) else chat_update.mensajes
            mensaje_nuevo = chat_update.mensajes[-1] if isinstance(chat_update.mensajes, list) else chat_update.mensajes
        elif isinstance(chat.mensajes, list):
            if isinstance(chat_update.mensajes, list):
                chat.mensajes.extend(chat_update.mensajes)
                mensaje_nuevo = chat_update.mensajes[-1]
            else:
                chat.mensajes.append(chat_update.mensajes)
                mensaje_nuevo = chat_update.mensajes
        else:
            chat.mensajes = [chat.mensajes, chat_update.mensajes]
            mensaje_nuevo = chat_update.mensajes

    # Si hay mensaje nuevo, analizar sentimiento y guardar en score
    if mensaje_nuevo is not None:
        try:
            chat.score = analizar_sentimiento_gemini(str(mensaje_nuevo))
        except Exception as e:
            chat.score = {"error": str(e)}

    # Si explícitamente se manda score, sobrescribe
    if chat_update.score is not None:
        chat.score = chat_update.score
    db.commit()
    db.refresh(chat)
    return chat

def get_score(db: Session, chat_id: str):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        return chat.score
    return None

def get_chat_messages(db: Session, chat_id: str):
    """
    Obtiene solo los mensajes de un chat específico
    """
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        return chat.mensajes if chat.mensajes else []
    return []

def get_chat_messages_by_user(db: Session, doc_id: int):
    """
    Obtiene los mensajes del chat de un usuario específico
    """
    usuario = get_usuario_y_chat(db, doc_id)
    if usuario and usuario.chat:
        return usuario.chat.mensajes if usuario.chat.mensajes else []
    return []

# Nueva función: obtener todos los chats y su último score
def get_all_chats_with_score(db: Session):
    chats = db.query(Chat).all()
    resultado = []
    for chat in chats:
        usuario = db.query(Usuario).filter(Usuario.chat_id == chat.id).first()
        doc_id = usuario.doc_id if usuario else None
        resultado.append({
            "doc_id": doc_id,
            "mensajes": chat.mensajes,
            "score": chat.score
        })
    return resultado
