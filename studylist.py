import re
import glob


def main():
    for file in glob.glob( "サイバーパンク_ エッジランナーズ/*/*/*.mp4"):
        m = re.match( r'.*_TANGO_\d+_(\w+)\.mp4', file )
        if m:
            print(m.group(1))
                
if __name__ == "__main__": 
    main()
