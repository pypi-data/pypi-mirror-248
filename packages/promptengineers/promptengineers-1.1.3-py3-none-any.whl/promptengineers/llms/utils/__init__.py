"""Utilites for Chains"""
from langchain_core.documents.base import Document

def get_chat_history(inputs: tuple) -> str:
    """Formats the chat history into a readable format for the chatbot"""
    res = []
    for human, assistant in inputs:
        res.append(f"Human: {human}\nAssistant: {assistant}")
    return "\n".join(res)

def combine_documents(documents: list[Document]):
    combined_content = ""
    for doc in documents:
        combined_content += doc.page_content + "\n"
    return combined_content

def retrieve_system_message(messages):
    """Retrieve the system message"""
    try:
        filtered_messages = list(filter(lambda message: message['role'] == 'system', messages))
        return filtered_messages[0]['content']
    except IndexError:
        return None

def retrieve_chat_messages(messages):
    """Retrieve the chat messages"""
    return [
        (msg["content"]) for msg in messages if msg["role"] in ["user", "assistant"]
    ]