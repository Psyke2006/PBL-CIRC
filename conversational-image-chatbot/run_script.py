#!/usr/bin/env python3
"""
Application Runner
Starts the Flask application with proper configuration
"""

import os
import sys
from app import app
from utils import create_required_directories
from database import db

def check_environment():
    """Check if environment is properly set up"""
    print("Checking environment...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required!")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check required directories
    create_required_directories()
    print("✓ Required directories ready")
    
    # Check database
    try:
        stats = db.get_statistics()
        print(f"✓ Database ready (Messages: {stats['total_messages']}, Images: {stats['total_images']})")
    except Exception as e:
        print(f"Warning: Database issue - {e}")
    
    print("")

def print_banner():
    """Print application banner"""
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║   Conversational Image Recognition Chatbot                 ║
    ║   MIT School of Computing                                  ║
    ║   Team: Radhika, Pranjal, Tanishkk, Tanishka              ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_info():
    """Print application information"""
    print("Server Information:")
    print(f"  • Environment: {'Development' if app.config['DEBUG'] else 'Production'}")
    print(f"  • Host: 0.0.0.0")
    print(f"  • Port: 5000")
    print(f"  • URL: http://localhost:5000")
    print("")
    print("API Endpoints:")
    print("  • POST /api/upload - Upload image with query")
    print("  • POST /api/chat - Send text message")
    print("  • GET /api/history - Get chat history")
    print("")
    print("Press CTRL+C to stop the server")
    print("="*60)
    print("")

def main():
    """Main function to run the application"""
    try:
        # Print banner
        print_banner()
        
        # Check environment
        check_environment()
        
        # Print info
        print_info()
        
        # Run application
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
        
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        print("Goodbye! 👋")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
