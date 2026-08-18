"""
RAG Knowledge Base Ingestion Script
Loads agricultural documents into the vector database

Run this script once to initialize the RAG knowledge base:
    python scripts/ingest_knowledge_base.py

Or to reset and reload:
    python scripts/ingest_knowledge_base.py --reset
"""
import sys
import os
from pathlib import Path
import logging
import argparse

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.rag_service import get_rag_service
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Split text into chunks with overlap for better context preservation
    
    Args:
        text: Text to chunk
        chunk_size: Approximate size of each chunk in characters
        overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    # Split by paragraphs first
    paragraphs = text.split('\n\n')
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        # If adding this paragraph would exceed chunk size, save current chunk
        if len(current_chunk) + len(para) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Start new chunk with overlap from previous
            words = current_chunk.split()
            overlap_text = " ".join(words[-overlap:]) if len(words) > overlap else current_chunk
            current_chunk = overlap_text + "\n\n" + para
        else:
            current_chunk += "\n\n" + para if current_chunk else para
    
    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


def load_document(file_path: Path) -> dict:
    """Load a single document and extract metadata"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata from filename
        filename = file_path.stem
        category = file_path.parent.name if file_path.parent.name != 'knowledge_base' else 'general'
        
        return {
            'content': content,
            'metadata': {
                'source': str(file_path),
                'filename': filename,
                'category': category,
                'type': 'agricultural_knowledge'
            }
        }
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return None


def ingest_knowledge_base(reset: bool = False):
    """
    Ingest all documents from knowledge base into RAG system
    
    Args:
        reset: If True, reset the database before ingestion
    """
    logger.info("=" * 60)
    logger.info("RAG Knowledge Base Ingestion")
    logger.info("=" * 60)
    
    # Get RAG service
    rag_service = get_rag_service()
    
    if not rag_service.enabled:
        logger.error("❌ RAG service is not enabled!")
        logger.error("Please install required packages:")
        logger.error("  pip install chromadb sentence-transformers langchain-community")
        return False
    
    # Reset database if requested
    if reset:
        logger.info("🔄 Resetting RAG database...")
        rag_service.reset_database()
        logger.info("✅ Database reset complete")
    
    # Get knowledge base path
    knowledge_base_path = Path(os.getenv('KNOWLEDGE_BASE_PATH', './knowledge_base'))
    
    if not knowledge_base_path.exists():
        logger.error(f"❌ Knowledge base directory not found: {knowledge_base_path}")
        return False
    
    logger.info(f"📁 Loading documents from: {knowledge_base_path}")
    
    # Find all text files
    text_files = list(knowledge_base_path.rglob('*.txt'))
    text_files.extend(knowledge_base_path.rglob('*.md'))
    
    if not text_files:
        logger.warning(f"⚠️ No documents found in {knowledge_base_path}")
        return False
    
    logger.info(f"📚 Found {len(text_files)} documents")
    
    # Process each document
    total_chunks = 0
    successful_docs = 0
    
    for file_path in text_files:
        logger.info(f"\n📄 Processing: {file_path.name}")
        
        # Load document
        doc = load_document(file_path)
        if not doc:
            continue
        
        # Chunk the document
        chunks = chunk_text(doc['content'], chunk_size=500, overlap=50)
        logger.info(f"   Split into {len(chunks)} chunks")
        
        # Prepare documents and metadata for ingestion
        documents = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:  # Skip very short chunks
                continue
            
            documents.append(chunk)
            
            # Create metadata for each chunk
            chunk_metadata = doc['metadata'].copy()
            chunk_metadata['chunk_id'] = i
            chunk_metadata['total_chunks'] = len(chunks)
            metadatas.append(chunk_metadata)
            
            # Generate unique ID
            ids.append(f"{file_path.stem}_chunk_{i}")
        
        # Add to RAG database
        if documents:
            success = rag_service.add_documents(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            if success:
                total_chunks += len(documents)
                successful_docs += 1
                logger.info(f"   ✅ Added {len(documents)} chunks to database")
            else:
                logger.error(f"   ❌ Failed to add document to database")
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("Ingestion Summary")
    logger.info("=" * 60)
    logger.info(f"✅ Documents processed: {successful_docs}/{len(text_files)}")
    logger.info(f"✅ Total chunks created: {total_chunks}")
    
    # Get statistics
    stats = rag_service.get_statistics()
    logger.info(f"✅ Database contains: {stats['total_documents']} documents")
    if 'embedding_model' in stats:
        logger.info(f"✅ Embedding model: {stats['embedding_model']}")
    if 'mode' in stats:
        logger.info(f"✅ RAG Mode: {stats['mode']}")
    logger.info(f"✅ Vector DB path: {stats['vector_db_path']}")
    logger.info("=" * 60)
    
    # Test query
    logger.info("\n🔍 Testing RAG with sample query...")
    test_query = "How to treat tomato early blight?"
    results = rag_service.query(test_query, n_results=2)
    
    if results:
        logger.info(f"✅ Query successful! Found {len(results)} relevant documents")
        logger.info(f"\nSample result:")
        logger.info(f"  {results[0]['document'][:200]}...")
    else:
        logger.warning("⚠️ No results found for test query")
    
    logger.info("\n✅ RAG Knowledge Base ingestion complete!")
    logger.info("You can now use RAG in your chatbot!")
    
    return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Ingest agricultural knowledge into RAG database')
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset the database before ingestion'
    )
    
    args = parser.parse_args()
    
    try:
        success = ingest_knowledge_base(reset=args.reset)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n⚠️ Ingestion interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Error during ingestion: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
