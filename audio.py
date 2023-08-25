import requests
import base64
import io

def generate_audio_stream(apikey, role, transcript, stream):
    elon_video_id = "t7EoxTx22W0catHmnoak"
    if role == "elon":
        video_id = elon_video_id
    elif role == "biden":
        video_id = "rw1hja2xibJD2qJzpBHJ"
    elif role == "trump":
        video_id = "aGHgh4gMY0lKysbmJkyc"
    else:
        video_id = elon_video_id

    CHUNK_SIZE = 1024

    if stream:
        url = "https://api.elevenlabs.io/v1/text-to-speech/{video_id}/stream"
    else:
        url = "https://api.elevenlabs.io/v1/text-to-speech/{video_id}"
    url = url.format(video_id=video_id)

    print(url)

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": apikey
    }

    data = {
    "text": transcript,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
    }

    response = requests.post(url, json=data, headers=headers, stream=True)
    print(response.status_code)

    audio_stream = io.BytesIO()

    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            audio_stream.write(chunk)

    audio_stream.seek(0)

    if stream:
        return audio_stream
    else:
        audio_data_bytes = audio_stream.read()
        audio_stream.close()
        audio_data_base64 = base64.b64encode(audio_data_bytes).decode('utf-8')
        audio_data_json = {
            'audio_bytes': audio_data_base64
        }
        return audio_data_json
