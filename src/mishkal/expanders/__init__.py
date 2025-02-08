from .numbers import num_to_word
from .dates import date_to_word

def expand_word(word: str) -> str:
    word = date_to_word(word)
    word = num_to_word(word)
    return word
    