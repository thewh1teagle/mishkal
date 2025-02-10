"""
The core of Mishkal.
Phonemes generated based on rules.

1. Vav vowels in index + 1
2. Yod vowels
3. Dagesh (Bet, Kaf, Kaf sofit, Fey, Fey Sofit), Sin, Shin dots
5. Het in end like Ko(ax)
6. Kamatz Gadol and Kamatz Katan (Kol VS Kala)
7. Shva Nah and Shva Na
"""

from mishkal.variants import Letter, Phoneme
from ..lexicon.symbols import LetterSymbol
from ..lexicon.letters import Letters
from .ipa_table import PHONEME_TABLE
import unicodedata

def phonemize_letters(letters: list[Letter]) -> list[Phoneme]:
    phonemes: list[Phoneme] = []
    index = 0
    current_word_str = ''.join(i.as_str() for i in letters)
    
    
    while index < len(letters):
        current_phoneme = Phoneme(phonemes='', word=current_word_str, letter=letters, reasons=[])
        current_letter= letters[index]
        # next_letter = letters[index + 1] if index + 1 < len(letters) else None
        previous_letter = letters[index - 1] if index - 1 >= 0 else None
        
        # Vav in middle
        if (
            index > 0 
            and current_letter.as_str() == '\u05d5'  # Vav
            and not previous_letter.plain_niqqud() # No previous niqqud
        ): 
            
            # Vav with no niqqud
            if not current_letter.get_symbols():
                current_phoneme.add_phonemes('o', 'Vav without niqqud')
                current_phoneme.mark_ready()
            # Vav with Holam
            elif current_letter.contains_any_symbol([LetterSymbol.holam, LetterSymbol.holam_haser_for_vav]):
                current_phoneme.add_phonemes('o', 'Vav with Holam')
                current_phoneme.mark_ready()
            
            # Vav with dagesh
            elif current_letter.contains_any_symbol([LetterSymbol.dagesh_or_mapiq]):
                current_phoneme.add_phonemes('u', 'Vav with Dagesh')
                current_phoneme.mark_ready()

        
        # Yod in middle          
        if (index > 0 and current_letter.as_str() == Letters.YOD):
            if not previous_letter.plain_niqqud(): # No previous niqqud
                current_phoneme.add_phonemes('i', 'yod in middle with no previous niqqud')
                current_phoneme.mark_ready()
            elif previous_letter.contains_any_symbol([LetterSymbol.hiriq]):
                current_phoneme.add_phonemes('', 'yod with previous hirik')
                current_phoneme.mark_ready()

        # Sin dot
        if current_letter.contains_any_symbol([LetterSymbol.sin_dot]):
            current_phoneme.add_phonemes('s', 'Sin dot')
            current_phoneme.mark_letter_ready()
            
        # Shin dot
        if current_letter.contains_any_symbol([LetterSymbol.shin_dot]):
            current_phoneme.add_phonemes('ʃ', 'Shin dot')
            current_phoneme.mark_letter_ready()
            
        # Dagesh in Vav in start
        if current_letter.contains_all_symbol([LetterSymbol.dagesh_or_mapiq, Letters.VAV]) and index == 0:
            current_phoneme.add_phonemes('u', 'vav with dagesh in start')
            current_phoneme.mark_ready()
        
        # Dagesh (Bet, Kaf, Kaf sofit, Fey, Fey Sofit), 
        if current_letter.contains_any_symbol([LetterSymbol.dagesh_or_mapiq]) and not current_phoneme.is_ready():
            if current_letter.as_str() in [Letters.BET, Letters.KAF, Letters.FINAL_KAF, Letters.PEY, Letters.FINAL_PEY]:
                current_phoneme.add_phonemes({
                    Letters.BET: 'b',
                    Letters.KAF: 'k',
                    Letters.FINAL_KAF: 'k',
                    Letters.PEY: 'p',
                    Letters.FINAL_PEY: 'p',
                }[current_letter.as_str()], f'{current_letter.as_str()} with dagesh')
                current_phoneme.mark_letter_ready()            
            
        # Het in end like Ko(ax)
        if current_letter.as_str() == Letters.CHET and current_letter.contains_any_symbol([LetterSymbol.patah]) and index == len(letters) - 1:
            current_phoneme.add_phonemes('ax', 'word ends with chet with patah')
            current_phoneme.mark_ready()
            
        # Base letter
        if not current_phoneme.is_ready() and not current_phoneme.is_letter_ready():
            from_table = PHONEME_TABLE.get(current_letter.as_str(), '')
            current_phoneme.add_phonemes(from_table, f'got letter {current_letter.as_str()} from table')
        
        # Symbols
        if not current_phoneme.is_ready():
            for s in current_letter.get_symbols():
                from_table = PHONEME_TABLE.get(s, '')
                symbol_name = unicodedata.name(s, '?')
                current_phoneme.add_phonemes(from_table, f'got symbol {symbol_name} from table')
            
        phonemes.append(current_phoneme)
        index += 1
        
    print(phonemes)
    return phonemes
