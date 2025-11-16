// MedSense AI - Main Application Script
class MedSenseApp {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.clearChatBtn = document.getElementById('clearChatBtn');
        this.themeToggle = document.getElementById('themeToggle');
        this.isProcessing = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadTheme();
        this.messageInput.focus();
        this.autoResizeTextarea();
    }

    setupEventListeners() {
        // Send message
        this.sendBtn.addEventListener('click', () => this.handleSend());
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSend();
            }
        });

        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => this.autoResizeTextarea());

        // Clear chat
        this.clearChatBtn.addEventListener('click', () => this.clearChat());

        // Theme toggle
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
    }

    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }

    async handleSend() {
        if (this.isProcessing) return;

        const message = this.messageInput.value.trim();
        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');

        // Clear input
        this.messageInput.value = '';
        this.autoResizeTextarea();

        // Disable input
        this.setProcessing(true);

        // Show loading
        const loadingId = this.showLoading();

        try {
            // Call API
            const result = await analyzeSymptoms(message);
            
            // Remove loading
            this.removeLoading(loadingId);
            
            // Display response
            this.displayResponse(result);
        } catch (error) {
            this.removeLoading(loadingId);
            this.addError(error.message);
        } finally {
            this.setProcessing(false);
        }
    }

    addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        
        if (type === 'bot') {
            avatar.innerHTML = '<div class="avatar-bot">🤖</div>';
        } else {
            const initials = this.getInitials(text);
            avatar.innerHTML = `<div class="avatar-user">${initials}</div>`;
        }

        const content = document.createElement('div');
        content.className = 'message-content';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.innerHTML = `<p>${this.escapeHtml(text)}</p>`;

        content.appendChild(textDiv);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        this.chatMessages.appendChild(messageDiv);

        this.scrollToBottom();
    }

    displayResponse(result) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<div class="avatar-bot">🤖</div>';

        const content = document.createElement('div');
        content.className = 'message-content';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';

        // Handle non-medical queries
        if (result.is_medical_query === false) {
            textDiv.innerHTML = `<p>${this.escapeHtml(result.response || result.message)}</p>`;
        } else {
            // Medical response
            let html = '';

            // Possible Conditions
            if (result.possible_conditions && result.possible_conditions.length > 0) {
                html += '<div class="conditions-card">';
                html += '<div class="conditions-title">🔍 Possible Conditions</div>';
                result.possible_conditions.forEach((condition, index) => {
                    html += `
                        <div class="condition-item">
                            <div class="condition-name">${index + 1}. ${this.escapeHtml(condition)}</div>
                        </div>
                    `;
                });
                html += '</div>';
            }

            // Severity
            if (result.severity) {
                const severityClass = result.severity.toLowerCase().replace('emergency', 'emergency');
                html += `
                    <div style="margin-top: 0.75rem;">
                        <span class="severity-badge severity-${severityClass}">${this.escapeHtml(result.severity)}</span>
                    </div>
                `;
            }

            // Recommendations
            if (result.recommendations) {
                html += `
                    <div class="recommendations-card">
                        <div class="recommendations-title">💡 Care Recommendations</div>
                        <div class="recommendations-text">${this.escapeHtml(result.recommendations)}</div>
                    </div>
                `;
            }

            // Doctor Consultation
            if (result.see_doctor) {
                const isEmergency = result.severity && result.severity.toLowerCase() === 'emergency';
                html += `
                    <div class="doctor-card">
                        <div class="doctor-title">${isEmergency ? '🚨 URGENT: ' : '👨‍⚕️ '}When to See a Doctor</div>
                        <div class="doctor-text">${this.escapeHtml(result.see_doctor)}</div>
                    </div>
                `;
            }

            textDiv.innerHTML = html || '<p>Unable to generate response. Please try again.</p>';
        }

        content.appendChild(textDiv);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        this.chatMessages.appendChild(messageDiv);

        this.scrollToBottom();
    }

    showLoading() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.id = 'loading-message';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<div class="avatar-bot">🤖</div>';

        const content = document.createElement('div');
        content.className = 'message-content';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text loading-message';
        textDiv.innerHTML = `
            <span>Analyzing symptoms</span>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        `;

        content.appendChild(textDiv);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        this.chatMessages.appendChild(messageDiv);

        this.scrollToBottom();
        return 'loading-message';
    }

    removeLoading(id) {
        const loading = document.getElementById(id);
        if (loading) loading.remove();
    }

    addError(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<div class="avatar-bot">🤖</div>';

        const content = document.createElement('div');
        content.className = 'message-content';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.innerHTML = `<p style="color: var(--accent-danger);">❌ Error: ${this.escapeHtml(message)}</p>`;

        content.appendChild(textDiv);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        this.chatMessages.appendChild(messageDiv);

        this.scrollToBottom();
    }

    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            this.chatMessages.innerHTML = `
                <div class="message bot-message">
                    <div class="message-avatar">
                        <div class="avatar-bot">🤖</div>
                    </div>
                    <div class="message-content">
                        <div class="message-text">
                            <p>Hello! I'm <strong>MedSense AI</strong>, your intelligent symptom checker assistant.</p>
                            <p>I can help you understand possible conditions based on symptoms, but I'm not a replacement for professional medical care.</p>
                            <p class="help-text">💡 <strong>How to use:</strong> Describe your symptoms in natural language. For example: "I have a fever and headache"</p>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        const sunIcon = document.getElementById('sunIcon');
        const moonIcon = document.getElementById('moonIcon');
        
        if (newTheme === 'dark') {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        } else {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        }
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        
        const sunIcon = document.getElementById('sunIcon');
        const moonIcon = document.getElementById('moonIcon');
        
        if (savedTheme === 'dark') {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        } else {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        }
    }

    setProcessing(processing) {
        this.isProcessing = processing;
        this.messageInput.disabled = processing;
        this.sendBtn.disabled = processing;
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    getInitials(text) {
        const words = text.trim().split(/\s+/);
        if (words.length >= 2) {
            return (words[0][0] + words[1][0]).toUpperCase();
        }
        return text.substring(0, 2).toUpperCase();
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new MedSenseApp();
});
