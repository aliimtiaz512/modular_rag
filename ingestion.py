import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import chromadb
from langchain_text_splitters import TokenTextSplitter

# We must initialize to a persistent client so the data survives across script runs
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="feb24")

def is_valid_url(url, base_domain):
    """Checks if a URL is valid and belongs to the base domain."""
    parsed = urlparse(url)
    return bool(parsed.netloc) and parsed.netloc == base_domain

def get_all_website_links(url):
    """Returns all URLs that are found on `url` belonging to the same website."""
    base_domain = urlparse(url).netloc
    urls = set()
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            
            href = urljoin(url, href)
            
            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            
            if is_valid_url(href, base_domain):
                urls.add(href)
                
    except Exception as e:
        print(f"Error extracting links from {url}: {e}")
        
    return urls

def crawl_and_extract(base_url, max_urls=75):
    """
    Crawls a website starting from base_url, extracts text, and returns a Python dictionary
    mapping the valid URLs to the clean extracted text content.
    """
    urls_to_visit = [base_url]
    visited_urls = set()
    extracted_data = {}
    
    print(f"Starting Web Crawler on {base_url}...")
    
    while urls_to_visit and len(visited_urls) < max_urls:
        current_url = urls_to_visit.pop(0)
        
        if current_url in visited_urls:
            continue
            
        print(f"Crawling ({len(visited_urls)+1}/{max_urls}): {current_url}")
        visited_urls.add(current_url)
        
        # 1. Extract the text on this page FIRST
        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Clean the noise (footers, headers, scripts, etc.)
            for junk in soup(["script", "style", "nav", "footer", "header"]):
                junk.decompose()
                
            page_text = soup.get_text(separator=' ', strip=True)
            
            if page_text:
                extracted_data[current_url] = page_text
                print(f"  -> Extracted {len(page_text)} chars.")
                
        except Exception as e:
            print(f"  -> Skipping extraction for {current_url}: {e}")
            
        # 2. Get all new links on this page
        new_links = get_all_website_links(current_url)
        for link in new_links:
            if link not in visited_urls and link not in urls_to_visit:
                urls_to_visit.append(link)
                
        # Ethical delay to avoid DDOSing the server
        time.sleep(1)
        
    print(f"Crawler finished. Visited {len(visited_urls)} total pages.")
    return extracted_data


if __name__ == "__main__":
    base_website_url = "https://rizviz.com.pk/"
    
    # 1. Crawl and gather all text data
    all_site_data = crawl_and_extract(base_website_url, max_urls=50)
    
    print("\nStarting Ingestion Process into Vector DB...")
    
    # 2. Initialize the text splitter
    token_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=50)
    
    total_chunks_added = 0
    all_chunks = []
    all_metadatas = []
    all_ids = []
    
    # 3. Process the data page by page
    for url, page_text in all_site_data.items():
        # Split the text of this specific URL into chunks
        chunks = token_splitter.split_text(page_text)
        
        if chunks:
            for i, chunk in enumerate(chunks):
                # Create a unique ID combining the URL name and chunk index
                safe_url_name = url.replace("https://", "").replace("http://", "").replace("/", "_").strip("_")
                chunk_id = f"chunk_{safe_url_name}_{i}"
                
                # Append to our master lists
                all_chunks.append(chunk)
                
                # Critical: Save the source URL as metadata so the LLM knows where it came from
                all_metadatas.append({"source_url": url})
                
                all_ids.append(chunk_id)
                
            total_chunks_added += len(chunks)
            print(f"Prepared {len(chunks)} chunks for {url}")
            
    # 4. Insert directly into ChromaDB
    if all_chunks:
        print(f"\nAdding all {total_chunks_added} chunks to ChromaDB collection 'feb24'...")
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
        print("No valid text chunks were generated during scraping.")