import chromadb
from extraction import extract_from_website
from langchain_text_splitters import TokenTextSplitter
import time

# We must initialize to a persistent client so the data survives across script runs
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="feb24")

if __name__ == "__main__":
    urls = [
        "https://rizviz.com.pk/",
        "https://rizviz.com.pk/about.php",
        "https://rizviz.com.pk/itsolutions.php",
        "https://rizviz.com.pk/servicenow.php",
        "https://rizviz.com.pk/salesforce.php",
        "https://rizviz.com.pk/bposervice.php",
        "https://rizviz.com.pk/contact.php"
    ]

    all_site_data = {}

    for url in urls:
        print(f"Scraping: {url}...")
        page_content = extract_from_website(url)
        all_site_data[url] = page_content
        time.sleep(1) # Ethical delay to avoid being blocked

    token_splitter=TokenTextSplitter(chunk_size=512,chunk_overlap=50)
    all_text_combined = " ".join(all_site_data.values())
    chunks=token_splitter.split_text(all_text_combined)

    chunks_ids=[f"chunk_{i}" for i in range(len(chunks))] 
    collection.add(
        ids=chunks_ids,
        documents=chunks
    )
    print("Ingestion complete. Data is saved to ./chroma_db")