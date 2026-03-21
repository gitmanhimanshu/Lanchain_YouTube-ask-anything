import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

MODEL_NAME = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"