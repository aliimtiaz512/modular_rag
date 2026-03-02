import chromadb
from extraction import website_data
from langchain_text_splitters import TokenTextSplitter

token_splitter=TokenTextSplitter(chunk_size=512,chunk_overlap=50,)
chunks=token_splitter.split_text(website_data)

client=chromadb.Client()
collection=client.create_collection(name="feb24")
chunks_ids=[f"chunk_{i}" for i in range(len(chunks))] 
collection.add(
    ids=chunks_ids,
    documents=chunks
)