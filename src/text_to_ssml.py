import sys


## these are plain text shortcuts for xml breaks
BREAKS = {
    "# break 500ms": '<break time="500ms" />',
    "# break 1s": '<break time="1000ms" />',
    "# break 2s": '<break time="2000ms" />',
    "# break 4s": '<break time="4000ms" />',
    "# break 3s": '<break time="3000ms" />',
    "# break 5s": '<break time="5000ms" />',
    "# break 8s": '<break time="8000ms" />'
}


SLIDE_DELIMETER = '# slide'


def build_ssml(notes: list[str], voice: str) -> list:
    items = []
    for i, note in enumerate(notes):
        note_text = note.strip()
        for break_key, break_value in BREAKS.items():
            note_text = note_text.replace(break_key, break_value)
        items.append(note_text)
        items.append(f'<bookmark mark="slide_{i}"/>')

    items_xml = "\n".join(['  ' + x for x in items])

    return f"""<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"> 
    <voice name="{voice}">
        {items_xml}
    </voice>
</speak>"""


def text_to_ssml(text: str, voice: str) -> str:
    """
    This is a simple function that takes a string of text and converts it to SSML.
    It adds
    a) bookmarks for each 'slide'
    b) adds SSML break for each `# break ` annotation
    """
    subslides = text.split(SLIDE_DELIMETER)
    print(subslides)
    ssml = build_ssml(subslides, voice)
    print(ssml)
    return ssml


def txt_file_to_ssml(txt_file: str, voice: str) -> str:
    with open(txt_file, 'r') as f:
        text = f.read()
    return text_to_ssml(text, voice)


if __name__ == '__main__':
    input_file_name = 'testdata/test_script.txt'
    output_file_name = 'testdata/output_ssml.xml'
    voice = 'en-US-JennyNeural'
    if len(sys.argv) > 1:
        input_file_name = sys.argv[1]
    if len(sys.argv) > 2:
        output_file_name = sys.argv[2]
    if len(sys.argv) > 3:
        voice = sys.argv[3]

    ssml = txt_file_to_ssml(input_file_name, voice)
    with open(output_file_name, 'w') as f:
        f.write(ssml)
