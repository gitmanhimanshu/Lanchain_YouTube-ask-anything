from flask import Flask, render_template, request, jsonify, session
from transcript import get_transcript
from splitter import split_text
from vector_store import create_vector_db
from rag_pipeline import get_answer
import logging
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store vector DBs in memory per session
vector_dbs = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_video', methods=['POST'])
def load_video():
    try:
        data = request.json
        video_id = data.get('video_id')
        
        if not video_id:
            return jsonify({'error': 'Video ID is required'}), 400
        
        logger.info(f"Loading video: {video_id}")
        
        # Fetch transcript
        text = get_transcript(video_id)
        if not text:
            return jsonify({'error': 'Failed to fetch transcript'}), 400
        
        # Split text
        chunks = split_text(text)
        
        # Create vector DB
        vector_db = create_vector_db(chunks)
        
        # Store in session
        session_id = secrets.token_hex(8)
        vector_dbs[session_id] = vector_db
        session['db_id'] = session_id
        session['video_id'] = video_id
        
        return jsonify({
            'success': True,
            'video_id': video_id,
            'chunks_count': len(chunks),
            'transcript_length': len(text)
        })
    
    except Exception as e:
        logger.error(f"Error loading video: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        db_id = session.get('db_id')
        if not db_id or db_id not in vector_dbs:
            return jsonify({'error': 'Please load a video first'}), 400
        
        vector_db = vector_dbs[db_id]
        
        # Get similar chunks
        docs = vector_db.similarity_search(query, k=4)
        chunks = [doc.page_content for doc in docs]
        
        # Get answer
        answer = get_answer(vector_db, query)
        
        return jsonify({
            'success': True,
            'answer': answer,
            'chunks': chunks
        })
    
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
