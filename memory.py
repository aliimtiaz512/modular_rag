# Global list to store the chat history in memory
chat_history_list = []

def add_to_memory(user_query: str, ai_response: str):
    """Adds the user query and AI response to the memory list."""
    chat_history_list.append({
        "user_query": user_query,
        "ai_response": ai_response
    })

def check_if_asked(user_query: str) -> bool:
    """Checks if the exact user query has already been asked."""
    for interaction in chat_history_list:
        if interaction['user_query'].strip().lower() == user_query.strip().lower():
            return True
    return False

def get_memory_context() -> str:
    """Retrieves the formatted chat history from the list."""
    if not chat_history_list:
        return ""
    
    context = "Previous Conversation Context:\n"
    for interaction in chat_history_list:
        context += f"User: {interaction['user_query']}\n"
        context += f"Assistant: {interaction['ai_response']}\n"
    
    return context

def clear_memory(clear: bool = True):
    """Clears the memory list if the condition is met."""
    if clear:
        chat_history_list.clear()
