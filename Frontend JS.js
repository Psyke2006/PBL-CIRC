let uploadedImage = null;
let uploadedFileName = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('imageInput');
    const messageInput = document.getElementById('messageInput');
    
    imageInput.addEventListener('change', handleImageUpload);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    clearWelcomeMessage();
});

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
    if (!validTypes.includes(file.type)) {
        showError('Please upload a valid image file (JPEG, PNG, or GIF)');
        return;
    }
    
    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
        showError('File size must be less than 16MB');
        return;
    }
    
    uploadedImage = file;
    uploadedFileName = file.name;
    
    // Display filename
    document.getElementById('fileName').textContent = `Selected: ${file.name}`;
    
    // Show preview in chat
    const reader = new FileReader();
    reader.onload = function(e) {
        displayImagePreview(e.target.result);
    };
    reader.readAsDataURL(file);
}

function displayImagePreview(imageData) {
    clearWelcomeMessage();
    
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const img = document.createElement('img');
    img.src = imageData;
    img.className = 'image-preview';
    img.alt = 'Uploaded image';
    
    const text = document.createElement('p');
    text.textContent = '📸 Image uploaded';
    
    contentDiv.appendChild(text);
    contentDiv.appendChild(img);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    scrollToBottom();
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) {
        showError('Please enter a message');
        return;
    }
    
    if (!uploadedImage) {
        // Send text-only message
        displayUserMessage(message);
        messageInput.value = '';
        await sendTextMessage(message);
    } else {
        // Send image with query
        displayUserMessage(message);
        messageInput.value = '';
        await sendImageWithQuery(message);
    }
}

function displayUserMessage(message) {
    clearWelcomeMessage();
    
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = message;
    
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    scrollToBottom();
}

function displayBotMessage(message) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = message;
    
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    scrollToBottom();
}

function displayLoadingMessage() {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = 'loadingMessage';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<div class="loading"></div> Analyzing...';
    
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    scrollToBottom();
}

function removeLoadingMessage() {
    const loadingMsg = document.getElementById('loadingMessage');
    if (loadingMsg) {
        loadingMsg.remove();
    }
}

async function sendTextMessage(message) {
    displayLoadingMessage();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        removeLoadingMessage();
        
        if (data.success) {
            displayBotMessage(data.response);
        } else {
            showError(data.error || 'Failed to get response');
        }
    } catch (error) {
        removeLoadingMessage();
        showError('Network error. Please try again.');
        console.error('Error:', error);
    }
}

async function sendImageWithQuery(query) {
    displayLoadingMessage();
    
    const formData = new FormData();
    formData.append('image', uploadedImage);
    formData.append('query', query);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        removeLoadingMessage();
        
        if (data.success) {
            displayBotMessage(data.response);
            // Reset image after successful query
            resetImageUpload();
        } else {
            showError(data.error || 'Failed to process image');
        }
    } catch (error) {
        removeLoadingMessage();
        showError('Network error. Please try again.');
        console.error('Error:', error);
    }
}

function resetImageUpload() {
    uploadedImage = null;
    uploadedFileName = null;
    document.getElementById('fileName').textContent = '';
    document.getElementById('imageInput').value = '';
}

function showError(message) {
    const chatContainer = document.getElementById('chatContainer');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = '⚠️ ' + message;
    
    chatContainer.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 3000);
    
    scrollToBottom();
}

function clearWelcomeMessage() {
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.style.display = 'none';
    }
}

function scrollToBottom() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
