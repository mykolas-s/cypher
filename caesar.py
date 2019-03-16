class Caesar():

    def __init__(self, key):
        self.key = int(key)

    def caesar_encode(
            self,
            pt,
            LANG=[
                'abcdefghijklmnopqrstuvwxyz',
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ'],
            ALPHABET=26,
            digits='0123456789'):
        # for every character in plaintext, shift it by shiftsize k (wrap
        # around the alphabet, is k > ALPHABET)
        ctext = ""
        for c in pt:
            if c.islower():
                ctext += LANG[0][(LANG[0].index(c) + self.key) % ALPHABET]
            elif c.isupper():
                ctext += LANG[1][(LANG[1].index(c) + self.key) % ALPHABET]
            elif c.isdigit():
                ctext += digits[(digits.index(c) + self.key) % 10]
            else:
                ctext += c
        return ctext

    def caesar_decode(
            self,
            ctext,
            LANG=[
                'abcdefghijklmnopqrstuvwxyz',
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ'],
            ALPHABET=26,
            digits='0123456789'):
        pt = ""
        for c in ctext:
            if c.islower():
                pt += LANG[0][(LANG[0].index(c) + ALPHABET -
                               self.key) % ALPHABET]
            elif c.isupper():
                pt += LANG[1][(LANG[1].index(c) + ALPHABET -
                               self.key) % ALPHABET]
            elif c.isdigit():
                pt += digits[(digits.index(c) + ALPHABET - self.key) % 10]
            else:
                pt += c
        return pt
