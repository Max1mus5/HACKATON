// Admin panel functionality
class AdminPanel {
    constructor() {
        this.searchTerm = '';
        this.activeTab = 'chats';
        this.allChats = [];
        this.allUsers = [];
        this.stats = {
            totalUsers: 0,
            totalChats: 0,
            avgSentiment: 0,
            avgResponseTime: "0s"
        };
        
        this.topKeywords = [];
        this.recentChats = [];
        this.hourlyActivity = new Array(24).fill(0);
        
        this.init();
    }
    
    async init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupElements());
        } else {
            await this.setupElements();
        }
    }
    
    async setupElements() {
        // Cargar datos del backend
        await this.loadBackendData();
        
        // Procesar datos
        this.processData();
        
        // Configurar UI
        this.setupStats();
        this.setupTabs();
        this.setupSearch();
        this.setupChats();
        this.setupKeywords();
        this.setupAnalytics();
        this.setupButtons();
    }
    
    async loadBackendData() {
        try {
            console.log('📊 Cargando datos del backend para admin...');
            
            // Cargar todos los chats con scores
            const chatsResponse = await fetch('https://hackaton-d1h6.onrender.com/admin/all-chats', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (chatsResponse.ok) {
                const data = await chatsResponse.json();
                this.allChats = data.chats || [];
                console.log(`✅ Cargados ${this.allChats.length} chats`);
            } else {
                console.warn('❌ No se pudieron cargar los chats');
                this.allChats = [];
            }
            
        } catch (error) {
            console.error('❌ Error al cargar datos del backend:', error);
            this.allChats = [];
        }
    }
    
    processData() {
        console.log('📊 Procesando datos para el panel de administración...');
        
        if (this.allChats.length === 0) {
            console.log('📊 No hay datos para procesar');
            return;
        }
        
        // Extraer usuarios únicos
        const uniqueUsers = new Set();
        let totalMessages = 0;
        let totalScore = 0;
        let scoreCount = 0;
        const wordCount = {};
        const hourlyStats = new Array(24).fill(0);
        const recentChatsData = [];
        
        this.allChats.forEach(chat => {
            uniqueUsers.add(chat.usuario_doc_id);
            
            // Procesar mensajes si existen
            if (chat.mensajes) {
                let messages = [];
                try {
                    if (typeof chat.mensajes === 'string') {
                        messages = JSON.parse(chat.mensajes);
                    } else if (Array.isArray(chat.mensajes)) {
                        messages = chat.mensajes;
                    }
                } catch (e) {
                    console.warn('Error parsing messages for chat:', chat.id);
                    return;
                }
                
                totalMessages += messages.length;
                
                // Procesar cada mensaje
                messages.forEach(message => {
                    // Procesar score
                    if (message.score) {
                        totalScore += parseFloat(message.score);
                        scoreCount++;
                    }
                    
                    // Procesar palabras clave del mensaje del usuario
                    if (message.message) {
                        this.extractKeywords(message.message, wordCount);
                    }
                    
                    // Procesar actividad por hora
                    if (message.timestamp) {
                        const hour = new Date(message.timestamp).getHours();
                        hourlyStats[hour]++;
                    }
                });
                
                // Crear datos para chats recientes
                if (messages.length > 0) {
                    const lastMessage = messages[messages.length - 1];
                    const sentiment = this.scoresToSentiment(messages.map(m => m.score || 5));
                    
                    recentChatsData.push({
                        id: chat.id,
                        user: chat.usuario_doc_id.toString(),
                        messages: messages.length,
                        sentiment: sentiment,
                        timestamp: lastMessage.timestamp || new Date().toISOString(),
                        duration: this.calculateChatDuration(messages)
                    });
                }
            }
        });
        
        // Actualizar estadísticas
        this.stats = {
            totalUsers: uniqueUsers.size,
            totalChats: this.allChats.length,
            avgSentiment: scoreCount > 0 ? Math.round((totalScore / scoreCount / 10) * 100) : 50,
            avgResponseTime: "2.3s" // Placeholder por ahora
        };
        
        // Procesar palabras clave más frecuentes
        this.topKeywords = this.getTopKeywords(wordCount, 5);
        
        // Normalizar actividad por hora
        const maxActivity = Math.max(...hourlyStats);
        this.hourlyActivity = hourlyStats.map(count => 
            maxActivity > 0 ? Math.round((count / maxActivity) * 100) : 0
        );
        
        // Ordenar chats recientes por timestamp
        this.recentChats = recentChatsData
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
            .slice(0, 10);
        
        console.log('✅ Datos procesados:', {
            users: this.stats.totalUsers,
            chats: this.stats.totalChats,
            avgSentiment: this.stats.avgSentiment,
            topKeywords: this.topKeywords.length,
            recentChats: this.recentChats.length
        });
    }
    
    extractKeywords(message, wordCount) {
        // Palabras comunes a ignorar
        const stopWords = new Set([
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'una', 'tiene', 'me', 'si', 'hay', 'o', 'ser', 'está', 'como', 'mi', 'sus', 'del', 'al', 'las', 'todo', 'pero', 'más', 'hace', 'muy', 'puede', 'sobre', 'años', 'estado', 'tan', 'porque', 'esta', 'cuando', 'él', 'también', 'antes', 'han', 'hasta', 'ahora', 'donde', 'quien', 'durante', 'siempre', 'todos', 'mismo', 'otro', 'entre'
        ]);
        
        const words = message.toLowerCase()
            .replace(/[^\w\sáéíóúñ]/g, ' ')
            .split(/\s+/)
            .filter(word => word.length > 3 && !stopWords.has(word));
        
        words.forEach(word => {
            wordCount[word] = (wordCount[word] || 0) + 1;
        });
    }
    
    getTopKeywords(wordCount, limit) {
        return Object.entries(wordCount)
            .sort(([,a], [,b]) => b - a)
            .slice(0, limit)
            .map(([word, count]) => ({
                word: word,
                count: count,
                sentiment: this.getWordSentiment(word)
            }));
    }
    
    getWordSentiment(word) {
        // Clasificación básica de sentimientos por palabra
        const positiveWords = ['gracias', 'excelente', 'perfecto', 'bueno', 'genial', 'fantástico', 'increíble', 'ayuda', 'útil'];
        const negativeWords = ['problema', 'error', 'mal', 'horrible', 'terrible', 'fallo', 'difícil'];
        
        if (positiveWords.includes(word)) return 'happy';
        if (negativeWords.includes(word)) return 'sad';
        return 'neutral';
    }
    
    scoresToSentiment(scores) {
        const validScores = scores.filter(s => s != null).map(s => parseFloat(s));
        if (validScores.length === 0) return 'neutral';
        
        const avgScore = validScores.reduce((sum, score) => sum + score, 0) / validScores.length;
        
        if (avgScore > 5) return 'happy';
        if (avgScore < 5) return 'sad';
        return 'neutral';
    }
    
    calculateChatDuration(messages) {
        if (messages.length < 2) return '1 min';
        
        const firstTimestamp = new Date(messages[0].timestamp || Date.now());
        const lastTimestamp = new Date(messages[messages.length - 1].timestamp || Date.now());
        
        const durationMs = lastTimestamp - firstTimestamp;
        const durationMin = Math.max(1, Math.round(durationMs / 60000));
        
        return `${durationMin} min`;
    }
    
    setupStats() {
        // Update stats display with real data
        const totalUsersEl = document.getElementById('total-users');
        const totalChatsEl = document.getElementById('total-chats');
        const avgSentimentEl = document.getElementById('avg-sentiment');
        const avgResponseTimeEl = document.getElementById('avg-response-time');
        
        if (totalUsersEl) totalUsersEl.textContent = this.stats.totalUsers.toLocaleString();
        if (totalChatsEl) totalChatsEl.textContent = this.stats.totalChats.toLocaleString();
        if (avgSentimentEl) avgSentimentEl.textContent = `${this.stats.avgSentiment}%`;
        if (avgResponseTimeEl) avgResponseTimeEl.textContent = this.stats.avgResponseTime;
        
        console.log('📊 Stats actualizadas:', this.stats);
    }
    
    setupTabs() {
        const tabTriggers = document.querySelectorAll('.tabs-trigger');
        const tabContents = document.querySelectorAll('.tabs-content');
        
        tabTriggers.forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                const targetTab = e.target.dataset.tab;
                this.switchTab(targetTab);
            });
        });
        
        // Set initial active tab
        this.switchTab(this.activeTab);
    }
    
    switchTab(tabName) {
        this.activeTab = tabName;
        
        // Update trigger states
        document.querySelectorAll('.tabs-trigger').forEach(trigger => {
            trigger.classList.remove('active');
            if (trigger.dataset.tab === tabName) {
                trigger.classList.add('active');
            }
        });
        
        // Update content visibility
        document.querySelectorAll('.tabs-content').forEach(content => {
            content.classList.remove('active');
            if (content.id === `tab-${tabName}`) {
                content.classList.add('active');
            }
        });
    }
    
    setupSearch() {
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchTerm = e.target.value.toLowerCase();
                this.filterChats();
            });
        }
    }
    
    setupChats() {
        const chatList = document.getElementById('chat-list');
        if (!chatList) return;
        
        chatList.innerHTML = '';
        
        this.recentChats.forEach(chat => {
            const chatItem = this.createChatItem(chat);
            chatList.appendChild(chatItem);
        });
    }
    
    createChatItem(chat) {
        const chatItem = document.createElement('div');
        chatItem.className = 'chat-item';
        chatItem.dataset.user = chat.user.toLowerCase();
        
        chatItem.innerHTML = `
            <div class="chat-info">
                <div class="chat-user">${chat.user}</div>
                <div class="badge badge-${chat.sentiment}">${chat.sentiment}</div>
                <div class="chat-details">
                    <div class="chat-detail-item">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z"/>
                        </svg>
                        <span>${chat.messages}</span>
                    </div>
                    <div class="chat-detail-item">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="10"/>
                            <polyline points="12,6 12,12 16,14"/>
                        </svg>
                        <span>${chat.duration}</span>
                    </div>
                    <div class="chat-detail-item">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                            <line x1="16" y1="2" x2="16" y2="6"/>
                            <line x1="8" y1="2" x2="8" y2="6"/>
                            <line x1="3" y1="10" x2="21" y2="10"/>
                        </svg>
                        <span>${chat.timestamp}</span>
                    </div>
                </div>
            </div>
            <button class="button button-sm" onclick="adminPanel.viewChatDetails('${chat.user}')">
                Ver Detalles
            </button>
        `;
        
        return chatItem;
    }
    
    filterChats() {
        const chatItems = document.querySelectorAll('.chat-item');
        chatItems.forEach(item => {
            const user = item.dataset.user;
            if (user.includes(this.searchTerm)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    }
    
    setupKeywords() {
        const keywordsGrid = document.getElementById('keywords-grid');
        if (!keywordsGrid) return;
        
        keywordsGrid.innerHTML = '';
        
        this.topKeywords.forEach(keyword => {
            const keywordItem = this.createKeywordItem(keyword);
            keywordsGrid.appendChild(keywordItem);
        });
    }
    
    createKeywordItem(keyword) {
        const keywordItem = document.createElement('div');
        keywordItem.className = 'keyword-item';
        
        keywordItem.innerHTML = `
            <div class="keyword-header">
                <span class="keyword-text">"${keyword.word}"</span>
                <div class="badge badge-${keyword.sentiment}">${keyword.sentiment}</div>
            </div>
            <div class="keyword-count">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="4" y1="9" x2="20" y2="9"/>
                    <line x1="4" y1="15" x2="20" y2="15"/>
                    <line x1="10" y1="3" x2="8" y2="21"/>
                    <line x1="16" y1="3" x2="14" y2="21"/>
                </svg>
                <span>${keyword.count} menciones</span>
            </div>
        `;
        
        return keywordItem;
    }
    
    setupAnalytics() {
        this.setupSentimentAnalysis();
        this.setupActivityChart();
    }
    
    setupSentimentAnalysis() {
        // Calcular sentimientos reales basados en los datos
        let positiveCount = 0;
        let neutralCount = 0;
        let negativeCount = 0;
        
        this.recentChats.forEach(chat => {
            switch(chat.sentiment) {
                case 'happy':
                    positiveCount++;
                    break;
                case 'sad':
                    negativeCount++;
                    break;
                default:
                    neutralCount++;
                    break;
            }
        });
        
        const total = this.recentChats.length || 1;
        const sentiments = [
            { 
                label: 'Positivo', 
                percentage: Math.round((positiveCount / total) * 100), 
                type: 'positive' 
            },
            { 
                label: 'Neutral', 
                percentage: Math.round((neutralCount / total) * 100), 
                type: 'neutral' 
            },
            { 
                label: 'Negativo', 
                percentage: Math.round((negativeCount / total) * 100), 
                type: 'negative' 
            }
        ];
        
        console.log('📊 Análisis de sentimientos:', sentiments);
        
        sentiments.forEach(sentiment => {
            const progressFill = document.getElementById(`progress-${sentiment.type}`);
            const percentageEl = document.getElementById(`percentage-${sentiment.type}`);
            
            if (progressFill) {
                setTimeout(() => {
                    progressFill.style.width = `${sentiment.percentage}%`;
                }, 300);
            }
            
            if (percentageEl) {
                percentageEl.textContent = `${sentiment.percentage}%`;
            }
        });
    }
    
    setupActivityChart() {
        const activityChart = document.getElementById('activity-chart');
        if (!activityChart) return;
        
        activityChart.innerHTML = '';
        
        this.hourlyActivity.forEach((height, index) => {
            const barContainer = document.createElement('div');
            barContainer.className = 'activity-bar';
            
            const bar = document.createElement('div');
            bar.className = 'activity-bar-fill';
            bar.style.height = `${height}%`;
            bar.title = `${index.toString().padStart(2, '0')}:00 - ${height}% actividad`;
            
            const hour = document.createElement('span');
            hour.className = 'activity-hour';
            hour.textContent = index.toString().padStart(2, '0');
            
            barContainer.appendChild(bar);
            barContainer.appendChild(hour);
            activityChart.appendChild(barContainer);
        });
    }
    
    setupButtons() {
        const exportButton = document.getElementById('export-data');
        const analysisButton = document.getElementById('deep-analysis');
        const filterButton = document.getElementById('filter-button');
        
        if (exportButton) {
            exportButton.addEventListener('click', () => this.exportData());
        }
        
        if (analysisButton) {
            analysisButton.addEventListener('click', () => this.openDeepAnalysis());
        }
        
        if (filterButton) {
            filterButton.addEventListener('click', () => this.toggleFilter());
        }
    }
    
    // Action methods
    viewChatDetails(userId) {
        // Redirect to chat detail page
        window.location.href = `chat-detail?userId=${userId}`;
    }
    
    exportData() {
        // Simulate data export
        const data = {
            stats: this.stats,
            chats: this.recentChats,
            keywords: this.topKeywords,
            timestamp: new Date().toISOString()
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `lean-admin-data-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showNotification('Datos exportados exitosamente', 'success');
    }
    
    openDeepAnalysis() {
        window.open('/insights', '_blank');
    }
    
    toggleFilter() {
        alert('Panel de filtros avanzados en desarrollo');
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : '#3b82f6'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            transform: translateX(100%);
            transition: transform 0.3s ease-in-out;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // Utility methods
    formatNumber(num) {
        return num.toLocaleString();
    }
    
    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    // Funciones utilitarias adicionales
    getSentimentClass(score) {
        if (score > 5) return 'positive';
        if (score < 5) return 'negative';
        return 'neutral';
    }
    
    getSentimentIcon(score) {
        if (score > 5) return '😊';
        if (score < 5) return '😞';
        return '😐';
    }
    
    getTimeAgo(timestamp) {
        const now = new Date();
        const time = new Date(timestamp);
        const diffInMs = now - time;
        const diffInMinutes = Math.floor(diffInMs / (1000 * 60));
        const diffInHours = Math.floor(diffInMinutes / 60);
        const diffInDays = Math.floor(diffInHours / 24);
        
        if (diffInDays > 0) return `hace ${diffInDays} día${diffInDays > 1 ? 's' : ''}`;
        if (diffInHours > 0) return `hace ${diffInHours} hora${diffInHours > 1 ? 's' : ''}`;
        if (diffInMinutes > 0) return `hace ${diffInMinutes} minuto${diffInMinutes > 1 ? 's' : ''}`;
        return 'hace un momento';
    }
    
    truncateMessage(message, maxLength = 80) {
        if (!message) return 'Sin mensaje';
        if (message.length <= maxLength) return message;
        return message.substring(0, maxLength) + '...';
    }
    
    // Función para ver detalles de chat específico
    viewChatDetails(userId) {
        console.log('🔍 Viendo detalles del usuario:', userId);
        // Esta función puede expandirse para mostrar un modal con detalles
        alert(`Mostrando detalles del chat para usuario: ${userId}`);
    }
    
    // Función para actualizar los datos periódicamente
    async refreshData() {
        console.log('🔄 Actualizando datos del panel de administración...');
        await this.loadBackendData();
    }
}

// Initialize admin panel
let adminPanel;

// Wait for DOM to be ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        adminPanel = new AdminPanel();
    });
} else {
    adminPanel = new AdminPanel();
}

// Export for potential use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdminPanel;
}

// Add to global scope for debugging
window.AdminPanel = AdminPanel;
