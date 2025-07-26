from sqlalchemy.orm import Session
from ..models.chat import Usuario, Chat

from ..schemas.chat_schemas import UsuarioCreate, ChatCreate, ChatUpdate
from ..utils.gemini_sentiment import analizar_sentimiento_gemini

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
