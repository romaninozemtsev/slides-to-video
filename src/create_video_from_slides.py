import json
import os
import subprocess
import time
import sys
from pathlib import Path

def pics_to_video(pics_file_path, out_video):
    with open(pics_file_path) as f:
        pics = json.loads(f.read())
        location = Path(pics_file_path).parent.absolute()
        pics_to_video_from_config(pics, out_video=out_video, location=location)


def pics_to_video_from_config(pics, size=None, out_video='out/video.mp4', location=None):
    results = []
    for pic in pics:
        img_path = pic['file']
        duration = pic['duration']
        if location is not None:
            img_path = os.path.join(location, img_path)
        print(img_path)
        video_output = image_to_mp4(img_path, duration, size=size)
        results.append(video_output)
    print(results)
    return concat_videos(results, out_video=out_video)

def concat_videos(video_paths, out_video):
    with open('videos.txt', 'w') as f:
        for video in video_paths:
            f.write(f'file {video}\n')
    os.system(f'ffmpeg -y -f concat -safe 0 -i videos.txt -c copy "{out_video}"')
    return out_video

def image_to_mp4(img_path, duration, size=None):
    name = "".join(img_path.split('/')[-1].split('.')[:-1]).replace(" ", "_")
    out_video_path = f'out/{name}.mp4'
    string_command = f'ffmpeg -y -loop 1 -i "{img_path}" -c:v libx264 -t "{duration}" -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{out_video_path}"'
    os.system(string_command)
    time.sleep(2)
    return out_video_path

def combine_with_mp3(input_video, audio_file, final_file):
    subprocess.run([
        'ffmpeg',
        '-y',
        '-i', input_video,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-shortest',
        final_file
    ])
    return final_file

if __name__ == '__main__':
    input_file = 'screenshot_config.json'
    output_file = 'out/slide_video.mp4'
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    pics_to_video(input_file, out_video=output_file)
    print("produced video at", output_file)
