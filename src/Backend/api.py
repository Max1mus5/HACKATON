
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, Base, Session as DBSession
from .schemas.chat_schemas import UsuarioCreate, UsuarioOut, ChatUpdate, ChatOut, MessageRequest, MessageResponse
from .repositories.chat_repository import create_usuario_y_chat, get_usuario_y_chat, update_chat, get_score, process_message
from .repositories.chat_repository import get_all_chats_with_score, get_chat_messages, get_chat_messages_by_user
from .utils.gemini_sentiment import analizar_sentimiento_gemini
import os
import json
import random
from datetime import datetime

app = FastAPI(title="LEAN BOT API", description="API para el chatbot LEAN de INGE LEAN")

# Health check endpoint
@app.get('/')
def health_check():
    return {"message": "LEAN BOT API funcionando correctamente", "status": "healthy"}

# Variable global temporal para almacenar la API key recibida
GEMINI_API_KEY_RUNTIME = None

def calculate_message_score(mensaje_usuario, respuesta_bot=None):
    """
    Calcula el score automático de un mensaje usando Gemini sentiment analysis
    Retorna un score numérico entre 1-10
    """
    try:
        # Crear el contexto completo para Gemini
        contexto_completo = f"Mensaje del usuario: {mensaje_usuario}"
        if respuesta_bot:
            contexto_completo += f"\nRespuesta del bot: {respuesta_bot}"
        
        # Usar Gemini para evaluar el score directamente
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("Warning: API key de Gemini no configurada, usando score neutral")
            return 5.0
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
        
        prompt = (
            "Eres un evaluador de conversaciones para LEAN BOT de INGE LEAN. "
            "Evalúa la siguiente conversación y asígnale un score entre 1-10 donde:\n"
            "1-3: Muy negativo (frustración, enojo, problemas graves)\n"
            "4-5: Negativo/Neutro (neutral, indiferente)\n"
            "6-7: Positivo (satisfecho, contento)\n"
            "8-10: Muy positivo (muy satisfecho, entusiasta)\n\n"
            "Responde únicamente con el número del score (ejemplo: 7).\n\n"
            f"Conversación:\n{contexto_completo}"
        )
        
        data = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 5,
                "topP": 0.95
            }
        }
        
        import requests
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # Extraer el score del resultado
        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                score_text = candidate["content"]["parts"][0]["text"].strip()
                # Extraer solo el número
                import re
                score_match = re.search(r'\b([1-9]|10)\b', score_text)
                if score_match:
                    score = float(score_match.group(1))
                    print(f"Score calculado por Gemini: {score} para mensaje: {mensaje_usuario[:50]}...")
                    return score
        
        # Fallback: usar análisis de sentimiento básico
        sentimiento = analizar_sentimiento_gemini(mensaje_usuario)
        if sentimiento == "positivo":
            return 7.0
        elif sentimiento == "negativo":
            return 3.0
        else:  # neutro
            return 5.0
            
    except Exception as e:
        print(f"Error calculando score con Gemini: {e}")
        # Fallback: usar análisis de sentimiento básico
        try:
            sentimiento = analizar_sentimiento_gemini(mensaje_usuario)
            if sentimiento == "positivo":
                return 7.0
            elif sentimiento == "negativo":
                return 3.0
            else:
                return 5.0
        except:
            return 5.0  # Score neutral por defecto
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

@app.get('/usuarios/{doc_id}/messages')
def obtener_mensajes_de_usuario(doc_id: int, db: Session = Depends(get_db)):
    """
    Obtiene solo los mensajes del chat de un usuario específico
    """
    mensajes = get_chat_messages_by_user(db, doc_id)
    return {"mensajes": mensajes}

@app.get('/chats/{chat_id}/messages')
def obtener_mensajes_de_chat(chat_id: str, db: Session = Depends(get_db)):
    """
    Obtiene solo los mensajes de un chat específico
    """
    mensajes = get_chat_messages(db, chat_id)
    if mensajes is None:
        raise HTTPException(status_code=404, detail='Chat no encontrado')
    return {"mensajes": mensajes}

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

# ENDPOINT PARA PANEL DE ADMINISTRACIÓN
@app.get('/admin/all-chats')
def obtener_todos_los_chats_admin(db: Session = Depends(get_db)):
    """
    Endpoint para el panel de administración que obtiene todos los chats con información de usuarios
    Calcula scores automáticamente para mensajes que no los tienen
    """
    try:
        chats_data = get_all_chats_with_score(db)
        
        # Procesar cada chat para asegurar que los mensajes tengan scores
        for chat in chats_data:
            if chat.get('mensajes') and isinstance(chat['mensajes'], list):
                updated_messages = []
                for message in chat['mensajes']:
                    # Si el mensaje no tiene score, calcularlo automáticamente
                    if not message.get('score') and message.get('message'):
                        # Usar contexto completo (mensaje + respuesta) para mejor scoring
                        respuesta_bot = message.get('response', '')
                        message['score'] = calculate_message_score(message['message'], respuesta_bot)
                        print(f"Score calculado para mensaje admin: {message['score']}")
                    
                    # Asegurar que tenga timestamp
                    if not message.get('timestamp'):
                        message['timestamp'] = datetime.now().isoformat()
                    
                    updated_messages.append(message)
                
                chat['mensajes'] = updated_messages
        
        return {"chats": chats_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# ENDPOINTS PARA ADMINISTRACIÓN
@app.get('/admin/chats')
def get_all_chats_admin(db: Session = Depends(get_db)):
    """
    Obtiene todos los chats con información del usuario para el panel de administración
    """
    try:
        chats_with_users = get_all_chats_with_score(db)
        return chats_with_users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener chats: {str(e)}")

@app.get('/admin/stats')
def get_admin_stats(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas generales para el panel de administración
    """
    try:
        chats_data = get_all_chats_with_score(db)
        
        # Calcular estadísticas básicas
        total_chats = len(chats_data)
        unique_users = len(set(chat.get('usuario_doc_id') for chat in chats_data))
        
        # Calcular promedio de sentimientos
        total_score = 0
        score_count = 0
        
        for chat in chats_data:
            if chat.get('mensajes'):
                try:
                    messages = chat['mensajes'] if isinstance(chat['mensajes'], list) else json.loads(chat['mensajes'])
                    for message in messages:
                        if message.get('score'):
                            total_score += float(message['score'])
                            score_count += 1
                except:
                    continue
        
        avg_sentiment = (total_score / score_count) if score_count > 0 else 5.0
        avg_sentiment_percentage = int((avg_sentiment / 10) * 100)
        
        return {
            "total_users": unique_users,
            "total_chats": total_chats,
            "avg_sentiment": avg_sentiment_percentage,
            "avg_response_time": "2.3s"  # Placeholder
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")
