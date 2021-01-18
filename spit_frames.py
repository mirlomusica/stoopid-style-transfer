import argparse
import os
import subprocess

import neural_style_transfer as st

FILE_NAME_NUM_DIGITS: int = 6

if __name__ == "__main__":
    fps = 24
    frame_extension = '.jpg'
    default_resource_dir = 'C:/Users/Jaume/PycharmProjects/stoopid-style-transfer/data/frames'
    content_images_dir = os.path.join(default_resource_dir, 'frames')
    style_images_dir = os.path.join(default_resource_dir, 'style-images')
    output_img_dir = os.path.join(default_resource_dir, 'output-images')

    video_path = frames_path = default_resource_dir
    frames_path = os.path.join(default_resource_dir,'frames')
    frame_name_format = rf'%0{FILE_NAME_NUM_DIGITS}d{frame_extension}'
    out_frame_pattern = os.path.join(frames_path, frame_name_format)
    os.makedirs(frames_path, exist_ok=True)
    ffmpeg = 'ffmpeg'

    #split frames
    subprocess.call(
        [ffmpeg, '-i', video_path, '-r', str(fps), '-start_number', '0', '-qscale:v', '2', out_frame_pattern, '-c:a', 'copy'])