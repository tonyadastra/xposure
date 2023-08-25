from moviepy.editor import VideoFileClip


def trim_video(input_file, start_time, end_time, output_file):
    """
    Cut a video based on start and end timestamps.

    Parameters:
    - input_file: Path to the input video file.
    - start_time: Start time in the format 'hh:mm:ss'.
    - end_time: End time in the format 'hh:mm:ss'.
    - output_file: Path to save the cut video.
    """
    
    
    with VideoFileClip(input_file) as video:
        new_video = video.subclip(start_time, end_time)
        new_video.write_videofile(output_file, codec="libx264")


