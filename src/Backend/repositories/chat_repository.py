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
    if chat_update.mensajes is not None:
        chat.mensajes = chat_update.mensajes
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
