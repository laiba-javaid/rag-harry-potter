#!/usr/bin/env python3
# run.py - Quick launcher script for Harry Potter RAG System

"""
🏰 Harry Potter RAG System Launcher 🏰
Quick start script for the magical knowledge assistant
"""

import sys
import os
from pathlib import Path

def main():
    """Launch the Harry Potter RAG system"""
    
    # Add src to path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    try:
        # Import and run main application
        from main import main as run_app
        
        print("🪄 Starting magical application...")
        success = run_app()
        
        if success:
            print("✨ Application completed successfully!")
        else:
            print("❌ Application encountered errors")
            
        return success
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)