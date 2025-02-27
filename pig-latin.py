import itertools
import string

punctuation = list(string.punctuation)

vowels = ['a', 'e', 'i', 'o', 'u']

consonants = [
    'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 
    'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'
]

def getWordInit(word: str) -> tuple[str, str]:
    if word == "": return ("", "")
    
    fword, punc = filterPunctuation(word)
    
    return (
        "".join(
            list(itertools.takewhile(lambda c: isIn(c, consonants), fword))
        ), 
        punc
    )

def isIn(item, list) -> bool:
    return any(a == item for a in list)

def filterPunctuation(word: str) -> tuple[str, str]:
    if word == "": return ("", "")
    
    endStr = ""
    puncStr = ""
    
    for c in word:
        if not isIn(c, punctuation):
            endStr += c
        else:
            puncStr += c

    return (endStr, puncStr)
        
def getWordTail(word: str) -> tuple[str, str]:
    if word == "": return ("", "")
    
    fword, punc = filterPunctuation(word)
    
    return (
        "".join(
            list(itertools.dropwhile(lambda c: isIn(c, consonants), fword))
        ), 
        punc
    )

def translate(word: str) -> str:
    initStr, initPunc = getWordInit(word)
    tailStr, tailPunc = getWordTail(word)
    
    return initPunc + tailStr + initStr + "ay" + tailPunc

input = input()

translated = " ".join(map(translate, input.split()))

print(translated)