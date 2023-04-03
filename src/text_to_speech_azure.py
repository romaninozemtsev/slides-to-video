#!/usr/bin/env python
# coding: utf-8

# this code is copy pasted from Microsoft Azure examples for text to speech.
# so keeping this copyright just in case.
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
import os
import sys
import json

"""
Speech synthesis samples for the Microsoft Cognitive Services Speech SDK
"""

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-text-to-speech-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)


# Set up the subscription info for the Speech Service:
# Replace with your own subscription key and service region (e.g., "westus").

SPEECH_KEY_ENV = "SPEECH_KEY"
SPEECH_REGION_ENV = "SPEECH_REGION"

if not os.environ.get(SPEECH_KEY_ENV) or not os.environ.get(SPEECH_REGION_ENV):
    print(f"Please set/export the environment variables {SPEECH_KEY_ENV} and {SPEECH_REGION_ENV}.")
    print(f"For example: export {SPEECH_KEY_ENV}=<key> && export {SPEECH_REGION_ENV}=<region>")
    sys.exit(1)

speech_key, service_region = os.environ[SPEECH_KEY_ENV], os.environ[SPEECH_REGION_ENV]


class SpeechSynthesisResult:
    def __init__(self, bookmarks: list[dict] = None, words: list[dict] = None):
        self.bookmarks = bookmarks
        self.words = words


def speech_synthesis_bookmark_event(ssml: str, file_name: str, capture_bookmarks: bool = True, capture_words: bool = False) -> SpeechSynthesisResult:
    """performs speech synthesis and shows the bookmark event.
    args:
        ssml: speech as SSML
        audio_file_name: name of the audio file to be created
        capture_bookmarks: whether to capture bookmark events
        capture_words: whether to capture word events
    returns:
        SpeechSynthesisResult object with the list of bookmarks and words captured
    """
    bookmarks = []
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    

    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    def on_bookmark(evt):
        print("Bookmark reached: {}, audio offset: {}ms, bookmark text: {}.".format(evt, evt.audio_offset / 10000, evt.text))
        bookmarks.append({"offset": evt.audio_offset / 10000, "text": evt.text})

    # Subscribes to viseme received event
    # The unit of evt.audio_offset is tick (1 tick = 100 nanoseconds), divide it by 10,000 to convert to milliseconds.
    if capture_bookmarks:
        speech_synthesizer.bookmark_reached.connect(on_bookmark)

    words = []

    def on_word(evt):
        print("Word boundary reached: {}, audio offset: {}ms, word: {}.".format(evt, evt.audio_offset / 10000, evt.text))
        words.append({"offset": evt.audio_offset / 10000, "text": evt.text})

    if capture_words:
        speech_synthesizer.synthesis_word_boundary.connect(on_word)

    result = speech_synthesizer.speak_ssml_async(ssml).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    return SpeechSynthesisResult(bookmarks = bookmarks, words = words)


if __name__ == "__main__":
    ssml_file_name = "audio.xml"
    file_name = "outputaudio1.mp3"
    capture_words = False
 
    if len(sys.argv) > 1:
        ssml_file_name = sys.argv[1]

    if len(sys.argv) > 2:
        file_name = sys.argv[2]
    
    if len(sys.argv) > 3:
        capture_words = sys.argv[3] == '--words'

    with open(ssml_file_name) as f:
        ssml = f.read()

    result = speech_synthesis_bookmark_event(ssml, file_name, capture_bookmarks=True, capture_words=capture_words)
    print(result.bookmarks)
    print(file_name)
    print(json.dumps(result.words, indent=4))
