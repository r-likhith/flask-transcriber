from flask import request, jsonify
from flask_cors import CORS
from app.whisper_transcriber import process_transcription
import logging

def configure_routes(app):
    # Enable CORS for all routes (you can restrict it to your frontend domain if needed)
    CORS(app)

    @app.route('/')
    def home():
        return "Whisper Transcriber Service is Running"

    @app.route('/transcribe', methods=['POST'])
    def transcribe():
        data = request.json

        audio_url = data.get('audio_url')
        meeting_id = data.get('meeting_id')
        audio_file_id = data.get('audio_file_id')

        if not audio_url or not meeting_id or not audio_file_id:
            return jsonify({"error": "Missing parameters"}), 400

        if not audio_url.startswith("https://"):
            return jsonify({"error": "Invalid audio URL"}), 400

        try:
            # Call the transcription process
            result = process_transcription(audio_url, meeting_id, audio_file_id)
            return jsonify(result), 200
        except Exception as e:
            logging.exception("Error during transcription process")
            return jsonify({"error": f"Transcription failed: {str(e)}"}), 500
