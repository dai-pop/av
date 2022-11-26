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

    subprocess.run( ["ffmpeg", "-i", videofile, "-i", mp3file, "-c:v", "copy", "-filter_complex", "[0:a][1:a] amix=inputs=2:duration=longest [audio_out]",
                     "-map", "0:v", "-map", "[audio_out]", "-y", videofile.replace(".mp4", "_voice.mp4")] )

#    output_str = subprocess.run('ls', capture_output=True, text=True).stdout
#    subprocess.run( 'ffmpeg -loop 1 -i screenshot.png -i a.mp3 -pix_fmt yuv420p -shortest -vf "drawtext=fontfile=/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf:fontsize=50:box=1:boxcolor=white@0.3:fontcolor=black:text=aaaaaa:x=0:y=h-th" output.mp4', shell=True )
#    subprocess.run( 'ffmpeg -i output.mp4 -vf "drawtext=fontfile=/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf:fontsize=50:box=1:boxcolor=white@0.3:fontcolor=black:text=aaaaaa:x=0:y=h-th" moji.mp4', shell=True )
#    subprocess.run( 'ffmpeg -i "concat:moji.mp4|stay.mp4" cat.mp4', shell=True )
# -filter_complex "amix=inputs=2:duration=longest:dropout_transition=2:weights=1 1" output    
#    x = subprocess.run( "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 a.mp3", shell=True, capture_output=True, text=True ).stdout
#    import pdb; pdb.set_trace()

def main():
    for f in sys.argv[1:]:
        m = re.search(r'_([a-z]+?)\.mp4', f)
        if m:
            addWordVoice( f, m.group(1) )

        
if __name__ == "__main__":
    main()
