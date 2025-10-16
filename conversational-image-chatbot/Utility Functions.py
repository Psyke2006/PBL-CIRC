import os
import uuid
from datetime import datetime
from PIL import Image
import cv2
import numpy as np

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_unique_filename(original_filename):
    """Generate unique filename with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    return f"{timestamp}_{unique_id}.{ext}"

def validate_image(file_path):
    """Validate if file is a valid image"""
    try:
        img = Image.open(file_path)
        img.verify()
        return True
    except Exception as e:
        print(f"Image validation error: {e}")
        return False

def get_image_info(file_path):
    """Get image information"""
    try:
        img = Image.open(file_path)
        return {
            'width': img.width,
            'height': img.height,
            'format': img.format,
            'mode': img.mode,
            'size': os.path.getsize(file_path)
        }
    except Exception as e:
        print(f"Error getting image info: {e}")
        return None

def preprocess_image(file_path, target_size=(224, 224)):
    """Preprocess image for CNN model input"""
    try:
        # Read image
        img = cv2.imread(file_path)
        if img is None:
            return None
        
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize
        img = cv2.resize(img, target_size)
        
        # Normalize pixel values to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    except Exception as e:
        print(f"Image preprocessing error: {e}")
        return None

def create_thumbnail(file_path, output_path, size=(150, 150)):
    """Create thumbnail of image"""
    try:
        img = Image.open(file_path)
        img.thumbnail(size, Image.Resampling.LANCZOS)
        img.save(output_path)
        return True
    except Exception as e:
        print(f"Thumbnail creation error: {e}")
        return False

def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def clean_old_uploads(upload_folder, days=7):
    """Clean old uploaded files"""
    try:
        current_time = datetime.now()
        deleted_count = 0
        
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                age_days = (current_time - file_time).days
                
                if age_days > days:
                    os.remove(file_path)
                    deleted_count += 1
        
        return deleted_count
    except Exception as e:
        print(f"Error cleaning old uploads: {e}")
        return 0

def sanitize_input(text, max_length=500):
    """Sanitize user input"""
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Limit length
    text = text[:max_length]
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '{', '}', '\\', ';']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text

def extract_keywords(text):
    """Extract keywords from text (simple implementation)"""
    # Common words to ignore
    stopwords = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or'}
    
    # Convert to lowercase and split
    words = text.lower().split()
    
    # Filter out stopwords and short words
    keywords = [word for word in words if word not in stopwords and len(word) > 2]
    
    return keywords

def generate_session_id():
    """Generate unique session ID"""
    return str(uuid.uuid4())

def log_error(error, context=""):
    """Log error with context"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {context}: {str(error)}\n"
    
    try:
        with open('error.log', 'a') as f:
            f.write(log_message)
    except Exception as e:
        print(f"Failed to write to log file: {e}")
    
    print(log_message)

def create_required_directories():
    """Create required directories if they don't exist"""
    directories = ['uploads', 'static/css', 'static/js', 'templates', 'models']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' ready")

if __name__ == "__main__":
    # Test utility functions
    create_required_directories()
    print("Utility functions ready!")
