import re
import json
import nltk
from nltk.metrics.distance import edit_distance
from nltk.corpus import stopwords
import argparse

nltk.download("stopwords", quiet=True)

parser = argparse.ArgumentParser(description="Digite a frase a ser corrigida")
parser.add_argument("--frase", "-f", type=str, help="Frase a ser corrigida")
args = parser.parse_args()

fraseDeEntrada = args.frase

with open("vocabulario.json", "r") as json_file:
    vocab = json.load(json_file)

LOWERCASE = [chr(x) for x in range(ord("a"), ord("z") + 1)]
LOWERCASE_OTHERS = ["ç", "á", "â", "é", "ã", "õ", "ê", "í", "ú", "ô", "ó"]  # etc.
LETTERS = LOWERCASE + LOWERCASE_OTHERS


def edit1(text):
    words = []

    # Fase 1: as remoçoes.
    for p in range(len(text)):
        new_word = text[:p] + text[p + 1 :]
        if len(new_word) > 0:
            words.append(new_word)

    # Fase 2: as adições.
    for p in range(len(text) + 1):
        for c in LETTERS:
            new_word = text[:p] + c + text[p:]
            words.append(new_word)

    # Fase 3: as substituições.
    for p in range(len(text)):
        orig_c = text[p]
        for c in LETTERS:
            if orig_c != c:
                new_word = text[:p] + c + text[p + 1 :]
                words.append(new_word)

    return set(words)


def edit2(text):
    words1 = edit1(text)
    words2 = set()
    for w in words1:
        candidate_words2 = edit1(w)
        candidate_words2 -= words1
        words2.update(candidate_words2)
    words2 -= set([text])
    return words2


def candidatos(palavra):
    if palavra in vocab:
        candidatos = [palavra]
    else:
        candidatos = []
        dist1 = [w for w in edit1(palavra) if w in vocab]
        if len(dist1) > 0:
            candidatos += dist1
        else:
            dist2 = [w for w in edit2(palavra) if w in vocab]
            candidatos += dist2 + [palavra]
    return candidatos


def tokenize(txt):
    scanner = re.Scanner(
        [
            (r"\d+", lambda scanner, token: ("NUM", token)),
            (r"[.,\/#!$%\^&\*;:{}=\-_`~()]", lambda scanner, token: ("SPECIAL", token)),
            (
                r"[^.,\/#!$%\^&\*;:{}=\-_`~()\d]+",
                lambda scanner, token: ("WORD", token),
            ),
        ]
    )
    results = scanner.scan(txt)[0]
    return results


# Adaptado de https://norvig.com/spell-correct.html
def probability(palavra, N=sum(vocab.values())):
    if palavra in vocab:
        return vocab[palavra] / N
    else:
        return 1 / N


# Referência: https://norvig.com/spell-correct.html
def corrige(txt):
    frase = txt.split()
    output = ""
    for palavra in frase:
        tokens = tokenize(palavra)
        for tk in tokens:
            if tk[0] == "WORD":
                if tk[1].lower() in stopwords.words("portuguese"):
                    output += tk[1]
                else:
                    candidates = candidatos(tk[1].lower())
                    if tk[1][0].isupper():
                        output += max(candidates, key=probability).capitalize()

                    else:
                        output += max(candidates, key=probability)
            else:
                output += tk[1]
        output += " "
    return output[:-1]


print(corrige(fraseDeEntrada))