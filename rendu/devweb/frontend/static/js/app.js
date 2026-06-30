/**
 * Assistant Financier — client de chat
 * JavaScript moderne (ES2022), sans étape de build : servi tel quel par Flask.
 *
 * Les blocs JSDoc ci-dessous donnent l'autocomplétion/typage dans l'éditeur
 * (VSCode, etc.) sans avoir besoin de TypeScript ni de compilation.
 */

/**
 * @typedef {Object} ChatMessage
 * @property {'user'|'assistant'} role
 * @property {string} content
 */

/**
 * @typedef {Object} SendMessageResponse
 * @property {boolean} success
 * @property {string} [bot_response]
 * @property {string} [session_id]
 * @property {string} [error]
 */

/**
 * @typedef {Object} SessionSummary
 * @property {string} id
 * @property {number} messages_count
 */

/**
 * API Client - Gestion des appels API
 */
class ApiClient {
    /** @param {string} [baseUrl] */
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl || window.location.origin;
    }

    /**
     * Envoie un message. En cas d'erreur HTTP, lève une Error dont le message
     * est le texte renvoyé par le serveur (jamais préfixé ici : c'est à
     * l'appelant de décider comment l'afficher, pour éviter les doublons).
     * @param {string} message
     * @param {string} sessionId
     * @returns {Promise<SendMessageResponse>}
     */
    async sendMessage(message, sessionId) {
        const response = await fetch(`${this.baseUrl}/api/chat/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, message })
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.error || 'Erreur serveur');
        }

        return response.json();
    }

    /**
     * @param {string} sessionId
     * @returns {Promise<{success: boolean, messages?: ChatMessage[]}>}
     */
    async getHistory(sessionId) {
        const response = await fetch(`${this.baseUrl}/api/chat/history/${sessionId}`);
        if (!response.ok) throw new Error("Erreur lors de la récupération de l'historique");
        return response.json();
    }

    /** @returns {Promise<{success: boolean, sessions?: SessionSummary[]}>} */
    async getSessions() {
        const response = await fetch(`${this.baseUrl}/api/chat/sessions`);
        if (!response.ok) throw new Error('Erreur lors de la récupération des sessions');
        return response.json();
    }

    /**
     * @param {string} sessionId
     * @returns {Promise<{success: boolean}>}
     */
    async deleteSession(sessionId) {
        const response = await fetch(`${this.baseUrl}/api/chat/session/${sessionId}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Erreur lors de la suppression');
        return response.json();
    }

    /** @returns {Promise<{status: string, ollama: string}>} */
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseUrl}/api/health`);
            return await response.json();
        } catch {
            return { status: 'disconnected', ollama: 'disconnected' };
        }
    }
}

/**
 * Chat Manager - Logique principale de l'application
 */
class ChatManager {
    constructor() {
        this.api = new ApiClient();
        this.currentSessionId = this.generateSessionId();
        this.isLoading = false;
        /** @type {ChatMessage[]} */
        this.messages = [];
        /** @type {SessionSummary[]} */
        this.sessions = [];

        this.initializeElements();
        this.setupEventListeners();
        this.checkConnection();
        this.loadHistory();
        this.loadSessions();

        setInterval(() => this.checkConnection(), 5000);
    }

    initializeElements() {
        this.messagesArea = this.require('messages');
        this.inputField = /** @type {HTMLInputElement} */ (this.require('message-input'));
        this.sendBtn = /** @type {HTMLButtonElement} */ (this.require('send-btn'));
        this.statusBadge = this.require('status-badge');
        this.sessionsList = this.require('sessions-list');
        this.sidebarCount = this.require('sidebar-count');
        this.newChatBtn = /** @type {HTMLButtonElement} */ (this.require('new-chat-btn'));
        this.alertZone = this.require('alert-zone');
    }

    /**
     * @param {string} id
     * @returns {HTMLElement}
     */
    require(id) {
        const el = document.getElementById(id);
        if (!el) throw new Error(`Élément #${id} introuvable dans le DOM`);
        return el;
    }

    setupEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        this.newChatBtn.addEventListener('click', () => this.newChat());
    }

    /** @returns {string} */
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    async checkConnection() {
        const health = await this.api.checkHealth();
        const isConnected = health.ollama === 'connected';

        this.statusBadge.className = `status-badge ${isConnected ? 'connected' : 'disconnected'}`;
        this.statusBadge.innerHTML = `
            <span class="status-dot"></span>
            <span class="status-text">${isConnected ? 'Connecté' : 'Hors ligne'}</span>
        `;
    }

    async sendMessage() {
        const message = this.inputField.value.trim();
        if (!message || this.isLoading) return;

        this.clearAlert();
        this.displayMessage(message, 'user');
        this.inputField.value = '';
        this.isLoading = true;
        this.sendBtn.disabled = true;
        this.displayLoading();

        try {
            const response = await this.api.sendMessage(message, this.currentSessionId);
            this.removeLoading();

            if (response.success && response.bot_response && response.session_id) {
                this.displayMessage(response.bot_response, 'assistant');
                this.currentSessionId = response.session_id;
                this.loadSessions();
            } else {
                // Le serveur a répondu sans succès : on affiche son message une seule fois.
                this.displayAlert(response.error || 'Une erreur est survenue.', 'error');
            }
        } catch (error) {
            this.removeLoading();
            // `error.message` contient déjà le texte renvoyé par le serveur
            // (ou un message générique) : on ne le préfixe pas une seconde fois.
            const text = error instanceof Error ? error.message : 'Erreur inconnue';
            this.displayAlert(text, 'error');
        } finally {
            this.isLoading = false;
            this.sendBtn.disabled = false;
            this.inputField.focus();
        }
    }

    /**
     * @param {string} content
     * @param {'user'|'assistant'} role
     */
    displayMessage(content, role) {
        this.messagesArea.classList.remove('empty');

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;

        const entry = document.createElement('div');
        entry.className = 'message-entry';

        const meta = document.createElement('div');
        meta.className = 'message-meta';
        meta.textContent = `${role === 'user' ? 'Vous' : 'Assistant'} · ${new Date().toLocaleTimeString('fr-FR', {
            hour: '2-digit',
            minute: '2-digit'
        })}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = content;

        entry.appendChild(meta);
        entry.appendChild(contentDiv);
        messageDiv.appendChild(entry);

        this.messagesArea.appendChild(messageDiv);
        this.messagesArea.scrollTop = this.messagesArea.scrollHeight;
    }

    displayLoading() {
        const loaderDiv = document.createElement('div');
        loaderDiv.id = 'loading-indicator';
        loaderDiv.className = 'message assistant';
        loaderDiv.innerHTML = `
            <div class="loading">
                <span>L'assistant réfléchit</span>
                <div class="loading-dots">
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                </div>
            </div>
        `;
        this.messagesArea.appendChild(loaderDiv);
        this.messagesArea.scrollTop = this.messagesArea.scrollHeight;
    }

    removeLoading() {
        document.getElementById('loading-indicator')?.remove();
    }

    clearAlert() {
        this.alertZone.innerHTML = '';
    }

    /**
     * @param {string} message
     * @param {'error'|'warning'} [type]
     */
    displayAlert(message, type = 'error') {
        // Un seul message d'alerte affiché à la fois, dans sa propre zone
        // (et non mélangé au fil des écritures).
        this.alertZone.innerHTML = '';
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert ${type}`;
        alertDiv.textContent = message;
        this.alertZone.appendChild(alertDiv);
    }

    async loadHistory() {
        try {
            const response = await this.api.getHistory(this.currentSessionId);
            if (response.success && response.messages) {
                this.messages = response.messages;
                this.renderMessages();
            }
        } catch (error) {
            console.error("Erreur lors du chargement de l'historique:", error);
        }
    }

    renderMessages() {
        this.messagesArea.innerHTML = '';
        if (this.messages.length === 0) {
            this.messagesArea.classList.add('empty');
            this.messagesArea.innerHTML = `
                <div class="messages-empty">
                    <span class="messages-empty-mark">€</span>
                    <p>Aucun message pour l'instant.</p>
                    <p class="messages-empty-sub">Posez une question pour démarrer la conversation.</p>
                </div>
            `;
        } else {
            this.messagesArea.classList.remove('empty');
            this.messages.forEach((msg) => this.displayMessage(msg.content, msg.role));
        }
    }

    newChat() {
        this.currentSessionId = this.generateSessionId();
        this.messages = [];
        this.clearAlert();
        this.renderMessages();
        this.inputField.focus();
    }

    async loadSessions() {
        try {
            const response = await this.api.getSessions();
            if (response.success && response.sessions) {
                this.sessions = response.sessions;
                this.renderSessions();
            }
        } catch (error) {
            console.error('Erreur lors du chargement des sessions:', error);
        }
    }

    renderSessions() {
        this.sidebarCount.textContent = this.sessions.length ? `${this.sessions.length}` : '';
        this.sessionsList.innerHTML = '';

        if (this.sessions.length === 0) {
            this.sessionsList.innerHTML = '<div class="sessions-empty">Aucune conversation enregistrée.</div>';
            return;
        }

        this.sessions.slice(0, 10).forEach((session) => {
            const item = document.createElement('div');
            item.className = `session-item${session.id === this.currentSessionId ? ' active' : ''}`;

            const idLine = document.createElement('div');
            idLine.className = 'session-item-id';
            idLine.textContent = `Conversation ${session.id.substr(8, 6)}`;

            const metaLine = document.createElement('div');
            metaLine.className = 'session-item-meta';
            metaLine.textContent = `${session.messages_count} message${session.messages_count > 1 ? 's' : ''}`;

            item.appendChild(idLine);
            item.appendChild(metaLine);

            item.addEventListener('click', () => {
                this.currentSessionId = session.id;
                this.loadHistory();
                this.renderSessions();
            });

            this.sessionsList.appendChild(item);
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ChatManager();
});