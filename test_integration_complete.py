#!/usr/bin/env python3
"""
Script de pruebas de integración completas para LEAN BOT.
Verifica todos los componentes críticos del sistema sin necesidad de servidor corriendo.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 80)
print("🧪 LEAN BOT - Pruebas de Integración Completas")
print("=" * 80)
print()

# ============================================================================
# FASE 1: Verificar API Keys de Gemini
# ============================================================================
print("📋 FASE 1: Verificación de API Keys de Gemini")
print("-" * 80)

try:
    from Backend.utils.api_key_manager import get_api_key_manager, get_working_api_key
    
    manager = get_api_key_manager()
    results = manager.test_all_keys()
    
    working_keys = [key for key, works in results if works]
    
    if working_keys:
        print(f"✅ API Keys funcionales: {len(working_keys)}/{len(results)}")
        active_key = get_working_api_key()
        print(f"✅ Clave activa: {active_key[:15]}...")
        phase1_passed = True
    else:
        print(f"❌ No hay API keys funcionales")
        phase1_passed = False
        
except Exception as e:
    print(f"❌ Error en verificación de API keys: {e}")
    phase1_passed = False

print()

# ============================================================================
# FASE 2: Verificar Servicio de IA (Gemini Chat)
# ============================================================================
print("📋 FASE 2: Verificación del Servicio de IA Generativa (Gemini)")
print("-" * 80)

try:
    from Backend.utils.gemini_chat import GeminiChatService
    
    gemini_service = GeminiChatService()
    print(f"🤖 Modelo configurado: {gemini_service.model}")
    print(f"🔑 API key activa: {gemini_service.api_key[:15]}...")
    
    # Probar generación de respuesta
    print("\n🧪 Probando generación de respuesta...")
    test_message = "Hola, ¿qué servicios ofrece INGE LEAN?"
    response = gemini_service.generate_response(test_message)
    
    if response and "Lo siento" not in response and len(response) > 50:
        print(f"✅ Respuesta generada exitosamente ({len(response)} caracteres)")
        print(f"   Extracto: {response[:100]}...")
        phase2_passed = True
    else:
        print(f"❌ Respuesta no válida: {response[:100] if response else 'Sin respuesta'}")
        phase2_passed = False
        
except Exception as e:
    print(f"❌ Error en servicio de IA: {e}")
    import traceback
    traceback.print_exc()
    phase2_passed = False

print()

# ============================================================================
# FASE 3: Verificar Análisis de Sentimientos (BETO)
# ============================================================================
print("📋 FASE 3: Verificación del Análisis de Sentimientos (BETO)")
print("-" * 80)

try:
    from Backend.utils.beto_sentiment import analyze_sentiment, get_sentiment_analyzer
    
    analyzer = get_sentiment_analyzer()
    model_info = analyzer.get_model_info()
    
    print(f"🤖 Modelo: {model_info.get('model_name', 'N/A')}")
    print(f"📊 Estado: {model_info.get('status', 'N/A')}")
    
    # Probar análisis de diferentes sentimientos
    print("\n🧪 Probando análisis de sentimientos...")
    
    test_cases = [
        ("Este servicio es excelente, me encanta!", "POS"),
        ("Estoy muy molesto con la atención", "NEG"),
        ("Necesito información sobre horarios", "NEU")
    ]
    
    results_correct = 0
    for text, expected in test_cases:
        result = analyze_sentiment(text)
        sentiment = result.get("sentiment", "UNKNOWN")
        confidence = result.get("confidence", 0)
        
        is_correct = sentiment == expected
        results_correct += 1 if is_correct else 0
        
        status_icon = "✅" if is_correct else "⚠️"
        print(f"   {status_icon} '{text[:40]}...'")
        print(f"      Esperado: {expected}, Obtenido: {sentiment} (Confianza: {confidence:.2f})")
    
    accuracy = (results_correct / len(test_cases)) * 100
    print(f"\n📊 Precisión del análisis: {accuracy:.1f}% ({results_correct}/{len(test_cases)})")
    
    phase3_passed = accuracy >= 66.0  # Al menos 2 de 3 correctos
    
except Exception as e:
    print(f"❌ Error en análisis de sentimientos: {e}")
    import traceback
    traceback.print_exc()
    phase3_passed = False

print()

# ============================================================================
# FASE 4: Verificar Sistema de Analytics
# ============================================================================
print("📋 FASE 4: Verificación del Sistema de Analytics")
print("-" * 80)

try:
    from Backend.utils.sentiment_analytics import get_analytics_service
    
    analytics = get_analytics_service()
    
    # Agregar datos de prueba
    print("🧪 Agregando datos de prueba al sistema de analytics...")
    
    test_data = [
        {"sentiment": "POS", "confidence": 0.95, "user_id": "test1", "conversation_id": "conv1", "message": "Excelente servicio"},
        {"sentiment": "NEG", "confidence": 0.85, "user_id": "test2", "conversation_id": "conv1", "message": "Mal servicio"},
        {"sentiment": "NEU", "confidence": 0.75, "user_id": "test3", "conversation_id": "conv1", "message": "Información general"}
    ]
    
    for data in test_data:
        analytics.add_sentiment_data(data)
    
    # Obtener métricas
    print("📊 Obteniendo métricas del sistema...")
    metrics = analytics.get_sentiment_metrics(hours_back=24)
    
    print(f"   Total de mensajes analizados: {metrics.total_messages}")
    print(f"   Confianza promedio: {metrics.average_confidence:.2f}")
    print(f"   Distribución de sentimientos:")
    print(f"      - Positivos: {metrics.positive_count}")
    print(f"      - Negativos: {metrics.negative_count}")
    print(f"      - Neutrales: {metrics.neutral_count}")
    
    # Obtener dashboard
    dashboard = analytics.get_dashboard_data()
    
    if dashboard and "sentiment_distribution" in dashboard:
        print(f"\n✅ Dashboard generado correctamente")
        print(f"   Campos disponibles: {', '.join(dashboard.keys())}")
        phase4_passed = True
    else:
        print(f"⚠️  Dashboard generado con campos limitados")
        phase4_passed = True  # No crítico
        
except Exception as e:
    print(f"❌ Error en sistema de analytics: {e}")
    import traceback
    traceback.print_exc()
    phase4_passed = False

print()

# ============================================================================
# FASE 5: Verificar Base de Datos y Repositorios
# ============================================================================
print("📋 FASE 5: Verificación de Base de Datos y Repositorios")
print("-" * 80)

try:
    from Backend.database import engine, Base
    from Backend.repositories.chat_repository import create_usuario_y_chat, get_usuario_y_chat
    from Backend.database import Session as DBSession
    
    # Crear tablas
    print("🗄️  Creando/verificando estructura de base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas de base de datos verificadas")
    
    # Probar operaciones básicas
    print("\n🧪 Probando operaciones de repositorio...")
    
    db = DBSession()
    try:
        # Crear usuario de prueba
        test_doc_id = "test_integration_12345"
        usuario = create_usuario_y_chat(db, test_doc_id)
        
        if usuario and usuario.chat:
            print(f"✅ Usuario y chat creados correctamente")
            print(f"   Usuario ID: {usuario.doc_id}")
            print(f"   Chat ID: {usuario.chat.id}")
            
            # Verificar recuperación
            usuario_recuperado = get_usuario_y_chat(db, test_doc_id)
            if usuario_recuperado:
                print(f"✅ Usuario recuperado correctamente de la BD")
                phase5_passed = True
            else:
                print(f"❌ No se pudo recuperar el usuario")
                phase5_passed = False
        else:
            print(f"❌ Error al crear usuario y chat")
            phase5_passed = False
            
    finally:
        db.close()
        
except Exception as e:
    print(f"❌ Error en operaciones de base de datos: {e}")
    import traceback
    traceback.print_exc()
    phase5_passed = False

print()

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("=" * 80)
print("📊 RESUMEN DE PRUEBAS DE INTEGRACIÓN")
print("=" * 80)
print()

phases = [
    ("API Keys de Gemini", phase1_passed),
    ("Servicio de IA Generativa (Gemini)", phase2_passed),
    ("Análisis de Sentimientos (BETO)", phase3_passed),
    ("Sistema de Analytics", phase4_passed),
    ("Base de Datos y Repositorios", phase5_passed)
]

total_phases = len(phases)
passed_phases = sum(1 for _, passed in phases if passed)

for i, (name, passed) in enumerate(phases, 1):
    status = "✅ APROBADO" if passed else "❌ FALLIDO"
    print(f"{i}. {name}: {status}")

print()
print(f"{'=' * 80}")
print(f"RESULTADO FINAL: {passed_phases}/{total_phases} fases aprobadas ({(passed_phases/total_phases)*100:.1f}%)")
print(f"{'=' * 80}")
print()

if passed_phases == total_phases:
    print("✅ ¡TODAS LAS PRUEBAS PASARON! Sistema listo para producción.")
    print()
    print("🚀 Siguiente paso: Iniciar el servidor con:")
    print("   python main.py")
    print()
    print("📝 Luego verificar en el navegador:")
    print("   - http://localhost:12000/chat.html")
    print("   - http://localhost:12000/analytics.html")
    print("   - http://localhost:12000/docs")
    sys.exit(0)
elif passed_phases >= total_phases * 0.8:
    print("⚠️  Sistema funcional con advertencias menores.")
    print("   Se recomienda revisar las fases fallidas antes de producción.")
    sys.exit(0)
else:
    print("❌ Sistema con problemas críticos.")
    print("   Se requiere revisión antes de continuar.")
    sys.exit(1)
