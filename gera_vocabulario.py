import re
import json

data = []
with open("dump_small.jsonln", "r") as file:
    for line in file:
        data.append(json.loads(line))

print("Leu todos os documentos")

# Baseado em https://gist.github.com/gruber/249502
def rm_htmlLinks(texto):
    return re.sub(
        r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))",
        "",
        texto,
    )


def sub_links(texto):
    return re.sub(r"\[\[(?:[^|]*?\|)*?([^|]*?)\]\]", r"\1", texto)


def rm_templates(texto):
    count = 0
    spansToRemove = []
    for item in re.finditer(r"{{|}}", texto):
        if item[0] == "{{":
            if count == 0:
                begin = item.span()[0]
            count += 1
        else:
            count -= 1
            if count == 0:
                end = item.span()[1]
                spansToRemove.append((begin, end))
    cleanText = ""
    begin = 0
    for span in spansToRemove:
        end, nextBegin = span
        cleanText += texto[begin:end]
        begin = nextBegin
    cleanText += texto[begin:]
    return cleanText


def rm_templates2(texto):
    count = 0
    spansToRemove = []
    for item in re.finditer(r"{[\|]|[\|]}", texto):
        if item[0] == "{|":
            if count == 0:
                begin = item.span()[0]
            count += 1
        else:
            count -= 1
            if count == 0:
                end = item.span()[1]
                spansToRemove.append((begin, end))
    cleanText = ""
    begin = 0
    for span in spansToRemove:
        end, nextBegin = span
        cleanText += texto[begin:end]
        begin = nextBegin
    cleanText += texto[begin:]
    return cleanText


def rm_refs(texto):
    return re.sub(r"<ref.*>.*</ref>|<ref.*>|</ref>", "", texto)


def rm_htmlTags(texto):
    return re.sub(r"<.*?>|</.*?>", "", texto)


def rm_aspas(texto):
    return re.sub(r"(['\"]+)(.*?)\1", r"\2", texto)


def rm_caracterPontuacao(texto):
    sem_travessao = re.sub(r"\s\-\s|\-\-+", " ", texto)
    return re.sub(r"[^\w\s\-]", " ", sem_travessao)


def rm_digitos(texto):
    return re.sub(r"\w*\d\w*", "", texto)


def rm_travessaoErrado(texto):
    return re.sub(r"(\w+)\-|\-(\w+)", r"\1\2", texto)


def rm_notLatin(texto):
    return re.sub(r"[^a-zA-Z0-9\u00B5-\u00FF\s]", r"", texto)


def limpa_textos(txt):
    output = rm_htmlLinks(txt)
    output = sub_links(output)
    output = rm_refs(output)
    output = rm_htmlTags(output)
    output = rm_templates(output)
    output = rm_templates2(output)
    output = rm_aspas(output)
    output = rm_caracterPontuacao(output)
    output = rm_digitos(output)
    output = rm_travessaoErrado(output)
    output = rm_notLatin(output)
    return output.lower()


def define_palavras(docs):
    output = {}
    for doc in docs:
        words = limpa_textos(doc["body"]).split()
        for word in words:
            if word in output.keys():
                output[word] += 1
            else:
                output[word] = 1
    return output


palavras = define_palavras(data)
print("Realizou a limpeza de todos os documentos")

sort_palavras = dict(sorted(palavras.items(), key=lambda item: -item[1]))
vocab = list(sort_palavras.items())[:10000]
vocab = dict(vocab)
print("Definiu as 10 mil palavras mais relevantes")

with open("vocabulario.json", "w") as f:
    json.dump(vocab, f)

print("Gerou o arquivo contendo o vocabulário")