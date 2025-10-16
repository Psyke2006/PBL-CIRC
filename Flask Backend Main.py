from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import base64
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """Handle image upload and return analysis"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        query = request.form.get('query', '')
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Mock response for prototype (replace with actual CNN/NLP model)
            response = generate_mock_response(filename, query)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'query': query,
                'response': response,
                'timestamp': timestamp
            })
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle text-only chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Mock response for prototype
        response = generate_text_response(message)
        
        return jsonify({
            'success': True,
            'message': message,
            'response': response
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_mock_response(filename, query):
    """Generate mock response based on image and query (prototype only)"""
    responses = {
        'what': f"Based on the uploaded image '{filename}', I can see various elements. {query}",
        'how': f"The image shows certain patterns. To answer '{query}', I would analyze the visual features.",
        'identify': f"From the image analysis, I can identify several objects related to your query: '{query}'",
        'explain': f"Let me explain what I see in the image regarding '{query}'..."
    }
    
    for keyword, response in responses.items():
        if keyword in query.lower():
            return response
    
    return f"I've analyzed your image. Regarding '{query}', the visual content suggests relevant information that can help answer your question."

def generate_text_response(message):
    """Generate mock text response (prototype only)"""
    if 'hello' in message.lower() or 'hi' in message.lower():
        return "Hello! I'm your conversational image recognition assistant. You can upload an image and ask questions about it!"
    elif 'help' in message.lower():
        return "I can help you analyze images! Just upload an image and ask questions like 'What objects are in this image?' or 'Describe what you see.'"
    elif 'how' in message.lower():
        return "To use this chatbot: 1) Upload an image, 2) Type your question about the image, 3) I'll analyze and respond with relevant information."
    else:
        return f"I received your message: '{message}'. Please upload an image so I can provide visual analysis along with answering your questions!"

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get chat history (mock implementation)"""
    return jsonify({
        'success': True,
        'history': []
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
