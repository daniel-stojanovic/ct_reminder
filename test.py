def test(**kwargs):
        print "{hello}".format(**kwargs)


test(hello="hallo danny")




def test(**kwargs):
    print '{hello}'.format(**kwargs)

test(hello="world")