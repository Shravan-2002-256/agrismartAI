"""
Knowledge Base Loader - Populate MongoDB with Agricultural Knowledge + Embeddings

This script:
1. Reads markdown files from data/knowledge_base/
2. Splits them into semantic chunks
3. Generates 768-dim embeddings using Ollama (nomic-embed-text)
4. Stores in MongoDB knowledge_base collection

Run: python populate_knowledge_base.py
"""

import os
import sys
import re
import requests
import pymongo
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "nomic-embed-text"
MONGODB_URL = "mongodb://localhost:27017"
MONGODB_DB = "agrismart_dev"
KNOWLEDGE_BASE_DIR = Path(__file__).parent / "data" / "knowledge_base"

# Chunking parameters
CHUNK_SIZE = 500  # characters per chunk
CHUNK_OVERLAP = 100  # overlap between chunks


def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
    except:
        pass
    
    print("❌ Ollama is not running. Start it with: ollama serve")
    print("   Then pull the model: ollama pull nomic-embed-text")
    return False


def generate_embedding(text: str) -> List[float]:
    """Generate 768-dimensional embedding using Ollama"""
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/embeddings",
            json={
                "model": OLLAMA_MODEL,
                "prompt": text
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["embedding"]
        else:
            print(f"⚠️ Embedding generation failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Embedding error: {e}")
        return None


def split_into_chunks(text: str, heading: str = "") -> List[Dict]:
    """
    Split markdown text into semantic chunks
    Returns list of {text, metadata} dicts
    """
    chunks = []
    
    # Split by sections (## headings)
    sections = re.split(r'\n## ', text)
    
    for section in sections:
        if not section.strip():
            continue
        
        # Extract section title
        lines = section.split('\n', 1)
        section_title = lines[0].strip('#').strip()
        section_content = lines[1] if len(lines) > 1 else ""
        
        # Split long sections into smaller chunks
        if len(section_content) > CHUNK_SIZE:
            # Split by paragraphs
            paragraphs = section_content.split('\n\n')
            current_chunk = ""
            
            for para in paragraphs:
                if len(current_chunk) + len(para) < CHUNK_SIZE:
                    current_chunk += para + "\n\n"
                else:
                    if current_chunk.strip():
                        chunks.append({
                            "text": f"{section_title}\n\n{current_chunk.strip()}",
                            "section": section_title,
                            "parent_heading": heading
                        })
                    current_chunk = para + "\n\n"
            
            # Add remaining chunk
            if current_chunk.strip():
                chunks.append({
                    "text": f"{section_title}\n\n{current_chunk.strip()}",
                    "section": section_title,
                    "parent_heading": heading
                })
        else:
            # Small section - keep as single chunk
            chunks.append({
                "text": f"{section_title}\n\n{section_content.strip()}",
                "section": section_title,
                "parent_heading": heading
            })
    
    return chunks


def load_markdown_files() -> List[Dict]:
    """Load and process all markdown files"""
    documents = []
    
    if not KNOWLEDGE_BASE_DIR.exists():
        print(f"❌ Knowledge base directory not found: {KNOWLEDGE_BASE_DIR}")
        return documents
    
    md_files = list(KNOWLEDGE_BASE_DIR.glob("*.md"))
    
    if not md_files:
        print(f"❌ No markdown files found in {KNOWLEDGE_BASE_DIR}")
        return documents
    
    print(f"\n📚 Found {len(md_files)} markdown files")
    
    for md_file in md_files:
        print(f"\n   Processing: {md_file.name}")
        
        try:
            content = md_file.read_text(encoding='utf-8')
            
            # Extract main title (first # heading)
            title_match = re.match(r'#\s+(.+)', content)
            title = title_match.group(1) if title_match else md_file.stem
            
            # Split into chunks
            chunks = split_into_chunks(content, heading=title)
            
            # Add metadata to each chunk
            for chunk in chunks:
                chunk['source_file'] = md_file.name
                chunk['title'] = title
                chunk['created_at'] = datetime.utcnow()
            
            documents.extend(chunks)
            print(f"      → Created {len(chunks)} chunks")
            
        except Exception as e:
            print(f"      ❌ Error processing {md_file.name}: {e}")
    
    return documents


def populate_mongodb(documents: List[Dict]):
    """Store documents with embeddings in MongoDB"""
    try:
        client = pymongo.MongoClient(MONGODB_URL)
        db = client[MONGODB_DB]
        collection = db.knowledge_base
        
        print(f"\n📊 Connected to MongoDB: {MONGODB_DB}")
        
        # Clear existing data
        existing_count = collection.count_documents({})
        if existing_count > 0:
            print(f"   Clearing {existing_count} existing documents...")
            collection.delete_many({})
        
        # Generate embeddings and insert
        print(f"\n🔢 Generating embeddings for {len(documents)} chunks...")
        
        inserted_count = 0
        failed_count = 0
        
        for i, doc in enumerate(documents, 1):
            # Generate embedding
            embedding = generate_embedding(doc['text'])
            
            if embedding:
                doc['embedding'] = embedding
                doc['embedding_model'] = OLLAMA_MODEL
                doc['embedding_dimension'] = len(embedding)
                
                # Insert into MongoDB
                collection.insert_one(doc)
                inserted_count += 1
                
                if i % 10 == 0:
                    print(f"   Progress: {i}/{len(documents)} ({inserted_count} inserted)")
            else:
                failed_count += 1
                print(f"   ⚠️ Failed to generate embedding for chunk {i}")
        
        # Create text index for fallback search
        collection.create_index([("text", "text")])
        collection.create_index([("section", 1)])
        collection.create_index([("title", 1)])
        
        print(f"\n✅ Successfully populated knowledge base!")
        print(f"   Total Chunks: {len(documents)}")
        print(f"   Inserted: {inserted_count}")
        print(f"   Failed: {failed_count}")
        print(f"   Embedding Dimension: 768")
        print(f"   Model: {OLLAMA_MODEL}")
        
        # Show sample
        sample = collection.find_one()
        if sample:
            print(f"\n📄 Sample Document:")
            print(f"   Title: {sample.get('title', 'N/A')}")
            print(f"   Section: {sample.get('section', 'N/A')}")
            print(f"   Text Length: {len(sample.get('text', ''))} chars")
            print(f"   Embedding: {len(sample.get('embedding', []))} dimensions")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ MongoDB error: {e}")
        sys.exit(1)


def main():
    """Main execution"""
    print("=" * 60)
    print("🌾 AgriSmart Knowledge Base Loader")
    print("=" * 60)
    
    # Check prerequisites
    if not check_ollama():
        sys.exit(1)
    
    # Load markdown files
    documents = load_markdown_files()
    
    if not documents:
        print("\n❌ No documents to load")
        sys.exit(1)
    
    # Populate MongoDB
    populate_mongodb(documents)
    
    print("\n" + "=" * 60)
    print("✅ Knowledge Base Population Complete!")
    print("=" * 60)
    print("\nYou can now test the RAG chatbot:")
    print("1. Start the Flask backend: flask run")
    print("2. Ask questions like:")
    print("   - 'How do I treat tomato early blight?'")
    print("   - 'What factors affect market prices?'")
    print("   - 'Tell me about drip irrigation'")


if __name__ == "__main__":
    main()
