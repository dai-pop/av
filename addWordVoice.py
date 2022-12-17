#!python

from google.cloud import texttospeech

import subprocess

import sys


import re


def addWordVoice( videofile, word ):

    client = texttospeech.TextToSpeechClient.from_service_account_json("./key.json")

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    synthesis_input = texttospeech.SynthesisInput(text=word)

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    mp3file = "tmp.mp3"

    with open( mp3file, "wb") as out:
        out.write(response.audio_content)

    subprocess.run( ["ffmpeg", "-i", videofile, "-af", "afade=t=in:st=0:d=1.5:curve=exp", "-c:v", "copy", videofile.replace(".mp4", "_fadeout.mp4")] )
    subprocess.run( ["ffmpeg", "-i", videofile.replace(".mp4", "_fadeout.mp4"), "-i", mp3file, "-c:v", "copy", "-filter_complex", "[0:a][1:a] amix=inputs=2:duration=longest [audio_out]",
                     "-map", "0:v", "-map", "[audio_out]", "-y", videofile.replace(".mp4", "_voice.mp4")] )

def main():
    for f in sys.argv[1:]:
        m = re.search(r'_([a-z]+?)\.mp4', f)
        if m:
            addWordVoice( f, m.group(1) )

        
if __name__ == "__main__":
    main()
