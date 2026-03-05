# 🏢 Rizvi International Impex - Modular RAG System

Welcome to the **Modular Retrieval-Augmented Generation (RAG)** system for Rizvi International Impex! This intelligent AI assistant is designed to answer user inquiries accurately by extracting information either from a private, pre-scraped Vector Database or by intelligently querying live web pages. 

The entire system is built utilizing **LangChain**, **ChromaDB**, and **Streamlit** to ensure high performance, context-aware memory, and modular code maintainability.

---

## ✨ Key Features
- **Dynamic Routing:** An LLM-powered router automatically categorizes queries to decide whether to search the internal knowledge base or crawl a live URL.
- **40% Confidence Score Threshold:** Prevents AI hallucinations! If a user asks an unrelated question and the database similarity drops below 40%, the system politely declines to answer instead of guessing randomly.
- **LangChain Native Processing:** Uses `RecursiveUrlLoader` to systematically crawl the company website and `WebBaseLoader` for on-the-fly extraction of live links.
- **Contextual Memory:** Employs LangChain's `InMemoryChatMessageHistory` to remember previous conversational turns and prevent redundant querying.
- **Premium User Interface:** A sleek, high-contrast Dark/Light Streamlit chat application.

---

## 🛠️ Tech Stack & Architecture
This project follows a strict **Modular** design pattern where each file serves one specific purpose:

1. **`app.py`**: The Streamlit frontend UI. Handles chat states, user inputs, and visual presentation.
2. **`orchestor.py`**: The central brain. It receives the UI input, asks the router where to go, executes the tool, calculates the 40% confidence threshold, injects the memory context, and finally commands the generation to respond.
3. **`router.py`**: A prompt-based LangChain classifier that analyzes user intent and outputs routing keys (`vector_db_query` vs `web_search`).
4. **`generation.py`**: The LangChain `ChatOpenAI` pipeline using the GPT models for parsing context and drafting the final response string.
5. **`ingestion.py`**: The offline Web Crawler script. Needs to be run manually to scrape data from `rizviz.com.pk`, split it into chunks, and save it to ChromaDB.
6. **`extraction.py`**: The on-the-fly web scraper using LangChain's `WebBaseLoader` to pull text out of external URLs the user copies into the chat.
7. **`tools.py`**: Contains the wrapper functions interacting directly with external dependencies like the ChromaDB `collection`.
8. **`memory.py`**: Manages LangChain's `HumanMessage` and `AIMessage` history states.

---

## 🚀 Installation Guide

### 1. Prerequisites
Ensure you have Python 3.9+ installed.

### 2. Clone and Setup Environment
Navigate to the project folder and install all the necessary dependencies.
```bash
pip install -r requirements.txt
```
*(Dependencies include: `streamlit`, `langchain`, `langchain-openai`, `langchain-community`, `chromadb`, `beautifulsoup4`, `python-dotenv`)*

### 3. API Key Configuration
This system requires an OpenAI-compatible API Key to power the language models. 
1. Create a `.env` file in the root directory (next to `app.py`).
2. Add your API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

---

## 💻 How to Run the Application

### Step 1: Ingest the Website into ChromaDB (One-Time Setup)
Before starting the chatbot, you must populate the vector database with the company's knowledge. Run the ingestion script:
```bash
python ingestion.py
```
*You will see the terminal recursively crawl the website, split the pages, and save them into the locally generated `./chroma_db` folder.*

### Step 2: Launch the Streamlit App
Once ingestion is complete, start your user interface:
```bash
streamlit run app.py
```

### Step 3: Start Chatting!
- Ask a company question: *"What products does Rizvi's sell?"* -> The Router triggers the Vector DB.
- Ask an external question: *"Can you summarize this link: https://example.com/article"* -> The Router bypasses the database and extracts the live web page instead!
- Ask a random question: *"How do I bake a cake?"* -> The system catches the >40% confidence threshold fail and safely refuses to generate a hallucinated answer.
