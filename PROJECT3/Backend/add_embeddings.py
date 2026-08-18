"""
Check and Add Embeddings to Knowledge Base Documents
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("🔍 CHECKING KNOWLEDGE BASE EMBEDDINGS")
print("=" * 70)

# Connect to MongoDB
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
db = client['agrismart_dev']
collection = db['knowledge_base']

# Check existing embeddings
total_docs = collection.count_documents({})
docs_with_embeddings = collection.count_documents({"embedding": {"$exists": True}})
docs_without_embeddings = total_docs - docs_with_embeddings

print(f"\n📊 Status:")
print(f"   Total documents: {total_docs}")
print(f"   With embeddings: {docs_with_embeddings}")
print(f"   Without embeddings: {docs_without_embeddings}")

if docs_without_embeddings > 0:
    print(f"\n⚠️ {docs_without_embeddings} documents need embeddings!")
    print("\n🔄 Generating embeddings with Ollama...")
    
    import requests
    
    # Fetch documents without embeddings
    docs_to_update = list(collection.find({"embedding": {"$exists": False}}))
    
    updated = 0
    failed = 0
    
    for i, doc in enumerate(docs_to_update, 1):
        try:
            content = doc.get('content', '')
            if not content:
                print(f"   ⚠️ [{i}/{len(docs_to_update)}] Skipping document with no content")
                continue
            
            # Generate embedding with Ollama
            response = requests.post(
                "http://localhost:11434/api/embeddings",
                json={
                    "model": "nomic-embed-text",
                    "prompt": content
                },
                timeout=30
            )
            
            if response.status_code == 200:
                embedding = response.json()["embedding"]
                
                # Update document with embedding
                collection.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"embedding": embedding}}
                )
                
                updated += 1
                print(f"   ✅ [{i}/{len(docs_to_update)}] Added embedding (768 dims)")
            else:
                failed += 1
                print(f"   ❌ [{i}/{len(docs_to_update)}] Ollama error: {response.status_code}")
                
        except Exception as e:
            failed += 1
            print(f"   ❌ [{i}/{len(docs_to_update)}] Error: {e}")
    
    print(f"\n✅ Embedding generation complete!")
    print(f"   Updated: {updated}")
    print(f"   Failed: {failed}")
    
else:
    print("\n✅ All documents already have embeddings!")

print("\n" + "=" * 70)
print("✅ CHECK COMPLETE")
print("=" * 70)
