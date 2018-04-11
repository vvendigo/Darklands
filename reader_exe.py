
def readZeroEnded(data, pos, endpos):
    out = []
    while pos < endpos:
        s = ''
        p2 = data.find('\0', pos)
        if p2 < 0: p2 = endpos
        out.append(data[pos:p2])
        pos = p2 + 1
    return out

def readData(dlPath):
    fname = dlPath + '/darkland.exe'
    data = open(fname).read()
    out = {}


    '''
month names
0x00187d00
0x00187d56

protection symbols names
0x00187d56
0x00187e12

alchemy menu opts?
0x00187e12
0x00187e5f

load game menu opts
0x00187e5f
0x00187e9e

character add menu opts
0x00187e9e
0x00187f26

... other menu opts

some action/quest related strings
0x0018804f
0x001881d9
    '''

    pos = 0x001881d9
    end = 0x00188222
    out['attributes'] = readZeroEnded(data, pos, end)

    pos = 0x00188222
    end = 0x001882f0
    out['skills'] = readZeroEnded(data, pos, end)

    '''
Menu opts,
0x001882f0
    '''
    pos = 0x00188350
    end = 0x001884d3
    out['occupations'] = readZeroEnded(data, pos, end)

    pos = 0x0018879a
    end = 0x00188801
    out['family'] = readZeroEnded(data, pos, end)


    '''
daemon names
...

card variable names
0x00188af4
0x00188dd2 ??

city/village ruller titles?
0x00188dd2
0x00188e71

'''

    pos = 0x00188e71
    end = 0x001891a0
    out['firstnames_male'] = readZeroEnded(data, pos, end)

    pos = 0x001891a0
    end = 0x0018945f
    out['firstnames_female'] = readZeroEnded(data, pos, end)

    pos = 0x0018945f
    end = 0x00189a20
    out['surnames'] = readZeroEnded(data, pos, end)

    '''
some tables??
0x00189a44
0x0018b710 cca
    '''

    #bg card fnames
    pos = 0x0018b710
    end = 0x0018c157
    out['bg_cards'] = readZeroEnded(data, pos, end)

    '''
some table??
0x0018c157
0x0018ccb7 cca.?

some game menus & msgs
0x00190fca

battle data (debug print?)
0x0019298a

files for map
0x00193685
0x001937ae


0x001937c6

pictures for inventory + texts (atts, skill abbrs)
0x00193844
0x00193cd8
    '''
    pos = 0x00193beb
    end = 0x00193c06
    out['attributes_abbr'] = readZeroEnded(data, pos, end)
    pos = 0x00193c10
    end = 0x00193c33
    sk1 = readZeroEnded(data, pos, end)
    pos = 0x00193c38
    end = 0x00193c55
    sk2 = readZeroEnded(data, pos, end)
    pos = 0x00193c8f
    end = 0x00193cad
    sk3 = readZeroEnded(data, pos, end)
    out['skills_abbr'] = sk1 + sk2 + sk3

    '''
buy/sell
0x00193cd8
0x00193fc2

alchemy
0x00193fc2
0x001941ae

saint texts, pics...
0x001941ae

party info texts
0x001943ec

cache operations
0x001945b8

gasthaus stay opts and texts
0x001947ec

camp opts and texts
0x00194ac2
    '''
    # msg card names + comments or what?
    pos = 0x00196502
    end = 0x0019783f
    #out['msg_cards'] = [t.upper() if t.startswith('$') else t for t in readZeroEnded(data, pos, end)]
    out['msg_cards'] = [t.upper() if t.startswith('$') else t for t in readZeroEnded(data, pos, end)]# if t.startswith('$')]

    return out

def ps(s):
    out = ''
    for ch in s:
        o = ord(ch)
        if ch >= ' ' and o < 127:
            out += ch
        else:
            out += '<'+str(o)+'>'
    return out

def serArr(a):
    return '"'+('","'.join([ tchars(n) for n in a ]))+'"'

# main ------------
if __name__ == '__main__':
    import sys
    from utils import itemStr, tchars

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    data = readData(dlPath)

    # print data
    #for i, s in enumerate(data['bg_cards']):
    #    print '%4d %s'%(i, ps(s))
    #print
    #idx = 0
    #for i, s in enumerate(data['msg_cards']):
    #    #if s.endswith('.MSG'): continue
    #    print '%4d %s'%(idx, ps(s))
    #    idx += 1
    print
    print serArr(data['attributes_abbr']) ; print
    print serArr(data['attributes']) ; print
    print serArr(data['skills_abbr']) ; print
    print serArr(data['skills']) ; print
    '''
    for abb, name in zip(data['attributes_abbr'], data['attributes']):
        print '    '+abb+': "'+name+'",'
    print
    for abb, name in zip(data['skills_abbr'], data['skills']):
        print '    '+abb+': "'+name+'",'
    '''
    print ', '.join(['%s:0'%s for s in data['skills_abbr']])


    print serArr(data['firstnames_male']) ; print
    print serArr(data['firstnames_female']) ; print
    print serArr(data['surnames']) ; print
    print serArr(data['occupations']) ; print
    print serArr(data['family']) ; print



