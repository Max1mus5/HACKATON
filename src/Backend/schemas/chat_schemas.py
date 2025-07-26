from pydantic import BaseModel
from typing import Optional, Any

class ChatBase(BaseModel):
    mensajes: Optional[Any] = None
    score: Optional[Any] = None

class ChatCreate(ChatBase):
    pass

class ChatUpdate(ChatBase):
    pass

class ChatOut(ChatBase):
    id: str
    class Config:
        orm_mode = True

class UsuarioBase(BaseModel):
    doc_id: int

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioOut(UsuarioBase):
    id: str
    chat: ChatOut
    class Config:
        orm_mode = True
