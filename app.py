import os
from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

app = Flask(__name__)

# Configure the Gemini API with your API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize_video():
    data = request.get_json()
    youtube_url = data.get('youtube_url')
    user_prompt = data.get('user_prompt')

    if not youtube_url:
        return jsonify({'error': 'No YouTube URL provided'}), 400

    try:
        # Extract the video ID from the URL
        video_id = youtube_url.split("v=")[1]
        
        # Get the transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
        transcript_text = " ".join([d['text'] for d in transcript_list])

        # Define the prompt for the Gemini API
        prompt = f"""
        Summarize the following YouTube video transcript.
        
        Transcript:
        {transcript_text}

        Additional instructions: {user_prompt}
        """

        # Call the Gemini model for summarization
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        return jsonify({'summary': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Cloud Run provides the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
