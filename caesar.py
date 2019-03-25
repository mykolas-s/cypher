from string import ascii_lowercase, ascii_uppercase, digits

class Caesar():

    def __init__(self, key):
        self.key = int(key)

    def caesar_encode(
            self,
            plaintext,
            LANG=[ascii_lowercase, ascii_uppercase],
            ALPHABET=len(ascii_lowercase)):
        # for every character in plaintext, shift it by shiftsize k (wrap
        # around the alphabet, is k > ALPHABET)
        ctext = ""
        for c in plaintext:
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
            LANG=[ascii_lowercase, ascii_uppercase],
            ALPHABET=len(ascii_lowercase)):
        plaintext = ""
        for c in ctext:
            if c.islower():
                plaintext += LANG[0][(LANG[0].index(c) + ALPHABET -
                               self.key) % ALPHABET]
            elif c.isupper():
                plaintext += LANG[1][(LANG[1].index(c) + ALPHABET -
                               self.key) % ALPHABET]
            elif c.isdigit():
                plaintext += digits[(digits.index(c) - self.key) % 10]
            else:
                plaintext += c
        return plaintext
