import json
import os
import subprocess
import time

def pics_to_video(pics_file_path):
    with open(pics_file_path) as f:
        pics = json.loads(f.read())
        pics_to_video_from_config(pics)


def pics_to_video_from_config(pics, size=None):
    results = []
    for pic in pics:
        print(pic)
        video_output = image_to_mp4(pic, size=size)
        results.append(video_output)
    print(results)
    return concat_videos(results)

def concat_videos(video_paths):
    out_video = "out/full_video.mp4"
    with open('videos.txt', 'w') as f:
        for video in video_paths:
            f.write(f'file {video}\n')
    os.system(f'ffmpeg -y -f concat -safe 0 -i videos.txt -c copy "{out_video}"')
    return out_video

def image_to_mp4(img_config, size=None):
    img_path = img_config['file']
    name = "".join(img_path.split('/')[-1].split('.')[:-1]).replace(" ", "_")
    duration = img_config['duration']
    out_video_path = f'out/{name}.mp4'
    string_command = f'ffmpeg -y -loop 1 -i "{img_path}" -c:v libx264 -t "{duration}" -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{out_video_path}"'
    os.system(string_command)
    time.sleep(2)
    return out_video_path

def combine_with_mp3(input_video, audio_file):
    final_file = 'out/full_video_with_audio.mp4'
    # 
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
    pics_to_video('screenshot_config.json')
