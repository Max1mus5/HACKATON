FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorio para cache de transformers
RUN mkdir -p /tmp/transformers_cache
ENV TRANSFORMERS_CACHE=/tmp/transformers_cache

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "src.Backend.api:app", "--host", "0.0.0.0", "--port", "8000"]