import sys
import json

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
    
    # read testsdata civic-test/questions.json
    with open('testdata/civic-test/questions.json', 'r') as f:
        sections = json.loads(f.read())
    
    # each section has "section" and "questions"

    # each question has "question" and "answer"

    result = []
    limit = 10
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
                        answers = question["answer"]
                        for answer in answers:
                            a_saml.append(paragraph_tag(answer))
                with open(f"out/civic-test/saml/q{question['number']}.txt", 'w') as f:
                    f.write("\n".join(q_saml))
                with open(f"out/civic-test/saml/a{question['number']}.txt", 'w') as f:
                    f.write("\n".join(a_saml))
                

    saml = "\n".join(result)


    q_saml_str = "\n".join(q_saml)

    speech_synthesis_bookmark_event(q_saml_str, 'out/civic-test/civic-test.wav', capture_bookmarks=False, capture_words=False)