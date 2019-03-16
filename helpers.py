from flask import render_template
from math import log10


def apology(message, code=400):
    # Render message as an apology to user.
    def escape(s):
        # Escape special characters.
        # https://github.com/jacebrowning/memegen#special-characters
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code,
                           bottom=escape(message)), code


class ngram:
    def __init__(self, f="ngrams/english_quadgrams.txt"):
        # load a file containing ngrams and counts, calculate log probabilities
        self.ngrams = {}
        for line in open(f):
            key, count = line.lower().split(" ")
            self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())
        # calculate log probabilities of ngrams
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(self.ngrams[key] / self.N)
        # Some ngrams appears 0 times in a file. So that the log probability
        # would not be -infinity, we floor all probabilities.
        self.floor = log10(0.01 / self.N)

    def score(self, text):
        # compute the score (i.e. sum of log probabilities) of text
        score = 0
        ngrams = self.ngrams.__getitem__
        # for every possible ngram in text, get its score and add to the
        # overall score of text. If ngram is not in text, floor its score
        for i in range(len(text) - self.L + 1):
            if text[i:i + self.L] in self.ngrams:
                score += ngrams(text[i:i + self.L])
            else:
                score += self.floor
        return score
