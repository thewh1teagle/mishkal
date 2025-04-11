from mishkal import lexicon
import unicodedata
import regex as re
from mishkal.variants import Letter
import mishkal

def sort_diacritics(match):
    letter = match.group(1)
    diacritics = "".join(sorted(match.group(2)))  # Sort diacritics
    return letter + diacritics


NORMALIZE_PATTERNS = {
    # Sort diacritics
    r"(\p{L})(\p{M}+)": sort_diacritics,
    "״": '"', # Hebrew geresh to normal geresh
    "׳": "'", # Same
}

def remove_nikud(text: str):
    return re.sub(lexicon.HE_NIKUD_PATTERN, "", text)


def has_nikud(text: str):
    return re.search(lexicon.HE_NIKUD_PATTERN, text) is not None


def normalize(text: str) -> str:
    """
    Normalize unicode (decomposite)
    Keep only Hebrew characters / punctuation / IPA
    Sort diacritics
    """

    # Decompose text
    text = unicodedata.normalize("NFD", text)
    for k, v in NORMALIZE_PATTERNS.items():
        text = re.sub(k, v, text)
    for k, v in lexicon.DEDUPLICATE.items():
        text = re.sub(k, v, text)
    return text


def post_normalize(phonemes: str):
    new_phonemes = []
    for word in phonemes.split(" "):
        # remove glottal stop from end
        word = re.sub(r"ʔ$", "", word)
        # remove h from end
        word = re.sub(r"h$", "", word)
        word = re.sub(r"ˈh$", "", word)
        # remove j followed by a i
        word = re.sub(r"ij", "i", word)
        new_phonemes.append(word)
    phonemes = " ".join(new_phonemes)
    return phonemes

def get_letters(word: str):
    letters: list[tuple[str, str]] = re.findall(r"(\p{L})([\p{M}']*)", word)  # with en_geresh
    letters: list[Letter] = [Letter(i[0], i[1]) for i in letters]
    return letters

def get_unicode_names(text: str):
    return [unicodedata.name(c, "?") for c in text]

def has_vowel(s: iter):
    return any(i in s for i in 'aeiou')

def has_constant(s: iter):
    return any(i not in 'aeiou' for i in s)



def get_syllables(phonemes: list[str]) -> list[str]:
    syllables = []
    cur_syllable = ''

    i = 0
    while i < len(phonemes):
        # Add current phoneme to the syllable
        cur_syllable += phonemes[i]
        
        # If we have a vowel in the current syllable
        if has_vowel(cur_syllable):
            # If there's a next phoneme that's a consonant followed by a vowel-containing phoneme
            if i+2 < len(phonemes) and not has_vowel(phonemes[i+1]) and has_vowel(phonemes[i+2]):
                # End the current syllable and start a new one
                syllables.append(cur_syllable)
                cur_syllable = ''
            # If we're at the end or next phoneme has a vowel
            elif i+1 >= len(phonemes) or has_vowel(phonemes[i+1]):
                # End the current syllable
                syllables.append(cur_syllable)
                cur_syllable = ''
        
        i += 1
    
    # Add any remaining syllable
    if cur_syllable:
        syllables.append(cur_syllable)
    
    return syllables