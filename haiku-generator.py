import random
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

def get_syllables(word):
    word = word.lower()
    if word in d: # if its in the pronunciation dictionary
        # Get the phonetic representation of the word
        phonetic_rep = d[word][0] # gets word from pronunciation dictionary
        # Count the number of syllables (syllables are typically represented by vowel sounds)
        syllables = [s for s in phonetic_rep if s[-1].isdigit()] # removes intonation and only takes sylables
        return len(syllables) # returns the length of the cleaned list
    else:
        return None # if not in pronunciation dictionary
    
def getWord(f):
    random_word = random.choice(words) # gets a random word
    
    # Ensure that the word has a valid syllable count (not None)
    syllable_count = get_syllables(random_word) # gets the amount of syllables
    
    print(f(syllable_count)) # test
    
    if syllable_count is not None and f(syllable_count): # returns the random_word if it was found in the pronunciation dictionary and passes the function passed in
        return random_word
    else:
        return getWord(f) # recuses if random_word could not be gotten

def getSyllablesInArr(arr):
    total = 0
    
    for word in arr:
        syllable_count = get_syllables(word)
        if syllable_count is not None:
            total += syllable_count
    
    return total

def getWordsTotalSyllables(x):
    arr = [] 
    
    while getSyllablesInArr(arr) < x: # runs if there less syllables in the array
        # runs function with lambda that checks if there are more syllables than needed until the syllables in the array are filled up
        arr.append(getWord(lambda a: a < (x - getSyllablesInArr(arr)))) 
        
    return arr

word = getWordsTotalSyllables(5)

print(word)
print(get_syllables(word))
