#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import glob
import subprocess
import sys
import pathlib
import os

                
def run():

    for file in sys.argv[1:]:
        basepath, ext = os.path.splitext(file)
        path = pathlib.Path(file)
        in_srt_e = glob.glob( basepath + "*English*.srt" )[0]
        in_srt_j = glob.glob( basepath + "*Japanese*.srt" )[0]
        
        timestamp = path.stem + " '%{pts\:gmtime\:0\:%H\\\\\\:%M\\\\\\:%S}'"

        vf_option = f"scale=1280:-1,subtitles={in_srt_j}:force_style='FontName=IPAGothic,Alignment=7',subtitles={in_srt_e}:force_style='FontName=IPAGothic,Alignment=3',drawtext=fontfile=/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf:fontsize=32:box=1:boxcolor=white@0.3:fontcolor=black:text={timestamp}:x=0:y=h-th"
        out_movie = basepath + ".sub.mp4"
        subprocess.run( ["ffmpeg", "-i", file, "-vf", vf_option, out_movie ] )
        


if __name__ == "__main__": 
    run()
