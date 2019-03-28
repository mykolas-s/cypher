from flask import Flask, render_template, request
from werkzeug.exceptions import default_exceptions
from helpers import apology
from caesar import Caesar
from vigenere import Vigenere
from decode import crack_cipher
from string import ascii_lowercase, ascii_uppercase, digits
# Configure application
app = Flask(__name__)

lt_lang, lt_alphabet = ['aąbcčdeęėfghiįyjklmnoprsštuųūvzž', 'AĄBCČDEĘĖFGHIĮYJKLMNOPRSŠTUŲŪVZŽ'], 32

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        # set language
        if request.form.get("lang") == 'english':
            LANG, ALPHABET = [ascii_lowercase, ascii_uppercase], len(ascii_lowercase)
        elif request.form.get("lang") == 'lithuanian':
            LANG, ALPHABET = lt_lang, lt_alphabet
        # get plaintext
        plaintext = request.form.get('plaintext')

        # BREAK (WITHOUT KNOWING CYPHER TYPE)
        if request.form.get("enc_dec") == ("Break"):
            try:
                broken = crack_cipher(plaintext, LANG, ALPHABET)
                if len(broken) == 2:
                    key, text = str(broken[0]) + ", Caesar", broken[1]
                    return render_template(
                        "index.html",
                        cyptext=key,
                        title="KEY, CYPHER: ",
                        footnote="DECRYPTED TEXT: ",
                        cyptext2=text)
                elif broken == "This text is most likely encoded in Vigenere. The program can break lithuanian text encoded only in Caesar's":
                    return render_template(
                        "index.html",
                        cyptext2=broken.upper())                    
                else:
                    return render_template(
                        "index.html",
                        broken=broken,
                        title="POSSIBLE KEYS AND DECRYPTED TEXT USING THEM:")
            except (ValueError, IndexError):
                return apology(
                    "please provide text in chosen language")
        # CAESAR
        if request.form.get("cypher") == 'caesar':
            # set key. If key is not a number, return apology
            try:
                key = int(request.form.get("shift"))
            except BaseException:
                return apology("must provide valid shift size")

            # check if user uses encryption or decryption
            if request.form.get("enc_dec") == 'Encrypt':
                try:
                    ctext = Caesar(key).caesar_encode(plaintext, LANG, ALPHABET)
                    return render_template(
                        "index.html", cyptext=ctext, title="ENCRYPTED TEXT:")
                except ValueError:
                    return apology(
                        "please provide text in chosen language")

            elif request.form.get("enc_dec") == 'Decrypt':
                try:
                    ctext = Caesar(key).caesar_decode(plaintext, LANG, ALPHABET)
                    return render_template(
                        "index.html", cyptext=ctext, title="DECRYPTED TEXT:")
                except ValueError:
                    return apology(
                        "please provide text in chosen language")

        # VIGENERE
        elif request.form.get("cypher") == 'vigenere':
            key = request.form.get("key")
            if key is None or key.isalpha() == False:
                return apology("must provide valid key")

            if request.form.get("enc_dec") == 'Encrypt':
                try:
                    ctext = Vigenere(key).vigenere_encode(plaintext, LANG, ALPHABET)
                    return render_template(
                        "index.html", cyptext=ctext, title="ENCRYPTED TEXT:")
                except ValueError:
                    return apology(
                        "please provide text in chosen language")

            elif request.form.get("enc_dec") == 'Decrypt':
                try:
                    ctext = Vigenere(key).vigenere_decode(plaintext, LANG, ALPHABET)
                    return render_template(
                        "index.html", cyptext=ctext, title="DECRYPTED TEXT:")
                except ValueError:
                    return apology(
                        "please provide text in chosen language")

    else:  # == if request.method == 'GET'
        return render_template("index.html")


def errorhandler(e):
    # handle error
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
