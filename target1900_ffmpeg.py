# -*- coding: utf-8 -*-

import pysrt
import json
import re
import glob
import subprocess

class OH(dict):
    __getattr__ = dict.get

def getStartTime( srtlist, index, initial_ms ):
    if index == 0 or srtlist[index].start.ordinal < initial_ms - 2000:
        return srtlist[index].start.ordinal
    return getStartTime( srtlist, index-1, initial_ms )

def getEndTime( srtlist, index, initial_ms ):
    if index == len(srtlist)-1 or srtlist[index].end.ordinal > initial_ms + 2000:
        return srtlist[index].end.ordinal
    return getEndTime( srtlist, index+1, initial_ms )

def main():
    tangocho = json.loads( open("svl8_12.json").read(), object_hook=OH )
    total_index = 1

    for file in glob.glob( "サイバーパンク_ エッジランナーズ/*/*/*.mp4"):
        in_mp4 = file
        in_srt = file.replace( ".mp4", ".English (CC).srt" )
        in_srt_j = file.replace( ".mp4", ".Japanese (CC).srt" )
    
        srt = list(pysrt.open(in_srt))
        for index, line in enumerate(srt):
            for word in re.findall( r'[\w\']+', line.text ):
                lowerword = word.lower()
                for w in tangocho:
                    if lowerword in w.forms:
                        with open("desc.txt", "w") as f:
                            print(w.desc, file=f)
                        text = line.text.replace("\n"," ")
                        start_time = getStartTime( srt, index, line.start.ordinal )
                        end_time = getEndTime( srt, index, line.end.ordinal )

                        desc_show_time = int( (line.end.ordinal - start_time ) / 1000 ) # 単語を含む行の最後で語義表示
                        vf_option = f"subtitles={in_srt_j}:force_style='FontName=IPAGothic,Alignment=7',subtitles={in_srt}:force_style='FontName=IPAGothic,Alignment=3',drawtext=fontfile=/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf:fontsize=50:box=1:boxcolor=white@0.3:fontcolor=black:text={w.base}:x=0:y=h-th,drawtext=fontfile=/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf:fontsize=14:box=1:boxcolor=white@0.3:fontcolor=black:textfile=desc.txt"
                        out_mp4 = in_mp4.removesuffix(".mp4") + f"_{line.start.minutes:02}{line.start.seconds:02}_TANGO_{total_index:04}_" + lowerword + ".mp4"
                        total_index += 1
                        subprocess.run( ["ffmpeg", "-i", in_mp4, "-ss", f"{start_time-200}ms", "-to", f"{end_time+200}ms", "-vf", vf_option, out_mp4 ] )
                

if __name__ == "__main__": 
    main()
