import requests
from pprint import pprint
import os
import time

API_URL = "https://api.twelvelabs.io/v1.1"
assert API_URL

API_KEY = os.getenv("TWELVE_LABS_API_KEY")
assert API_KEY

# warriors vs cavaliers
# INDEX_ID = "64e668c489748de6618ab3f8"

# carolina vs arkansas
INDEX_ID = "64e80d2f89748de6618ab524"

def create_index(index_name):
    INDEXES_URL = f"{API_URL}/indexes"

    INDEX_NAME = index_name

    headers = {
        "x-api-key": API_KEY
    }

    data = {
    "engine_id": "marengo2.5",
    "index_options": ["visual", "conversation", "text_in_video", "logo"],
    "index_name": INDEX_NAME,
    }

    response = requests.post(INDEXES_URL, headers=headers, json=data)
    INDEX_ID = response.json().get('_id')
    
    return INDEX_ID



def upload(filename, index_id):
    TASKS_URL = f"{API_URL}/tasks"
    
    file_name = f"{filename}"
    file_path = f"/uploads/{filename}"
    file_stream = open(file_path,"rb")
    
    data = {
        "index_id": index_id,
        "language": "en"
    }
    file_param = [
        ("video_file", (file_name, file_stream, "application/octet-stream")),]
    
    response = requests.post(TASKS_URL, headers={"x-api-key": API_KEY}, data=data, files=file_param)

    TASK_ID = response.json().get("_id")
    print (f"Status code: {response.status_code}")
    pprint (response.json())
    
    
    print("started uploading task " + TASK_ID)
    return TASK_ID


def check_status(task_id):
    TASK_STATUS_URL = f"{API_URL}/tasks/{task_id}"
    while True:
        response = requests.get(TASK_STATUS_URL, headers={"x-api-key": API_KEY})
        STATUS = response.json().get("status")
        if STATUS == "ready":
            break
        time.sleep(10)
    VIDEO_ID = response.json().get('video_id')
    return VIDEO_ID


def search_video(keyword, index_id=INDEX_ID, video_id=None):
    # This code assumes that you've already created an index and the unique identifier of your index is stored in a variable named `INDEX_ID`
    SEARCH_URL = f"{API_URL}/search"

    headers = {
        "x-api-key": API_KEY
    }

    data = {
        "query": keyword,
        "index_id": index_id,
        "search_options": ["visual"],
        # "search_options": ["visual", "conversation"],
        "threshold": "medium",
    }

    try:
        response = requests.post(SEARCH_URL, headers=headers, json=data)
        print(f"Status code: {response.status_code}")
        
        return response.json()['data']
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(3)
        return []
