import sqlite3
from datetime import datetime
import json

class Database:
    """Database handler for chat history and user interactions"""
    
    def __init__(self, db_path='chatbot.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create chat_history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                message_type TEXT NOT NULL,
                content TEXT NOT NULL,
                image_path TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create image_uploads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS image_uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER,
                upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create queries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id INTEGER,
                query_text TEXT NOT NULL,
                response_text TEXT,
                query_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (image_id) REFERENCES image_uploads (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_chat_message(self, session_id, message_type, content, image_path=None):
        """Add a chat message to history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_history (session_id, message_type, content, image_path)
            VALUES (?, ?, ?, ?)
        ''', (session_id, message_type, content, image_path))
        
        conn.commit()
        message_id = cursor.lastrowid
        conn.close()
        
        return message_id
    
    def get_chat_history(self, session_id, limit=50):
        """Get chat history for a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def add_image_upload(self, filename, original_filename, file_path, file_size):
        """Record an image upload"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO image_uploads (filename, original_filename, file_path, file_size)
            VALUES (?, ?, ?, ?)
        ''', (filename, original_filename, file_path, file_size))
        
        conn.commit()
        image_id = cursor.lastrowid
        conn.close()
        
        return image_id
    
    def add_query(self, image_id, query_text, response_text):
        """Record a query and response"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO queries (image_id, query_text, response_text)
            VALUES (?, ?, ?)
        ''', (image_id, query_text, response_text))
        
        conn.commit()
        query_id = cursor.lastrowid
        conn.close()
        
        return query_id
    
    def get_recent_queries(self, limit=10):
        """Get recent queries"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT q.*, i.filename, i.original_filename
            FROM queries q
            LEFT JOIN image_uploads i ON q.image_id = i.id
            ORDER BY q.query_timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def clear_old_data(self, days=30):
        """Clear data older than specified days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM chat_history
            WHERE timestamp < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        cursor.execute('''
            DELETE FROM queries
            WHERE query_timestamp < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()
        
        return deleted_count
    
    def get_statistics(self):
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total messages
        cursor.execute('SELECT COUNT(*) as count FROM chat_history')
        stats['total_messages'] = cursor.fetchone()['count']
        
        # Total images
        cursor.execute('SELECT COUNT(*) as count FROM image_uploads')
        stats['total_images'] = cursor.fetchone()['count']
        
        # Total queries
        cursor.execute('SELECT COUNT(*) as count FROM queries')
        stats['total_queries'] = cursor.fetchone()['count']
        
        # Today's activity
        cursor.execute('''
            SELECT COUNT(*) as count FROM chat_history
            WHERE DATE(timestamp) = DATE('now')
        ''')
        stats['today_messages'] = cursor.fetchone()['count']
        
        conn.close()
        
        return stats

# Initialize database instance
db = Database()
