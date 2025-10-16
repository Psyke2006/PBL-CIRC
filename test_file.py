"""
Unit tests for the Conversational Image Recognition Chatbot
Run with: python -m pytest test_app.py
"""

import unittest
import os
import json
from app import app
from database import Database
from utils import allowed_file, generate_unique_filename, sanitize_input

class TestFlaskApp(unittest.TestCase):
    """Test Flask application endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_index_route(self):
        """Test index page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_chat_endpoint_success(self):
        """Test chat endpoint with valid message"""
        response = self.client.post('/api/chat',
                                   json={'message': 'Hello'},
                                   content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('response', data)
    
    def test_chat_endpoint_empty_message(self):
        """Test chat endpoint with empty message"""
        response = self.client.post('/api/chat',
                                   json={'message': ''},
                                   content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    def test_upload_endpoint_no_file(self):
        """Test upload endpoint without file"""
        response = self.client.post('/api/upload')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)


class TestDatabase(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        """Set up test database"""
        self.db = Database('test_chatbot.db')
    
    def tearDown(self):
        """Clean up test database"""
        if os.path.exists('test_chatbot.db'):
            os.remove('test_chatbot.db')
    
    def test_add_chat_message(self):
        """Test adding chat message"""
        message_id = self.db.add_chat_message(
            session_id='test_session',
            message_type='user',
            content='Test message'
        )
        self.assertIsNotNone(message_id)
        self.assertGreater(message_id, 0)
    
    def test_get_chat_history(self):
        """Test retrieving chat history"""
        session_id = 'test_session'
        self.db.add_chat_message(session_id, 'user', 'Message 1')
        self.db.add_chat_message(session_id, 'bot', 'Response 1')
        
        history = self.db.get_chat_history(session_id)
        self.assertEqual(len(history), 2)
    
    def test_add_image_upload(self):
        """Test recording image upload"""
        image_id = self.db.add_image_upload(
            filename='test.jpg',
            original_filename='original.jpg',
            file_path='/uploads/test.jpg',
            file_size=1024
        )
        self.assertIsNotNone(image_id)
        self.assertGreater(image_id, 0)
    
    def test_get_statistics(self):
        """Test getting database statistics"""
        stats = self.db.get_statistics()
        self.assertIn('total_messages', stats)
        self.assertIn('total_images', stats)


class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_allowed_file_valid(self):
        """Test allowed file with valid extension"""
        allowed_extensions = {'jpg', 'png', 'gif'}
        self.assertTrue(allowed_file('test.jpg', allowed_extensions))
        self.assertTrue(allowed_file('test.PNG', allowed_extensions))
    
    def test_allowed_file_invalid(self):
        """Test allowed file with invalid extension"""
        allowed_extensions = {'jpg', 'png', 'gif'}
        self.assertFalse(allowed_file('test.txt', allowed_extensions))
        self.assertFalse(allowed_file('test', allowed_extensions))
    
    def test_generate_unique_filename(self):
        """Test unique filename generation"""
        filename1 = generate_unique_filename('test.jpg')
        filename2 = generate_unique_filename('test.jpg')
        
        self.assertNotEqual(filename1, filename2)
        self.assertTrue(filename1.endswith('.jpg'))
    
    def test_sanitize_input(self):
        """Test input sanitization"""
        dangerous_input = "<script>alert('xss')</script>"
        sanitized = sanitize_input(dangerous_input)
        
        self.assertNotIn('<', sanitized)
        self.assertNotIn('>', sanitized)
    
    def test_sanitize_input_length(self):
        """Test input length limiting"""
        long_input = 'a' * 1000
        sanitized = sanitize_input(long_input, max_length=100)
        
        self.assertEqual(len(sanitized), 100)


class TestModelHandler(unittest.TestCase):
    """Test model handler functions"""
    
    def setUp(self):
        """Set up model handler"""
        from model_handler import ModelHandler
        self.handler = ModelHandler()
    
    def test_model_initialization(self):
        """Test model handler initialization"""
        self.assertIsNotNone(self.handler)
        self.assertEqual(self.handler.cnn_model_name, 'mobilenet_v2')
    
    def test_get_model_info(self):
        """Test getting model information"""
        info = self.handler.get_model_info()
        self.assertIn('cnn_model', info)
        self.assertIn('nlp_model', info)
    
    def test_generate_response(self):
        """Test response generation"""
        import numpy as np
        dummy_features = np.random.rand(1, 1768)
        response = self.handler.generate_response(dummy_features, "What is this?")
        
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)


def run_tests():
    """Run all tests"""
    unittest.main()


if __name__ == '__main__':
    run_tests()
