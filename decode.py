import re
from vigenere import Vigenere
from caesar import Caesar
from itertools import permutations
from helpers import ngram


def crack_caesar(
        ctext,
        LANG=[
            'abcdefghijklmnopqrstuvwxyz',
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'],
        ALPHABET=26):
    # crack Caesar using quadgrams statistics
    # preserve text with punctuation
    ctext_c = ctext[::]

    # leave only letters in ctext
    ctext = re.sub(r'[^a-z]', '', ctext.lower())

    qgram = ngram()  # load our quadgram statistics
    # calculate score for key=1
    pt = Caesar(1).caesar_decode(ctext, LANG, ALPHABET)
    best_score, best_key = qgram.score(pt), 1

    # check for the bestscoring key
    for i in range(2, 26):
        pt = Caesar(i).caesar_decode(ctext, LANG, ALPHABET)
        pt_score = qgram.score(pt)
        if pt_score > best_score:
            best_score, best_key = pt_score, i

    pt = Caesar(best_key).caesar_decode(ctext_c, LANG, ALPHABET)
    print('Decrypted text with key', best_key, ':', pt)
    return best_key, pt


def crack_vigenere(
        ctext,
        LANG=[
            'abcdefghijklmnopqrstuvwxyz',
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'],
        ALPHABET=26):
    # crack Vigenere using quadgrams statistics
    trigram, qgram = ngram(
        'ngrams/english_trigrams.txt'), ngram('ngrams/english_quadgrams.txt')

    # preserve text with punctuation
    ctext_c = ctext[::]

    # leave only letters in ctext
    ctext = re.sub(r'[^a-z]', '', ctext.lower())

    # keep a list of the N best possible keys we have seen, discard anything
    # else
    class nbest:
        def __init__(self, N=100):
            self.store = []
            self.N = N

        # add item to store, sort store descending, keep N best items (keys)
        def add(self, item):
            self.store.append(item)
            self.store.sort(reverse=True)
            self.store = self.store[:self.N]

        # this is needed to support indexing for nbest object (look to
        # rec[k][1])
        def __getitem__(self, k):
            return self.store[k]

    items = []  # a list for final key-decoded text pairs
    for k_len in range(
            3, 6):  # we will be testing keys of lenght from 3 to 10
        rec = nbest()
        # first, calculate scores of every possible trigram + a's (as a key)
        # and add N best scores to rec
        for i in permutations(LANG[0], 3):
            key = ''.join(i) + 'a' * (k_len - len(i))
            pt = Vigenere(key).vigenere_decode(ctext, LANG, ALPHABET)
            score = 0
            for j in range(0, len(ctext), k_len):
                score += trigram.score(pt[j:j + 3])
            rec.add((score, ''.join(i)))

        next_rec = nbest()
        # next, calculate score for every possible key of k_len
        for i in range(0, k_len - 3):
            for k in range(rec.N):
                for c in LANG[0]:
                    key = rec[k][1] + c
                    fullkey = key + 'a' * (k_len - len(key))
                    pt = Vigenere(fullkey).vigenere_decode(
                        ctext, LANG, ALPHABET)
                    score = 0
                    for j in range(0, len(ctext), k_len):
                        score += qgram.score(pt[j:j + len(key)])
                    next_rec.add((score, key))
            rec = next_rec
            next_rec = nbest()
        bestkey = rec[0][1]
        pt = Vigenere(bestkey).vigenere_decode(ctext, LANG, ALPHABET)
        bestscore = qgram.score(pt)

        # check if there is better score than bestscore. this is needed because
        # keys in rec were tested with a's (f.e. ciphaaa). Now they have to be
        # used without a's
        for i in range(rec.N):
            pt = Vigenere(rec[i][1]).vigenere_decode(ctext, LANG, ALPHABET)
            score = qgram.score(pt)
            if score > bestscore:
                bestkey = rec[i][1]
                bestscore = score

        pt = Vigenere(bestkey).vigenere_decode(ctext_c, LANG, ALPHABET)
        print(bestscore, 'Vigenere, k_len', k_len, ':"' + bestkey + '",', pt)
        items.append((bestkey.upper() + ": " + pt))
    return items


def crack_cipher(
    ctext,
    LANG=[
        'abcdefghijklmnopqrstuvwxyz',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ']):
    # Check if cipher is monoalphabetic (caesar) or polyalphabetic (vigenere)
    # using Index of Coincidence
    ctext_c = ctext[::]

    # leave only letters in ctext
    ctext = re.sub(r'[^a-z]', '', ctext.lower())
    total_n = len(ctext)

    # count letters in ctext and add count to the dictionary
    letters = {}
    for letter in LANG[0]:
        letters[letter] = ctext.count(letter)

    # calculate I.C. for ctext
    ic_up = 0
    for count in letters.values():
        ic_up += count * (count - 1)
    ic = round(ic_up / (total_n * (total_n - 1)), 3)

    if ic > 0.053:
        print("PROBABLY CAESAR, I.C.:", ic)
        return crack_caesar(ctext_c)
    else:
        print("PROBABLY VIGENERE, I.C.:", ic)
        return crack_vigenere(ctext_c)
