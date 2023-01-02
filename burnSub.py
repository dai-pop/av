#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import glob
import subprocess
import sys
import pathlib
import os
import click

@click.command()
@click.option('--movie_in', required=True, type=str)
@click.option('--movie_out', required=True, type=str)
@click.option('--en', required=True, type=str)
@click.option('--jp', required=False, type=str)
def run(movie_in, movie_out, en, jp):

    timestamp = pathlib.Path(movie_in).stem + " '%{pts\:gmtime\:0\:%H\\\\\\:%M\\\\\\:%S}'"

    vf_option = f"scale=1280:-1,subtitles={en}:force_style='FontName=IPAGothic,Alignment=3',drawtext=fontfile=/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf:fontsize=32:box=1:boxcolor=white@0.3:fontcolor=black:text={timestamp}:x=0:y=h-th"

    if jp:
        vf_option += f",subtitles={jp}:force_style='FontName=IPAGothic,Alignment=7'"

    subprocess.run( ["ffmpeg", "-i", movie_in, "-vf", vf_option, movie_out ] )


if __name__ == "__main__": 
    run()
