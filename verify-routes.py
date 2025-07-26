#!/usr/bin/env python3
"""
Script de verificación para las rutas sin .html
Verifica que todas las rutas principales respondan correctamente
"""

import requests
import sys
from urllib.parse import urljoin

def test_url(base_url, path, expected_status=200):
    """Prueba una URL y retorna el resultado"""
    url = urljoin(base_url, path)
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        status = "✅ OK" if response.status_code == expected_status else f"❌ ERROR ({response.status_code})"
        print(f"{status} - {url}")
        return response.status_code == expected_status
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR - {url} - {str(e)}")
        return False

def main():
    # URL base - cambiar según el entorno
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "https://7-lean-chat.vercel.app"  # Por defecto Vercel
    
    print(f"🔍 Verificando rutas en: {base_url}")
    print("=" * 50)
    
    # Rutas a verificar (sin .html)
    routes = [
        "/",
        "/login",
        "/chat", 
        "/admin",
        "/dashboard",
        "/chat-detail"
    ]
    
    # Verificar cada ruta
    success_count = 0
    total_count = len(routes)
    
    for route in routes:
        if test_url(base_url, route):
            success_count += 1
    
    print("=" * 50)
    print(f"📊 Resultado: {success_count}/{total_count} rutas funcionando")
    
    if success_count == total_count:
        print("🎉 ¡Todas las rutas funcionan correctamente!")
        return 0
    else:
        print("⚠️  Algunas rutas tienen problemas")
        return 1

if __name__ == "__main__":
    exit(main())
