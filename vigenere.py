class Vigenere():

    def __init__(self, key):
        self.key = key.lower()
        self.L = len(key)

    def vigenere_encode(
            self,
            pt,
            LANG=[
                'abcdefghijklmnopqrstuvwxyz',
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ'],
            ALPHABET=26,
            digits='0123456789'):
        count = 0  # set count for special characters
        # for every character in plaintext, shift it by key[j] (wrap around the
        # alphabet, if key+pt[i] > ALPHABET)
        ctext = ""
        for i in range(len(pt)):
            j = (i - count) % self.L
            if pt[i].islower():
                ctext += LANG[0][(LANG[0].index(pt[i]) +
                                  LANG[0].index(self.key[j])) %
                                 ALPHABET]
            elif pt[i].isupper():
                ctext += LANG[1][(LANG[1].index(pt[i]) +
                                  LANG[0].index(self.key[j])) %
                                 ALPHABET]
            elif pt[i].isdigit():
                ctext += digits[(digits.index(pt[i]) +
                                 LANG[0].index(self.key[j])) % 10]
            else:
                ctext += pt[i]
                count += 1
        return ctext

    def vigenere_decode(
            self,
            ctext,
            LANG=[
                'abcdefghijklmnopqrstuvwxyz',
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ'],
            ALPHABET=26,
            digits='0123456789'):
        count = 0
        pt = ""
        for i in range(len(ctext)):
            j = (i - count) % self.L
            if ctext[i].islower():
                pt += LANG[0][(LANG[0].index(ctext[i]) +
                               ALPHABET -
                               LANG[0].index(self.key[j])) %
                              ALPHABET]
            elif ctext[i].isupper():
                pt += LANG[1][(LANG[1].index(ctext[i]) +
                               ALPHABET -
                               LANG[0].index(self.key[j])) %
                              ALPHABET]
            elif ctext[i].isdigit():
                pt += digits[(digits.index(ctext[i]) +
                              LANG[0].index(self.key[j])) % 10]
            else:
                pt += ctext[i]
                count += 1
        return pt
