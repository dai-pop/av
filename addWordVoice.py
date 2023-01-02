#!python
import os
import tempfile

from google.cloud import texttospeech
import subprocess
import click

def add_word_voice( word, infile, outfile, keyfile, voicedir):

    mp3file = os.path.join( voicedir, f"{word}.mp3" )

    if not os.path.exists(mp3file):
        client = texttospeech.TextToSpeechClient.from_service_account_json(keyfile)
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

        with open(mp3file, "wb") as out:
            out.write(response.audio_content)

    tmpdir = tempfile.TemporaryDirectory()

    tmpmp4 = os.path.join( tmpdir.name, infile)
    subprocess.run(["ffmpeg", "-i", infile, "-af", "afade=t=in:st=0:d=1.5:curve=exp", "-c:v", "copy", tmpmp4])
    subprocess.run(["ffmpeg", "-i", tmpmp4, "-i", mp3file, "-c:v", "copy", "-filter_complex",
                    "[0:a][1:a] amix=inputs=2:duration=longest [audio_out]",
                    "-map", "0:v", "-map", "[audio_out]", "-y", outfile])

    tmpdir.cleanup()

@click.command()
@click.option('--word', required=True, type=str, help='word to speak')
@click.option('--infile', required=True, type=str, help='input movie file')
@click.option('--outfile', required=True, type=str, help='output movie file')
@click.option('--key', required=True, type=str, help='key file')
@click.option('--voicedir', required=True, type=str, help='voice directory')
def main(word, infile, outfile, key, voicedir):
    add_word_voice(word, infile, outfile, key, voicedir)


if __name__ == "__main__":
    main()
