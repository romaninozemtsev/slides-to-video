import json
import os
import time
import argparse
import random    

from create_video_from_slides import concat_videos, image_to_mp4_with_location

parser = argparse.ArgumentParser(
                    prog='civic_test_combine_video',
                    description='Combine civic test videos',
                    epilog='Example: python civic_test_combine_video.py override')

parser.add_argument('--override', action='store_true', help='override existing videos')
parser.add_argument('--random', action='store_true', help='randomize video order')
parser.add_argument('--difficulty', help='difficulty of questions to include', choices=['easy', 'medium', 'hard', 'all'], default='all')
parser.add_argument('--out', help='output video path', default='out/civic-test/final-video.mp4')
parser.add_argument('--splash', help='splash screen image')

def ffmpeg_combine_audio_and_image(img_path, audio_path, out_video_path, duration=None):
    dur_str = f'-t {duration}' if duration else ''

    string_command = f'ffmpeg -y -loop 1 {dur_str} -i "{img_path}" -i "{audio_path}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "{out_video_path}"'
    print("===", string_command)
    os.system(string_command)
    time.sleep(2)
    return out_video_path


def difficulty_above(diff_a, diff_b) -> bool:
    if diff_a == 'easy' or diff_a == 'all':
        return True
    if diff_a == 'medium' and diff_b != 'easy':
        return True
    if diff_a == 'hard' and diff_b == 'hard':
        return True
    return False


if __name__ == '__main__':
    args = parser.parse_args()
    videos_txt = []
    override = args.override
    difficulty = args.difficulty
    out_video = args.out

    video_pairs = []

    if args.splash:
        splash_v_path = 'out/civic-test/splash/splash.mp4'
        silence_audio = 'out/civic-test/splash/silence.mp3'
        #if not os.path.isfile(splash_v_path) or override:
        ffmpeg_combine_audio_and_image(args.splash, silence_audio, splash_v_path, duration=2)
        #else:
        #    print("skipping", splash_v_path)
        videos_txt.append(splash_v_path)

    with open('testdata/civic-test/questions_with_duration.json', 'r') as f:
        sections = json.loads(f.read())
        for section in sections:
            all_questions = section["questions"]
            questions = [x for x in all_questions if difficulty_above(difficulty, x.get("difficulty", 'easy'))]
            #print("questions", [q["question"] for q in questions])
            #exit()
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
    if args.random:
        random.shuffle(video_pairs)
    
    # construct videos_txt from video_pairs
    for q_v_path, a_v_path in video_pairs:
        videos_txt.append(q_v_path)
        videos_txt.append(a_v_path)
    print(videos_txt)

    concat_videos(video_paths=videos_txt, out_video=out_video)