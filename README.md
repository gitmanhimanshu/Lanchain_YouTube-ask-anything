# YouTube RAG - Ask Anything

A RAG (Retrieval Augmented Generation) application that lets you ask questions about any YouTube video using its transcript.

## Features

- 📹 Fetch transcripts from YouTube videos automatically
- 🔍 Smart text chunking with overlap for better context
- 🧠 Vector database using FAISS for semantic search
- 💬 Ask questions and get AI-powered answers based on video content
- 📝 Automatic transcript saving (stored in `transcripts/` folder)
- 🔄 Automatic retry logic for API rate limits
- 📊 Comprehensive logging to track the entire flow

## How It Works

1. **Transcript Extraction** - Fetches YouTube video transcript using video ID
2. **Text Splitting** - Breaks transcript into 500-character chunks with 100-character overlap
3. **Vector Database** - Creates embeddings and stores them in FAISS vector store
4. **Question Answering** - Retrieves 4 most relevant chunks and uses Gemini to generate answers

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install youtube-transcript-api langchain langchain-google-genai langchain-community faiss-cpu python-dotenv
   ```

4. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```bash
   python app.py
   ```

## Usage

```bash
Enter YouTube Video ID: 9bANpAwmANU
Fetching transcript...
Splitting text...
Creating vector DB...
Ready! Ask questions 👇

Ask: What is the main topic?
```

## Project Structure

- `app.py` - Main application entry point
- `transcript.py` - YouTube transcript fetching
- `splitter.py` - Text chunking logic
- `vector_store.py` - FAISS vector database creation
- `rag_pipeline.py` - Question answering with RAG
- `config.py` - Configuration and API keys
- `transcripts/` - Saved transcript files

## Technologies Used

- LangChain - RAG framework
- Google Gemini - LLM and embeddings
- FAISS - Vector similarity search
- YouTube Transcript API - Transcript extraction
