from pydantic import BaseModel
from typing import Optional, Any, List
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
    doc_id: Optional[int] = None

class MessageResponse(BaseModel):
    message: str
    score: Optional[float]
    timestamp: str
    response: str

class UsuarioBase(BaseModel):
    doc_id: int

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioOut(UsuarioBase):
    id: str
    chat: ChatOut
    class Config:
        orm_mode = True
