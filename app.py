from flask import Flask, request, jsonify, render_template, redirect, url_for
from youtube_transcript_api import YouTubeTranscriptApi
import requests
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')  # Place the HTML file in /templates folder
@app.route('/summarize', methods=['POST'])
def summarize():
    video_url = request.form.get('youtube_url')
    model = request.form.get('model')
    prompt = request.form.get('prompt', '')
    # Validate YouTube URL format
    if not video_url or 'youtube.com/watch?v=' not in video_url:
        return jsonify({"error": "Invalid YouTube URL"}), 400
    # Extract video ID from URL
    video_id = video_url.split('v=')[1].split('&')[0]
    # Get transcript for the video
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        return jsonify({"error": "Transcript not available for this video"}), 404
    # Combine transcript texts
    transcript_text = " ".join([item['text'] for item in transcript])
    # Call AI summarization API function with prompt and transcript (mocked here)
    summary = call_summary_api(transcript_text, model, prompt)
    # Return summary result (you can redirect/open in new tab in frontend)
    return jsonify({"summary": summary})
def call_summary_api(text, model, prompt):
    # Replace this with your Google Cloud or other AI API calling logic
    # For example, send text & prompt to Google Cloud AI model using requests
    # Mock response for demo
    return f"[Model: {model}] Summary based on prompt: '{prompt}'\n{text[:250]}..."
if __name__ == '__main__':
    app.run(debug=True)
