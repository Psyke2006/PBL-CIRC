Conversational Image Recognition Chatbot
AI-based methodology to recognize and interpret visual information through conversational interaction.

Team Members
Radhika Patange
Pranjal Khandagale
Tanishkk Pachpute
Tanishka Mhetre
Faculty Guide: Prof. Nitin Alzende
Institution: MIT School of Computing, Department of Computer Science & Engineering
Class: SY0615 | Group ID: 15

Problem Statement
Conventional chatbots are limited to text or voice-based interactions and lack the ability to process and understand visual information. This creates a gap in human-computer interaction where users cannot effectively communicate contextual information through images. There is a need for an AI-based conversational chatbot that integrates image recognition with natural language processing, enabling more intuitive, intelligent, and human-like interactions for applications in diverse domains such as education, healthcare, and customer support.

Proposed Solution
The proposed solution is to develop a conversational chatbot that integrates image recognition with natural language processing. A convolutional neural network (CNN) will analyze images and extract features, which are combined with user queries to generate context-aware responses. This approach enables intelligent and human-like interaction with the system.

Features
📸 Image Upload: Support for JPEG, PNG, and GIF formats
💬 Natural Language Processing: Text-based query understanding
🤖 Context-Aware Responses: Combines visual and textual information
🎨 Modern UI: Clean and intuitive chat interface
⚡ Real-time Processing: Fast response generation
📱 Responsive Design: Works on desktop and mobile devices
Technology Stack
Frontend
HTML5
CSS3
JavaScript
Bootstrap
Backend
Python 3.8+
Flask
Flask-CORS
AI/ML
Image Processing: OpenCV, Pillow
CNN Model: MobileNetV2 (planned)
NLP: Hugging Face Transformers, DistilBERT (planned)
Framework: PyTorch/TensorFlow
Database
SQLite (for logging and history)
Project Structure
conversational-image-chatbot/
├── app.py                  # Flask backend main file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── static/
│   ├── css/
│   │   └── style.css      # Frontend styles
│   └── js/
│       └── script.js      # Frontend JavaScript
├── templates/
│   └── index.html         # Main HTML page
└── uploads/               # Image upload directory
Installation & Setup
Prerequisites
Python 3.8 or higher
pip (Python package manager)
Virtual environment (recommended)
Step 1: Clone the Repository
bash
git clone https://github.com/your-username/conversational-image-chatbot.git
cd conversational-image-chatbot
Step 2: Create Virtual Environment
bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
Step 3: Install Dependencies
bash
pip install -r requirements.txt
Step 4: Create Required Directories
bash
mkdir uploads
mkdir static/css
mkdir static/js
mkdir templates
Step 5: Run the Application
bash
python app.py
The application will start at http://localhost:5000

Usage
Open the Application: Navigate to http://localhost:5000 in your browser
Upload an Image: Click the "Upload Image" button and select an image file
Ask a Question: Type your question about the image in the text input
Get Response: The chatbot will analyze the image and respond to your query
API Endpoints
POST /api/upload
Upload an image with a text query

Request:

Method: POST
Content-Type: multipart/form-data
Body:
image: Image file (JPEG, PNG, GIF)
query: Text query string
Response:

json
{
  "success": true,
  "filename": "20251016_123456_image.jpg",
  "query": "What objects are in this image?",
  "response": "Based on the image analysis...",
  "timestamp": "20251016_123456"
}
POST /api/chat
Send a text-only message

Request:

json
{
  "message": "Hello, how can you help me?"
}
Response:

json
{
  "success": true,
  "message": "Hello, how can you help me?",
  "response": "Hello! I'm your conversational image recognition assistant..."
}
Development Roadmap
Sprint 1 (Completed) ✅
 Project setup and planning
 System architecture design
 UI/UX wireframe design
 Technology stack finalization
Sprint 2 (Completed) ✅
 Frontend HTML structure
 CSS styling and layout
 Image upload interface
 Chat interface design
Sprint 3 (Completed) ✅
 Flask backend setup
 API endpoint creation
 Frontend-backend integration
 Image handling functionality
Sprint 4 (In Progress) 🔄
 Response generation logic
 Chat functionality implementation
 Testing and bug fixes
 Prototype deployment
Future Enhancements 🚀
 CNN model integration (MobileNetV2)
 NLP model integration (DistilBERT)
 Feature fusion mechanism
 Offline model deployment
 Database integration for history
 Multi-language support
 Voice interaction
Applications
🎓 Education
Visual learning assistance
Homework help with diagrams
Interactive study tools
🏥 Healthcare
Medical image interpretation
Symptom analysis
Patient education
💼 Customer Support
Product identification
Troubleshooting with images
Visual documentation
♿ Accessibility
Assistance for visually impaired
Scene description
Object recognition
Testing
Manual Testing Checklist
 Image upload functionality
 File type validation
 File size validation
 Chat message sending
 Response generation
 Error handling
 UI responsiveness
 Cross-browser compatibility
Test Cases
Upload valid image → Should display preview and accept queries
Upload invalid file → Should show error message
Send text without image → Should provide text-only response
Send empty message → Should show validation error
Large file upload → Should validate size limit
Known Issues
Current version uses mock responses (CNN/NLP models not yet integrated)
Image history not persisted in database
Limited error handling for edge cases
Contributing
Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
License
This project is developed as part of academic coursework at MIT School of Computing.

Acknowledgments
Faculty Guide: Prof. Nitin Alzende
MIT School of Computing
Department of Computer Science & Engineering
Contact
For questions or feedback, please contact the team members through the MIT School of Computing.

Last Updated: October 16, 2025
Version: 1.0.0 (Web Prototype)
