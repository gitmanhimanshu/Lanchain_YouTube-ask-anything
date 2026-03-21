from youtube_transcript_api import YouTubeTranscriptApi
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_transcript(video_id):
    logger.info(f"Starting transcript fetch for video ID: {video_id}")
    
    try:
        ytt_api = YouTubeTranscriptApi()

        # get available transcripts
        transcript_list = ytt_api.list(video_id)

        # auto pick available language
        transcript = transcript_list.find_transcript(
            [t.language_code for t in transcript_list]
        )

        fetched = transcript.fetch()

        logger.info(f"Fetched {len(fetched)} segments")

        text = " ".join([t.text for t in fetched])

        logger.info(f"Transcript length: {len(text)} characters")
        
        # Save transcript to file
        os.makedirs("transcripts", exist_ok=True)
        filename = f"transcripts/{video_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        logger.info(f"Transcript saved to {filename}")

        return text

    except Exception as e:
        logger.error(f"Failed to fetch transcript: {str(e)}")
        return None