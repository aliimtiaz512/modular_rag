from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

history = InMemoryChatMessageHistory()

def add_to_memory(user_query: str, ai_response: str):
    history.add_message(HumanMessage(content=user_query))
    history.add_message(AIMessage(content=ai_response))

def check_if_asked(user_query: str) -> bool:
    for message in history.messages:
        if isinstance(message, HumanMessage):
            if message.content.strip().lower() == user_query.strip().lower():
                return True
    return False

def get_memory_context() -> str:
    if not history.messages:
        return ""
    
    context = "Previous Conversation Context:\n"
    for message in history.messages:
        if isinstance(message, HumanMessage):
            context += f"User: {message.content}\n"
        elif isinstance(message, AIMessage):
            context += f"Assistant: {message.content}\n"
            
    return context

def clear_memory(clear: bool = True):
    if clear:
        history.clear()
