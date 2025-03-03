import random
import sys
from typing import Callable
import nltk

nltk.download('cmudict')
nltk.download('shakespeare')

from nltk.corpus import cmudict
from nltk.corpus import shakespeare

# Load CMU Pronouncing Dictionary
d = cmudict.dict()

file_ids = shakespeare.fileids()
random_file = random.choice(file_ids)

words = shakespeare.words(random_file)

def get_syllables(word) -> int:
    word = word.lower()
    if word in d: # if its in the pronunciation dictionary
        # Get the phonetic representation of the word
        phonetic_rep = d[word][0] # gets word from pronunciation dictionary
        # Count the number of syllables (syllables are typically represented by vowel sounds)
        syllables = [s for s in phonetic_rep if s[-1].isdigit()] # removes intonation and only takes sylables
        return len(syllables) # returns the length of the cleaned list
    else:
        return None # if not in pronunciation dictionary
    
def getWord(f: Callable[[int], bool]):
    max_val: int = 100
    random_word: str
    
    while True:
        if max_val <= 0:
            sys.exit("Unreachable end condition given to getWord")
        
        max_val -= 1
        
        random_word = random.choice(words) # gets a random word
        
        if get_syllables(random_word) is None:
            continue
        
        if f(get_syllables(random_word)):
            break
    
    return random_word
    

def getSyllablesInArr(arr: list[str]) -> int:
    total = 0
    
    for word in arr:
        syllable_count = get_syllables(word)
        if syllable_count is not None:
            total += syllable_count
    
    return total

def getWordsTotalSyllables(x: int) -> list[str]:
    arr: list[str] = [] 
    
    while getSyllablesInArr(arr) < x: # runs if there less syllables in the array
        # runs function with lambda that checks if there are more syllables than needed until the syllables in the array are filled up
        arr.append(getWord(lambda a: a <= (x - getSyllablesInArr(arr)))) 
        
    return arr

def capitalize(s: str)  -> str:
    if len(s) == 0:
        return ""
    
    lower = s.lower()
    
    return lower[0].upper() + lower[1:]

haikuListList: list[list[str]] = [
    getWordsTotalSyllables(5), 
    getWordsTotalSyllables(7), 
    getWordsTotalSyllables(5)
]

haiku = "\n".join(map(lambda a: " ".join(a), haikuListList))

haikuCaseClean = capitalize(haiku)

print(haikuCaseClean)