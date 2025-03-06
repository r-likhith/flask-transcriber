import whisper
import requests
import json
import tempfile
import os
from supabase import create_client
from config import DB_URL, SERVICE_ROLE_KEY

supabase = create_client(DB_URL, SERVICE_ROLE_KEY)

def process_transcription(audio_url, meeting_id, audio_file_id):
    # Download audio file
    response = requests.get(audio_url)
    if response.status_code != 200:
        return {"error": "Failed to download audio file"}

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        temp_audio.write(response.content)
        temp_audio_path = temp_audio.name

    # Load and run Whisper
    model = whisper.load_model("base")
    result = model.transcribe(temp_audio_path, language="en")

    os.remove(temp_audio_path)

    # Process result into paragraphs
    paragraphs = []
    current_para = {"start": None, "end": None, "text": ""}
    pause_threshold = 2.0

    for i, segment in enumerate(result['segments']):
        start, end, text = segment['start'], segment['end'], segment['text'].strip()

        if i == 0 or start - result['segments'][i-1]['end'] <= pause_threshold:
            if current_para['start'] is None:
                current_para['start'] = start
            current_para['end'] = end
            current_para['text'] += ' ' + text
        else:
            paragraphs.append(current_para)
            current_para = {"start": start, "end": end, "text": text}

    if current_para['text']:
        paragraphs.append(current_para)

    transcript_text = "\n\n".join(
        [f"[{p['start']} - {p['end']}] {p['text']}" for p in paragraphs]
    )
    transcript_json = json.dumps(paragraphs)

    # Save to Supabase (transcriptions table)
    data = {
        "audio_file_id": audio_file_id,
        "transcript_json": transcript_json,
        "transcript_text": transcript_text,
    }
    supabase.table("transcriptions").insert(data).execute()

    return {"message": "Transcription completed and saved."}
# Whisper Processing Logic
