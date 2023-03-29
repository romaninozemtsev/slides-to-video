import sys
import os
from create_video_from_slides import combine_with_mp3, pics_to_video_from_config

from pptx_notes_to_ssml import pptx_to_ssml, txt_file_to_ssml
from text_to_speech_azure import speech_synthesis_bookmark_event



def run_full_program(ppt_location: str, img_location: str, voice: str):
    if ppt_location.endswith('.pptx'):
        ssml_text = pptx_to_ssml(ppt_location, voice)
    else:
        ssml_text = txt_file_to_ssml(ppt_location, voice)
    print("constructed ssml text")
    (bookmarks, mp3_location) = speech_synthesis_bookmark_event(ssml_text)
    print("got bookmarks", bookmarks, "and mp3", mp3_location)
    files = sorted(os.listdir(img_location))
    if len(files) != len(bookmarks):
        raise Exception(f'Number of images and number of bookmarks do not match slides {len(files)} and bookmarks {len(bookmarks)}')
    images_config = []

    prev_offset = 0
    for i, bookmark in enumerate(sorted(bookmarks, key=lambda x: x['offset'])):
        images_config.append({
            'file': os.path.join(img_location, files[i]),
            'duration': str(int(bookmark['offset'] - prev_offset)) + "ms"
        })
        prev_offset = bookmark['offset']
    print("constructed config", images_config)
    video_with_slides = pics_to_video_from_config(images_config)
    print("got video with slides", video_with_slides)
    final_video_path = 'out/full_video_with_audio.mp4'
    combine_with_mp3(video_with_slides, mp3_location, final_video_path)
    print("got video with slides", final_video_path)


if __name__ == '__main__':
    ppt_location = sys.argv[1]
    img_location = sys.argv[2]
    if len(sys.argv) > 3:
        voice = sys.argv[3]
    else:
        voice = 'en-US-JennyNeural'
    run_full_program(ppt_location, img_location, voice)
