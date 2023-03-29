


### setup project environment, python venv and install packages
```bash
source setup.sh
```


## Azure text to speech

### important
you need to get your keys from azure and set env variables.

e.g
```bash
export SPEECH_KEY='lkjasldkjflaskjdflajsldfkjasd'
export SPEECH_REGION='eastus'
```

### test azure text to spech with bookmarks
```bash
python3 src/text_to_speech_azure.py testdata/audio.xml testdata/audio.mp3
```

### test on a file that doesn't have any bookmarks
```bash
python3 src/text_to_speech_azure.py testdata/audio_without_bookmarks.xml testdata/audio_no_bookmarks.mp3
```


## Convert text to SSML 

that wraps text into ssml xml.
it also adds bookmarks in place of `# slide`
and it replaces `# brake 3s` with proper SSML break.

the idea is that in slides you write text not XML.

```bash
python3 src/text_to_ssml.py testdata/test_slides.txt testdata/test_slices.xml
```


## Extract PPTX notes

reads PPTX file and extract all notes from it into a text file.
that file can be used as input to ssml conversion above.

```bash
python3 src/pptx_notes_to_ssml.py testdata/test_slides.pptx testdata/output_ppt_notes.txt
```


## Convert images + timestamps into a single video with changing slides
later you can add voice over on that to have full video.

```bash
python3 src/create_video_from_slides.py testdata/screenshot_config.json out/slide_video.mp4
```


# end to end script options

## Convert PPTX + screenshots to video file with sound.

notes are extracted from PPTX file, then Text to speech on azure. then video is glued together. 
```bash
python3 src/overall_script.py testdata/test_slides.pptx testdata/test_slides1
```

## Other helpful commands just for reference


```bash
ffmpeg -loop 1 -i screenshot_test.png -c:v libx264 -t 15 -pix_fmt yuv420p out.mp4
```


```bash
python3 read_pptx.py   
```


```bash
python3 create_video_from_slides.py
```


1. create slides in google slides.
2. download as PPTX.
3. open PPTX in Keynote
4. export as images, select checkbox about image per build stage
5. run magic script
```python3 overall_script.py test_slides.pptx test_slides1 en-US-SaraNeural```

ALTERNATIVE

1. have a script for slides in a txt file (copy from gdoc after people edit)
2. ensure you have `# slide` breaks between subslides
3. take screenshots of each subslide and put into a single folder
4. run magic script
```python3 overall_script.py test_slides.txt test_slides_folder "en-US-SaraNeural"```

note that it will break if number of subslides mismatches number of notes.

if for some reason there are no notes for the slide, just add small break like 
```
#break 500ms
```


