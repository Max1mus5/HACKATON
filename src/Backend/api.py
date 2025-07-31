
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Union
from .database import engine, Base, Session as DBSession
from .schemas.chat_schemas import UsuarioCreate, UsuarioOut, ChatUpdate, ChatOut, MessageRequest, MessageResponse
from .repositories.chat_repository import create_usuario_y_chat, get_usuario_y_chat, update_chat, get_score, process_message
from .repositories.chat_repository import get_all_chats_with_score, get_chat_messages, get_chat_messages_by_user, get_ai_service
from .utils.beto_sentiment import analyze_sentiment, get_sentiment_analyzer, get_sentiment_score
from .utils.sentiment_analytics import get_analytics_service
import os
import json
import random
from datetime import datetime
import os

# Configurar API key por defecto si no existe
if not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = "AIzaSyCrzdwv-viQnqcFnc7PBAimEzyDMf4dXY0"

app = FastAPI(title="LEAN BOT API", description="API para el chatbot LEAN de INGE LEAN")

# Health check endpoint (eliminado duplicado)

# Variable global temporal para almacenar la API key recibida
GEMINI_API_KEY_RUNTIME = None

# Endpoint para configurar API key de Gemini
@app.post('/config/gemini_api_key')
def configure_gemini_api_key(request: dict):
    """
    Recibe un JSON con {"api_key": "..."} y la almacena en una variable global para uso en el backend.
    """
    global GEMINI_API_KEY_RUNTIME
    try:
        api_key = request.get('api_key')
        if api_key and api_key.strip():
            GEMINI_API_KEY_RUNTIME = api_key.strip()
            # También configurar en el entorno para que lo use gemini_chat.py
            os.environ["GEMINI_API_KEY"] = api_key.strip()
            print(f"✅ API key de Gemini configurada: {api_key[:10]}...")
            return {"status": "success", "message": "API key configurada correctamente"}
        else:
            return {"status": "error", "message": "API key vacía"}
    except Exception as e:
        print(f"❌ Error configurando API key: {e}")
        return {"status": "error", "message": str(e)}

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

@app.get("/health")
def health_check_alt():
    """Endpoint alternativo de health check"""
    return {"message": "LEAN BOT API funcionando correctamente", "status": "healthy"}

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@app.get('/usuarios/{doc_id}/chat', response_model=ChatOut)
def obtener_chat_de_usuario(doc_id: Union[int, str], db: Session = Depends(get_db)):
    usuario = get_usuario_y_chat(db, doc_id)
    if not usuario or not usuario.chat:
        raise HTTPException(status_code=404, detail='Chat no encontrado para este usuario')
    return usuario.chat

@app.get('/usuarios/{doc_id}/messages')
def obtener_mensajes_de_usuario(doc_id: Union[int, str], db: Session = Depends(get_db)):
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
def enviar_mensaje_por_usuario(doc_id: Union[int, str], message_request: MessageRequest, db: Session = Depends(get_db)):
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
def obtener_usuario_y_chat_endpoint(doc_id: Union[int, str], db: Session = Depends(get_db)):
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

# ENDPOINTS PARA GESTIÓN DE PROVEEDORES DE IA
@app.get('/ai/providers')
def get_available_providers():
    """
    Obtiene la lista de proveedores de IA disponibles
    """
    ai_service = get_ai_service()
    return {
        "providers": ai_service.get_available_providers(),
        "default": "gemini"
    }

@app.post('/ai/test')
def test_ai_provider(request: dict):
    """
    Prueba la conexión con un proveedor de IA específico
    
    Body: {
        "provider": "gemini" | "mistral",
        "api_key": "optional_custom_api_key"
    }
    """
    provider = request.get("provider", "gemini")
    api_key = request.get("api_key")
    
    ai_service = get_ai_service()
    result = ai_service.test_provider(provider, api_key)
    
    return result

# NUEVOS ENDPOINTS PARA ANÁLISIS DE SENTIMIENTOS CON BETO

@app.post('/sentiment/analyze')
def analyze_text_sentiment(request: dict):
    """
    Analiza el sentimiento de un texto usando BETO
    
    Body: {
        "text": "texto a analizar",
        "user_id": "optional_user_id",
        "conversation_id": "optional_conversation_id"
    }
    """
    try:
        text = request.get("text", "")
        user_id = request.get("user_id", "unknown")
        conversation_id = request.get("conversation_id", "default")
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Texto vacío")
        
        # Analizar sentimiento con BETO
        sentiment_result = analyze_sentiment(text)
        
        # Agregar datos adicionales para analytics
        sentiment_data = {
            **sentiment_result,
            "user_id": user_id,
            "conversation_id": conversation_id,
            "message": text
        }
        
        # Registrar en analytics
        analytics_service = get_analytics_service()
        analytics_service.add_sentiment_data(sentiment_data)
        
        return sentiment_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis de sentimiento: {str(e)}")

@app.get('/sentiment/model-info')
def get_sentiment_model_info():
    """
    Obtiene información sobre el modelo de análisis de sentimientos
    """
    try:
        analyzer = get_sentiment_analyzer()
        return analyzer.get_model_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo información del modelo: {str(e)}")

@app.get('/analytics/dashboard')
def get_sentiment_dashboard():
    """
    Obtiene datos del dashboard de análisis de sentimientos
    """
    try:
        analytics_service = get_analytics_service()
        dashboard_data = analytics_service.get_dashboard_data()
        return dashboard_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo datos del dashboard: {str(e)}")

@app.get('/analytics/metrics')
def get_sentiment_metrics(hours_back: int = 24, conversation_id: str = None):
    """
    Obtiene métricas de sentimiento para un período específico
    
    Query params:
    - hours_back: Horas hacia atrás para el análisis (default: 24)
    - conversation_id: ID de conversación específica (opcional)
    """
    try:
        analytics_service = get_analytics_service()
        metrics = analytics_service.get_sentiment_metrics(
            hours_back=hours_back,
            conversation_id=conversation_id
        )
        
        # Convertir dataclass a dict para JSON serialization
        from dataclasses import asdict
        return asdict(metrics)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas: {str(e)}")

@app.get('/analytics/conversation/{conversation_id}')
def get_conversation_analytics(conversation_id: str):
    """
    Obtiene análisis detallado de una conversación específica
    """
    try:
        analytics_service = get_analytics_service()
        conversation_analytics = analytics_service.analyze_conversation(conversation_id)
        
        # Convertir dataclass a dict para JSON serialization
        from dataclasses import asdict
        return asdict(conversation_analytics)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando conversación: {str(e)}")

@app.get('/analytics/trends/hourly')
def get_hourly_sentiment_trends():
    """
    Obtiene tendencias de sentimiento por hora del día
    """
    try:
        analytics_service = get_analytics_service()
        dashboard_data = analytics_service.get_dashboard_data()
        return {"hourly_trends": dashboard_data.get("hourly_trends", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo tendencias: {str(e)}")

@app.get('/analytics/keywords')
def get_sentiment_keywords():
    """
    Obtiene palabras clave asociadas a cada sentimiento
    """
    try:
        analytics_service = get_analytics_service()
        dashboard_data = analytics_service.get_dashboard_data()
        return {"sentiment_keywords": dashboard_data.get("sentiment_keywords", {})}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo palabras clave: {str(e)}")

@app.get('/analytics/conversations/active')
def get_active_conversations():
    """
    Obtiene conversaciones activas en las últimas 24 horas
    """
    try:
        analytics_service = get_analytics_service()
        dashboard_data = analytics_service.get_dashboard_data()
        return {"active_conversations": dashboard_data.get("active_conversations", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo conversaciones activas: {str(e)}")

# ENDPOINT PARA PRUEBAS DEL SISTEMA DE SENTIMIENTOS
@app.post('/test/sentiment')
def test_sentiment_system():
    """
    Endpoint de prueba para verificar el funcionamiento del sistema de análisis de sentimientos
    """
    try:
        test_texts = [
            "¡Este chatbot es increíble! Me ha ayudado muchísimo.",
            "El servicio al cliente fue pésimo, estoy muy molesto.",
            "Necesito información sobre los horarios de atención.",
            "La idea es buena, pero la implementación fue un desastre."
        ]
        
        results = []
        analytics_service = get_analytics_service()
        
        for i, text in enumerate(test_texts):
            # Analizar sentimiento
            sentiment_result = analyze_sentiment(text)
            
            # Agregar a analytics
            sentiment_data = {
                **sentiment_result,
                "user_id": f"test_user_{i}",
                "conversation_id": "test_conversation",
                "message": text
            }
            analytics_service.add_sentiment_data(sentiment_data)
            
            results.append({
                "text": text,
                "sentiment": sentiment_result
            })
        
        # Obtener métricas de prueba
        test_metrics = analytics_service.get_sentiment_metrics(
            hours_back=1,
            conversation_id="test_conversation"
        )
        
        from dataclasses import asdict
        return {
            "status": "success",
            "test_results": results,
            "test_metrics": asdict(test_metrics),
            "model_info": get_sentiment_analyzer().get_model_info()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error en prueba del sistema: {str(e)}"
        }
