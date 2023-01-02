#!python
import json
import os
import tempfile
import re
import pysrt
from google.cloud import texttospeech
import subprocess
import click
import dataclasses
import datetime


class OH(dict):
    __getattr__ = dict.get


@dataclasses.dataclass
class TsvEntry:
    front_text: str
    back_text: str
    back_mp3: str
    back_img: str


def genTsv(in_srt, dict_json, outtsv):
    tangocho = json.loads(open(dict_json).read(), object_hook=OH)

    outdata = []

    srt = list(pysrt.open(in_srt))
    for e in srt:
        text = e.text.replace("\n", " ")
        text = re.sub(r'\(.+\)', '', text)
        text = re.sub(r'\[.+\]', '', text)

        for word in re.findall(r'[\w\'’]+', text):
            lowerword = word.lower()
            for w in tangocho:
                if lowerword in w.forms:
                    desc = w.desc.replace("\n", "<br>")
                    starttime = str( datetime.timedelta( milliseconds=e.start.ordinal))

                    back_text = f"{desc}<br>{text}<br>{starttime}"
                    outdata.append( TsvEntry( w.base, back_text, f"{e.index}.mp3", f"{e.index}.jpg"))

    with open(outtsv, "w") as out:
        print("Text 1\tText 2\tSound 2\tPicture 2", file=out)
        for e in outdata:
            print( f"{e.front_text}\t{e.back_text}\t{e.back_mp3}\t{e.back_img}", file=out)


def genSplitMedia(in_movie, in_srt, outdir):
    srt = list(pysrt.open(in_srt))
    PRE_AUDIO_MSEC = 3000
    POST_AUDIO_MSEC = 2000
#    PRE_VIDEO_MSEC = 15000
    for e in srt:
        basepath = os.path.join(outdir, f"{e.index}")
        audio_start = e.start.ordinal - PRE_AUDIO_MSEC
        audio_duration = e.end.ordinal - e.start.ordinal + PRE_AUDIO_MSEC + POST_AUDIO_MSEC
#        video_start = e.start.ordinal - PRE_VIDEO_MSEC
#        video_duration = e.end.ordinal - e.start.ordinal + PRE_VIDEO_MSEC

        #subprocess.run(["ffmpeg", "-ss", f"{video_start}ms", "-i", in_movie, "-t", f"{video_duration}ms", "-af", "afade=t=in:st=0:d=1.5:curve=exp", basepath + ".mp4"])
        subprocess.run(["ffmpeg", "-ss", f"{audio_start}ms", "-i", in_movie, "-t", f"{audio_duration}ms", "-af", "afade=t=in:st=0:d=1.5:curve=exp", basepath + ".mp3"])


@click.command()
@click.option('--in_movie', required=True, type=str)
@click.option('--in_srt', required=True, type=str)
@click.option('--dict_json', required=True, type=str)
@click.option('--outdir', required=True, type=str)
@click.option('--outtsv', required=True, type=str)
def main(in_movie, in_srt, dict_json, outdir, outtsv):
   genTsv(in_srt, dict_json, outtsv)
   genSplitMedia(in_movie, in_srt, outdir)

if __name__ == "__main__":
    main()
