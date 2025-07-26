
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, Base, Session as DBSession
from .schemas.chat_schemas import UsuarioCreate, UsuarioOut, ChatUpdate, ChatOut
from .repositories.chat_repository import create_usuario_y_chat, get_usuario_y_chat, update_chat, get_score
from .repositories.chat_repository import get_all_chats_with_score
import os

# Variable global temporal para almacenar la API key recibida
GEMINI_API_KEY_RUNTIME = None
# Endpoint para recibir y almacenar la API key de Gemini
@app.post('/config/gemini_api_key')
def set_gemini_api_key(payload: dict):
    """
    Recibe un JSON con {"api_key": "..."} y la almacena en una variable global para uso en el backend.
    """
    global GEMINI_API_KEY_RUNTIME
    api_key = payload.get("api_key")
    if not api_key:
        raise HTTPException(status_code=400, detail="Falta el campo 'api_key'")
    GEMINI_API_KEY_RUNTIME = api_key
    os.environ["GEMINI_API_KEY"] = api_key  # Para que la función de sentimiento la use
    return {"message": "API key almacenada correctamente"}
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origins
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    """Endpoint de prueba para verificar que la API funciona y CORS está configurado"""
    return {"message": "API LEAN Chatbot funcionando correctamente", "cors": "enabled"}

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@app.get('/usuarios/{doc_id}/chat', response_model=ChatOut)
def obtener_chat_de_usuario(doc_id: int, db: Session = Depends(get_db)):
    usuario = get_usuario_y_chat(db, doc_id)
    if not usuario or not usuario.chat:
        raise HTTPException(status_code=404, detail='Chat no encontrado para este usuario')
    return usuario.chat

@app.post('/usuarios/', response_model=UsuarioOut)
def crear_usuario_y_chat_endpoint(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Validar si el usuario ya existe
    usuario_existente = get_usuario_y_chat(db, usuario.doc_id)
    if usuario_existente:
        return usuario_existente
    db_usuario = create_usuario_y_chat(db, usuario.doc_id)
    return db_usuario

@app.get('/usuarios/{doc_id}', response_model=UsuarioOut)
def obtener_usuario_y_chat_endpoint(doc_id: int, db: Session = Depends(get_db)):
    usuario = get_usuario_y_chat(db, doc_id)
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return usuario

@app.put('/chats/{chat_id}', response_model=ChatOut)
def actualizar_chat_endpoint(chat_id: str, chat_update: ChatUpdate, db: Session = Depends(get_db)):
    chat = update_chat(db, chat_id, chat_update)
    if not chat:
        raise HTTPException(status_code=404, detail='Chat no encontrado')
    return chat

@app.get('/chats/{chat_id}/score')
def obtener_score_endpoint(chat_id: str, db: Session = Depends(get_db)):
    score = get_score(db, chat_id)
    if score is None:
        raise HTTPException(status_code=404, detail='Chat no encontrado')
    return {"score": score}

# Nuevo endpoint: obtener todos los chats y su último score
@app.get('/chats/', response_model=list[dict])
def obtener_todos_los_chats_con_score(db: Session = Depends(get_db)):
    """
    Retorna una lista de objetos con: doc_id, mensajes (json) y score para cada chat.
    """
    return get_all_chats_with_score(db)
