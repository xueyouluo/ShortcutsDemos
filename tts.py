import base64
import json
import uuid
import requests

def tts(app_id, access_token, text, voice_type='BV700_V2_streaming'):
    cluster = "volcano_tts"
    host = "openspeech.bytedance.com"
    api_url = f"https://{host}/api/v1/tts"

    headers = {
        'Authorization': f'Bearer;{access_token}'
    }
    
    
    request_json = {
        "app": {
            "appid": app_id,
            "token": "access_token",
            "cluster": cluster,
        },
        "user": {
            "uid": "xueyou"
        },
        "audio": {
            "voice_type": voice_type,
            "encoding": "mp3",
            "speed_ratio": 1.0,
            "volume_ratio": 1.0,
            "pitch_ratio": 1.0,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson"

        }
    }

    try:
        resp = requests.post(api_url, json.dumps(request_json), headers=headers)
        if "data" in resp.json():
            data = resp.json()["data"]
            return data
        
        raise Exception("TTS request failed")
    except Exception as e:
        e.with_traceback()
        raise Exception("TTS request failed")