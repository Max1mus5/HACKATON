"""
Servicio de análisis y estadísticas avanzadas de sentimientos
Proporciona métricas detalladas y análisis temporal de conversaciones
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, Counter
import statistics
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class SentimentMetrics:
    """Métricas de sentimiento para un período específico"""
    total_messages: int
    positive_count: int
    negative_count: int
    neutral_count: int
    average_confidence: float
    sentiment_trend: str
    dominant_sentiment: str
    confidence_distribution: Dict[str, int]
    temporal_pattern: List[Dict]

@dataclass
class ConversationAnalytics:
    """Análisis completo de una conversación"""
    conversation_id: str
    start_time: datetime
    end_time: datetime
    total_duration_minutes: float
    message_count: int
    sentiment_evolution: List[Dict]
    overall_sentiment: str
    sentiment_stability: float
    engagement_score: float
    key_moments: List[Dict]

class SentimentAnalytics:
    """
    Servicio de análisis avanzado de sentimientos y estadísticas
    """
    
    def __init__(self):
        self.sentiment_history = []
        self.conversation_cache = {}
    
    def add_sentiment_data(self, message_data: Dict):
        """
        Agrega datos de sentimiento al historial para análisis
        """
        timestamp = datetime.now()
        
        sentiment_entry = {
            "timestamp": timestamp.isoformat(),
            "message": message_data.get("message", ""),
            "sentiment": message_data.get("sentiment", "NEU"),
            "confidence": message_data.get("confidence", 0.5),
            "scores": message_data.get("scores", {}),
            "user_id": message_data.get("user_id", "unknown"),
            "conversation_id": message_data.get("conversation_id", "default")
        }
        
        self.sentiment_history.append(sentiment_entry)
        
        # Mantener solo los últimos 1000 registros para evitar uso excesivo de memoria
        if len(self.sentiment_history) > 1000:
            self.sentiment_history = self.sentiment_history[-1000:]
    
    def get_sentiment_metrics(self, 
                            hours_back: int = 24,
                            conversation_id: Optional[str] = None) -> SentimentMetrics:
        """
        Obtiene métricas de sentimiento para un período específico
        """
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        # Filtrar datos relevantes
        relevant_data = []
        for entry in self.sentiment_history:
            entry_time = datetime.fromisoformat(entry["timestamp"])
            if entry_time >= cutoff_time:
                if conversation_id is None or entry.get("conversation_id") == conversation_id:
                    relevant_data.append(entry)
        
        if not relevant_data:
            return self._empty_metrics()
        
        # Calcular métricas básicas
        total_messages = len(relevant_data)
        sentiments = [entry["sentiment"] for entry in relevant_data]
        confidences = [entry["confidence"] for entry in relevant_data]
        
        sentiment_counts = Counter(sentiments)
        positive_count = sentiment_counts.get("POS", 0)
        negative_count = sentiment_counts.get("NEG", 0)
        neutral_count = sentiment_counts.get("NEU", 0)
        
        # Calcular métricas avanzadas
        average_confidence = statistics.mean(confidences) if confidences else 0.0
        dominant_sentiment = sentiment_counts.most_common(1)[0][0] if sentiment_counts else "NEU"
        
        # Análisis de tendencia
        sentiment_trend = self._calculate_trend(relevant_data)
        
        # Distribución de confianza
        confidence_distribution = self._calculate_confidence_distribution(confidences)
        
        # Patrón temporal
        temporal_pattern = self._calculate_temporal_pattern(relevant_data)
        
        return SentimentMetrics(
            total_messages=total_messages,
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count,
            average_confidence=average_confidence,
            sentiment_trend=sentiment_trend,
            dominant_sentiment=dominant_sentiment,
            confidence_distribution=confidence_distribution,
            temporal_pattern=temporal_pattern
        )
    
    def analyze_conversation(self, conversation_id: str) -> ConversationAnalytics:
        """
        Analiza una conversación específica en detalle
        """
        # Filtrar datos de la conversación
        conversation_data = [
            entry for entry in self.sentiment_history 
            if entry.get("conversation_id") == conversation_id
        ]
        
        if not conversation_data:
            return self._empty_conversation_analytics(conversation_id)
        
        # Ordenar por timestamp
        conversation_data.sort(key=lambda x: x["timestamp"])
        
        # Calcular métricas básicas
        start_time = datetime.fromisoformat(conversation_data[0]["timestamp"])
        end_time = datetime.fromisoformat(conversation_data[-1]["timestamp"])
        duration = (end_time - start_time).total_seconds() / 60  # en minutos
        
        # Evolución del sentimiento
        sentiment_evolution = self._calculate_sentiment_evolution(conversation_data)
        
        # Sentimiento general
        overall_sentiment = self._calculate_overall_sentiment(conversation_data)
        
        # Estabilidad del sentimiento
        sentiment_stability = self._calculate_sentiment_stability(conversation_data)
        
        # Score de engagement
        engagement_score = self._calculate_engagement_score(conversation_data, duration)
        
        # Momentos clave
        key_moments = self._identify_key_moments(conversation_data)
        
        return ConversationAnalytics(
            conversation_id=conversation_id,
            start_time=start_time,
            end_time=end_time,
            total_duration_minutes=duration,
            message_count=len(conversation_data),
            sentiment_evolution=sentiment_evolution,
            overall_sentiment=overall_sentiment,
            sentiment_stability=sentiment_stability,
            engagement_score=engagement_score,
            key_moments=key_moments
        )
    
    def get_dashboard_data(self) -> Dict:
        """
        Obtiene datos para el dashboard de análisis
        """
        # Métricas de las últimas 24 horas
        metrics_24h = self.get_sentiment_metrics(hours_back=24)
        
        # Métricas de la última semana
        metrics_week = self.get_sentiment_metrics(hours_back=168)  # 7 días
        
        # Conversaciones activas
        active_conversations = self._get_active_conversations()
        
        # Tendencias por hora
        hourly_trends = self._calculate_hourly_trends()
        
        # Palabras clave por sentimiento
        sentiment_keywords = self._extract_sentiment_keywords()
        
        return {
            "metrics_24h": asdict(metrics_24h),
            "metrics_week": asdict(metrics_week),
            "active_conversations": active_conversations,
            "hourly_trends": hourly_trends,
            "sentiment_keywords": sentiment_keywords,
            "total_conversations": len(set(entry.get("conversation_id", "default") 
                                         for entry in self.sentiment_history)),
            "last_updated": datetime.now().isoformat()
        }
    
    def _calculate_trend(self, data: List[Dict]) -> str:
        """Calcula la tendencia del sentimiento"""
        if len(data) < 2:
            return "stable"
        
        # Dividir en dos mitades y comparar
        mid_point = len(data) // 2
        first_half = data[:mid_point]
        second_half = data[mid_point:]
        
        def sentiment_score(entries):
            scores = []
            for entry in entries:
                if entry["sentiment"] == "POS":
                    scores.append(1)
                elif entry["sentiment"] == "NEG":
                    scores.append(-1)
                else:
                    scores.append(0)
            return statistics.mean(scores) if scores else 0
        
        first_score = sentiment_score(first_half)
        second_score = sentiment_score(second_half)
        
        diff = second_score - first_score
        
        if diff > 0.2:
            return "improving"
        elif diff < -0.2:
            return "declining"
        else:
            return "stable"
    
    def _calculate_confidence_distribution(self, confidences: List[float]) -> Dict[str, int]:
        """Calcula la distribución de confianza"""
        distribution = {"low": 0, "medium": 0, "high": 0}
        
        for conf in confidences:
            if conf < 0.6:
                distribution["low"] += 1
            elif conf < 0.8:
                distribution["medium"] += 1
            else:
                distribution["high"] += 1
        
        return distribution
    
    def _calculate_temporal_pattern(self, data: List[Dict]) -> List[Dict]:
        """Calcula patrones temporales por hora"""
        hourly_data = defaultdict(list)
        
        for entry in data:
            timestamp = datetime.fromisoformat(entry["timestamp"])
            hour = timestamp.hour
            hourly_data[hour].append(entry)
        
        pattern = []
        for hour in range(24):
            hour_entries = hourly_data.get(hour, [])
            if hour_entries:
                sentiments = [e["sentiment"] for e in hour_entries]
                sentiment_counts = Counter(sentiments)
                dominant = sentiment_counts.most_common(1)[0][0]
                count = len(hour_entries)
            else:
                dominant = "NEU"
                count = 0
            
            pattern.append({
                "hour": hour,
                "message_count": count,
                "dominant_sentiment": dominant
            })
        
        return pattern
    
    def _calculate_sentiment_evolution(self, data: List[Dict]) -> List[Dict]:
        """Calcula la evolución del sentimiento a lo largo de la conversación"""
        evolution = []
        
        for i, entry in enumerate(data):
            evolution.append({
                "message_index": i + 1,
                "timestamp": entry["timestamp"],
                "sentiment": entry["sentiment"],
                "confidence": entry["confidence"],
                "message_preview": entry["message"][:50] + "..." if len(entry["message"]) > 50 else entry["message"]
            })
        
        return evolution
    
    def _calculate_overall_sentiment(self, data: List[Dict]) -> str:
        """Calcula el sentimiento general de la conversación"""
        sentiments = [entry["sentiment"] for entry in data]
        confidences = [entry["confidence"] for entry in data]
        
        # Ponderar por confianza
        weighted_scores = []
        for sentiment, confidence in zip(sentiments, confidences):
            if sentiment == "POS":
                weighted_scores.append(confidence)
            elif sentiment == "NEG":
                weighted_scores.append(-confidence)
            else:
                weighted_scores.append(0)
        
        if not weighted_scores:
            return "neutral"
        
        avg_score = statistics.mean(weighted_scores)
        
        if avg_score > 0.1:
            return "positive"
        elif avg_score < -0.1:
            return "negative"
        else:
            return "neutral"
    
    def _calculate_sentiment_stability(self, data: List[Dict]) -> float:
        """Calcula la estabilidad del sentimiento (0-1)"""
        if len(data) < 2:
            return 1.0
        
        # Calcular varianza de los scores de sentimiento
        scores = []
        for entry in data:
            if entry["sentiment"] == "POS":
                scores.append(1)
            elif entry["sentiment"] == "NEG":
                scores.append(-1)
            else:
                scores.append(0)
        
        if len(set(scores)) == 1:
            return 1.0  # Completamente estable
        
        variance = statistics.variance(scores)
        # Normalizar la varianza a un score de estabilidad (0-1)
        stability = max(0, 1 - (variance / 2))
        
        return stability
    
    def _calculate_engagement_score(self, data: List[Dict], duration_minutes: float) -> float:
        """Calcula un score de engagement basado en varios factores"""
        if not data or duration_minutes <= 0:
            return 0.0
        
        # Factores del engagement
        message_frequency = len(data) / max(duration_minutes, 1)  # mensajes por minuto
        avg_confidence = statistics.mean([entry["confidence"] for entry in data])
        sentiment_variety = len(set(entry["sentiment"] for entry in data))
        
        # Normalizar y combinar factores
        frequency_score = min(message_frequency / 2, 1.0)  # máximo 2 mensajes/minuto = 1.0
        confidence_score = avg_confidence
        variety_score = sentiment_variety / 3.0  # máximo 3 sentimientos diferentes = 1.0
        
        engagement = (frequency_score + confidence_score + variety_score) / 3
        
        return min(engagement, 1.0)
    
    def _identify_key_moments(self, data: List[Dict]) -> List[Dict]:
        """Identifica momentos clave en la conversación"""
        key_moments = []
        
        for i, entry in enumerate(data):
            # Momento de alta confianza
            if entry["confidence"] > 0.9:
                key_moments.append({
                    "type": "high_confidence",
                    "timestamp": entry["timestamp"],
                    "message": entry["message"][:100],
                    "sentiment": entry["sentiment"],
                    "confidence": entry["confidence"]
                })
            
            # Cambio drástico de sentimiento
            if i > 0:
                prev_sentiment = data[i-1]["sentiment"]
                curr_sentiment = entry["sentiment"]
                
                if ((prev_sentiment == "POS" and curr_sentiment == "NEG") or 
                    (prev_sentiment == "NEG" and curr_sentiment == "POS")):
                    key_moments.append({
                        "type": "sentiment_shift",
                        "timestamp": entry["timestamp"],
                        "message": entry["message"][:100],
                        "from_sentiment": prev_sentiment,
                        "to_sentiment": curr_sentiment
                    })
        
        return key_moments[:10]  # Limitar a 10 momentos clave
    
    def _get_active_conversations(self) -> List[Dict]:
        """Obtiene conversaciones activas en las últimas 24 horas"""
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        conversation_data = defaultdict(list)
        
        for entry in self.sentiment_history:
            entry_time = datetime.fromisoformat(entry["timestamp"])
            if entry_time >= cutoff_time:
                conv_id = entry.get("conversation_id", "default")
                conversation_data[conv_id].append(entry)
        
        active_conversations = []
        for conv_id, entries in conversation_data.items():
            if entries:
                last_activity = max(datetime.fromisoformat(e["timestamp"]) for e in entries)
                sentiment_counts = Counter(e["sentiment"] for e in entries)
                
                active_conversations.append({
                    "conversation_id": conv_id,
                    "message_count": len(entries),
                    "last_activity": last_activity.isoformat(),
                    "dominant_sentiment": sentiment_counts.most_common(1)[0][0],
                    "user_id": entries[0].get("user_id", "unknown")
                })
        
        return sorted(active_conversations, key=lambda x: x["last_activity"], reverse=True)
    
    def _calculate_hourly_trends(self) -> List[Dict]:
        """Calcula tendencias por hora del día"""
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        hourly_data = defaultdict(list)
        
        for entry in self.sentiment_history:
            entry_time = datetime.fromisoformat(entry["timestamp"])
            if entry_time >= cutoff_time:
                hour = entry_time.hour
                hourly_data[hour].append(entry)
        
        trends = []
        for hour in range(24):
            entries = hourly_data.get(hour, [])
            if entries:
                sentiments = [e["sentiment"] for e in entries]
                sentiment_counts = Counter(sentiments)
                avg_confidence = statistics.mean([e["confidence"] for e in entries])
                
                trends.append({
                    "hour": hour,
                    "message_count": len(entries),
                    "positive_count": sentiment_counts.get("POS", 0),
                    "negative_count": sentiment_counts.get("NEG", 0),
                    "neutral_count": sentiment_counts.get("NEU", 0),
                    "average_confidence": avg_confidence
                })
            else:
                trends.append({
                    "hour": hour,
                    "message_count": 0,
                    "positive_count": 0,
                    "negative_count": 0,
                    "neutral_count": 0,
                    "average_confidence": 0.0
                })
        
        return trends
    
    def _extract_sentiment_keywords(self) -> Dict[str, List[str]]:
        """Extrae palabras clave por sentimiento"""
        sentiment_words = defaultdict(list)
        
        for entry in self.sentiment_history[-100:]:  # Últimos 100 mensajes
            words = entry["message"].lower().split()
            sentiment = entry["sentiment"]
            
            # Filtrar palabras comunes y cortas
            filtered_words = [
                word for word in words 
                if len(word) > 3 and word not in ["para", "este", "esta", "como", "pero", "solo", "muy"]
            ]
            
            sentiment_words[sentiment].extend(filtered_words)
        
        # Obtener las palabras más comunes por sentimiento
        result = {}
        for sentiment, words in sentiment_words.items():
            if words:
                word_counts = Counter(words)
                result[sentiment] = [word for word, count in word_counts.most_common(10)]
            else:
                result[sentiment] = []
        
        return result
    
    def _empty_metrics(self) -> SentimentMetrics:
        """Retorna métricas vacías"""
        return SentimentMetrics(
            total_messages=0,
            positive_count=0,
            negative_count=0,
            neutral_count=0,
            average_confidence=0.0,
            sentiment_trend="stable",
            dominant_sentiment="NEU",
            confidence_distribution={"low": 0, "medium": 0, "high": 0},
            temporal_pattern=[]
        )
    
    def _empty_conversation_analytics(self, conversation_id: str) -> ConversationAnalytics:
        """Retorna análisis de conversación vacío"""
        now = datetime.now()
        return ConversationAnalytics(
            conversation_id=conversation_id,
            start_time=now,
            end_time=now,
            total_duration_minutes=0.0,
            message_count=0,
            sentiment_evolution=[],
            overall_sentiment="neutral",
            sentiment_stability=1.0,
            engagement_score=0.0,
            key_moments=[]
        )

# Instancia global del servicio de analytics
_analytics_service = None

def get_analytics_service() -> SentimentAnalytics:
    """Obtiene la instancia global del servicio de analytics"""
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = SentimentAnalytics()
    return _analytics_service