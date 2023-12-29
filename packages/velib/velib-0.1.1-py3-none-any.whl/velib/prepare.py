
def dict_to_inline(d):
    try:
        return ', '.join([str(x) + ': ' + str(d[x]) for x in d.keys()])
    except:
        return str(d)
