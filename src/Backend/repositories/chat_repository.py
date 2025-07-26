from sqlalchemy.orm import Session
from ..models.chat import Usuario, Chat
from ..schemas.chat_schemas import UsuarioCreate, ChatCreate, ChatUpdate

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
    if chat_update.mensajes is not None:
        if chat.mensajes is None:
            # Si no hay mensajes previos, inicializa como lista
            chat.mensajes = [chat_update.mensajes] if not isinstance(chat_update.mensajes, list) else chat_update.mensajes
        elif isinstance(chat.mensajes, list):
            # Si ya es una lista, agrega el/los nuevos mensajes
            if isinstance(chat_update.mensajes, list):
                chat.mensajes.extend(chat_update.mensajes)
            else:
                chat.mensajes.append(chat_update.mensajes)
        else:
            # Si por alguna razón no es lista, lo convierte en lista
            chat.mensajes = [chat.mensajes, chat_update.mensajes]
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
