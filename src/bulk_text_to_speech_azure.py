import sys
import os
from pathlib import Path
from text_to_speech_azure import speech_synthesis_bookmark_event
from text_to_ssml import text_to_ssml

def txt_to_mp3(txt_file, mp3_file, voice):
    print(f"converting txt {txt_file} to {mp3_file}")
    with open(txt_file, 'r') as f:
        text = f.read()
        ssml = text_to_ssml(text, voice)
    speech_synthesis_bookmark_event(ssml, mp3_file)


def ssml_to_mp3(ssml_file, mp3_file):
    print(f"converting ssml {ssml_file} to {mp3_file}")
    with open(ssml_file, 'r') as f:
        ssml = f.read()
    speech_synthesis_bookmark_event(ssml, mp3_file)


if __name__ == '__main__':
    scripts_folder = 'testdata/scripts'
    out_folder = 'testdata/audio'
    if len(sys.argv) > 1:
        scripts_folder = sys.argv[1]
    if len(sys.argv) > 2:
        out_folder = sys.argv[2]
    voice = 'en-US-JennyNeural'
    if len(sys.argv) > 3:
        voice = sys.argv[3]

    Path(out_folder).mkdir(parents=True, exist_ok=True)

    print(f'converting scripts in {scripts_folder}  to mp3 in {out_folder}')

    for file in os.listdir(scripts_folder):
        full_path = os.path.join(scripts_folder, file)
        extension = Path(full_path).suffix
        mp3_file = os.path.join(out_folder, file.replace(extension, '.mp3'))
        print(f"converting {full_path} to {mp3_file}, extension {extension}")
        if extension == '.txt':
            txt_to_mp3(full_path, mp3_file, voice)
        elif extension == '.xml':
            ssml_to_mp3(full_path, mp3_file)
