# database_troubleshoot.py - Troubleshoot Chroma database issues

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from config import config
    from langchain_chroma import Chroma
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're in the right directory and dependencies are installed")
    sys.exit(1)

def check_database_structure():
    """Check the structure of the Chroma database"""
    print("🔍 TROUBLESHOOTING CHROMA DATABASE")
    print("=" * 50)
    
    db_path = str(config.CHROMA_DB_PATH)
    print(f"📁 Database Path: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ Database directory doesn't exist!")
        return False
    
    # List all files in the database directory
    print("\n📂 Database Directory Contents:")
    for root, dirs, files in os.walk(db_path):
        level = root.replace(db_path, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            print(f"{subindent}{file} ({size} bytes)")
    
    return True

def test_direct_chroma_access():
    """Test direct access to Chroma database"""
    print("\n🧪 TESTING DIRECT CHROMA ACCESS")
    print("=" * 50)
    
    try:
        # Initialize embedding model
        print("📥 Loading embedding model...")
        embedding_model = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("✅ Embedding model loaded")
        
        # Try to load the vector store
        print("💎 Loading vector database...")
        vectorstore = Chroma(
            persist_directory=str(config.CHROMA_DB_PATH),
            embedding_function=embedding_model,
            collection_name=config.COLLECTION_NAME
        )
        print("✅ Vector store loaded")
        
        # Check the collection
        print("\n📊 COLLECTION INFORMATION")
        print("-" * 30)
        
        # Get collection info
        collection = vectorstore._collection
        print(f"Collection name: {collection.name}")
        print(f"Collection count: {collection.count()}")
        
        if collection.count() == 0:
            print("❌ Collection is empty!")
            return False
        
        # Try to peek at some documents
        print("\n📖 SAMPLE DOCUMENTS")
        print("-" * 30)
        
        # Get first few documents
        results = collection.peek(limit=3)
        if results and 'documents' in results:
            for i, doc in enumerate(results['documents'][:3]):
                print(f"\nDocument {i+1}:")
                print(f"Content preview: {doc[:200]}...")
                if 'metadatas' in results and i < len(results['metadatas']):
                    print(f"Metadata: {results['metadatas'][i]}")
        
        # Test similarity search
        print("\n🔍 TESTING SIMILARITY SEARCH")
        print("-" * 30)
        
        test_queries = ["Harry Potter", "Hogwarts", "magic", "wizard"]
        
        for query in test_queries:
            print(f"\nTesting query: '{query}'")
            try:
                docs = vectorstore.similarity_search(query, k=2)
                print(f"  Found {len(docs)} documents")
                if docs:
                    print(f"  First result preview: {docs[0].page_content[:100]}...")
                else:
                    print("  No documents found")
            except Exception as e:
                print(f"  Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")
        return False

def test_different_collection_names():
    """Test if documents exist under different collection names"""
    print("\n🔎 TESTING DIFFERENT COLLECTION NAMES")
    print("=" * 50)
    
    possible_names = [
        config.COLLECTION_NAME,
        "harry_potter",
        "harry-potter", 
        "default",
        "langchain",
        "documents"
    ]
    
    try:
        embedding_model = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        for collection_name in possible_names:
            print(f"\n🔍 Trying collection: '{collection_name}'")
            try:
                vectorstore = Chroma(
                    persist_directory=str(config.CHROMA_DB_PATH),
                    embedding_function=embedding_model,
                    collection_name=collection_name
                )
                
                collection = vectorstore._collection
                count = collection.count()
                print(f"  Count: {count}")
                
                if count > 0:
                    print(f"  ✅ Found {count} documents in collection '{collection_name}'!")
                    
                    # Test a simple search
                    docs = vectorstore.similarity_search("Harry", k=1)
                    if docs:
                        print(f"  Sample doc: {docs[0].page_content[:100]}...")
                        print(f"  🎯 SOLUTION: Use collection_name='{collection_name}'")
                        return collection_name
                
            except Exception as e:
                print(f"  Error: {e}")
                
    except Exception as e:
        print(f"❌ Error in collection testing: {e}")
    
    return None

def main():
    """Main troubleshooting function"""
    print("🪄 HARRY POTTER RAG DATABASE TROUBLESHOOTER")
    print("=" * 60)
    
    # Step 1: Check database structure
    if not check_database_structure():
        print("\n❌ Database structure check failed")
        return
    
    # Step 2: Test direct Chroma access
    if test_direct_chroma_access():
        print("\n✅ Database appears to be working correctly!")
        print("The issue might be with the retriever configuration.")
    else:
        print("\n❌ Database access failed")
        
        # Step 3: Test different collection names
        working_collection = test_different_collection_names()
        
        if working_collection:
            print(f"\n🎯 SOLUTION FOUND!")
            print(f"Update your config.py to use:")
            print(f"COLLECTION_NAME = '{working_collection}'")
        else:
            print("\n❌ No documents found in any collection")
            print("You may need to recreate the database or check the data ingestion process")

if __name__ == "__main__":
    main()