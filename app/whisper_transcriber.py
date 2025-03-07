# import whisper
# import requests
# import json
# import tempfile
# import os
# from config import supabase

# def format_timestamp(seconds):
#     minutes = int(seconds // 60)
#     seconds = int(seconds % 60)
#     return f"{minutes}:{seconds:02d}"

# def process_transcription(audio_url, meeting_id, audio_file_id):
#     # Download audio file
#     response = requests.get(audio_url)
#     if response.status_code != 200:
#         return {"error": "Failed to download audio file"}

#     with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
#         temp_audio.write(response.content)
#         temp_audio_path = temp_audio.name

#     try:
#         # Load and run Whisper
#         model = whisper.load_model("tiny")
#         result = model.transcribe(temp_audio_path, language="en")
#     finally:
#         os.remove(temp_audio_path)

#     if 'segments' not in result:
#         return {"error": "No transcription segments found"}

#     # Process result into paragraphs
#     paragraphs = []
#     current_para = {"start": None, "end": None, "text": ""}
#     pause_threshold = 2.0

#     for i, segment in enumerate(result['segments']):
#         start, end, text = segment['start'], segment['end'], segment['text'].strip()

#         if i == 0 or start - result['segments'][i - 1]['end'] <= pause_threshold:
#             if current_para['start'] is None:
#                 current_para['start'] = start
#             current_para['end'] = end
#             current_para['text'] += ' ' + text
#         else:
#             paragraphs.append(current_para)
#             current_para = {"start": start, "end": end, "text": text}

#     if current_para['text']:
#         paragraphs.append(current_para)

#     transcript_text = "\n\n".join(
#         [f"[{format_timestamp(p['start'])} - {format_timestamp(p['end'])}] {p['text']}" for p in paragraphs]
#     )
#     transcript_json = json.dumps(paragraphs)

#     # Save to Supabase (transcriptions table)
#     data = {
#         "audio_file_id": audio_file_id,
#         "transcript_json": transcript_json,
#         "transcript_text": transcript_text,
#     }

#     response = supabase.table("transcriptions").insert(data).execute()

#     if response.data is None or response.error:
#         return {"error": f"Failed to save transcription: {response.error}"}

#     return {"message": "Transcription completed and saved."}









import whisper
import requests
import json
import tempfile
import os
import logging
from config import supabase

def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"

def process_transcription(audio_url, meeting_id, audio_file_id):
    logging.info(f"Starting transcription for file: {audio_file_id}, meeting: {meeting_id}")

    # Download audio file
    try:
        response = requests.get(audio_url)
        response.raise_for_status()  # Raises exception for 4xx/5xx responses
    except requests.RequestException as e:
        logging.error(f"Failed to download audio file: {e}")
        return {"error": f"Failed to download audio file: {e}"}

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        temp_audio.write(response.content)
        temp_audio_path = temp_audio.name

    try:
        # Load and run Whisper
        model = whisper.load_model("tiny")  # Consider "base" if tiny is inaccurate
        result = model.transcribe(temp_audio_path, language="en")

        if 'segments' not in result:
            logging.warning(f"No transcription segments found for file {audio_file_id}")
            return {"error": "No transcription segments found"}

        # Process result into paragraphs
        paragraphs = []
        current_para = {"start": None, "end": None, "text": ""}
        pause_threshold = 2.0

        for i, segment in enumerate(result['segments']):
            start, end, text = segment['start'], segment['end'], segment['text'].strip()

            if i == 0 or start - result['segments'][i - 1]['end'] <= pause_threshold:
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
            [f"[{format_timestamp(p['start'])} - {format_timestamp(p['end'])}] {p['text']}" for p in paragraphs]
        )
        transcript_json = json.dumps(paragraphs)

        # Save to Supabase (transcriptions table)
        data = {
            "audio_file_id": audio_file_id,
            "transcript_json": transcript_json,
            "transcript_text": transcript_text,
        }

        response = supabase.table("transcriptions").insert(data).execute()

        if response.data is None or response.error:
            logging.error(f"Failed to save transcription to Supabase: {response.error}")
            return {"error": f"Failed to save transcription: {response.error}"}

        logging.info(f"Successfully saved transcription for file: {audio_file_id}")
        return {"message": "Transcription completed and saved."}

    except Exception as e:
        logging.exception(f"Unexpected error during transcription process: {e}")
        return {"error": f"Transcription failed: {str(e)}"}

    finally:
        os.remove(temp_audio_path)  # Cleanup file even if error occurs
        logging.info(f"Temporary file removed: {temp_audio_path}")

