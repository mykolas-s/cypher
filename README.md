<Cypher>

Cypher is a web application, which have 3 features: it can encode, decode or break (without knowing particular encryption key and cypher type) text using two types of cyphers: [Caesar](https://en.wikipedia.org/wiki/Caesar_cipher) and [Vigenere](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)

# Requirements
A microframework for Python – [Flask](http://flask.pocoo.org/)

# Supported languages
Cypher currently supports English and Lithuanian languages for encryption and decryption. However, only English is supported for breaking the cyphertext.

# Usage
It's pretty straightforward – enter a piece of text you would like to encrypt/decrypt/break and choose the method. 
The program uses quadgram statistics for breaking a cypher. This is not a foolproof method, it can only return best guesses for encryption key and cypher type. If program estimates Caesar cypher was used, it outputs statistically the most viable key (and decrypted text with that key). If it estimates Vigenere was used, it outputs statistically the most viable keys and corresponding decrypted texts for each key lenght from 3 to 10.
Breaking Vigenere might take up some time depending on text lenght.

# Licence
The content of this repository is licensed under a [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Feel free to use this code as you want.


