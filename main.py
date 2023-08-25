from dotenv import load_dotenv
load_dotenv()
import moviepy
from twelvelabs import search_video, create_index, upload, check_status
from cut_videos import trim_video

import requests
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Optional
import os
import shutil

from pydantic import BaseModel
from get_keywords import extract_keywords
import reduce
from audio import generate_audio_stream
from stitch import stitch_together, replace_audio
from replicate_musicgen import generate_music_replicate

from fastapi.middleware.cors import CORSMiddleware

SCORE_THRESHOLD = 80
MAX_DURATION = 30
MAX_RESULTS = 7

max_video_length = 60
        
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
  

# class UploadInput(BaseModel):
#     file: UploadFile = File(...)


# @app.post("/upload")
# def upload(payload: UploadInput):
#     print(payload.file)
#     return {"filename": payload.file.filename}
    
    
    
# class SearchInput(BaseModel):
#     video: UploadFile = File(...)
#     category: str
#     prompt: str
#     music_prompt: str
#     email: str
    
    
@app.post('/video')
async def main(video: UploadFile = File(...), category: str = None, prompt: str = None, music_prompt: str = None, email: str = None):
    # video, category, prompt, music_prompt, email = payload.video, payload.category, payload.prompt, payload.music_prompt, payload.email
    print(video, category, prompt, music_prompt, email)
    
    # Save the uploaded video to the uploads directory
    video_filename = email + "_" + category
    video_path = os.path.join("uploads", video_filename)
    
    
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    
    index_name = email + "_" + category + "_index"
    index_id = create_index(index_name=index_name)
    
    task_id = upload(video_filename, index_id=index_id)
    
    return task_id


# def get_video_id(task_id):


# @app.get('/status/{task_id}')
# async def status(task_id: str):
#     check_status(task_id)
    


# result: {'score': 83.9, 'start': 1.58, 'end': 60.95, ...}
def main(index_id="64e80d2f89748de6618ab524", output_dir="output-sc-ark"):
    output = extract_keywords("basketball")
    domain, key_highlights = output["domain"], output["key_highlights"]
    
    output_dir = output_dir
    # make sure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for keyword in key_highlights:
        print(f"Searching for {keyword}")
        search_results = search_video(domain + " " + keyword, index_id=index_id)
        print(f"Found {len(search_results)} results")
        
        search_results = search_results[:MAX_RESULTS]
        
        for i, r in enumerate(search_results):
            start = r['start']
            end = r['end']
            
            if end - start > MAX_DURATION:
                print(f"Skipping {keyword} {i} because it's too long. Duration: {end - start}")
                continue
            if r['score'] < SCORE_THRESHOLD:
                print(f"Skipping {keyword} {i} because it's score is too low. Score: {r['score']}")
                continue
            
            output_filename = f"{output_dir}/{start}-{keyword.replace(' ', '_')}_{i}.mp4"
            start_time, end_time = reduce.get_median_n_seconds(start, end, n=6)
            trim_video(input_file=f'src/{output_dir}.mp4', 
                       start_time=start_time, end_time=end_time + 5,
                       output_file=output_filename
                       )
            
    duration = stitch_together(output_dir, f'{output_dir}/combined_output.mp4', max_video_length)
    url = generate_music_replicate(duration=duration, 
                                   prompt="exciting basketball game with hard rock music")
    
    output_filename = f"{output_dir}/final_output.mp4"
    replace_audio(f'{output_dir}/combined_output.mp4', url, output_filename)
    
    # start musicgen
    return url

    
if __name__ == "__main__":
    main()