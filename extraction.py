import bs4
from langchain_community.document_loaders import WebBaseLoader

def extract_with_langchain(url):
    loader = WebBaseLoader(
        web_paths=[url],
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                name=["article", "main", "div", "p", "footer"]
            )
        )
    )
    
    docs = loader.load()
    
    context = "\n\n".join([doc.page_content.strip() for doc in docs])
    return context