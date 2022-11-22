import re
import json
import csv

from decimal import Decimal


def decimal_to_int(obj):
    if isinstance(obj, Decimal):
        return int(obj)


def add_data( base, forms, description, number, out ):
    a = {}
    a['base'] = base
    a['forms'] = forms
    a['desc'] = description
    a['number'] = number
    out.append( a )


def deal_doublechar( forms ):
    ret = []
    for form in forms:
        m = re.match(r"^(?P<head>\w+)\((?P<doublestr>\w+)\)(?P<tail>\w+)$", form)
        if m:
            ret.append( m.group('head') + m.group('tail') )
            ret.append( m.group('head') + m.group('doublestr') + m.group('tail') )
        else:
            ret.append(form)

    return ret


    
alldata = []
target1900 = []

with open( "target1900.csv" ) as f:
    for e in csv.reader(f):
        target1900.append(e[1])

source = open("EIJIRO-1448.TXT", encoding="cp932")

prev_word = ""
prev_description = ""
infected_forms = []

for line in source:
    m = re.match(r"^■(?P<word>[^\{]+) (?: \{(?P<tag>.+)\} )?: (?P<description>.+)$", line)
    word = m.group("word")
    tag = m.group("tag")
    if tag:
        description = f'{{{m.group("tag")}}} {m.group("description")}'
    else:
        description = m.group("description")

    m = re.search(r"【変化】(?P<infected>.*?)[【\n]", line)
    if m:
        infected_forms = deal_doublechar( re.findall( r'[a-zA-Z\(\)]+', m.group('infected') ) )

    if (prev_word == word):
        prev_description += "\n" + description
    else:
        if prev_word in target1900:
            number = target1900.index(prev_word) + 1
            infected_forms.insert( 0, prev_word )
            add_data( prev_word, infected_forms, prev_description, number, alldata )

        prev_word = word
        prev_description = description
        infected_forms = []

if ( prev_word in target1900 ):
    number = target1900.index(prev_word) + 1
    infected_forms.insert( 0, prev_word )
    add_data( prev_word, infected_forms, prev_description, number, alldata )

source.close()

print( json.dumps( alldata, default=decimal_to_int, indent=4) )


