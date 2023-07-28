import json
import os
import subprocess

def read_duration(wave_file_path):
    print(wave_file_path)
    result = subprocess.check_output(f'ffprobe -i "{wave_file_path}" -show_entries format=duration -v quiet -of csv="p=0"', shell=True)
    print(result, float(result))
    return float(result)

if __name__ == "__main__":
    with open('testdata/civic-test/questions.json', 'r') as f:
        sections = json.loads(f.read())
    
    # use ffmpeg to get duration from each wave file located in out/civic-test/audio
    # use that to create a json file with the same structure as questions.json but with duration added

    for section in sections:
        questions = section["questions"]
        for question in questions:
            question_file_location = f'out/civic-test/audio/q{question["number"]}.wav'
            answer_file_location = f'out/civic-test/audio/a{question["number"]}.wav'
            question["duration"] = read_duration(question_file_location)
            question["answer_duration"] = read_duration(answer_file_location)

    with open('testdata/civic-test/questions_with_duration.json', 'w') as f:
        f.write(json.dumps(sections, indent=2))