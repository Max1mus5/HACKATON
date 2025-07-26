
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, Base, Session as DBSession
from .schemas.chat_schemas import UsuarioCreate, UsuarioOut, ChatUpdate, ChatOut, MessageRequest, MessageResponse
from .repositories.chat_repository import create_usuario_y_chat, get_usuario_y_chat, update_chat, get_score, process_message
from .repositories.chat_repository import get_all_chats_with_score

app = FastAPI(title="LEAN BOT API", description="API para el chatbot LEAN de INGE LEAN")

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
    return {"message": "LEAN BOT API funcionando correctamente", "cors": "enabled", "version": "2.0"}

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

# NUEVO ENDPOINT: Enviar mensaje al chatbot LEAN BOT
@app.post('/chats/{chat_id}', response_model=MessageResponse)
def enviar_mensaje_al_chat(chat_id: str, message_request: MessageRequest, db: Session = Depends(get_db)):
    """
    Endpoint principal para enviar mensajes al chatbot LEAN BOT.
    Procesa el mensaje completo: genera respuesta con Gemini, analiza sentimiento y guarda en BD.
    """
    try:
        response = process_message(db, chat_id, message_request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# ENDPOINT ALTERNATIVO: Enviar mensaje con doc_id en lugar de chat_id
@app.post('/usuarios/{doc_id}/message', response_model=MessageResponse)
def enviar_mensaje_por_usuario(doc_id: int, message_request: MessageRequest, db: Session = Depends(get_db)):
    """
    Endpoint alternativo para enviar mensajes usando doc_id del usuario.
    """
    usuario = get_usuario_y_chat(db, doc_id)
    if not usuario or not usuario.chat:
        # Si no existe el usuario, crearlo automáticamente
        usuario = create_usuario_y_chat(db, doc_id)
    
    message_request.doc_id = doc_id
    try:
        response = process_message(db, usuario.chat.id, message_request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.get('/usuarios/{doc_id}', response_model=UsuarioOut)
def obtener_usuario_y_chat_endpoint(doc_id: int, db: Session = Depends(get_db)):
    usuario = get_usuario_y_chat(db, doc_id)
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return usuario

# ENDPOINT LEGACY: Mantener compatibilidad con el sistema anterior
@app.put('/chats/{chat_id}', response_model=ChatOut)
def actualizar_chat_endpoint(chat_id: str, chat_update: ChatUpdate, db: Session = Depends(get_db)):
    """
    Endpoint legacy para compatibilidad. Se recomienda usar POST /chats/{chat_id} para nuevos mensajes.
    """
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

# Endpoint de prueba para verificar integración con Gemini
@app.get('/test/gemini')
def test_gemini_integration():
    """
    Endpoint de prueba para verificar que la integración con Gemini funciona correctamente.
    """
    try:
        from .utils.gemini_chat import GeminiChatService
        gemini_service = GeminiChatService()
        
        if gemini_service.test_connection():
            return {
                "status": "success", 
                "message": "Conexión con Gemini API establecida correctamente",
                "lean_bot": "LEAN BOT listo para funcionar"
            }
        else:
            return {
                "status": "error", 
                "message": "No se pudo conectar con Gemini API",
                "lean_bot": "LEAN BOT no disponible"
            }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Error al probar Gemini: {str(e)}",
            "lean_bot": "LEAN BOT no disponible"
        }
