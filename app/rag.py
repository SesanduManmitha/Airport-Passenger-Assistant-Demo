from pathlib import Path
import chromadb

BASE_DIR = Path(__file__).resolve().parent.parent
FAQ_DIR = BASE_DIR / "data" / "faq"
DB_DIR = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_DIR))

def load_chunks():
    """Read every .txt file and split it into paragrpgh-sized chunks."""
    ids, docs, metas = [], [], []
    for file in sorted(FAQ_DIR.glob("*.txt")):
        text = file.read_text(encoding="utf-8")
        paragrapghs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for i, para in enumerate(paragrapghs):
            if para.startswith("SAMPLE CONTENT"):
                continue ##skip label line
            ids.append(f"{file.stem}-{i}")
            docs.append(para)
            metas.append({"source": file.name})
    return ids, docs, metas

def build_index():
    """(Re)build the vector index from the FAQ lines."""
    try:
        client.delete_collection("airport_faq")
    except Exception:
        pass ## collection doesnt exist yet

    collection = client.create_collection("airport_faq")
    ids, docs, metas = load_chunks()
    collection.add(ids=ids, documents=docs, metadatas=metas)

def search(question: str, k: int = 3):
    """Return the k chunks most similar to the question."""
    collection = client.get_collection("airport_faq")
    result = collection.query(query_texts=[question], n_results=k)

    return [
        {"text": doc, "source":meta["source"]}
        for doc, meta in zip(result["documents"][0], result["metadatas"][0])
    ]

if __name__ =="__main__":
    build_index()
    while True:
        q = input("\nAsk something (of 'q' to quit)")
        if q.lower() == "q":
            break
        for r in search(q):
            print(f"\n[{r['source']}]\n{r['text']}")