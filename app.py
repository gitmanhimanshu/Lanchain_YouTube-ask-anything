from transcript import get_transcript
from splitter import split_text
from vector_store import create_vector_db
from rag_pipeline import get_answer
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("=== YouTube RAG Application Started ===")
    video_id = input("Enter YouTube Video ID: ")
    logger.info(f"User entered video ID: {video_id}")

    print("Fetching transcript...")
    text = get_transcript(video_id)
    logger.info("Transcript fetched successfully")

    print("Splitting text...")
    chunks = split_text(text)
    logger.info("Text splitting completed")

    print("Creating vector DB...")
    vector_db = create_vector_db(chunks)
    logger.info("Vector database ready")

    print("Ready! Ask questions 👇")
    logger.info("=== Entering Q&A Loop ===")

    while True:
        query = input("\nAsk: ")
        if query.lower() in ['exit', 'quit', 'q']:
            logger.info("User exited the application")
            break
        logger.info(f"New question received: {query}")
        answer = get_answer(vector_db, query)
        print("Answer:", answer)
        logger.info("Answer delivered to user")

if __name__ == "__main__":
    main()