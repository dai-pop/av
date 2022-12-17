import glob
import re

files = {}

for i in range(1,19+1):
    files[i] = []

for f in glob.glob("NO_*_voice.mp4"):
    m = re.search( r'NO_(\d+)_', f )
    if m:
        number = int(m.group(1))
        index = int( (number-1) / 100 ) + 1
        files[index].append( f )

for k in files:
    with open(f"{k:02}.txt", "w" ) as f:
        for mp4file in files[k]:
            print( f"file {mp4file}", file=f )
