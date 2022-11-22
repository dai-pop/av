#!python

import json
import re

class OH(dict):
    __getattr__ = dict.get

eijiro = json.loads( open("eijirosvl.json").read(), object_hook=OH)



with open( "edgerunners.txt" ) as f:
    for line in f.readlines():
        for word in re.findall( r'[\w\']+', line ):
            lowerword = word.lower()
            for e in eijiro:
                if lowerword in e.forms and e.level > 8:
                    print( word )
                    print( e.desc )
