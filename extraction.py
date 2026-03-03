import requests
from bs4 import BeautifulSoup

def extract_from_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Clean the noise
        for junk in soup(["script", "style", "nav", "footer", "header"]):
            junk.decompose()
            
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        return f"Error on {url}: {e}"
