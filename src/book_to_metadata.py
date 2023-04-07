
from dataclasses import dataclass
from text_to_speech_azure import speech_synthesis_bookmark_event
from text_to_ssml import text_to_ssml
import sys
import json
# example input

example_input = """
# Cheetah the Superhero
## Cheetah is fast
Meet Cheetah.
She's a fast cat.
She has spots on her fur and long legs.
She can run really fast.

## Cheetah rides her bike
Cheetah likes to ride her bike.
She wears a helmet and goes fast.
She can ride faster than anyone else.

## Cheetah reads a book
Cheetah likes to read.
She goes to the library and picks a book.
She reads about heroes who help people.
It makes her happy.

## Cheetah helps firefighters
Cheetah heard a siren.
She saw the firefighters trying to put out a fire.
She ran to help.
She carried water to put out the fire.
The firefighters thanked her.

## The End
Cheetah is a superhero because she is fast and helps people.
We can be superheroes too by being kind and helpful.
"""

@dataclass
class Page:
    title: str  # page title
    text: str # plain text
    ssml: str = None  # SSML formatted text
    words: list = None  # list of words and their offsets
    audio: str = None  # location of mp3 file

@dataclass
class Book:
    title: str
    pages: list[Page] = None


def parse(text: str) -> Book:
    pages = []
    lines = text.split('\n')
    title = ''
    current_page_title = ''
    current_page_text = []
    for line in lines:
        print(line)
        if line.startswith('# '):
            title = line[2:]
        elif line.startswith('## '):
            if current_page_title:
                pages.append(Page(current_page_title, "\n".join(current_page_text).strip()))
                current_page_text = []
                current_page_title = ''
            current_page_title = line[3:]
        else:
            if (line.strip() or current_page_text):
                current_page_text.append(line)
    if current_page_title and current_page_text:
        pages.append(Page(current_page_title, "\n".join(current_page_text).strip()))
    return Book(title, pages)


if __name__ == '__main__':
    input_text = example_input
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            input_text = f.read()
    
    voice = 'en-US-JennyNeural'
    if len(sys.argv) > 2:
        voice = sys.argv[2]

    
    book = parse(input_text)
    book_file_name = book.title.lower().replace(' ', '_')
    out_json_file = f'out/book/{book_file_name}'
    if len(sys.argv) > 3:
        out_json_file = sys.argv[3]

    for page in book.pages:
        ssml = text_to_ssml(page.text, voice)
        title_name = page.title.lower().replace(' ', '_')
        out_file_name = f'out/book/{title_name}.mp3'
        result = speech_synthesis_bookmark_event(ssml,
                                                 out_file_name,
                                                 capture_words=True,
                                                 capture_bookmarks=False)
        page.words = result.words
        page.audio = out_file_name
    result_as_dict = {
        'title': book.title, 
        'pages': [{'text': x.text, 'title': x.title, 'voice': x.audio, 'wordsOffset': x.words}
                  for x in book.pages]
        
    }
    
    with open(out_json_file, 'w') as f:
        f.write(json.dumps(result_as_dict, indent=2))
