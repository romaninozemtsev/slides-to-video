#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
import os

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

speech_key, service_region = os.environ["SPEECH_KEY"], os.environ["SPEECH_REGION"]


def speech_synthesis_to_mp3_file():
    """performs speech synthesis to a mp3 file"""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Sets the synthesis output format.
    # The full list of supported format can be found here:
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    # Creates a speech synthesizer using file as audio output.
    # Replace with your own audio file name.
    file_name = "outputaudio1.mp3"
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    # Receives a text from console input and synthesizes it to mp3 file.
    while True:
        print("Enter some text that you want to synthesize, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(text, file_name))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))


def speech_synthesis_bookmark_event(ssml):
    """performs speech synthesis and shows the bookmark event."""
    bookmarks = []
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    file_name = "outputaudio1.mp3"
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
    speech_synthesizer.bookmark_reached.connect(on_bookmark)

    result = speech_synthesizer.speak_ssml_async(ssml).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    return (bookmarks, file_name)



if __name__ == "__main__":

    with open('audio.xml') as f:
        ssml = f.read()
    
    (bookmarks, file_name) = speech_synthesis_bookmark_event(ssml)
    print(bookmarks)
    print(file_name)