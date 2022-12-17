# -*- coding: utf-8 -*-

import pysrt
import json
import re
import glob
import subprocess
import pandas as pd

class OH(dict):
    __getattr__ = dict.get

def getStartTime( srtlist, index, initial_ms ):
    if index == 0 or srtlist[index].start.ordinal - srtlist[index-1].start.ordinal > 10000  :
        return srtlist[index].start.ordinal
    else:
        return srtlist[index-1].start.ordinal
    
def getEndTime( srtlist, index, initial_ms ):
    if index == len(srtlist)-1 or srtlist[index+1].start.ordinal - srtlist[index].start.ordinal > 10000  :
        return srtlist[index].end.ordinal
    else:
        return srtlist[index+1].end.ordinal

def makeDataFrame():
    words = []
    texts = []
    start_times = []
    end_times = []
    movie_files = []
    
    for file in glob.glob( "*.English.srt"):
        srt = list(pysrt.open(file))
        for i,e in enumerate(srt):
            text = e.text.replace("\n"," ")
            text = re.sub(r'\(.+\)', '', text )
            
            for word in re.findall( r'[\w\']+', text ):
                words.append(word.lower())
                texts.append(text)
                start_times.append( getStartTime( srt, i, e.start.ordinal ) )
                end_times.append( getEndTime( srt, i, e.end.ordinal ) )
                movie_files.append( file.replace(".English.srt",".mkv") )

    return pd.DataFrame( {"w":words,"t":texts, "st":start_times, "et":end_times, "mf":movie_files} )

    
def getTangocho():
    return json.loads( open("../target1900_ne.json").read(), object_hook=OH )
    
                
def run():

    df = makeDataFrame()
    tangocho = getTangocho()

    for tango in tangocho:
        for form in tango.forms:
            match_df = df[ df.w == form ]
            if len( match_df ) > 0:
                with open("desc.txt", "w") as f:
                    print(tango.desc, file=f)
                
                in_movie = match_df['mf'].values[0]
                in_srt_e = in_movie.replace( ".mkv", ".English.srt" )
                in_srt_j = in_movie.replace( ".mkv", ".Japanese.srt" )
                episode = "EP" + in_movie.replace( ".mkv", "" ) + " "

                start_time_ms = match_df['st'].values[0]
                end_time_ms = match_df['et'].values[0]

                timestamp = episode + "'%{pts\:gmtime\:0\:%M\\\\\\:%S}'"

                vf_option = f"subtitles={in_srt_j}:force_style='FontName=IPAGothic,Alignment=7',subtitles={in_srt_e}:force_style='FontName=IPAGothic,Alignment=3',drawtext=fontfile=/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf:fontsize=80:box=1:boxcolor=white@0.3:fontcolor=black:text={str(tango.number)} {tango.base}:x=w-tw:y=h/2,drawtext=fontfile=/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf:fontsize=28:box=1:boxcolor=white@0.3:fontcolor=black:textfile=desc.txt,drawtext=fontfile=/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf:fontsize=32:box=1:boxcolor=white@0.3:fontcolor=black:text={timestamp}:x=0:y=h-th"
                out_movie = in_movie.removesuffix(".mkv") + f"_NO_{tango.number:03}_" + tango.base + ".mp4"
                subprocess.run( ["ffmpeg", "-ss", f"{start_time_ms-200}ms", "-i", in_movie, "-t", f"{end_time_ms-start_time_ms+200}ms", "-vf", vf_option, out_movie ] )

                break
                


if __name__ == "__main__": 
    run()
