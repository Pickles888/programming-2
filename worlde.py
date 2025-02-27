from enum import Enum
from typing import List

CharString = List[str]

class Matching(Enum):
    Matches = 1
    Close = 2
    Incorrect = 3
    
MatchedChar = tuple[str, Matching]
MatchedCharString = List[MatchedChar]

def match(char1: str, char2: str, word: CharString) -> Matching:
    result: Matching
    if char1 == char2: 
        result = Matching.Matches
    else: 
        if isClose(char1, word):
            result = Matching.Close
        else:
            result = Matching.Incorrect
    return result

def isClose(char: str, str: CharString) -> bool:
    return any(lambda a: a == char, str)

def addMatchingData(str1: CharString, str2: CharString) -> MatchedCharString:
    return map(lambda a: map(lambda b: match(a, b, str2), str2), str1)

def makeCharDisplayable(char: MatchedChar) -> str:
    match char[1]:
        case Matching.Matches:
    