#!/usr/bin/env python3
# install_dependencies.py - Smart dependency installer with conflict resolution

"""
🔧 Harry Potter RAG System - Dependency Installer 🔧
Handles dependency conflicts and ensures clean installation
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def clean_install():
    """Perform a clean installation resolving dependency conflicts"""
    print("🏰 HARRY POTTER RAG SYSTEM - DEPENDENCY INSTALLER 🏰")
    print("=" * 60)
    
    # Step 1: Upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Step 2: Install core dependencies first (most stable versions)
    core_deps = [
        "numpy>=1.24.3,<2.0.0",
        "pandas>=2.1.4", 
        "scipy>=1.11.4",
        "scikit-learn>=1.3.2",
        "typing-extensions>=4.12.0",
        "tqdm>=4.66.1"
    ]
    
    print("\n📦 Installing core dependencies...")
    for dep in core_deps:
        if not run_command(f"{sys.executable} -m pip install '{dep}'", f"Installing {dep.split('>=')[0]}"):
            print(f"⚠️ Warning: Failed to install {dep}")
    
    # Step 3: Install pydantic with proper version
    if not run_command(f"{sys.executable} -m pip install 'pydantic>=2.7.0,<3.0.0'", "Installing Pydantic"):
        return False
    
    # Step 4: Install LangChain ecosystem (compatible versions)
    langchain_deps = [
        "langchain-core>=0.3.15,<0.4.0",
        "langchain>=0.3.0,<0.4.0", 
        "langchain-community>=0.3.0,<0.4.0"
    ]
    
    print("\n🦜 Installing LangChain ecosystem...")
    for dep in langchain_deps:
        if not run_command(f"{sys.executable} -m pip install '{dep}'", f"Installing {dep.split('>=')[0]}"):
            print(f"⚠️ Warning: Failed to install {dep}")
    
    # Step 5: Install AI/ML libraries
    ai_deps = [
        "sentence-transformers>=2.7.0",
        "transformers>=4.40.0",
        "torch>=2.3.0",
        "huggingface-hub>=0.23.4"
    ]
    
    print("\n🧠 Installing AI/ML libraries...")
    for dep in ai_deps:
        if not run_command(f"{sys.executable} -m pip install '{dep}'", f"Installing {dep.split('>=')[0]}"):
            print(f"⚠️ Warning: Failed to install {dep}")
    
    # Step 6: Install remaining dependencies
    other_deps = [
        "chromadb>=0.4.24",
        "requests>=2.32.3",
        "groq>=0.9.0",
        "gradio>=4.44.0",
        "python-dotenv>=1.0.1",
        "httpx>=0.27.0",
        "httpx-sse>=0.4.0"
    ]
    
    print("\n🔧 Installing remaining dependencies...")
    for dep in other_deps:
        if not run_command(f"{sys.executable} -m pip install '{dep}'", f"Installing {dep.split('>=')[0]}"):
            print(f"⚠️ Warning: Failed to install {dep}")
    
    # Step 7: Final verification
    print("\n🔍 Verifying installation...")
    
    test_imports = [
        ("langchain", "LangChain"),
        ("langchain_community", "LangChain Community"),
        ("sentence_transformers", "Sentence Transformers"),
        ("chromadb", "ChromaDB"),
        ("gradio", "Gradio"),
        ("requests", "Requests"),
        ("groq", "Groq")
    ]
    
    failed_imports = []
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError as e:
            print(f"   ❌ {name} - {str(e)}")
            failed_imports.append(name)
    
    if failed_imports:
        print(f"\n⚠️ Some packages failed to import: {', '.join(failed_imports)}")
        print("💡 Try running: pip install --force-reinstall -r requirements.txt")
        return False
    
    print("\n🎉 All dependencies installed successfully!")
    print("🚀 You can now run: python run.py")
    return True

def alternative_install():
    """Alternative installation method using requirements.txt"""
    print("\n🔄 Trying alternative installation method...")
    
    # First, try to resolve conflicts by upgrading all packages
    if not run_command(f"{sys.executable} -m pip install --upgrade --force-reinstall -r requirements.txt", 
                      "Force reinstalling from requirements.txt"):
        return False
    
    print("✅ Alternative installation completed!")
    return True

def main():
    """Main installation function"""
    try:
        # Method 1: Clean step-by-step install
        if clean_install():
            return True
        
        print("\n🔄 Clean install failed, trying alternative method...")
        
        # Method 2: Force reinstall from requirements.txt
        if alternative_install():
            return True
        
        print("\n❌ Both installation methods failed!")
        print("\n💡 Manual steps to try:")
        print("1. pip install --upgrade pip")
        print("2. pip uninstall langchain langchain-community langchain-core -y")
        print("3. pip install langchain>=0.3.0 langchain-community>=0.3.0")
        print("4. pip install -r requirements.txt")
        
        return False
        
    except KeyboardInterrupt:
        print("\n\n🛑 Installation cancelled by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error during installation: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)