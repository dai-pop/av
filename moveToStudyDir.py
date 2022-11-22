import glob


import shutil


import os


import subprocess


def main():
    with open( "words.txt" ) as f:
        words = f.read().split()

    for w in words:
        mp4files = glob.glob( f"サイバーパンク_ エッジランナーズ/**/*_{w}.mp4", recursive=True )
        for file in mp4files:
            mp4 = f"{w}_{os.path.basename(file)}"
            mp3 = mp4.replace( ".mp4", ".mp3" ) 
            shutil.copy( file, f"studydir/mp4/{mp4}" )
            subprocess.run( ["ffmpeg", "-i", file, f"studydir/mp3/{mp3}"] )
                
if __name__ == "__main__": 
    main()
