import glob
import re

files = {}

for f in glob.glob("kime/*_NO_*_voice.mp4"):
    m = re.search( r'_NO_(\d+)_', f )
    if m:
        number = int(m.group(1))
        if number <= 100:
            files[number] = f


for i in sorted(files):
    print( f"file {files[i]}" )
