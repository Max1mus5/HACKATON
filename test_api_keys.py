#!/usr/bin/env python3
"""
Script de prueba para validar todas las API keys de Gemini disponibles.
Verifica cuáles funcionan correctamente y reporta el estado.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Backend.utils.api_key_manager import get_api_key_manager
from Backend.utils.gemini_chat import GeminiChatService


def main():
    """
    Ejecuta pruebas completas del sistema de API keys
    """
    print("=" * 70)
    print("🧪 LEAN BOT - Test de API Keys de Gemini")
    print("=" * 70)
    print()
    
    # 1. Probar todas las API keys disponibles
    print("📋 FASE 1: Probando todas las API keys registradas")
    print("-" * 70)
    
    manager = get_api_key_manager()
    results = manager.test_all_keys()
    
    working_keys = [key for key, works in results if works]
    failed_keys = [key for key, works in results if not works]
    
    print("\n📊 RESULTADOS:")
    print(f"   ✅ Claves funcionales: {len(working_keys)}/{len(results)}")
    print(f"   ❌ Claves no funcionales: {len(failed_keys)}/{len(results)}")
    
    if not working_keys:
        print("\n❌ ERROR CRÍTICO: Ninguna API key está funcionando.")
        print("   Por favor, verifica las claves o contacta al administrador.")
        return False
    
    print(f"\n✅ Al menos una clave funciona. El sistema puede operar normalmente.")
    
    # 2. Probar el servicio de chat con la clave activa
    print("\n" + "=" * 70)
    print("📋 FASE 2: Probando el servicio de chat con GeminiChatService")
    print("-" * 70)
    
    try:
        gemini_service = GeminiChatService()
        print(f"\n🔑 API key activa: {gemini_service.api_key[:15]}...")
        print(f"🤖 Modelo: {gemini_service.model}")
        print(f"🌐 URL base: {gemini_service.base_url}")
        
        # Probar generación de respuesta
        print("\n🧪 Probando generación de respuesta...")
        test_message = "¿Qué servicios ofrece INGE LEAN?"
        print(f"   Mensaje de prueba: '{test_message}'")
        
        response = gemini_service.generate_response(test_message)
        
        if response and "Lo siento" not in response:
            print(f"\n✅ Respuesta generada exitosamente:")
            print(f"   {response[:150]}...")
            test_passed = True
        else:
            print(f"\n❌ Error en la generación de respuesta:")
            print(f"   {response}")
            test_passed = False
            
    except Exception as e:
        print(f"\n❌ Error al probar el servicio de chat:")
        print(f"   {str(e)}")
        test_passed = False
    
    # 3. Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 70)
    
    print(f"\n1️⃣  API Keys disponibles: {len(results)}")
    print(f"   ✅ Funcionales: {len(working_keys)}")
    print(f"   ❌ No funcionales: {len(failed_keys)}")
    
    print(f"\n2️⃣  Servicio de Chat (GeminiChatService):")
    print(f"   {'✅ FUNCIONANDO' if test_passed else '❌ CON ERRORES'}")
    
    print(f"\n3️⃣  Estado general del sistema:")
    if working_keys and test_passed:
        print(f"   ✅ SISTEMA OPERATIVO - Listo para producción")
        print(f"\n💡 Recomendación: Iniciar el servidor con: python main.py")
        return True
    else:
        print(f"   ⚠️  SISTEMA CON PROBLEMAS - Revisar configuración")
        return False
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
