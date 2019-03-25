from string import ascii_lowercase, ascii_uppercase, digits

class Vigenere():

    def __init__(self, key):
        self.key = key.lower()
        self.L = len(key)

    def vigenere_encode(
            self,
            plaintext,
            LANG=[ascii_lowercase, ascii_uppercase],
            ALPHABET=len(ascii_lowercase)):
        count = 0  # set count for special characters
        # for every character in plaintext, shift it by key[j] (wrap around the
        # alphabet, if key+pt[i] > ALPHABET)
        ctext = ""
        for i in range(len(plaintext)):
            j = (i - count) % self.L
            if plaintext[i].islower():
                ctext += LANG[0][(LANG[0].index(plaintext[i]) +
                                  LANG[0].index(self.key[j])) %
                                 ALPHABET]
            elif plaintext[i].isupper():
                ctext += LANG[1][(LANG[1].index(plaintext[i]) +
                                  LANG[0].index(self.key[j])) %
                                 ALPHABET]
            elif plaintext[i].isdigit():
                ctext += digits[(digits.index(plaintext[i]) +
                                 LANG[0].index(self.key[j])) % 10]
            else:
                ctext += plaintext[i]
                count += 1
        return ctext

    def vigenere_decode(
            self,
            ctext,
            LANG=[ascii_lowercase, ascii_uppercase],
            ALPHABET=len(ascii_lowercase)):
        count = 0
        plaintext = ""
        for i in range(len(ctext)):
            j = (i - count) % self.L
            if ctext[i].islower():
                plaintext += LANG[0][(LANG[0].index(ctext[i]) +
                               ALPHABET -
                               LANG[0].index(self.key[j])) %
                              ALPHABET]
            elif ctext[i].isupper():
                plaintext += LANG[1][(LANG[1].index(ctext[i]) +
                               ALPHABET -
                               LANG[0].index(self.key[j])) %
                              ALPHABET]
            elif ctext[i].isdigit():
                plaintext += digits[(digits.index(ctext[i]) +
                              LANG[0].index(self.key[j])) % 10]
            else:
                plaintext += ctext[i]
                count += 1
        return plaintext
