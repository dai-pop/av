import re

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


def add_data( base, forms, description, number, out ):
    a = {}
    a['base'] = base
    a['forms'] = forms
    a['desc'] = description
    a['number'] = number
    out.append( a )



def get_dic( words ):

    alldata = []

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

        description = re.sub( r'■.*', '', description )

        m = re.search(r"【変化】(?P<infected>.*?)[【\n]", line)
        if m:
            infected_forms = deal_doublechar( re.findall( r'[a-zA-Z\(\)]+', m.group('infected') ) )

        if (prev_word == word):
            prev_description += "\n" + description
        else:
            if prev_word in words:
                number = words.index(prev_word) + 1
                infected_forms.insert( 0, prev_word )
                add_data( prev_word, infected_forms, prev_description, number, alldata )

            prev_word = word
            prev_description = description
            infected_forms = []

    if ( prev_word in words ):
        number = words.index(prev_word) + 1
        infected_forms.insert( 0, prev_word )
        add_data( prev_word, infected_forms, prev_description, number, alldata )

    source.close()

    return alldata

