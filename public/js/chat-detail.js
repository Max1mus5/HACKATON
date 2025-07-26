class ChatDetailManager {
    constructor() {
        this.chatData = {
            id: "1",
            user: {
                documento: "12345678",
                id: "user_uuid_123"
            },
            startTime: "2024-01-15T09:30:00Z",
            endTime: "2024-01-15T09:42:00Z",
            duration: "12 min",
            totalMessages: 15,
            avgSentiment: {
                score: 0.72,
                label: "happy"
            },
            status: "completed",
            messages: [
                {
                    id: "msg_1",
                    text: "Hola, necesito ayuda con mi cuenta",
                    sender: "user",
                    timestamp: "2024-01-15T09:30:00Z",
                    sentiment: { score: 0.2, label: "neutral", confidence: 0.85 },
                    keywords: ["ayuda", "cuenta"]
                },
                {
                    id: "msg_2",
                    text: "¡Hola! Estaré encantado de ayudarte con tu cuenta. ¿Podrías ser más específico sobre el problema que estás experimentando?",
                    sender: "bot",
                    timestamp: "2024-01-15T09:30:05Z",
                    sentiment: { score: 0.8, label: "happy", confidence: 0.92 },
                    keywords: ["ayuda", "problema"]
                },
                {
                    id: "msg_3",
                    text: "No puedo acceder a mi perfil, me dice que hay un error",
                    sender: "user",
                    timestamp: "2024-01-15T09:30:30Z",
                    sentiment: { score: -0.3, label: "sad", confidence: 0.78 },
                    keywords: ["acceder", "perfil", "error"]
                },
                {
                    id: "msg_4",
                    text: "Entiendo tu frustración. Vamos a resolver este problema paso a paso. Primero, ¿podrías intentar cerrar sesión y volver a iniciar sesión?",
                    sender: "bot",
                    timestamp: "2024-01-15T09:30:45Z",
                    sentiment: { score: 0.6, label: "happy", confidence: 0.88 },
                    keywords: ["resolver", "problema", "sesión"]
                },
                {
                    id: "msg_5",
                    text: "Ya lo intenté varias veces y sigue igual",
                    sender: "user",
                    timestamp: "2024-01-15T09:31:15Z",
                    sentiment: { score: -0.4, label: "sad", confidence: 0.82 },
                    keywords: ["intenté", "veces"]
                },
                {
                    id: "msg_6",
                    text: "Perfecto, gracias por intentarlo. Ahora voy a verificar tu cuenta desde mi sistema. Dame un momento por favor.",
                    sender: "bot",
                    timestamp: "2024-01-15T09:31:30Z",
                    sentiment: { score: 0.7, label: "happy", confidence: 0.9 },
                    keywords: ["verificar", "cuenta", "sistema"]
                },
                {
                    id: "msg_7",
                    text: "Está bien, espero",
                    sender: "user",
                    timestamp: "2024-01-15T09:32:00Z",
                    sentiment: { score: 0.1, label: "neutral", confidence: 0.75 },
                    keywords: ["espero"]
                },
                {
                    id: "msg_8",
                    text: "He encontrado el problema. Había una actualización pendiente en tu perfil que estaba causando el error. Ya lo he solucionado. ¿Podrías intentar acceder nuevamente?",
                    sender: "bot",
                    timestamp: "2024-01-15T09:33:00Z",
                    sentiment: { score: 0.9, label: "happy", confidence: 0.95 },
                    keywords: ["encontrado", "problema", "solucionado", "acceder"]
                },
                {
                    id: "msg_9",
                    text: "¡Perfecto! Ya puedo acceder sin problemas",
                    sender: "user",
                    timestamp: "2024-01-15T09:33:30Z",
                    sentiment: { score: 0.9, label: "happy", confidence: 0.93 },
                    keywords: ["perfecto", "acceder", "problemas"]
                },
                {
                    id: "msg_10",
                    text: "¡Excelente! Me alegra saber que ya está funcionando correctamente. ¿Hay algo más en lo que pueda ayudarte hoy?",
                    sender: "bot",
                    timestamp: "2024-01-15T09:33:45Z",
                    sentiment: { score: 0.95, label: "happy", confidence: 0.97 },
                    keywords: ["excelente", "funcionando", "ayudarte"]
                },
                {
                    id: "msg_11",
                    text: "No, eso era todo. Muchas gracias por la ayuda",
                    sender: "user",
                    timestamp: "2024-01-15T09:34:00Z",
                    sentiment: { score: 0.85, label: "happy", confidence: 0.91 },
                    keywords: ["gracias", "ayuda"]
                },
                {
                    id: "msg_12",
                    text: "¡De nada! Ha sido un placer ayudarte. Si tienes alguna otra consulta en el futuro, no dudes en contactarnos. ¡Que tengas un excelente día!",
                    sender: "bot",
                    timestamp: "2024-01-15T09:34:15Z",
                    sentiment: { score: 0.98, label: "happy", confidence: 0.98 },
                    keywords: ["placer", "ayudarte", "consulta", "excelente"]
                }
            ],
            keywords: [
                { word: "ayuda", count: 4, sentiment: "neutral" },
                { word: "problema", count: 3, sentiment: "sad" },
                { word: "cuenta", count: 2, sentiment: "neutral" },
                { word: "acceder", count: 3, sentiment: "neutral" },
                { word: "excelente", count: 2, sentiment: "happy" },
                { word: "gracias", count: 2, sentiment: "happy" }
            ],
            sentimentEvolution: [
                { messageIndex: 0, sentiment: 0.2 },
                { messageIndex: 1, sentiment: 0.8 },
                { messageIndex: 2, sentiment: -0.3 },
                { messageIndex: 3, sentiment: 0.6 },
                { messageIndex: 4, sentiment: -0.4 },
                { messageIndex: 5, sentiment: 0.7 },
                { messageIndex: 6, sentiment: 0.1 },
                { messageIndex: 7, sentiment: 0.9 },
                { messageIndex: 8, sentiment: 0.9 },
                { messageIndex: 9, sentiment: 0.95 },
                { messageIndex: 10, sentiment: 0.85 },
                { messageIndex: 11, sentiment: 0.98 }
            ]
        };
        
        this.init();
    }
    
    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupElements());
        } else {
            this.setupElements();
        }
    }
    
    setupElements() {
        this.setupButtons();
        this.renderMessages();
        this.renderSentimentChart();
        this.renderKeywords();
        this.setupScrollBehavior();
    }
    
    setupButtons() {
        const backButton = document.getElementById('back-button');
        const exportButton = document.getElementById('export-button');
        
        if (backButton) {
            backButton.addEventListener('click', () => {
                window.location.href = 'admin.html';
            });
        }
        
        if (exportButton) {
            exportButton.addEventListener('click', () => {
                this.exportChat();
            });
        }
    }
    
    renderMessages() {
        const timeline = document.getElementById('messages-timeline');
        if (!timeline) return;
        
        timeline.innerHTML = '';
        
        this.chatData.messages.forEach((message, index) => {
            const messageElement = this.createMessageElement(message, index);
            timeline.appendChild(messageElement);
        });
    }
    
    createMessageElement(message, index) {
        const messageItem = document.createElement('div');
        messageItem.className = 'message-item';
        
        const avatar = this.createAvatar(message.sender);
        const content = this.createMessageContent(message, index);
        
        messageItem.appendChild(avatar);
        messageItem.appendChild(content);
        
        return messageItem;
    }
    
    createAvatar(sender) {
        const avatar = document.createElement('div');
        avatar.className = `message-avatar ${sender}`;
        
        const icon = sender === 'user' 
            ? `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                 <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                 <circle cx="12" cy="7" r="4"/>
               </svg>`
            : `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                 <rect width="18" height="10" x="3" y="11" rx="2"/>
                 <circle cx="12" cy="5" r="2"/>
                 <path d="m12 7 2 3H8l2-3"/>
                 <path d="M8 21V7a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v14"/>
               </svg>`;
        
        avatar.innerHTML = icon;
        return avatar;
    }
    
    createMessageContent(message, index) {
        const content = document.createElement('div');
        content.className = 'message-content';
        
        // Header
        const header = document.createElement('div');
        header.className = 'message-header';
        
        const sender = document.createElement('span');
        sender.className = 'message-sender';
        sender.textContent = message.sender === 'user' ? 'Usuario' : 'LEAN Bot';
        
        const time = document.createElement('span');
        time.className = 'message-time';
        time.textContent = this.formatTime(message.timestamp);
        
        const sentiment = this.createSentimentInfo(message.sentiment);
        
        header.appendChild(sender);
        header.appendChild(time);
        header.appendChild(sentiment);
        
        // Bubble
        const bubble = document.createElement('div');
        bubble.className = `message-bubble ${message.sender}`;
        
        const text = document.createElement('p');
        text.className = 'message-text';
        text.textContent = message.text;
        
        bubble.appendChild(text);
        
        // Keywords
        const keywords = this.createKeywordTags(message.keywords);
        
        content.appendChild(header);
        content.appendChild(bubble);
        content.appendChild(keywords);
        
        return content;
    }
    
    createSentimentInfo(sentiment) {
        const container = document.createElement('div');
        container.className = 'message-sentiment';
        
        const icon = document.createElement('div');
        icon.className = `sentiment-icon ${sentiment.label}`;
        
        const iconSvg = this.getSentimentIcon(sentiment.label);
        icon.innerHTML = iconSvg;
        
        const confidence = document.createElement('span');
        confidence.className = 'confidence-score';
        confidence.textContent = `${(sentiment.confidence * 100).toFixed(0)}%`;
        
        container.appendChild(icon);
        container.appendChild(confidence);
        
        return container;
    }
    
    getSentimentIcon(sentiment) {
        switch (sentiment) {
            case 'happy':
                return `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"/>
                          <path d="m9 9 1.5 1.5L12 9"/>
                          <path d="m15 9-1.5 1.5L12 9"/>
                          <path d="m9 15 3-3 3 3"/>
                        </svg>`;
            case 'neutral':
                return `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"/>
                          <line x1="8" y1="15" x2="16" y2="15"/>
                          <line x1="9" y1="9" x2="9.01" y2="9"/>
                          <line x1="15" y1="9" x2="15.01" y2="9"/>
                        </svg>`;
            case 'sad':
                return `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"/>
                          <path d="m16 16-4-4-4 4"/>
                          <line x1="9" y1="9" x2="9.01" y2="9"/>
                          <line x1="15" y1="9" x2="15.01" y2="9"/>
                        </svg>`;
            default:
                return `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"/>
                          <line x1="8" y1="15" x2="16" y2="15"/>
                          <line x1="9" y1="9" x2="9.01" y2="9"/>
                          <line x1="15" y1="9" x2="15.01" y2="9"/>
                        </svg>`;
        }
    }
    
    createKeywordTags(keywords) {
        const container = document.createElement('div');
        container.className = 'message-keywords';
        
        keywords.forEach(keyword => {
            const tag = document.createElement('span');
            tag.className = 'keyword-tag';
            tag.textContent = keyword;
            container.appendChild(tag);
        });
        
        return container;
    }
    
    renderSentimentChart() {
        const chart = document.getElementById('sentiment-chart');
        if (!chart) return;
        
        chart.innerHTML = '';
        
        this.chatData.sentimentEvolution.forEach((point, index) => {
            const barContainer = document.createElement('div');
            barContainer.className = 'sentiment-bar';
            
            const bar = document.createElement('div');
            bar.className = `bar-fill ${point.sentiment >= 0 ? 'positive' : 'negative'}`;
            
            const height = Math.abs(point.sentiment) * 80; // Max height 80px
            bar.style.height = `${Math.max(height, 4)}px`;
            bar.title = `Mensaje ${index + 1}: ${point.sentiment.toFixed(2)}`;
            
            const number = document.createElement('span');
            number.className = 'bar-number';
            number.textContent = index + 1;
            
            barContainer.appendChild(bar);
            barContainer.appendChild(number);
            chart.appendChild(barContainer);
        });
    }
    
    renderKeywords() {
        const keywordsList = document.getElementById('keywords-list');
        if (!keywordsList) return;
        
        keywordsList.innerHTML = '';
        
        this.chatData.keywords.forEach(keyword => {
            const item = document.createElement('div');
            item.className = 'keyword-item';
            
            const info = document.createElement('div');
            info.className = 'keyword-info';
            
            const word = document.createElement('span');
            word.className = 'keyword-word';
            word.textContent = `"${keyword.word}"`;
            
            const sentiment = document.createElement('span');
            sentiment.className = `keyword-sentiment status-badge badge-${keyword.sentiment}`;
            sentiment.textContent = keyword.sentiment;
            
            const count = document.createElement('span');
            count.className = 'keyword-count';
            count.textContent = keyword.count;
            
            info.appendChild(word);
            info.appendChild(sentiment);
            item.appendChild(info);
            item.appendChild(count);
            
            keywordsList.appendChild(item);
        });
    }
    
    setupScrollBehavior() {
        const timeline = document.getElementById('messages-timeline');
        if (timeline) {
            // Smooth scroll to bottom
            timeline.scrollTop = timeline.scrollHeight;
        }
        
        // Add hover effects to sentiment bars
        const bars = document.querySelectorAll('.sentiment-bar');
        bars.forEach(bar => {
            bar.addEventListener('mouseenter', () => {
                bar.style.transform = 'scale(1.1)';
            });
            
            bar.addEventListener('mouseleave', () => {
                bar.style.transform = 'scale(1)';
            });
        });
    }
    
    formatTime(timestamp) {
        return new Date(timestamp).toLocaleTimeString('es-ES', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }
    
    formatDate(timestamp) {
        return new Date(timestamp).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
    
    exportChat() {
        // Simulate chat export
        const data = {
            chatId: this.chatData.id,
            user: this.chatData.user,
            startTime: this.chatData.startTime,
            endTime: this.chatData.endTime,
            duration: this.chatData.duration,
            totalMessages: this.chatData.totalMessages,
            avgSentiment: this.chatData.avgSentiment,
            status: this.chatData.status,
            messages: this.chatData.messages,
            keywords: this.chatData.keywords,
            sentimentEvolution: this.chatData.sentimentEvolution,
            exportedAt: new Date().toISOString()
        };
        
        // Create download link
        const dataStr = JSON.stringify(data, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `chat-${this.chatData.id}-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        // Show success message
        this.showNotification('Chat exportado exitosamente', 'success');
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--success-color);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
            z-index: 1000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
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
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// Initialize when DOM is ready
const chatDetailManager = new ChatDetailManager();
