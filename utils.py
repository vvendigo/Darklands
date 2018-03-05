# coding=utf-8
import string

def bread(d):
    ''' read multibyte int (in DL common order)'''
    out = d[-1]
    for n in reversed(d[:-1]):
        out = (out << 8) | n
    return out

def rbread(d):
    ''' read multibyte int (in reversed order)'''
    out = d[0]
    for n in d[1:]:
        out = (out << 8) | n
    return out

def sread(d):
    ''' read string'''
    out = ''
    for b in d:
        if b == 0:
            return out
        out += chr(b)
    return out

def tchars(txt):
    ''' translate special chars to proper letters'''
    #print txt
    return txt.replace('|', 'ü').replace('{', 'ö').replace(chr(0x1f), 'æ')

def itemStr(c, attrs=None):
    ''' str(struct) '''
    out = ''
    for k, v in c.iteritems():
        if attrs and k not in attrs:
            continue
        out += "%s: "%k
        if type(v) == dict:
            out += '{\n'
            for vk, vv in v.iteritems():
                out += "\t%s: %s\n"%(vk, vv)
            out += '}'
        else:
            out += str(v)
        out += '\n'
    return out

def itemLn(c, attrs=None):
    ''' render in line '''
    out = ''
    if not attrs:
        attrs = c.keys()

    for k in attrs:
        l = 5
        if type(k) == tuple:
            k, l = k
        fmt = "%%%ds "%(l)
        out += fmt%(str(c[k])[:l])
    return out
