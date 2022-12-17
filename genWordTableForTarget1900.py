import glob
import json
import urllib
import re
import pdb
from collections import Counter

files = glob.glob("*_voice.mp4")

words = list( map( lambda x: (int(x[0]), x[1]) , re.findall(r'NO_(\d+)_([a-z]+)_voice', " ".join(files) ) ) )
words.sort( key=lambda x: x[0] )

counter = Counter( map( lambda x : int((x[0]-1)/100) + 1, words ))

f = open("w.txt", "w")
for a, b in words:
    print( f"{a} {b}", file=f )
f.close()

f = open("coverrate.txt", "w", encoding="utf8")
for k in counter:
    print( f"No.{k*100-99} ～ {k*100}　カバー率{counter[k]}%", file=f )
f.close()
