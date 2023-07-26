
from contextlib import ContextDecorator

def break_tag(time='1s'):
    return f'<break time="{time}" />'

def paragraph_tag(content: str):
    return f'<p>{content}</p>'

class voice_tag(ContextDecorator):
    def __init__(self, name='en-US-JennyNeural', result: list[str] = None):
        self.name = name
        self.result = result
    
    def __enter__(self):
        self.result.append(f'<voice name="{self.name}">')
    
    def __exit__(self, *exc):
        self.result.append('</voice>')

class speak_tag(ContextDecorator):
    def __init__(self, result: list[str] = None):
        self.result = result

    def __enter__(self):
        self.result.append('<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">')

    def __exit__(self, *exc):
        self.result.append('</speak>')
