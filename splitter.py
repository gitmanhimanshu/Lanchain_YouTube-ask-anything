from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

def split_text(text):
    logger.info(f"Starting text splitting. Input text length: {len(text)} characters")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_text(text)
    logger.info(f"Text split into {len(chunks)} chunks")
    logger.debug(f"First chunk preview: {chunks[0][:100]}..." if chunks else "No chunks created")
    return chunks