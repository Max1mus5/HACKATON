// Login functionality
class LoginManager {
    constructor() {
        this.documentoInput = null;
        this.loginButton = null;
        this.documento = '';
        
        this.init();
    }
    
    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupElements());
        } else {
            this.setupElements();
        }
    }
    
    setupElements() {
        // Get DOM elements
        this.documentoInput = document.getElementById('documento');
        this.loginButton = document.getElementById('login-button');
        
        if (!this.documentoInput || !this.loginButton) {
            console.error('Required elements not found');
            return;
        }
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Initial state
        this.updateButtonState();
    }
    
    setupEventListeners() {
        // Input event listener
        this.documentoInput.addEventListener('input', (e) => {
            this.documento = e.target.value;
            this.updateButtonState();
        });
        
        // Enter key event listener
        this.documentoInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleLogin();
            }
        });
        
        // Button click event listener
        this.loginButton.addEventListener('click', () => {
            this.handleLogin();
        });
        
        // Focus on input when page loads
        this.documentoInput.focus();
    }
    
    updateButtonState() {
        const isValid = this.documento.trim().length > 0;
        this.loginButton.disabled = !isValid;
        
        if (isValid) {
            this.loginButton.classList.remove('disabled');
        } else {
            this.loginButton.classList.add('disabled');
        }
    }
    
    validateDocumento(documento) {
        // Basic validation
        const trimmed = documento.trim();
        
        if (trimmed.length === 0) {
            return {
                valid: false,
                message: 'El documento de identidad es requerido'
            };
        }
        
        if (trimmed.length < 3) {
            return {
                valid: false,
                message: 'El documento debe tener al menos 3 caracteres'
            };
        }
        
        // Check if it contains only numbers and letters
        const validPattern = /^[a-zA-Z0-9\s-]+$/;
        if (!validPattern.test(trimmed)) {
            return {
                valid: false,
                message: 'El documento solo puede contener letras, números, espacios y guiones'
            };
        }
        
        return {
            valid: true,
            message: 'Documento válido'
        };
    }
    
    showError(message) {
        // Create error element if it doesn't exist
        let errorElement = document.getElementById('error-message');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.id = 'error-message';
            errorElement.className = 'error-message';
            errorElement.style.cssText = `
                color: #dc3545;
                font-size: 0.875rem;
                margin-top: 0.5rem;
                padding: 0.5rem;
                background-color: rgba(220, 53, 69, 0.1);
                border: 1px solid rgba(220, 53, 69, 0.3);
                border-radius: 0.375rem;
            `;
            this.documentoInput.parentNode.appendChild(errorElement);
        }
        
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (errorElement) {
                errorElement.style.display = 'none';
            }
        }, 5000);
    }
    
    hideError() {
        const errorElement = document.getElementById('error-message');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }
    
    showLoading() {
        const originalText = this.loginButton.innerHTML;
        this.loginButton.innerHTML = `
            <svg class="loading" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <path d="m16 12-4-4-4 4"/>
                <path d="m12 16 4-4-4-4"/>
            </svg>
            Ingresando...
        `;
        this.loginButton.disabled = true;
        
        return originalText;
    }
    
    hideLoading(originalText) {
        this.loginButton.innerHTML = originalText;
        this.updateButtonState();
    }
    
    saveSession(documento) {
        // Save session data to localStorage
        const sessionData = {
            documento: documento,
            loginTime: new Date().toISOString(),
            sessionId: this.generateSessionId()
        };
        
        localStorage.setItem('lean_session', JSON.stringify(sessionData));
        
        // Set session expiry (24 hours)
        const expiryTime = new Date();
        expiryTime.setHours(expiryTime.getHours() + 24);
        localStorage.setItem('lean_session_expiry', expiryTime.toISOString());
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    handleLogin() {
        this.hideError();
        
        // Validate input
        const validation = this.validateDocumento(this.documento);
        if (!validation.valid) {
            this.showError(validation.message);
            this.documentoInput.focus();
            return;
        }
        
        // Show loading state
        const originalText = this.showLoading();
        
        // Simulate API call delay (in real app, this would be an actual API call)
        setTimeout(() => {
            try {
                // Save session
                this.saveSession(this.documento);
                
                // Navigate to chat
                window.location.href = './index.html';
                
            } catch (error) {
                console.error('Login error:', error);
                this.hideLoading(originalText);
                this.showError('Error al iniciar sesión. Por favor, intente nuevamente.');
            }
        }, 1000);
    }
    
    // Check if user is already logged in
    static checkSession() {
        const session = localStorage.getItem('lean_session');
        const expiry = localStorage.getItem('lean_session_expiry');
        
        if (!session || !expiry) {
            return null;
        }
        
        const expiryDate = new Date(expiry);
        const now = new Date();
        
        if (now > expiryDate) {
            // Session expired
            localStorage.removeItem('lean_session');
            localStorage.removeItem('lean_session_expiry');
            return null;
        }
        
        try {
            return JSON.parse(session);
        } catch (error) {
            console.error('Session parse error:', error);
            localStorage.removeItem('lean_session');
            localStorage.removeItem('lean_session_expiry');
            return null;
        }
    }
    
    // Logout function
    static logout() {
        localStorage.removeItem('lean_session');
        localStorage.removeItem('lean_session_expiry');
        window.location.href = './login.html';
    }
}

// Initialize login manager when script loads
const loginManager = new LoginManager();

// Export for potential use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LoginManager;
}

// Add to global scope for debugging
window.LoginManager = LoginManager;
