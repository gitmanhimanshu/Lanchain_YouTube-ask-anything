from langchain_google_genai import ChatGoogleGenerativeAI
from config import MODEL_NAME
import logging

logger = logging.getLogger(__name__)

def get_answer(vector_db, query):
    logger.info(f"Processing query: {query}")
    
    docs = vector_db.similarity_search(query, k=4)
    logger.info(f"Found {len(docs)} relevant documents from vector search")
    
    print("\n📄 Retrieved Chunks:")
    print("=" * 80)
    for i, doc in enumerate(docs, 1):
        print(f"\nChunk {i}:")
        print(f"{doc.page_content}")
        print("-" * 80)
    
    context = " ".join([doc.page_content for doc in docs])
    logger.info(f"Combined context length: {len(context)} characters")
    
    logger.info(f"Initializing LLM with model: {MODEL_NAME}")
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME)

    prompt = f"""
    Answer the question based only on the context below:

    Context:
    {context}

    Question:
    {query}
    """
    
    logger.info("Sending prompt to LLM...")
    response = llm.invoke(prompt)
    logger.info(f"Received response from LLM (length: {len(response.content)} characters)")
    return response.content