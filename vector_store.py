from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from config import EMBEDDING_MODEL
import logging
import time

logger = logging.getLogger(__name__)

def create_vector_db(chunks):
    logger.info(f"Creating vector database from {len(chunks)} chunks")
    logger.info(f"Using embedding model: {EMBEDDING_MODEL}")
    
    max_retries = 3
    retry_delay = 30
    
    for attempt in range(max_retries):
        try:
            embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
            logger.info("Embedding model initialized successfully")
            vector_db = FAISS.from_texts(chunks, embeddings)
            logger.info("Vector database created successfully")
            return vector_db
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                if attempt < max_retries - 1:
                    logger.warning(f"Rate limit hit. Waiting {retry_delay}s before retry {attempt + 2}/{max_retries}...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    logger.error(f"Failed after {max_retries} attempts: {error_msg}")
                    raise
            else:
                logger.error(f"Failed to create vector database: {error_msg}")
                raise