import os
import moviepy.editor as mpy


def stitch_together(folder_name, output_file, max_video_length=60):
    # Code to stitch together the videos
    # traverse the folder for video files and combine
    clips = []
    total_length = 0
    
    # Loop through all files in the folder
    for filename in os.listdir(folder_name):
        if filename.endswith('.mp4'): 
            clip = mpy.VideoFileClip(os.path.join(folder_name, filename))
            clips.append(clip)
            total_length += clip.duration

            # If reached max length, stop adding clips
            if total_length >= max_video_length:
                break
    
    # Stitch clips together
    final_clip = mpy.concatenate_videoclips(clips)
    
    # Output final video
    final_clip.write_videofile(output_file)
    
    # get length of final video
    length = final_clip.duration
    
    return length


def replace_audio(video_file, audio_url, output_file):

    video = mpy.VideoFileClip(video_file)

    audio = mpy.AudioFileClip(audio_url)

    if video.duration > audio.duration:
        # Make the audio as long as the video
        n_loops = int(video.duration / audio.duration)
        audio = mpy.concatenate_audioclips([audio] * n_loops)

        # Calculate remaining padding time
        padding_time = video.duration - audio.duration
        print(padding_time, video.duration, audio.duration)

        # Generate silent audio for remaining time 
        padding_audio = mpy.AudioClip(make_frame=lambda t: 0, duration=padding_time)
        
        # Concatenate audio with padding
        audio = mpy.concatenate_audioclips([audio, padding_audio])


    video = video.set_audio(audio)

    video.write_videofile(output_file)