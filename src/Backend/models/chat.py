from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.orm import relationship
from src.Backend.database import Base
from datetime import datetime
import uuid

class Chat(Base):
    __tablename__ = 'chats'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    mensajes = Column(SQLiteJSON, nullable=True)
    score = Column(Float, nullable=True, default=5.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario = relationship('Usuario', back_populates='chat', uselist=False)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    doc_id = Column(String, nullable=False, unique=True)
    chat_id = Column(String, ForeignKey('chats.id'), nullable=False, unique=True)
    chat = relationship('Chat', back_populates='usuario', uselist=False)
