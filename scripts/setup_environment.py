#!/usr/bin/env python3
# scripts/setup_environment.py - Environment setup script

"""
🏰 Harry Potter RAG System - Environment Setup 🏰
This script helps set up your local development environment
"""

import os
import sys
import shutil
from pathlib import Path

def create_directory_structure():
    """Create the project directory structure"""
    print("📁 Creating project directory structure...")
    
    directories = [
        "data/chroma_db",
        "src"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {dir_path}")
    
    # Create __init__.py files
    init_files = ["src/__init__.py"]
    for init_file in init_files:
        Path(init_file).touch()
        print(f"   📄 Created: {init_file}")

def check_chroma_database():
    """Check if Chroma database exists"""
    print("\n💾 Checking Chroma Database...")
    
    data_dir = Path("data/chroma_db")
    
    if data_dir.exists() and any(data_dir.iterdir()):
        print("   ✅ Chroma database found!")
        
        # Show database info
        db_files = list(data_dir.glob("*"))
        total_size = sum(f.stat().st_size for f in db_files if f.is_file())
        
        print(f"   📊 Files: {len(db_files)}")
        print(f"   💾 Size: {round(total_size / (1024 * 1024), 2)} MB")
        return True
    else:
        print("   ❌ Chroma database not found!")
        print("   📋 Please copy your Chroma database files to: data/chroma_db/")
        print("   📂 Your database should include files like:")
        print("      • chroma.sqlite3")
        print("      • Various UUID-named directories")
        print("      • index files")
        return False

def setup_environment_file():
    """Set up the .env file"""
    print("\n🔧 Setting up environment variables...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("   ✅ .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("   📄 Copied .env.example to .env")
    else:
        # Create basic .env file
        env_content = """# Harry Potter RAG System Environment Variables
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here
"""
        env_file.write_text(env_content)
        print("   📄 Created basic .env file")
    
    print("   ⚠️  Please edit .env file and add your API keys!")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        "langchain",
        "chromadb", 
        "gradio",
        "sentence_transformers",
        "requests",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   📥 Install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        print("   OR")
        print("   pip install -r requirements.txt")
        return False
    
    print("   ✅ All required packages are installed!")
    return True

def test_setup():
    """Test the setup"""
    print("\n🧪 Testing setup...")
    
    # Test imports and basic configuration
    try:
        sys.path.insert(0, "src")
        from config import config
        print("   ✅ Configuration module loads correctly")
        
        # Test database path
        if config.CHROMA_DB_PATH.exists():
            print("   ✅ Chroma database path exists")
        else:
            print("   ❌ Chroma database path not found")
            return False
            
        # Test config validation
        errors = config.validate_config()
        if errors:
            print("   ❌ Configuration errors:")
            for error in errors:
                print(f"      • {error}")
            return False
        else:
            print("   ✅ Configuration validation passed")
            
    except Exception as e:
        print(f"   ❌ Setup test failed: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🏰 HARRY POTTER RAG SYSTEM - SETUP 🏰")
    print("=" * 50)
    
    try:
        # Step 1: Create directories
        create_directory_structure()
        
        # Step 2: Check database
        if not check_chroma_database():
            print("\n❌ Database setup incomplete. Please copy your Chroma database files.")
            print("   Run this script again after copying the database.")
            return False
        
        # Step 3: Setup environment
        setup_environment_file()
        
        # Step 4: Check dependencies
        if not check_dependencies():
            print("\n❌ Missing dependencies. Please install them and run again.")
            return False
        
        # Step 5: Test setup
        if not test_setup():
            print("\n❌ Setup test failed. Please check your configuration.")
            return False
        
        print("\n🎉 Setup completed successfully!")
        print("🚀 You can now run: python run.py")
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)