import json
import os
import time
import sys

from create_video_from_slides import concat_videos

def ffmpeg_combine_audio_and_image(img_path, audio_path, out_video_path):
    string_command = f'ffmpeg -y -loop 1 -i "{img_path}" -i "{audio_path}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "{out_video_path}"'
    os.system(string_command)
    time.sleep(2)
    return out_video_path


if __name__ == '__main__':
    videos_txt = []
    override = False
    random = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "override":
            override = True
        if sys.argv[1] == "random":
            random = True
    video_pairs = []
    with open('testdata/civic-test/questions_with_duration.json', 'r') as f:
        sections = json.loads(f.read())
        for section in sections:
            questions = section["questions"]
            for question in questions:
                qnum = question["number"]
                q_v_path = f'out/civic-test/video/{qnum}_q.mp4'
                a_v_path = f'out/civic-test/video/{qnum}_a.mp4'
                if not os.path.isfile(q_v_path) or override:
                    ffmpeg_combine_audio_and_image(question["question_image"], question["question_audio"], q_v_path)
                else:
                    print("skipping", q_v_path)
                if not os.path.isfile(a_v_path) or override:
                    ffmpeg_combine_audio_and_image(question["answer_image"], question["answer_audio"], a_v_path)
                else:
                    print("skipping", a_v_path)
                
                video_pairs.append((q_v_path, a_v_path))
    out_video = 'out/civic-test/final-video.mp4'
    if random:
        import random
        random.shuffle(video_pairs)
        out_video = 'out/civic-test/final-video-random.mp4'
    # construct videos_txt from video_pairs
    for q_v_path, a_v_path in video_pairs:
        videos_txt.append(q_v_path)
        videos_txt.append(a_v_path)

    concat_videos(video_paths=videos_txt, out_video=out_video)