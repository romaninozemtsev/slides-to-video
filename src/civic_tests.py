import sys
import json
import os

from ssml_helper import voice_tag, speak_tag, paragraph_tag, break_tag
from text_to_speech_azure import speech_synthesis_bookmark_event


def wrap_saml(voice, saml: str|list[str]):
    result = []
    with speak_tag(result):
        with voice_tag(voice, result):
            if isinstance(saml, list):
                result.extend(saml)
            else:
                result.append(saml)
    return "\n".join(result)

if __name__ == '__main__':
    voice = 'en-US-SaraNeural'
    if len(sys.argv) > 1:
        voice = sys.argv[1]
    
    voice2 = 'en-US-BrandonNeural'
    if len(sys.argv) > 2:
        voice2 = sys.argv[2]

    override = False
    if len(sys.argv) > 3 and sys.argv[3] == 'override':
        override = True
    
    print("generating with voice", voice, "and voice2", voice2, "and override", override)
    
    # read testsdata civic-test/questions.json
    with open('testdata/civic-test/questions.json', 'r') as f:
        sections = json.loads(f.read())

    result = []
    total = 0
    with speak_tag(result):
        for section in sections:
            section_name = section["section"]
            questions = section["questions"]                
            # with voice_tag(voice, result):
            #     result.append(paragraph_tag(section_name))

            for question in questions:
                q_saml = []
                a_saml = []
                with speak_tag(q_saml):
                    with voice_tag(voice, q_saml):
                        question_name = question["question"]
                        q_saml.append(paragraph_tag(question_name))
                        q_saml.append(break_tag('1s'))
                with speak_tag(a_saml):
                    with voice_tag(voice2, a_saml):
                        answer_candidates = question["answer"]
                        answers = answer_candidates
                        if question.get("byState"):
                            answers = question["byState"]["CA"]
                            # if answers is not array. make it array
                            if not isinstance(answers, list):
                                answers = [answers]
                        best_answers = [0]
                        if question.get("bestAnswer"):
                            best_answers = question["bestAnswer"]
                            if not isinstance(best_answers, list):
                                best_answers = [best_answers]

                        for i, answer in enumerate(answers):
                            if i in best_answers:
                                a_saml.append(paragraph_tag(answer))
                with open(f"out/civic-test/saml/q{question['number']}.txt", 'w') as f:
                    f.write("\n".join(q_saml))
                with open(f"out/civic-test/saml/a{question['number']}.txt", 'w') as f:
                    f.write("\n".join(a_saml))
                total += 1

    saml = "\n".join(result)


    q_saml_str = "\n".join(q_saml)

    print("creating audio files")

    for i in range(1, total + 1):
        with open(f"out/civic-test/saml/q{i}.txt", 'r') as f:
            q_saml_str = f.read()
        with open(f"out/civic-test/saml/a{i}.txt", 'r') as f:
            a_saml_str = f.read()
        
        q_audio_file = f'out/civic-test/audio/q{i}.wav'
        if not os.path.isfile(q_audio_file) or override:
            print(f"creating {q_audio_file}")
            speech_synthesis_bookmark_event(q_saml_str, q_audio_file, capture_bookmarks=False, capture_words=False)
        else:
            print(f"skipping {q_audio_file}")
         
        a_audio_file = f'out/civic-test/audio/a{i}.wav'
        if not os.path.isfile(a_audio_file) or override:
            print(f"creating {a_audio_file}")
            speech_synthesis_bookmark_event(a_saml_str, a_audio_file, capture_bookmarks=False, capture_words=False)
        else:
            print(f"skipping {a_audio_file}")

    #speech_synthesis_bookmark_event(q_saml_str, 'out/civic-test/civic-test.wav', capture_bookmarks=False, capture_words=False)