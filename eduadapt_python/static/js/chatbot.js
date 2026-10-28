/**
 * EduAdapt-AI Interactive Chatbot Client
 * Powers both the floating widget and the full /chatbot page.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Floating Widget Toggle
    const widgetBtn = document.getElementById('chatWidgetBtn');
    const widgetDock = document.getElementById('chatWidgetDock');
    const closeBtn = document.getElementById('chatWidgetCloseBtn');

    if (widgetBtn && widgetDock) {
        widgetBtn.addEventListener('click', () => {
            widgetDock.classList.toggle('open');
            if (widgetDock.classList.contains('open')) {
                const input = widgetDock.querySelector('.chat-input');
                if (input) input.focus();
                scrollChatToBottom(widgetDock.querySelector('.chat-messages'));
            }
        });
    }

    if (closeBtn && widgetDock) {
        closeBtn.addEventListener('click', () => {
            widgetDock.classList.remove('open');
        });
    }

    // 2. Chat Messaging Engine Setup (works for both widget and full page)
    setupChatContainer('chatWidgetDock');
    setupChatContainer('fullChatPageContainer');

    function setupChatContainer(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const messagesEl = container.querySelector('.chat-messages');
        const inputEl = container.querySelector('.chat-input');
        const sendBtn = container.querySelector('.chat-send-btn');
        const clearBtn = container.querySelector('.chat-clear-btn');
        const subjectSelect = container.querySelector('.chat-subject-select');

        if (!messagesEl || !inputEl || !sendBtn) return;

        const sendMessage = async () => {
            const rawMsg = inputEl.value.trim();
            if (!rawMsg) return;

            inputEl.value = '';
            inputEl.disabled = true;
            sendBtn.disabled = true;

            // Render user bubble
            appendUserMessage(messagesEl, rawMsg);
            scrollChatToBottom(messagesEl);

            // Render typing indicator
            const typingEl = appendTypingIndicator(messagesEl);
            scrollChatToBottom(messagesEl);

            // Determine context
            const subjectContext = subjectSelect ? subjectSelect.value : (container.dataset.subjectContext || '');
            const levelContext = container.dataset.levelContext || '';

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: rawMsg,
                        subject_context: subjectContext,
                        level_context: levelContext
                    })
                });

                const data = await res.json();
                if (typingEl) typingEl.remove();

                if (data.response) {
                    appendAssistantMessage(messagesEl, data.response, data.source, data.timestamp);
                } else {
                    appendAssistantMessage(messagesEl, "I apologize, but I encountered an error processing your request. Please try again.", 'error');
                }
            } catch (err) {
                if (typingEl) typingEl.remove();
                appendAssistantMessage(messagesEl, "Network connection issue. Please check your connection and try again.", 'error');
            } finally {
                inputEl.disabled = false;
                sendBtn.disabled = false;
                inputEl.focus();
                scrollChatToBottom(messagesEl);
            }
        };

        sendBtn.addEventListener('click', sendMessage);
        inputEl.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Prompt suggestions
        container.querySelectorAll('.chat-suggestion-pill').forEach(pill => {
            pill.addEventListener('click', () => {
                inputEl.value = pill.innerText.trim();
                sendMessage();
            });
        });

        // Clear chat
        if (clearBtn) {
            clearBtn.addEventListener('click', async () => {
                if (confirm("Clear your conversation history?")) {
                    try {
                        await fetch('/api/chat/clear', { method: 'POST' });
                        messagesEl.innerHTML = '';
                        appendAssistantMessage(messagesEl, "Chat history cleared. How can I help you today?", 'system');
                    } catch (e) {
                        console.error('Failed to clear chat:', e);
                    }
                }
            });
        }
    }

    function appendUserMessage(container, text) {
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble chat-bubble-user';
        bubble.innerHTML = `<div>${escapeHtml(text)}</div><div class="text-end" style="font-size: 0.7rem; opacity: 0.8; margin-top: 4px;">${time}</div>`;
        container.appendChild(bubble);
    }

    function appendAssistantMessage(container, text, source, timestamp) {
        const time = timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble chat-bubble-assistant';
        
        // Basic markdown formatting (bold, code blocks, bullet points)
        let formatted = formatMarkdown(text);
        
        let sourceBadge = '';
        if (source === 'gemini_cloud_ai' || source === 'openai_cloud_ai') {
            sourceBadge = '<span class="badge bg-primary-subtle text-primary border" style="font-size:0.65rem;">Cloud AI</span>';
        } else {
            sourceBadge = '<span class="badge bg-light text-muted border" style="font-size:0.65rem;">EduAdapt Tutor</span>';
        }

        bubble.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-1">
                ${sourceBadge}
                <span class="text-muted" style="font-size: 0.7rem;">${time}</span>
            </div>
            <div class="assistant-content">${formatted}</div>
        `;
        container.appendChild(bubble);
    }

    function appendTypingIndicator(container) {
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble chat-bubble-assistant';
        bubble.innerHTML = `
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        `;
        container.appendChild(bubble);
        return bubble;
    }

    function scrollChatToBottom(container) {
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }

    function escapeHtml(str) {
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function formatMarkdown(text) {
        // Code blocks: ```language ... ```
        let formatted = text.replace(/```([a-zA-Z]*)\n([\s\S]*?)```/g, (match, lang, code) => {
            return `<pre><code class="language-${lang}">${escapeHtml(code.trim())}</code></pre>`;
        });

        // Inline code `...`
        formatted = formatted.replace(/`([^`]+)`/g, (match, code) => {
            return `<code>${escapeHtml(code)}</code>`;
        });

        // Bold **...**
        formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Italic *...*
        formatted = formatted.replace(/\*([^*]+)\*/g, '<em>$1</em>');

        // Bullet lists
        formatted = formatted.replace(/^\s*-\s+(.+)$/gm, '<li>$1</li>');
        formatted = formatted.replace(/(<li>.+<\/li>)+/g, '<ul class="mb-2 ps-3">$1</ul>');

        // Newlines to line breaks (outside pre)
        formatted = formatted.split('\n\n').map(p => {
            if (p.startsWith('<pre>') || p.startsWith('<ul>')) return p;
            return `<p class="mb-2">${p.replace(/\n/g, '<br>')}</p>`;
        }).join('');

        return formatted;
    }
});
