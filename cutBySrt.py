# -*- coding: utf-8 -*-
import click
import pysrt
import json
import re
import glob
import subprocess
import pandas as pd


class OH(dict):
    __getattr__ = dict.get


def get_start_time( srtlist, index, initial_ms):
    if index == 0 or srtlist[index].start.ordinal - srtlist[index-1].start.ordinal > 10000  :
        return srtlist[index].start.ordinal
    else:
        return srtlist[index-1].start.ordinal


def get_end_time( srtlist, index, initial_ms):
    if index == len(srtlist)-1 or srtlist[index+1].start.ordinal - srtlist[index].start.ordinal > 10000  :
        return srtlist[index].end.ordinal
    else:
        return srtlist[index+1].end.ordinal


def makeDataFrame(srtfile):
    words = []
    texts = []
    start_times = []
    end_times = []

    srt = list(pysrt.open(srtfile))
    for i, e in enumerate(srt):
        text = e.text.replace("\n"," ")
        text = re.sub(r'\(.+\)', '', text )

        for word in re.findall( r'[\w\']+', text ):
            words.append(word.lower())
            texts.append(text)
            start_times.append(get_start_time(srt, i, e.start.ordinal))
            end_times.append(get_end_time(srt, i, e.end.ordinal))

    return pd.DataFrame( {"w": words,"t": texts, "st": start_times, "et": end_times})

    
def get_tangocho(file):
    return json.loads( open(file).read(), object_hook=OH )
    
                
@click.command()
@click.option('--srt', required=True, type=str, help='subtitle file')
@click.option('--movie', required=True, type=str, help='movie file')
@click.option('--dic', required=True, type=str, help='dictionary file')
def main(srt, movie, dic):
    df = makeDataFrame(srt)
    tangocho = get_tangocho(dic)

    for tango in tangocho:
        for form in tango.forms:
            match_df = df[ df.w == form ]
            if len( match_df ) > 0:
                with open("desc.txt", "w") as f:
                    print(tango.desc, file=f)
                
                in_movie = movie

                start_time_ms = match_df['st'].values[0]
                end_time_ms = match_df['et'].values[0]

                vf_option = f"drawtext=fontfile=/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf:fontsize=80:box=1:boxcolor=white@0.3:fontcolor=black:text={tango.base}:x=w-tw:y=h/2,drawtext=fontfile=/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf:fontsize=28:box=1:boxcolor=white@0.3:fontcolor=black:textfile=desc.txt"
                out_movie = tango.base + "_" + in_movie
                subprocess.run( ["ffmpeg", "-ss", f"{start_time_ms-200}ms", "-i", in_movie, "-t", f"{end_time_ms-start_time_ms+200}ms", "-vf", vf_option, out_movie])

                break


if __name__ == '__main__':
    main()
