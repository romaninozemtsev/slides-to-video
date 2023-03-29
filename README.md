

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


