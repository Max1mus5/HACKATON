from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.orm import relationship
from ..database import Base
import uuid

class Chat(Base):
    __tablename__ = 'chats'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    mensajes = Column(SQLiteJSON, nullable=True)
    score = Column(SQLiteJSON, nullable=True)
    usuario = relationship('Usuario', back_populates='chat', uselist=False)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    doc_id = Column(Integer, nullable=False, unique=True)
    chat_id = Column(String, ForeignKey('chats.id'), nullable=False, unique=True)
    chat = relationship('Chat', back_populates='usuario', uselist=False)
