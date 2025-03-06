# Flask Routes
from flask import request, jsonify
from app.whisper_transcriber import process_transcription

def configure_routes(app):

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

        result = process_transcription(audio_url, meeting_id, audio_file_id)
        return jsonify(result)
