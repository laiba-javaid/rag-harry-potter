# src/rag_pipeline.py - RAG Pipeline for Harry Potter Knowledge System

# Updated imports with proper fallback handling
try:
    # Try newer langchain-huggingface first (most recommended)
    from langchain_huggingface import HuggingFaceEmbeddings
    print("✅ Using langchain_huggingface")
except ImportError:
    try:
        # Fallback to langchain-community
        from langchain_community.embeddings import HuggingFaceEmbeddings
        print("✅ Using langchain_community.embeddings")
    except ImportError:
        try:
            # Final fallback to older langchain
            from langchain.embeddings import HuggingFaceEmbeddings
            print("✅ Using langchain.embeddings")
        except ImportError as e:
            print(f"❌ HuggingFaceEmbeddings import error: {e}")
            print("💡 Try: pip install --upgrade langchain langchain-community sentence-transformers")
            raise

try:
    # Try langchain-chroma first (recommended)
    from langchain_chroma import Chroma
    print("✅ Using langchain_chroma")
except ImportError:
    try:
        # Fallback to langchain-community
        from langchain_community.vectorstores import Chroma
        print("✅ Using langchain_community.vectorstores")
    except ImportError:
        try:
            # Final fallback to older langchain
            from langchain.vectorstores import Chroma
            print("✅ Using langchain.vectorstores")
        except ImportError as e:
            print(f"❌ Chroma import error: {e}")
            print("💡 Try: pip install --upgrade langchain langchain-chroma chromadb")
            raise

from typing import List, Dict, Any
import os
from config import config
from groq_client import groq_client

class HarryPotterRAG:
    """RAG pipeline for Harry Potter knowledge retrieval"""
    
    def __init__(self, chroma_db_path: str = None):
        self.chroma_db_path = chroma_db_path or str(config.CHROMA_DB_PATH)
        self.embedding_model = None
        self.vectorstore = None
        self.retriever = None
        self.is_initialized = False
        
    def initialize(self) -> bool:
        """Initialize the RAG pipeline components"""
        try:
            print("🧠 Initializing Harry Potter RAG System...")
            
            # Check if database exists
            if not os.path.exists(self.chroma_db_path):
                raise FileNotFoundError(f"Chroma database not found at: {self.chroma_db_path}")
            
            # Test sentence-transformers import explicitly
            print("🔍 Testing sentence-transformers import...")
            try:
                import sentence_transformers
                print("✅ sentence-transformers imported successfully")
            except ImportError as e:
                print(f"❌ sentence-transformers import failed: {e}")
                print("💡 Install with: pip install sentence-transformers")
                raise ImportError("Could not import sentence_transformers python package. Please install it with `pip install sentence-transformers`.")
            
            # Initialize embedding model
            print("📥 Loading embedding model...")
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=config.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            # Load existing vector store
            print("💎 Loading existing vector database...")
            self.vectorstore = Chroma(
                persist_directory=self.chroma_db_path,
                embedding_function=self.embedding_model,
                collection_name=config.COLLECTION_NAME
            )
            
            # Create retriever - REMOVED score_threshold as it's not supported
            print("🔍 Setting up document retriever...")
            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": config.RETRIEVAL_K
                    # Removed "score_threshold": config.SCORE_THRESHOLD - not supported
                }
            )
            
            # Test the system - Updated to use invoke() instead of get_relevant_documents()
            print("🧪 Testing retriever...")
            
            # First check collection count
            try:
                collection_count = self.vectorstore._collection.count()
                print(f"📊 Collection '{config.COLLECTION_NAME}' contains {collection_count} documents")
                
                if collection_count == 0:
                    raise ValueError(f"Collection '{config.COLLECTION_NAME}' is empty - no documents found in database")
                
            except Exception as e:
                print(f"⚠️ Could not check collection count: {e}")
            
            # Test retrieval
            try:
                # Try the new method first
                test_docs = self.retriever.invoke("Harry Potter")
            except AttributeError:
                # Fallback to older method if available
                test_docs = self.retriever.get_relevant_documents("Harry Potter")
            
            if not test_docs:
                # Try alternative test queries
                test_queries = ["magic", "wizard", "Hogwarts", "book"]
                for query in test_queries:
                    try:
                        if hasattr(self.retriever, 'invoke'):
                            test_docs = self.retriever.invoke(query)
                        else:
                            test_docs = self.retriever.get_relevant_documents(query)
                        if test_docs:
                            print(f"✅ Found documents with query: '{query}'")
                            break
                    except:
                        continue
                
                if not test_docs:
                    raise ValueError("No documents found with any test query - database might be empty or misconfigured")
            
            self.is_initialized = True
            print("✅ RAG System initialized successfully!")
            print(f"📊 Found {len(test_docs)} test documents")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize RAG system: {str(e)}")
            return False
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze query to determine optimal retrieval strategy"""
        query_lower = query.lower()
        
        # Query type classification
        if any(phrase in query_lower for phrase in ["who is", "tell me about", "describe", "character"]):
            query_type = "character_analysis"
            k_docs = 4
        elif any(word in query_lower for word in ["summarize", "summary", "what happens", "events", "plot"]):
            query_type = "plot_summary"
            k_docs = 6
        elif any(word in query_lower for word in ["how", "why", "what", "where", "when", "trivia"]):
            query_type = "detail_query"
            k_docs = 3
        elif any(word in query_lower for word in ["compare", "difference", "vs", "versus"]):
            query_type = "comparison"
            k_docs = 5
        else:
            query_type = "general"
            k_docs = 5
        
        return {
            "type": query_type,
            "k_docs": k_docs,
            "complexity": len(query.split())
        }
    
    def retrieve_context(self, query: str, analysis: Dict = None) -> List[str]:
        """Retrieve relevant context with smart deduplication"""
        if not self.is_initialized:
            raise RuntimeError("RAG system not initialized. Call initialize() first.")
        
        analysis = analysis or self.analyze_query(query)
        
        # Get documents - Updated to use invoke() method
        try:
            # Try the new method first
            context_docs = self.retriever.invoke(query)
        except AttributeError:
            # Fallback to older method if available
            context_docs = self.retriever.get_relevant_documents(query)
        
        if not context_docs:
            return []
        
        # Smart context selection and deduplication
        context_parts = []
        seen_content = set()
        max_docs = analysis["k_docs"]
        
        for doc in context_docs[:max_docs]:
            content = doc.page_content.strip()
            
            # Create a hash for duplicate detection
            content_hash = hash(content[:100])  # Use first 100 chars for similarity
            
            if content_hash not in seen_content and len(content) > 50:
                context_parts.append(content)
                seen_content.add(content_hash)
        
        return context_parts
    
    def create_enhanced_prompt(self, query: str, context_parts: List[str], analysis: Dict) -> str:
        """Create an enhanced prompt based on query analysis"""
        
        context = "\n\n---\n\n".join(context_parts)
        
        # Base system instructions
        base_instructions = """You are an expert on the Harry Potter series with deep knowledge of all seven books. Use the provided context to answer the user's question comprehensively and accurately."""
        
        # Query-specific instructions
        type_instructions = {
            "character_analysis": "Focus on character development, personality traits, relationships, and key moments. Reference specific books when possible.",
            "plot_summary": "Organize information chronologically and provide a comprehensive overview of events. Include key details and outcomes.",
            "detail_query": "Be specific and precise with facts. Provide exact details and reference the source material.",
            "comparison": "Clearly contrast the different elements being compared. Use structured comparisons and specific examples.",
            "general": "Provide a well-rounded answer that covers all relevant aspects of the topic."
        }
        
        specific_instruction = type_instructions.get(analysis["type"], type_instructions["general"])
        
        prompt = f"""{base_instructions}

**Context from Harry Potter books:**
{context}

**User Question:** {query}

**Instructions:**
- {specific_instruction}
- Reference specific books, characters, or events when relevant
- If you're not completely certain about something, acknowledge it
- Keep the magical tone but be informative and accurate
- Structure your response clearly

**Answer:**"""

        return prompt
    
    def generate_response(self, query: str) -> str:
        """Generate a complete RAG response"""
        try:
            # Input validation
            if not query or not query.strip():
                return "🪄 Please cast a question spell by typing your query!"
            
            if not self.is_initialized:
                return "🚨 RAG system not initialized. Please check the setup."
            
            query = query.strip()
            
            # Analyze query
            analysis = self.analyze_query(query)
            
            # Retrieve context
            context_parts = self.retrieve_context(query, analysis)
            
            if not context_parts:
                return "🔍 I couldn't find relevant information in the Harry Potter books for your query. Try rephrasing your question or asking about specific characters, events, or magical elements."
            
            # Create enhanced prompt
            prompt = self.create_enhanced_prompt(query, context_parts, analysis)
            
            # Generate response using Groq
            response = groq_client.chat(prompt)
            
            # Format final response
            if response and not any(error_word in response.lower() for error_word in ["sorry", "error", "failed", "unavailable"]):
                num_sources = len(context_parts)
                
                enhanced_response = f"""🔮 **Magical Knowledge Retrieved:**

{response}

---
✨ *Answer compiled from {num_sources} relevant passages across the Harry Potter books*  
🏰 *Query type: {analysis['type'].replace('_', ' ').title()}*"""
                
                return enhanced_response
            else:
                return f"🧙‍♂️ **Magical Response:** {response}"
                
        except Exception as e:
            error_msg = f"An error occurred in the magical pipeline: {str(e)}"
            print(f"❌ {error_msg}")
            return f"🚨 **Spell Malfunction:** {error_msg}"
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        if not self.is_initialized:
            return {"status": "not_initialized"}
        
        try:
            # Test retrieval - Updated to use invoke() method
            try:
                test_docs = self.retriever.invoke("test")
            except AttributeError:
                test_docs = self.retriever.get_relevant_documents("test")
            
            return {
                "status": "ready",
                "database_path": self.chroma_db_path,
                "embedding_model": config.EMBEDDING_MODEL,
                "collection_name": config.COLLECTION_NAME,
                "test_documents_found": len(test_docs),
                "retrieval_k": config.RETRIEVAL_K,
                "is_functional": len(test_docs) > 0
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

# Create global RAG instance
harry_potter_rag = HarryPotterRAG()