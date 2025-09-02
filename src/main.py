# src/main.py - Main application entry point
import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from rag_pipeline import harry_potter_rag
from groq_client import groq_client
from ui_components import HarryPotterUI

def validate_environment():
    """Validate the environment and configuration"""
    print("🔍 Validating environment...")
    print("=" * 50)
    
    # Check configuration
    config_errors = config.validate_config()
    
    if config_errors:
        print("❌ Configuration errors found:")
        for error in config_errors:
            print(f"   • {error}")
        return False
    
    # Check database
    db_info = config.get_database_info()
    if db_info:
        print("✅ Chroma Database Found:")
        print(f"   📁 Path: {db_info['path']}")
        print(f"   📊 Files: {db_info['files']}")
        print(f"   💾 Size: {db_info['size_mb']} MB")
    else:
        print("❌ Chroma database not found!")
        return False
    
    # Test Groq API
    print("\n🔗 Testing Groq API connection...")
    api_test = groq_client.test_connection()
    if api_test["status"] == "success":
        print("✅ Groq API connection successful")
    else:
        print(f"❌ Groq API test failed: {api_test['message']}")
        return False
    
    print("\n✅ Environment validation successful!")
    return True

def initialize_system():
    """Initialize the RAG system"""
    print("\n🏰 Initializing Harry Potter RAG System...")
    print("=" * 50)
    
    # Initialize RAG pipeline
    if not harry_potter_rag.initialize():
        print("❌ Failed to initialize RAG system")
        return False
    
    # Get system stats
    stats = harry_potter_rag.get_system_stats()
    if stats["status"] == "ready":
        print("\n📊 System Statistics:")
        print(f"   🎯 Status: {stats['status'].title()}")
        print(f"   🧠 Embedding Model: {stats['embedding_model']}")
        print(f"   💎 Collection: {stats['collection_name']}")
        print(f"   📚 Test Documents: {stats['test_documents_found']}")
        print(f"   🔍 Retrieval K: {stats['retrieval_k']}")
        print(f"   ⚡ Functional: {'Yes' if stats['is_functional'] else 'No'}")
    else:
        print(f"❌ System status: {stats['status']}")
        if "error" in stats:
            print(f"   Error: {stats['error']}")
        return False
    
    print("\n✅ RAG System initialized successfully!")
    return True

def create_interface():
    """Create and configure the UI interface"""
    print("\n🎨 Creating Magical User Interface...")
    print("=" * 50)
    
    try:
        # Initialize UI
        ui = HarryPotterUI()
        
        # Create interface with RAG pipeline
        interface = ui.create_interface(harry_potter_rag.generate_response)
        
        print("✅ UI created successfully!")
        return interface
        
    except Exception as e:
        print(f"❌ Failed to create UI: {str(e)}")
        return None

def launch_application():
    """Launch the complete application"""
    print("\n🚀 Launching Harry Potter RAG Assistant...")
    print("=" * 60)
    
    # Display launch information
    print(f"🌐 Server: http://{config.GRADIO_HOST}:{config.GRADIO_PORT}")
    print(f"🔧 Debug Mode: {'Enabled' if config.DEBUG_MODE else 'Disabled'}")
    print(f"🌍 Public Sharing: {'Enabled' if config.SHARE_LINK else 'Disabled'}")
    print(f"🎯 Models Available: {len(groq_client.get_available_models())}")
    
    # Create interface
    interface = create_interface()
    if not interface:
        print("❌ Failed to create interface")
        return False
    
    try:
        # Launch the interface
        interface.launch(
            server_name=config.GRADIO_HOST,
            server_port=config.GRADIO_PORT,
            share=config.SHARE_LINK,
            debug=config.DEBUG_MODE,
            show_error=True,
            max_threads=10,
            favicon_path=None
        )
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to launch application: {str(e)}")
        return False

def main():
    """Main application function"""
    print("⚡ HARRY POTTER RAG SYSTEM ⚡")
    print("🏰 Magical Knowledge Assistant 🏰")
    print("=" * 60)
    
    try:
        # Step 1: Validate environment
        if not validate_environment():
            print("\n❌ Environment validation failed. Please check your setup.")
            return False
        
        # Step 2: Initialize system
        if not initialize_system():
            print("\n❌ System initialization failed.")
            return False
        
        # Step 3: Launch application
        if not launch_application():
            print("\n❌ Application launch failed.")
            return False
        
        print("\n🎉 Harry Potter RAG System launched successfully!")
        print("🏰 Ready to answer your magical questions!")
        return True
        
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
        return True
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)