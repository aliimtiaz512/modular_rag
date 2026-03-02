import requests
from bs4 import BeautifulSoup

def extract_from_website(url):
    try:
        response=requests.get(url)
        response.raise_for_status() 
        soup=BeautifulSoup(response.text,'html.parser')
        for script_or_style in soup(["script","style","nav","footer"]):
            script_or_style.decompose()
        raw_text=soup.get_text(separator='',strip=True)
        return raw_text
    except Exception as e:
        return f"Error:{e}"

url="https://rizviz.com.pk/"
website_data=extract_from_website(url)
 