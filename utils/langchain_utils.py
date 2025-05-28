import streamlit as st
import json
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
import os
import tempfile

def save_analysis_to_file(analysis_data: dict) -> str:
    """
    Save analysis data to a temporary file and return the file path
    """
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json', mode='w') as temp_file:
        json.dump(analysis_data, temp_file, indent=2)
        return temp_file.name

def create_chat_chain(file_path: str):
    """
    Create a chat chain that can answer questions about the analysis data
    """
    # Get API key from session state first, then environment
    api_key = st.session_state.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set your API key in the sidebar.")
    
    # Initialize embeddings and vector store
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    
    # Load and process the analysis data
    with open(file_path, 'r') as f:
        analysis_data = json.load(f)
    
    # Create text chunks from analysis data
    text_chunks = []
    for section, content in analysis_data.items():
        text_chunks.append(f"{section}: {json.dumps(content, indent=2)}")
    
    # Create vector store
    docsearch = FAISS.from_texts(text_chunks, embeddings)
    
    # Create chat chain
    model = ChatOpenAI(temperature=0.0, openai_api_key=api_key)
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=docsearch.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    
    return qa

def answer_question(qa_chain, question: str, chat_history: list):
    """
    Get an answer to a question using the chat chain
    """
    result = qa_chain({
        "question": question,
        "chat_history": chat_history
    })
    
    return result["answer"]
