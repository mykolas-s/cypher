import re
from vigenere import Vigenere
from caesar import Caesar
from itertools import permutations
from helpers import ngram
from string import ascii_lowercase, ascii_uppercase, digits


def crack_caesar(
        ctext,
        LANG=[ascii_lowercase, ascii_uppercase],
        ALPHABET=len(ascii_lowercase)):
    # crack Caesar using quadgrams statistics
    # preserve text with punctuation
    ctext_c = ctext[::]

    # leave only letters in ctext
    ctext = re.sub(r'[^a-z]', '', ctext.lower())

    quadgram = ngram()  # load our quadgram statistics
    # calculate score for key=1
    plaintext = Caesar(1).caesar_decode(ctext, LANG, ALPHABET)
    best_score, best_key = quadgram.score(plaintext), 1

    # check for the bestscoring key
    for i in range(2, 26):
        plaintext = Caesar(i).caesar_decode(ctext, LANG, ALPHABET)
        plaintext_score = quadgram.score(plaintext)
        if plaintext_score > best_score:
            best_score, best_key = plaintext_score, i

    plaintext = Caesar(best_key).caesar_decode(ctext_c, LANG, ALPHABET)
    print('Decrypted text with key', best_key, ':', plaintext)
    return best_key, plaintext


def crack_vigenere(
        ctext,
        LANG=[ascii_lowercase, ascii_uppercase],
        ALPHABET=len(ascii_lowercase)):
    # crack Vigenere using quadgrams statistics
    trigram, quadgram = ngram(
        'ngrams/english_trigrams.txt'), ngram('ngrams/english_quadgrams.txt')

    # preserve text with punctuation
    ctext_copy = ctext[::]

    # leave only letters in ctext
    ctext = re.sub(r'[^a-z]', '', ctext.lower())

    # keep a list of the N best possible keys yet, discard anything else
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
            3, 11):  # we will be testing keys of lenght from 3 to 10
        rec = nbest()
        # first, calculate scores of every possible trigram + a's (as a key)
        # and add N best scores to rec
        for i in permutations(LANG[0], 3):
            key = ''.join(i) + 'a' * (k_len - len(i))
            plaintext = Vigenere(key).vigenere_decode(ctext, LANG, ALPHABET)
            score = 0
            for j in range(0, len(ctext), k_len):
                score += trigram.score(plaintext[j:j + 3])
            rec.add((score, ''.join(i)))

        next_rec = nbest()
        # next, calculate score for every possible key of k_len
        for i in range(0, k_len - 3):
            for k in range(rec.N):
                for c in LANG[0]:
                    key = rec[k][1] + c
                    fullkey = key + 'a' * (k_len - len(key))
                    plaintext = Vigenere(fullkey).vigenere_decode(
                        ctext, LANG, ALPHABET)
                    score = 0
                    for j in range(0, len(ctext), k_len):
                        score += quadgram.score(plaintext[j:j + len(key)])
                    next_rec.add((score, key))
            rec = next_rec
            next_rec = nbest()
        bestkey = rec[0][1]
        plaintext = Vigenere(bestkey).vigenere_decode(ctext, LANG, ALPHABET)
        bestscore = quadgram.score(plaintext)

        # check if there is better score than bestscore. this is needed because
        # keys in rec were tested with a's (f.e. pytaaa). Now they have to be
        # used without a's
        for i in range(rec.N):
            plaintext = Vigenere(rec[i][1]).vigenere_decode(ctext, LANG, ALPHABET)
            score = quadgram.score(plaintext)
            if score > bestscore:
                bestkey = rec[i][1]
                bestscore = score

        plaintext = Vigenere(bestkey).vigenere_decode(ctext_copy, LANG, ALPHABET)
        print(bestscore, 'Vigenere, k_len', k_len, ':"' + bestkey + '",', plaintext)
        items.append((bestkey.upper() + ": " + plaintext))
    return items


def crack_cipher(
    ctext,
    LANG=[ascii_lowercase, ascii_uppercase],
    ALPHABET=len(ascii_lowercase)):
    # Check if cipher is monoalphabetic (caesar) or polyalphabetic (vigenere)
    # using Index of Coincidence
    ctext_copy = ctext[::]

    # leave only letters in ctext
    ctext = re.sub(r'[^a-z]', '', ctext.lower())
    total_n = len(ctext)

    # count letters in ctext and add count to the dictionary
    letters = {}
    for letter in LANG[0]:
        letters[letter] = ctext.count(letter)

    # calculate I.C. for ctext
    ic_numerator = 0
    for count in letters.values():
        ic_numerator += count * (count - 1)
    ic = round(ic_numerator / (total_n * (total_n - 1)), 3)

    if LANG == [ascii_lowercase, ascii_uppercase]:
        if ic > 0.053:
            print("PROBABLY CAESAR, I.C.:", ic)
            return crack_caesar(ctext_copy, LANG, ALPHABET)
        else:
            print("PROBABLY VIGENERE, I.C.:", ic)
            return crack_vigenere(ctext_copy, LANG, ALPHABET)
    else:
        if ic > 0.058:
            print("PROBABLY CAESAR, I.C.:", ic)
            return crack_caesar_lt(ctext_copy, LANG, ALPHABET)
        else:
            print("PROBABLY VIGENERE, I.C.:", ic)
            message = "This text is most likely encoded in Vigenere. The program can break lithuanian text encoded only in Caesar's"
            return message


def crack_caesar_lt(
        ctext,
        LANG=[ascii_lowercase, ascii_uppercase],
        ALPHABET=len(ascii_lowercase)):
    # crack Caesar using bigrams statistics
    # preserve text with punctuation
    ctext_c = ctext[::]

    # leave only letters in ctext
    ctext = re.sub(r'[^a-z]', '', ctext.lower())

    bigram = ngram('ngrams/lt_bigrams.txt')  # load our bigram statistics
    # calculate score for key=1
    plaintext = Caesar(1).caesar_decode(ctext, LANG, ALPHABET)
    best_score, best_key = bigram.score(plaintext), 1

    # check for the bestscoring key
    for i in range(2, 26):
        plaintext = Caesar(i).caesar_decode(ctext, LANG, ALPHABET)
        plaintext_score = bigram.score(plaintext)
        if plaintext_score > best_score:
            best_score, best_key = plaintext_score, i

    plaintext = Caesar(best_key).caesar_decode(ctext_c, LANG, ALPHABET)
    print('Decrypted text with key', best_key, ':', plaintext)
    return best_key, plaintext