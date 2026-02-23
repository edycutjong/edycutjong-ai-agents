import sys
import os

# Add the project root to sys.path to resolve imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.ingestion import ingest_file

def test_ingest_txt():
    # Create a dummy text file
    test_file = "test_doc.txt"
    with open(test_file, "w") as f:
        f.write("This is a test document. " * 50) # Create some length

    try:
        docs = ingest_file(test_file, chunk_size=100, chunk_overlap=20)
        print(f"Successfully ingested {test_file}")
        print(f"Number of chunks: {len(docs)}")
        print(f"First chunk content: {docs[0].page_content[:50]}...")
        assert len(docs) > 1
    finally:
        os.remove(test_file)

if __name__ == "__main__":
    test_ingest_txt()
