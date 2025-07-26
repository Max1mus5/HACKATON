// Admin panel functionality
class AdminPanel {
    constructor() {
        this.searchTerm = '';
        this.activeTab = 'chats';
        this.stats = {
            totalUsers: 1247,
            totalChats: 3891,
            avgSentiment: 72,
            avgResponseTime: "2.3s"
        };
        
        this.topKeywords = [
            { word: "ayuda", count: 234, sentiment: "neutral" },
            { word: "problema", count: 189, sentiment: "sad" },
            { word: "gracias", count: 156, sentiment: "happy" },
            { word: "información", count: 143, sentiment: "neutral" },
            { word: "excelente", count: 98, sentiment: "happy" }
        ];
        
        this.recentChats = [
            { id: 1, user: "12345678", messages: 15, sentiment: "happy", timestamp: "2024-01-15 14:30", duration: "12 min" },
            { id: 2, user: "87654321", messages: 8, sentiment: "neutral", timestamp: "2024-01-15 14:25", duration: "6 min" },
            { id: 3, user: "11223344", messages: 22, sentiment: "sad", timestamp: "2024-01-15 14:20", duration: "18 min" },
            { id: 4, user: "44332211", messages: 5, sentiment: "happy", timestamp: "2024-01-15 14:15", duration: "4 min" }
        ];
        
        this.hourlyActivity = [20, 15, 10, 8, 12, 25, 35, 45, 60, 70, 65, 55, 50, 45, 40, 35, 30, 25, 20, 15, 12, 10, 8, 5];
        
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
        this.setupStats();
        this.setupTabs();
        this.setupSearch();
        this.setupChats();
        this.setupKeywords();
        this.setupAnalytics();
        this.setupButtons();
    }
    
    setupStats() {
        // Update stats display
        const totalUsersEl = document.getElementById('total-users');
        const totalChatsEl = document.getElementById('total-chats');
        const avgSentimentEl = document.getElementById('avg-sentiment');
        const avgResponseTimeEl = document.getElementById('avg-response-time');
        
        if (totalUsersEl) totalUsersEl.textContent = this.stats.totalUsers.toLocaleString();
        if (totalChatsEl) totalChatsEl.textContent = this.stats.totalChats.toLocaleString();
        if (avgSentimentEl) avgSentimentEl.textContent = `${this.stats.avgSentiment}%`;
        if (avgResponseTimeEl) avgResponseTimeEl.textContent = this.stats.avgResponseTime;
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
        const sentiments = [
            { label: 'Positivo', percentage: 65, type: 'positive' },
            { label: 'Neutral', percentage: 25, type: 'neutral' },
            { label: 'Negativo', percentage: 10, type: 'negative' }
        ];
        
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
