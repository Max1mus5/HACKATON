from pydantic import BaseModel
from typing import Optional, Any, List, Union
from datetime import datetime

class MessageSchema(BaseModel):
    message: str
    score: Optional[float] = None
    timestamp: str
    response: Optional[str] = None

class ChatBase(BaseModel):
    mensajes: Optional[List[MessageSchema]] = None
    score: Optional[Any] = None

class ChatCreate(ChatBase):
    pass

class ChatUpdate(ChatBase):
    pass

class ChatOut(ChatBase):
    id: str
    class Config:
        orm_mode = True

class MessageRequest(BaseModel):
    message: str
    doc_id: Optional[Union[int, str]] = None
    ai_provider: Optional[str] = "gemini"  # "gemini" o "mistral"
    api_key: Optional[str] = None  # API key personalizada

class MessageResponse(BaseModel):
    message: str
    response: str  # Respuesta del bot
    score: Optional[float]
    ai_provider: Optional[str] = "gemini"  # Proveedor usado para generar la respuesta
    timestamp: str

class UsuarioBase(BaseModel):
    doc_id: Union[int, str]

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioOut(UsuarioBase):
    id: str
    chat: ChatOut
    class Config:
        orm_mode = True
