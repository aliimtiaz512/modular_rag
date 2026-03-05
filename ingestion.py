import os
import re
import chromadb
from bs4 import BeautifulSoup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_text_splitters import TokenTextSplitter

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="feb24")

def extract_content(html: str) -> str:
    """Extractor function to clean the HTML for RecursiveUrlLoader."""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        for junk in soup(["script", "style", "nav", "header", "noscript"]):
            junk.decompose()
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return ""

if __name__ == "__main__":
    base_website_url = "https://rizviz.com.pk/"
    
    print(f"Starting Web Crawler on {base_website_url} using LangChain RecursiveUrlLoader...")
    
    loader = RecursiveUrlLoader(
        url=base_website_url, 
        max_depth=3, 
        extractor=extract_content,
        prevent_outside=True 
    )
    docs = loader.load()
    print(f"Crawler finished. Parsed {len(docs)} total pages from {base_website_url}.")
    
    if docs:
        print("\nStarting Ingestion Process into Vector DB...")
        
        token_splitter = TokenTextSplitter(chunk_size=700, chunk_overlap=150)
        splits = token_splitter.split_documents(docs)
        print(f"Prepared {len(splits)} total chunks after splitting.")
        
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        for i, split in enumerate(splits):
            page_content = split.page_content
            source_url = split.metadata.get('source', base_website_url)
            
            safe_url_name = re.sub(r'[^a-zA-Z0-9]', '_', source_url.replace("https://", "").replace("http://", ""))
            chunk_id = f"chunk_{safe_url_name}_{i}"
            
            all_chunks.append(page_content)
            all_metadatas.append({"source_url": source_url})
            all_ids.append(chunk_id)

        if all_chunks:
            print(f"\nAdding all {len(all_chunks)} chunks to ChromaDB collection 'feb24'...")
            try:
                collection.add(
                    ids=all_ids,
                    documents=all_chunks,
                    metadatas=all_metadatas
                )
                print("Ingestion complete. Data is saved to ./chroma_db with URL metadata.")
            except Exception as e:
                print(f"Error saving to vector DB: {e}")
    else:
        print("No valid text documents were generated during loading.")