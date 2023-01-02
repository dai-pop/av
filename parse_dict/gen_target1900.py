import re
import json
import csv

import eijiro


from decimal import Decimal

def decimal_to_int(obj):
    if isinstance(obj, Decimal):
        return int(obj)


target1900 = []

with open( "target1900.csv", encoding='utf8') as f:
    for e in csv.reader(f):
        target1900.append(e[1])

alldata = eijiro.get_dic( target1900 )

print( json.dumps( alldata, default=decimal_to_int, indent=4) )


