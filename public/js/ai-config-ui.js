// Configuración de la interfaz de usuario para proveedores de IA
class AIConfigUI {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.loadSavedConfig();
    }

    initializeElements() {
        this.modal = document.getElementById('settings-modal');
        this.providerSelect = document.getElementById('ai-provider-select');
        this.apiKeyInput = document.getElementById('api-key-input');
        this.apiKeyHelp = document.getElementById('api-key-help');
        this.geminiModelGroup = document.getElementById('gemini-model-group');
        this.geminiModelSelect = document.getElementById('gemini-model-select');
        this.saveButton = document.getElementById('save-api-settings');
        this.testButton = document.getElementById('test-api-connection');
        this.testResult = document.getElementById('api-test-result');
        this.togglePasswordButton = document.getElementById('toggle-password');
        this.settingsNav = document.getElementById('settings-nav');
        this.closeButton = this.modal.querySelector('.close');
    }

    bindEvents() {
        // Abrir modal
        this.settingsNav.addEventListener('click', (e) => {
            e.preventDefault();
            this.openModal();
        });

        // Cerrar modal
        this.closeButton.addEventListener('click', () => this.closeModal());
        window.addEventListener('click', (e) => {
            if (e.target === this.modal) this.closeModal();
        });

        // Cambio de proveedor
        this.providerSelect.addEventListener('change', () => this.onProviderChange());

        // Guardar configuración
        this.saveButton.addEventListener('click', () => this.saveConfig());

        // Probar conexión
        this.testButton.addEventListener('click', () => this.testConnection());

        // Toggle password visibility
        this.togglePasswordButton.addEventListener('click', () => this.togglePasswordVisibility());
    }

    openModal() {
        this.modal.style.display = 'block';
        this.loadAvailableProviders();
    }

    closeModal() {
        this.modal.style.display = 'none';
        this.clearTestResult();
    }

    async loadAvailableProviders() {
        try {
            const providers = await window.leanBotAPI.getAvailableProviders();
            
            // Limpiar opciones existentes
            this.providerSelect.innerHTML = '';
            
            // Agregar opciones disponibles
            providers.providers.forEach(provider => {
                const option = document.createElement('option');
                option.value = provider;
                option.textContent = this.getProviderDisplayName(provider);
                this.providerSelect.appendChild(option);
            });

            // Seleccionar el proveedor por defecto
            this.providerSelect.value = providers.default;
            this.onProviderChange();
            
        } catch (error) {
            console.error('Error al cargar proveedores:', error);
            // Fallback a opciones estáticas
            this.providerSelect.innerHTML = `
                <option value="gemini">Gemini (Google)</option>
                <option value="mistral">Mistral AI</option>
            `;
        }
    }

    getProviderDisplayName(provider) {
        const names = {
            'gemini': 'Gemini (Google)',
            'mistral': 'Mistral AI'
        };
        return names[provider] || provider;
    }

    onProviderChange() {
        const selectedProvider = this.providerSelect.value;
        
        // Actualizar placeholder y ayuda según el proveedor
        if (selectedProvider === 'gemini') {
            this.apiKeyInput.placeholder = 'Ingresa tu clave API de Gemini...';
            this.apiKeyHelp.textContent = 'Obtén tu API key en Google AI Studio (ai.google.dev)';
            this.geminiModelGroup.style.display = 'block';
        } else if (selectedProvider === 'mistral') {
            this.apiKeyInput.placeholder = 'Ingresa tu clave API de Mistral...';
            this.apiKeyHelp.textContent = 'Obtén tu API key en aimlapi.com para Mistral AI';
            this.geminiModelGroup.style.display = 'none';
        }

        // Cargar configuración guardada para este proveedor
        this.loadSavedConfigForProvider(selectedProvider);
    }

    loadSavedConfig() {
        const currentConfig = window.leanBotAPI.getCurrentAIConfig();
        this.providerSelect.value = currentConfig.provider;
        this.onProviderChange();
    }

    loadSavedConfigForProvider(provider) {
        const savedApiKey = localStorage.getItem(`ai_api_key_${provider}`);
        if (savedApiKey) {
            this.apiKeyInput.value = savedApiKey;
        } else {
            this.apiKeyInput.value = '';
        }

        if (provider === 'gemini') {
            const savedModel = localStorage.getItem('gemini_model');
            if (savedModel) {
                this.geminiModelSelect.value = savedModel;
            }
        }
    }

    async saveConfig() {
        const provider = this.providerSelect.value;
        const apiKey = this.apiKeyInput.value.trim();
        
        if (!provider) {
            this.showTestResult('Por favor selecciona un proveedor', 'error');
            return;
        }

        // Guardar en localStorage
        if (apiKey) {
            localStorage.setItem(`ai_api_key_${provider}`, apiKey);
        } else {
            localStorage.removeItem(`ai_api_key_${provider}`);
        }

        if (provider === 'gemini') {
            localStorage.setItem('gemini_model', this.geminiModelSelect.value);
        }

        // Configurar en la API
        const success = window.leanBotAPI.setAIProvider(provider, apiKey || null);
        
        if (success) {
            this.showTestResult(`Configuración guardada para ${this.getProviderDisplayName(provider)}`, 'success');
        } else {
            this.showTestResult('Error al guardar la configuración', 'error');
        }
    }

    async testConnection() {
        const provider = this.providerSelect.value;
        const apiKey = this.apiKeyInput.value.trim();
        
        if (!provider) {
            this.showTestResult('Por favor selecciona un proveedor', 'error');
            return;
        }

        this.showTestResult('Probando conexión...', 'info');
        this.testButton.disabled = true;

        try {
            const result = await window.leanBotAPI.testAIProvider(provider, apiKey || null);
            
            if (result.working) {
                this.showTestResult(`✅ Conexión exitosa con ${this.getProviderDisplayName(provider)}`, 'success');
            } else {
                this.showTestResult(`❌ Error de conexión: ${result.error || 'Desconocido'}`, 'error');
            }
        } catch (error) {
            this.showTestResult(`❌ Error al probar conexión: ${error.message}`, 'error');
        } finally {
            this.testButton.disabled = false;
        }
    }

    togglePasswordVisibility() {
        const isPassword = this.apiKeyInput.type === 'password';
        this.apiKeyInput.type = isPassword ? 'text' : 'password';
        
        const icon = this.togglePasswordButton.querySelector('svg');
        if (isPassword) {
            // Cambiar a icono de "ocultar"
            icon.innerHTML = `
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
            `;
        } else {
            // Cambiar a icono de "mostrar"
            icon.innerHTML = `
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
            `;
        }
    }

    showTestResult(message, type) {
        this.testResult.textContent = message;
        this.testResult.className = `test-result ${type}`;
        this.testResult.style.display = 'block';
    }

    clearTestResult() {
        this.testResult.style.display = 'none';
        this.testResult.textContent = '';
        this.testResult.className = 'test-result';
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Esperar a que leanBotAPI esté disponible
    const initAIConfig = () => {
        if (window.leanBotAPI) {
            new AIConfigUI();
        } else {
            setTimeout(initAIConfig, 100);
        }
    };
    initAIConfig();
});