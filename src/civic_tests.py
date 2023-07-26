import sys
import json

from ssml_helper import voice_tag, speak_tag, paragraph_tag, break_tag
from text_to_speech_azure import speech_synthesis_bookmark_event

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
    with speak_tag(result):
        for section in sections:
            section_name = section["section"]
            questions = section["questions"]                
            with voice_tag(voice, result):
                result.append(paragraph_tag(section_name))

            for question in questions:
                with voice_tag(voice, result):
                    question_name = question["question"]
                    result.append(paragraph_tag(question_name))
                    result.append(break_tag('1s'))
                with voice_tag(voice2, result):
                    answers = question["answer"]
                    for answer in answers:
                        result.append(paragraph_tag(answer))

    saml = "\n".join(result)

    speech_synthesis_bookmark_event(saml, 'out/civic-test.mp3', capture_bookmarks=False, capture_words=False)