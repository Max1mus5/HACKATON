"""
Servicio de análisis de sentimientos usando BETO (BERT en español)
Modelo: finiteautomata/beto-sentiment-analysis
"""

import os
import logging
from typing import Dict, Optional, Tuple

# Importaciones con manejo de errores
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
    TORCH_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Warning: transformers no disponible: {e}")
    TRANSFORMERS_AVAILABLE = False
    TORCH_AVAILABLE = False
    torch = None  # Definir torch como None para evitar errores

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BetoSentimentAnalyzer:
    """
    Analizador de sentimientos usando el modelo BETO específicamente entrenado para español
    """
    
    def __init__(self):
        self.model_name = "finiteautomata/beto-sentiment-analysis"
        self.analyzer = None
        self.available = TRANSFORMERS_AVAILABLE
        
        if TRANSFORMERS_AVAILABLE and TORCH_AVAILABLE:
            try:
                self.device = "cuda" if torch and torch.cuda.is_available() else "cpu"
            except:
                self.device = "cpu"
            self._initialize_model()
        else:
            self.device = "cpu"  # Valor por defecto cuando transformers no está disponible
            logger.warning("BETO no disponible - usando análisis básico de palabras clave")
    
    def _initialize_model(self):
        """
        Inicializa el modelo BETO para análisis de sentimientos
        """
        if not TRANSFORMERS_AVAILABLE:
            return
            
        try:
            logger.info(f"Inicializando modelo BETO en dispositivo: {self.device}")
            
            # Cargar el pipeline de análisis de sentimientos
            self.analyzer = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name,
                device=0 if self.device == "cuda" else -1,
                return_all_scores=True
            )
            
            logger.info("Modelo BETO inicializado correctamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar modelo BETO: {e}")
            self.analyzer = None
    
    def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """
        Analiza el sentimiento de un texto usando BETO
        
        Args:
            text (str): Texto a analizar
            
        Returns:
            Dict con el análisis de sentimiento
        """
        if not TRANSFORMERS_AVAILABLE or not self.analyzer:
            logger.warning("Modelo BETO no disponible, usando análisis básico")
            return self._fallback_analysis(text)
        
        try:
            # Limpiar y preparar el texto
            clean_text = self._preprocess_text(text)
            
            if not clean_text.strip():
                return {
                    "sentiment": "NEU",
                    "confidence": 0.5,
                    "label": "neutral",
                    "scores": {"POS": 0.33, "NEG": 0.33, "NEU": 0.34},
                    "analysis_type": "empty_text"
                }
            
            # Realizar análisis con BETO
            results = self.analyzer(clean_text)
            
            # Procesar resultados
            sentiment_data = self._process_beto_results(results[0])
            
            # Agregar información adicional
            sentiment_data.update({
                "original_text": text,
                "processed_text": clean_text,
                "model": self.model_name,
                "device": self.device,
                "analysis_type": "beto_model"
            })
            
            logger.info(f"Análisis completado: {sentiment_data['label']} ({sentiment_data['confidence']:.2f})")
            
            return sentiment_data
            
        except Exception as e:
            logger.error(f"Error en análisis BETO: {e}")
            return self._fallback_analysis(text)
    
    def _process_beto_results(self, results: list) -> Dict[str, any]:
        """
        Procesa los resultados del modelo BETO
        """
        # Crear diccionario de scores
        scores = {}
        max_score = 0
        predicted_label = "NEU"
        
        for result in results:
            label = result['label']
            score = result['score']
            scores[label] = score
            
            if score > max_score:
                max_score = score
                predicted_label = label
        
        # Mapear etiquetas a formato estándar
        label_mapping = {
            "POS": "positivo",
            "NEG": "negativo", 
            "NEU": "neutral"
        }
        
        return {
            "sentiment": predicted_label,
            "confidence": max_score,
            "label": label_mapping.get(predicted_label, "neutral"),
            "scores": scores
        }
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocesa el texto para el análisis
        """
        if not text:
            return ""
        
        # Limpiar texto básico
        clean_text = text.strip()
        
        # Limitar longitud para evitar problemas con el modelo
        if len(clean_text) > 512:
            clean_text = clean_text[:512]
            logger.warning("Texto truncado a 512 caracteres")
        
        return clean_text
    
    def _fallback_analysis(self, text: str) -> Dict[str, any]:
        """
        Análisis de respaldo cuando BETO no está disponible
        """
        # Análisis básico por palabras clave
        positive_words = [
            "bueno", "excelente", "genial", "perfecto", "gracias", "bien", 
            "fantástico", "increíble", "maravilloso", "estupendo", "feliz",
            "contento", "satisfecho", "encantado", "amor", "gustar"
        ]
        
        negative_words = [
            "malo", "terrible", "horrible", "pésimo", "odio", "detesto",
            "molesto", "enojado", "furioso", "triste", "decepcionado",
            "frustrado", "problema", "error", "fallo", "disgusto"
        ]
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = "POS"
            label = "positivo"
            confidence = min(0.6 + (pos_count * 0.1), 0.9)
        elif neg_count > pos_count:
            sentiment = "NEG"
            label = "negativo"
            confidence = min(0.6 + (neg_count * 0.1), 0.9)
        else:
            sentiment = "NEU"
            label = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "label": label,
            "scores": {
                "POS": 0.6 if sentiment == "POS" else 0.2,
                "NEG": 0.6 if sentiment == "NEG" else 0.2,
                "NEU": 0.6 if sentiment == "NEU" else 0.2
            },
            "analysis_type": "fallback_keywords",
            "original_text": text
        }
    
    def get_model_info(self) -> Dict[str, any]:
        """
        Obtiene información sobre el modelo cargado
        """
        cuda_available = False
        if TORCH_AVAILABLE and torch:
            try:
                cuda_available = torch.cuda.is_available()
            except:
                cuda_available = False
        
        return {
            "model_name": self.model_name,
            "device": self.device,
            "available": self.analyzer is not None,
            "cuda_available": cuda_available,
            "transformers_available": TRANSFORMERS_AVAILABLE,
            "torch_available": TORCH_AVAILABLE
        }

# Instancia global del analizador
_sentiment_analyzer = None

def get_sentiment_analyzer() -> BetoSentimentAnalyzer:
    """
    Obtiene la instancia global del analizador de sentimientos
    """
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = BetoSentimentAnalyzer()
    return _sentiment_analyzer

def analyze_sentiment(text: str) -> Dict[str, any]:
    """
    Función de conveniencia para analizar sentimientos
    """
    analyzer = get_sentiment_analyzer()
    return analyzer.analyze_sentiment(text)

def get_sentiment_score(text: str) -> float:
    """
    Obtiene solo el score de sentimiento (para compatibilidad)
    """
    result = analyze_sentiment(text)
    
    # Convertir a score numérico (1-10)
    confidence = result.get('confidence', 0.5)
    sentiment = result.get('sentiment', 'NEU')
    
    if sentiment == 'POS':
        return 5 + (confidence * 5)  # 5-10 para positivo
    elif sentiment == 'NEG':
        return 5 - (confidence * 4)  # 1-5 para negativo
    else:
        return 5.0  # 5 para neutral

# Función de compatibilidad con el sistema anterior
def analizar_sentimiento_gemini(texto: str, api_key: Optional[str] = None) -> str:
    """
    Función de compatibilidad que mantiene la interfaz anterior
    pero usa BETO internamente
    """
    try:
        result = analyze_sentiment(texto)
        return result.get('label', 'neutral')
    except Exception as e:
        logger.error(f"Error en análisis de compatibilidad: {e}")
        return 'neutral'