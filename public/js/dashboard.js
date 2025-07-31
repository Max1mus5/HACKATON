// ================================
// DASHBOARD FUNCTIONALITY
// ================================

class DashboardManager {
    constructor() {
        this.chatHistory = [];
        this.userData = null;
        this.sentimentData = {
            positive: 0,
            neutral: 0,
            negative: 0
        };
        this.totalMessages = 0;
        this.totalChatTime = 0;
        this.trendData = [];
        
        this.init();
    }
    
    async init() {
        // Verificar sesión
        const session = this.checkSession();
        if (!session) {
            window.location.href = './login';
            return;
        }
        
        // Cargar datos del usuario
        await this.loadUserData(session);
        
        // Procesar y mostrar datos
        this.processData();
        this.updateUI();
        this.setupEventListeners();
        this.addHoverEffects();
    }
    
    checkSession() {
        try {
            const session = localStorage.getItem('lean_session');
            return session ? JSON.parse(session) : null;
        } catch (error) {
            console.error('Error al verificar sesión:', error);
            return null;
        }
    }
    
    async loadUserData(session) {
        if (!session.doc_id) {
            console.warn('No se encontró doc_id en la sesión');
            return;
        }
        
        try {
            console.log(`📊 Cargando datos del dashboard para usuario: ${session.doc_id}`);
            
            const response = await fetch(`https://hackaton-d1h6.onrender.com/usuarios/${session.doc_id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }

            this.userData = await response.json();
            
            // Extraer mensajes del chat
            if (this.userData.chat && this.userData.chat.mensajes) {
                try {
                    if (typeof this.userData.chat.mensajes === 'string') {
                        this.chatHistory = JSON.parse(this.userData.chat.mensajes);
                    } else if (Array.isArray(this.userData.chat.mensajes)) {
                        this.chatHistory = this.userData.chat.mensajes;
                    }
                    
                    console.log(`✅ Datos cargados: ${this.chatHistory.length} mensajes encontrados`);
                } catch (parseError) {
                    console.error('Error al parsear mensajes:', parseError);
                    this.chatHistory = [];
                }
            } else {
                console.log('📊 No hay mensajes en el historial');
                this.chatHistory = [];
            }
            
        } catch (error) {
            console.error('❌ Error al cargar datos del usuario:', error);
            this.chatHistory = [];
        }
    }
    
    processData() {
        if (this.chatHistory.length === 0) {
            console.log('📊 No hay datos para procesar');
            return;
        }
        
        // Contadores básicos
        this.totalMessages = this.chatHistory.length;
        
        // Procesar sentimientos (score > 5 = positivo, = 5 = neutral, < 5 = negativo)
        let positiveCount = 0;
        let neutralCount = 0;
        let negativeCount = 0;
        
        // Agrupar por días para tendencias
        const dayGroups = {};
        
        this.chatHistory.forEach(message => {
            // Contar sentimientos
            const score = parseFloat(message.score) || 5;
            if (score > 5) {
                positiveCount++;
            } else if (score === 5) {
                neutralCount++;
            } else {
                negativeCount++;
            }
            
            // Agrupar por día para tendencias
            if (message.timestamp) {
                const date = new Date(message.timestamp);
                const dayKey = date.toISOString().split('T')[0]; // YYYY-MM-DD
                
                if (!dayGroups[dayKey]) {
                    dayGroups[dayKey] = {
                        scores: [],
                        count: 0
                    };
                }
                
                dayGroups[dayKey].scores.push(score);
                dayGroups[dayKey].count++;
            }
        });
        
        // Calcular porcentajes de sentimiento
        if (this.totalMessages > 0) {
            this.sentimentData = {
                positive: Math.round((positiveCount / this.totalMessages) * 100),
                neutral: Math.round((neutralCount / this.totalMessages) * 100),
                negative: Math.round((negativeCount / this.totalMessages) * 100)
            };
        }
        
        // Calcular tendencias por día (últimos 7 días)
        const sortedDays = Object.keys(dayGroups).sort();
        const last7Days = sortedDays.slice(-7);
        
        // Crear array con los últimos 7 días (incluyendo días sin datos)
        const today = new Date();
        this.trendData = [];
        this.dayLabels = [];
        
        for (let i = 6; i >= 0; i--) {
            const date = new Date(today);
            date.setDate(today.getDate() - i);
            const dayKey = date.toISOString().split('T')[0];
            
            // Obtener nombre del día
            const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
            this.dayLabels.push(dayNames[date.getDay()]);
            
            if (dayGroups[dayKey]) {
                const dayData = dayGroups[dayKey];
                const avgScore = dayData.scores.reduce((sum, score) => sum + score, 0) / dayData.scores.length;
                // Convertir score promedio a porcentaje (0-10 -> 0-100)
                this.trendData.push(Math.round((avgScore / 10) * 100));
            } else {
                // Día sin datos
                this.trendData.push(50); // Valor neutral
            }
        }
        
        console.log('📊 Datos procesados:', {
            totalMessages: this.totalMessages,
            sentimentData: this.sentimentData,
            trendData: this.trendData,
            daysWithData: last7Days.length
        });
    }
    
    updateUI() {
        // Actualizar información en el header
        this.updateHeader();
        
        // Actualizar sentimientos
        this.updateSentimentCards();
        
        // Actualizar gráfico de tendencias
        this.updateTrendChart();
        
        // Animar las actualizaciones
        this.animateProgressBars();
        this.animateChartBars();
    }
    
    updateHeader() {
        const subtitle = document.querySelector('.dashboard-subtitle');
        if (subtitle && this.totalMessages > 0) {
            subtitle.textContent = `${this.totalMessages} mensajes analizados • Datos actualizados`;
        }
    }
    
    updateSentimentCards() {
        // Actualizar porcentajes en las tarjetas
        const percentageElements = document.querySelectorAll('.percentage');
        const progressFills = document.querySelectorAll('.progress-fill');
        
        const values = [this.sentimentData.positive, this.sentimentData.neutral, this.sentimentData.negative];
        
        percentageElements.forEach((el, index) => {
            if (values[index] !== undefined) {
                el.textContent = `${values[index]}%`;
            }
        });
        
        progressFills.forEach((fill, index) => {
            if (values[index] !== undefined) {
                fill.setAttribute('data-value', values[index]);
            }
        });
    }
    
    updateTrendChart() {
        const chartBars = document.querySelectorAll('.chart-bar');
        
        chartBars.forEach((barContainer, index) => {
            if (this.trendData[index] !== undefined && this.dayLabels[index] !== undefined) {
                barContainer.setAttribute('data-height', this.trendData[index]);
                barContainer.setAttribute('data-day', this.dayLabels[index]);
                
                // Actualizar el contenido del día si existe
                const dayLabel = barContainer.querySelector('.day-label');
                if (dayLabel) {
                    dayLabel.textContent = this.dayLabels[index];
                }
            }
        });
    }
    
    // ================================
    // PROGRESS BARS ANIMATION
    // ================================
    animateProgressBars() {
        setTimeout(() => {
            const progressFills = document.querySelectorAll('.progress-fill');
            
            progressFills.forEach(fill => {
                const value = fill.getAttribute('data-value');
                fill.style.width = `${value}%`;
            });
        }, 500);
    }
    
    // ================================
    // CHART BARS ANIMATION
    // ================================
    animateChartBars() {
        const chartBars = document.querySelectorAll('.chart-bar');
        
        chartBars.forEach((barContainer, index) => {
            const bar = barContainer.querySelector('.bar');
            const height = barContainer.getAttribute('data-height');
            
            setTimeout(() => {
                bar.style.setProperty('--bar-height', `${height}%`);
                bar.style.height = `${height}%`;
            }, 800 + (index * 100));
        });
    }
    
    // ================================
    // EVENT LISTENERS
    // ================================
    setupEventListeners() {
        // Back button functionality
        const backButton = document.querySelector('.back-button');
        if (backButton) {
            backButton.addEventListener('click', () => {
                this.navigateToChat();
            });
        }
        
        // Chart bar hover effects
        const chartBars = document.querySelectorAll('.bar');
        chartBars.forEach(bar => {
            bar.addEventListener('mouseenter', (e) => {
                this.showChartTooltip(e, bar);
            });
            
            bar.addEventListener('mouseleave', () => {
                this.hideChartTooltip();
            });
        });
        
        // Chat item clicks
        const chatItems = document.querySelectorAll('.chat-item');
        chatItems.forEach(item => {
            item.addEventListener('click', () => {
                this.handleChatItemClick(item);
            });
        });
    }
    
    // ================================
    // NAVIGATION
    // ================================
    navigateToChat() {
        // Add loading state
        const backButton = document.querySelector('.back-button');
        const originalText = backButton.innerHTML;
        
        backButton.innerHTML = `
            <div class="loading"></div>
            Cargando...
        `;
        backButton.disabled = true;
        
        // Simulate navigation delay for smooth transition
        setTimeout(() => {
            window.location.href = 'chat';
        }, 300);
    }
    
    // ================================
    // CHART TOOLTIP
    // ================================
    showChartTooltip(event, bar) {
        const barContainer = bar.parentElement;
        const height = barContainer.getAttribute('data-height');
        const day = barContainer.getAttribute('data-day');
        
        // Remove existing tooltip
        this.hideChartTooltip();
        
        // Create tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'chart-tooltip';
        tooltip.innerHTML = `
            <div class="tooltip-content">
                <strong>${day}</strong><br>
                Sentimiento: ${height}%
            </div>
        `;
        
        // Position tooltip
        const rect = bar.getBoundingClientRect();
        tooltip.style.cssText = `
            position: fixed;
            top: ${rect.top - 60}px;
            left: ${rect.left + rect.width / 2 - 50}px;
            background: var(--crowshead);
            color: var(--dust-storm);
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid var(--taupe);
            font-size: 12px;
            z-index: 1000;
            text-align: center;
            box-shadow: var(--shadow-md);
            pointer-events: none;
            opacity: 0;
            transform: translateY(10px);
            transition: all 0.2s ease;
        `;
        
        document.body.appendChild(tooltip);
        
        // Animate in
        setTimeout(() => {
            tooltip.style.opacity = '1';
            tooltip.style.transform = 'translateY(0)';
        }, 10);
    }
    
    hideChartTooltip() {
        const existingTooltip = document.querySelector('.chart-tooltip');
        if (existingTooltip) {
            existingTooltip.style.opacity = '0';
            existingTooltip.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                existingTooltip.remove();
            }, 200);
        }
    }
    
    // ================================
    // CHAT ITEM INTERACTIONS
    // ================================
    handleChatItemClick(item) {
        // Add ripple effect
        this.createRippleEffect(item);
        
        // Get chat data
        const sentiment = item.getAttribute('data-sentiment');
        const date = item.querySelector('.chat-date').textContent;
        const messages = item.querySelector('.chat-messages').textContent;
        const duration = item.querySelector('.chat-duration').textContent;
        
        // Show chat details (could be expanded to show a modal)
        console.log('Chat clicked:', { sentiment, date, messages, duration });
        
        // Add visual feedback
        item.style.transform = 'scale(0.98)';
        setTimeout(() => {
            item.style.transform = '';
        }, 150);
    }
    
    // ================================
    // VISUAL EFFECTS
    // ================================
    createRippleEffect(element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = rect.width / 2;
        const y = rect.height / 2;
        
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 123, 0, 0.3);
            transform: scale(0);
            animation: ripple 0.6s linear;
            left: ${x - size / 2}px;
            top: ${y - size / 2}px;
            width: ${size}px;
            height: ${size}px;
            pointer-events: none;
        `;
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
    
    addHoverEffects() {
        // Add enhanced hover effects for cards
        const cards = document.querySelectorAll('.sentiment-card, .trend-card, .chats-card');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-4px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
        
        // Add glow effect to sentiment indicators
        const indicators = document.querySelectorAll('.sentiment-indicator');
        indicators.forEach(indicator => {
            indicator.addEventListener('mouseenter', () => {
                indicator.style.boxShadow = '0 0 15px currentColor';
                indicator.style.transform = 'scale(1.2)';
            });
            
            indicator.addEventListener('mouseleave', () => {
                indicator.style.boxShadow = '';
                indicator.style.transform = '';
            });
        });
    }
    
    // ================================
    // DATA UPDATES (Future enhancement)
    // ================================
    updateSentimentData(newData) {
        this.sentimentData = { ...this.sentimentData, ...newData };
        this.refreshProgressBars();
    }
    
    refreshProgressBars() {
        const progressFills = document.querySelectorAll('.progress-fill');
        const percentages = document.querySelectorAll('.percentage');
        
        progressFills.forEach((fill, index) => {
            const values = Object.values(this.sentimentData);
            fill.style.width = `${values[index]}%`;
        });
        
        percentages.forEach((percentage, index) => {
            const values = Object.values(this.sentimentData);
            percentage.textContent = `${values[index]}%`;
        });
    }
    
    // ================================
    // UTILITY METHODS
    // ================================
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }
    
    getSentimentColor(sentiment) {
        const colors = {
            happy: 'var(--color-positive)',
            neutral: 'var(--color-neutral)',
            sad: 'var(--color-negative)'
        };
        return colors[sentiment] || colors.neutral;
    }
    
    // ================================
    // KEYBOARD NAVIGATION
    // ================================
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.navigateToChat();
            }
            
            if (e.key === 'Enter' && e.target.classList.contains('chat-item')) {
                this.handleChatItemClick(e.target);
            }
        });
    }
}

// ================================
// CSS ANIMATIONS (Added via JavaScript)
// ================================
const additionalStyles = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .chart-tooltip {
        transition: all 0.2s ease;
    }
    
    .sentiment-card:hover .percentage {
        transform: scale(1.05);
        transition: transform 0.3s ease;
    }
    
    .bar:hover::after {
        content: '';
        position: absolute;
        top: -4px;
        left: -4px;
        right: -4px;
        bottom: -4px;
        background: linear-gradient(45deg, var(--orange), #e66a00);
        border-radius: 6px;
        z-index: -1;
        opacity: 0.3;
    }
`;

// ================================
// INITIALIZATION
// ================================
document.addEventListener('DOMContentLoaded', () => {
    // Add additional styles
    const styleSheet = document.createElement('style');
    styleSheet.textContent = additionalStyles;
    document.head.appendChild(styleSheet);
    
    // Initialize dashboard
    const dashboard = new DashboardManager();
    
    // Add keyboard navigation
    dashboard.setupKeyboardNavigation();
    
    // Add accessibility improvements
    addAccessibilityFeatures();
    
    // Add responsive behavior
    handleResponsiveFeatures();
});

// ================================
// ACCESSIBILITY FEATURES
// ================================
function addAccessibilityFeatures() {
    // Add ARIA labels
    const progressBars = document.querySelectorAll('.progress-fill');
    progressBars.forEach((bar, index) => {
        const value = bar.getAttribute('data-value');
        const types = ['positivo', 'neutral', 'negativo'];
        bar.setAttribute('aria-label', `Sentimiento ${types[index]}: ${value}%`);
        bar.setAttribute('role', 'progressbar');
        bar.setAttribute('aria-valuenow', value);
        bar.setAttribute('aria-valuemin', '0');
        bar.setAttribute('aria-valuemax', '100');
    });
    
    // Add keyboard focus indicators
    const focusableElements = document.querySelectorAll('.back-button, .chat-item, .bar');
    focusableElements.forEach(el => {
        el.setAttribute('tabindex', '0');
        
        el.addEventListener('focus', () => {
            el.style.outline = '2px solid var(--orange)';
            el.style.outlineOffset = '2px';
        });
        
        el.addEventListener('blur', () => {
            el.style.outline = '';
            el.style.outlineOffset = '';
        });
    });
}

// ================================
// RESPONSIVE FEATURES
// ================================
function handleResponsiveFeatures() {
    const mediaQuery = window.matchMedia('(max-width: 768px)');
    
    function handleMobileView(e) {
        const chartContainer = document.querySelector('.chart-container');
        const chatDetails = document.querySelectorAll('.chat-details');
        
        if (e.matches) {
            // Mobile view adjustments
            chartContainer.style.height = '200px';
            chatDetails.forEach(detail => {
                detail.style.flexDirection = 'column';
                detail.style.alignItems = 'flex-start';
            });
        } else {
            // Desktop view
            chartContainer.style.height = '256px';
            chatDetails.forEach(detail => {
                detail.style.flexDirection = 'row';
                detail.style.alignItems = 'center';
            });
        }
    }
    
    mediaQuery.addListener(handleMobileView);
    handleMobileView(mediaQuery);
}

// ================================
// ERROR HANDLING
// ================================
window.addEventListener('error', (e) => {
    console.error('Dashboard error:', e.error);
    
    // Show user-friendly error message
    const errorMessage = document.createElement('div');
    errorMessage.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--color-negative);
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        z-index: 10000;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    `;
    errorMessage.textContent = 'Ocurrió un error. Por favor, recarga la página.';
    
    document.body.appendChild(errorMessage);
    
    setTimeout(() => {
        errorMessage.style.opacity = '1';
        errorMessage.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        errorMessage.style.opacity = '0';
        errorMessage.style.transform = 'translateX(100%)';
        setTimeout(() => errorMessage.remove(), 300);
    }, 5000);
});

// ================================
// PERFORMANCE OPTIMIZATION
// ================================
// Debounce function for resize events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimized resize handler
window.addEventListener('resize', debounce(() => {
    // Recalculate chart dimensions
    const chartBars = document.querySelectorAll('.chart-bar');
    chartBars.forEach(bar => {
        const barElement = bar.querySelector('.bar');
        const height = bar.getAttribute('data-height');
        barElement.style.height = `${height}%`;
    });
}, 250));

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DashboardManager;
}
