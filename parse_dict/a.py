import re
import json


def add_data( base, level, forms, description, out ):
    a = {}
    a['base'] = base
    a['level'] = level
    a['forms'] = forms
    a['desc'] = description
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

source = open("EIJIRO-1448.TXT", encoding="cp932")

prev_word = ""
prev_description = ""
prev_level = 0
infected_forms = []

for line in source:
    m = re.match(r"^■(?P<word>[^\{]+) (?: \{(?P<tag>.+)\} )?: (?P<description>.+)$", line)
    word = m.group("word")
    tag = m.group("tag")
    if tag:
        description = f'{{{m.group("tag")}}} {m.group("description")}'
    else:
        description = m.group("description")

    m = re.search(r"【レベル】(?P<level>\d+)", line)
    if m and m.group("level"):
        level = int(m.group("level"))
    else:
        level = 0

    m = re.search(r"【変化】(?P<infected>.*?)[【\n]", line)
    if m:
        infected_forms = deal_doublechar( re.findall( r'[a-zA-Z]+', m.group('infected') ) )

    if (prev_word == word):
        prev_description += "\n" + description
        prev_level = max(prev_level, level)
    else:
        if (prev_level >= 1):
            infected_forms.insert( 0, prev_word )
            add_data( prev_word, prev_level, infected_forms, prev_description, alldata )

        prev_word = word
        prev_description = description
        prev_level = 0
        infected_forms = []

if (prev_level >= 1):
    infected_forms.insert( 0, prev_word )
    add_data( prev_word, prev_level, infected_forms, prev_description, alldata )

source.close()

print( json.dumps( alldata, indent=4 ) )
