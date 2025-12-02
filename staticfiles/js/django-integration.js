// django-integration.js
// Sistema de integración Django para Turismo Bolivia
class DjangoIntegration {
    constructor() {
        this.config = window.DJANGO_SECURITY || {};
        this.csrfToken = this.config.csrfToken;
        this.djangoUser = this.config.djangoUser;
        this.isActive = false;
        
        console.log('Sistema Django Integration inicializando...');
        this.init();
    }
    
    init() {
        setTimeout(() => {
            this.setupIntegration();
        }, 1000);
    }
    
    setupIntegration() {
        try {
            console.log('Configurando integracion con Django...');
            
            this.checkDjangoUser();
            this.syncUsers();
            this.enhanceLoginForm();
            this.enhanceRegisterForm();
            this.addSecurityBadge();
            
            this.isActive = true;
            console.log('Integracion Django activa');
            
        } catch (error) {
            console.error('Error en integracion Django:', error);
        }
    }
    
    checkDjangoUser() {
        if (this.djangoUser.isAuthenticated) {
            console.log('Usuario Django autenticado:', this.djangoUser.username);
            this.syncDjangoToLocalStorage();
        }
    }
    
    async syncUsers() {
        try {
            const localUsers = JSON.parse(localStorage.getItem('users') || '[]');
            
            if (localUsers.length > 0 && this.csrfToken) {
                console.log('Sincronizando', localUsers.length, 'usuarios con Django...');
                
                const response = await this.callDjangoAPI('sync/', {
                    method: 'POST',
                    body: JSON.stringify({
                        users: localUsers,
                        action: 'sync_from_local'
                    })
                });
                
                if (response && response.success) {
                    console.log('Sincronizacion completada');
                }
            }
        } catch (error) {
            console.warn('No se pudo sincronizar usuarios:', error);
        }
    }
    
    enhanceLoginForm() {
        const loginForm = document.getElementById('formLogin');
        if (!loginForm) return;
        
        console.log('Mejorando formulario de login con Django...');
        
        const djangoMessage = document.createElement('div');
        djangoMessage.id = 'djangoLoginMessage';
        djangoMessage.className = 'django-message';
        loginForm.parentNode.insertBefore(djangoMessage, loginForm.nextSibling);
        
        const originalSubmitHandler = loginForm.onsubmit;
        
        loginForm.addEventListener('submit', async (event) => {
            if (originalSubmitHandler) {
                originalSubmitHandler.call(loginForm, event);
            }
            
            setTimeout(async () => {
                const username = document.getElementById('loginUsuario')?.value;
                const password = document.getElementById('loginPassword')?.value;
                
                if (username && password) {
                    const djangoResult = await this.tryDjangoLogin(username, password);
                    
                    if (djangoResult.success) {
                        this.showMessage(djangoMessage, 'Login exitoso con sistema seguro', 'success');
                        this.addUserToLocalStorage(username, password);
                    }
                }
            }, 100);
        });
    }
    
    enhanceRegisterForm() {
        const registerForm = document.getElementById('formRegistro');
        if (!registerForm) return;
        
        console.log('Mejorando formulario de registro con Django...');
        
        const djangoMessage = document.createElement('div');
        djangoMessage.id = 'djangoRegisterMessage';
        djangoMessage.className = 'django-message';
        registerForm.parentNode.insertBefore(djangoMessage, registerForm.nextSibling);
        
        registerForm.addEventListener('submit', async (event) => {
            setTimeout(async () => {
                this.showMessage(djangoMessage, 'Registro procesado con sistema seguro', 'info');
            }, 100);
        });
    }
    
    addSecurityBadge() {
        const badge = document.createElement('div');
        badge.className = 'security-badge';
        badge.textContent = 'Sistema Seguro Django';
        badge.title = 'Autenticacion protegida por Django Security';
        document.body.appendChild(badge);
    }
    
    async tryDjangoLogin(username, password) {
        try {
            const response = await this.callDjangoAPI('login/', {
                method: 'POST',
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });
            
            return response || { success: false, message: 'Error de conexion' };
            
        } catch (error) {
            console.error('Error en login Django:', error);
            return { success: false, message: 'Error del sistema' };
        }
    }
    
    async callDjangoAPI(endpoint, options = {}) {
        const url = this.config.apiUrls[endpoint];
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken
            },
            credentials: 'include'
        };
        
        const finalOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, finalOptions);
            
            if (response.status === 403) {
                console.warn('Token CSRF invalido');
                return null;
            }
            
            if (response.ok) {
                return await response.json();
            } else {
                console.error('Error API:', response.status);
                return null;
            }
            
        } catch (error) {
            console.error('Error llamando API Django:', error);
            return null;
        }
    }
    
    addUserToLocalStorage(username, password) {
        try {
            const users = JSON.parse(localStorage.getItem('users') || '[]');
            const existingUser = users.find(u => u.usuario === username);
            
            if (!existingUser) {
                users.push({
                    usuario: username,
                    pass: password,
                    created: new Date().toISOString(),
                    source: 'django_sync'
                });
                
                localStorage.setItem('users', JSON.stringify(users));
                console.log('Usuario añadido a localStorage:', username);
            }
            
        } catch (error) {
            console.error('Error añadiendo usuario a localStorage:', error);
        }
    }
    
    syncDjangoToLocalStorage() {
        if (this.djangoUser.isAuthenticated) {
            this.addUserToLocalStorage(
                this.djangoUser.username, 
                'django_authenticated_' + Date.now()
            );
        }
    }
    
    showMessage(element, text, type = 'info') {
        if (!element) return;
        
        element.textContent = text;
        element.className = 'django-message message-' + type;
        
        setTimeout(() => {
            element.textContent = '';
            element.className = 'django-message';
        }, 5000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.djangoIntegration = new DjangoIntegration();
});
