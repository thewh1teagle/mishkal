"""
The actual letters phonemization happens here.
Phonemes generated based on rules.

Early rules:
1. Niqqud malle vowels
2. Dagesh (custom beged kefet)
3. Final letter without niqqud
4. Final Het gnuva
5. Geresh (Gimel, Ttadik, Zain)
6. Shva na
Revised rules:
1. Consonants
2. Niqqud

Reference:
- https://hebrew-academy.org.il/2020/08/11/איך-הוגים-את-השווא-הנע
- https://en.wikipedia.org/wiki/Unicode_and_HTML_for_the_Hebrew_alphabet#Compact_table
- https://en.wikipedia.org/wiki/Help:IPA/Hebrew
- https://he.wikipedia.org/wiki/הברה
"""

from mishkal import lexicon
from .expander import Expander
from mishkal.utils import normalize, post_normalize, has_vowel, has_constant
from typing import Callable
import regex as re


class Phonemizer:
    def __init__(self):
        self.expander = Expander()

    def phonemize(
        self,
        text: str,
        preserve_punctuation=True,
        preserve_stress=True,
        use_expander=False,
        use_post_normalize=False,  # For TTS
        predict_stress=False,
        predict_shva_nah=False,
        fallback: Callable[[str], str] = None,
    ) -> str:
        # normalize
        text = normalize(text)
        # TODO: is that enough? what if there's punctuation around? other chars?
        he_pattern = r"[\u05b0-\u05ea\u05ab\u05bd']+"
        fallback_pattern = r"[a-zA-Z]+"

        def fallback_replace_callback(match: re.Match):
            word = match.group(0)

            if self.expander.dictionary.dict.get(word):
                # skip
                # TODO: better API
                return word
            phonemes = fallback(word).strip()
            # TODO: check that it has only IPA?!
            for c in phonemes:
                lexicon.SET_OUTPUT_CHARACTERS.add(c)
            return phonemes

        if fallback is not None:
            text = re.sub(fallback_pattern, fallback_replace_callback, text)
        if use_expander:
            text = self.expander.expand_text(text)
        self.fallback = fallback

        def heb_replace_callback(match: re.Match):
            word = match.group(0)

            word = normalize(word)
            word = "".join(
                i for i in word if i in lexicon.SET_LETTERS or i in lexicon.SET_NIQQUD
            )
            letters = re.findall(r"(\p{L})([\p{M}']*)", word)  # with en_geresh
            syllables = self.phonemize_hebrew(letters, predict_shva_na=predict_shva_nah)
            phonemes = "".join(syllable[1] for syllable in syllables)
            if post_normalize:
                phonemes = post_normalize(phonemes)

            if predict_stress and lexicon.STRESS not in phonemes:
                stressed = []

                # Iterate through each syllable
                for idx, syllable in enumerate(syllables):
                    # If it's the last syllable, add stress
                    if idx == len(syllables) - 1:
                        stressed.append(f'ˈ{syllable[1]}')
                    else:
                        stressed.append(syllable[1])
                phonemes = "".join(stressed)
            
            return phonemes

        text = re.sub(he_pattern, heb_replace_callback, text)

        if not preserve_punctuation:
            text = "".join(i for i in text if i not in lexicon.PUNCTUATION or i == " ")
        if not preserve_stress:
            text = "".join(
                i for i in text if i not in [lexicon.STRESS]
            )

        def expand_hyper_phonemes(text: str):
            """
            Expand hyper phonemes into normal phonemes
            eg. [hello](/hɛˈloʊ/) -> hɛˈloʊ
            """
            def hyper_phonemes_callback(match: re.Match):
                matched_phonemes = match.group(2)
                for c in matched_phonemes:
                    lexicon.SET_OUTPUT_CHARACTERS.add(c)
                return matched_phonemes  # The phoneme is in the second group

            text = re.sub(r"\[(.+?)\]\(\/(.+?)\/\)", hyper_phonemes_callback, text)
            return text

        text = expand_hyper_phonemes(text)
        text = "".join(i for i in text if i in lexicon.SET_OUTPUT_CHARACTERS)

        return text

    def phonemize_hebrew(self, letters: list[str], predict_shva_na: bool) -> list[str]:
        phonemes = []
        i = 0

        
        syllables = []
        cur_syllable = ['', '']
        while i < len(letters):
            cur = letters[i]
            prev = letters[i - 1] if i > 0 else None
            next = letters[i + 1] if i < len(letters) - 1 else None
            cur_phonemes = []
            skip_diacritics = False
            skip_constants = False
            skip_offset = 0
            # revised rules

            # יַאלְלָה
            if cur[0] == "ל" and cur[1] == "\u05b0" and next and next[0] == "ל":
                skip_diacritics = True
                skip_constants = True

            if (
                cur[0] == "ו"
                and not prev
                and next
                and not next[1]
                and cur[0] + cur[1] == "וַא"
            ):
                skip_offset += 1
                cur_phonemes.append("wa")

            if cur[0] == "א" and not cur[1] and prev:
                if next and next[0] != 'ו':
                    skip_constants = True

            # TODO ?
            if cur[0] == "י" and next and not cur[1]:
                skip_constants = True

            if cur[0] == "ש" and "\u05c2" in cur[1]:
                cur_phonemes.append("s")
                skip_constants = True

            # shin without niqqud after sin = sin
            if cur[0] == "ש" and not cur[1] and prev and "\u05c2" in prev[1]:
                cur_phonemes.append("s")
                skip_constants = True

            if not next and cur[0] == "ח" and '\u05b7' in cur[1]:
                # Final Het gnuva
                cur_phonemes.append("ax")
                skip_diacritics = True
                skip_constants = True

            if cur and "'" in cur[1] and cur[0] in lexicon.GERESH_LETTERS:
                if cur[0] == "ת":
                    cur_phonemes.append(lexicon.GERESH_LETTERS.get(cur[0], ""))
                    skip_diacritics = True
                    skip_constants = True
                else:
                    # Geresh
                    cur_phonemes.append(lexicon.GERESH_LETTERS.get(cur[0], ""))
                    skip_constants = True

            elif (
                "\u05bc" in cur[1] and cur[0] + "\u05bc" in lexicon.LETTERS_PHONEMES
            ):  # dagesh
                cur_phonemes.append(lexicon.LETTERS_PHONEMES.get(cur[0] + "\u05bc", ""))
                skip_constants = True
            elif cur[0] == "ו":
                skip_constants = True
                if next and next[0] == "ו" and next[1] == cur[1]:
                    # patah and next[1] empty
                    if cur[1] == "\u05b7" and not next[1]:
                        cur_phonemes.append("w")
                        skip_diacritics = True
                        skip_offset += 1
                    elif cur[1] == next[1]:
                        # double vav
                        cur_phonemes.append("wo")
                        skip_diacritics = True
                        skip_offset += 1
                    else:
                        # TODO ?
                        # skip_consonants = False
                        skip_diacritics = False
                else:
                    # Single vav

                    # Vav with Patah
                    if "\u05b7" in cur[1]:
                        cur_phonemes.append("va")

                    # Holam haser
                    elif "\u05b9" in cur[1]:
                        cur_phonemes.append("o")
                    # Shuruk / Kubutz
                    elif "\u05bb" in cur[1] or "\u05bc" in cur[1]:
                        cur_phonemes.append("u")
                    # Vav with Shva in start
                    elif "\u05b0" in cur[1] and not prev:
                        cur_phonemes.append("ve")
                    # Hirik
                    elif "\u05b4" in cur[1]:
                        cur_phonemes.append("vi")
                    # Tsere
                    elif "\u05b5" in cur[1]:
                        cur_phonemes.append("ve")
                    
                    else:
                        cur_phonemes.append("v")
                    skip_diacritics = True

            if not skip_constants:
                cur_phonemes.append(lexicon.LETTERS_PHONEMES.get(cur[0], ""))
            
            if predict_shva_na and '\u05b0' in cur[1] and not skip_diacritics and lexicon.SHVA_NA_DIACRITIC not in cur[1]:
                # shva na prediction
                if not prev:
                    if cur[0] in 'למנרי' or cur[0] in 'אהע' or cur[0] in 'וכלב':
                        cur_phonemes.append("e")
                        skip_diacritics = True 
                else:
                    if next and next[0] == cur[0]:
                        cur_phonemes.append("e")
                        skip_diacritics = True
                    elif prev and '\u05b0' in prev[1] and phonemes[-1] != 'e':
                        cur_phonemes.append("e")
                        skip_diacritics = True

                

            niqqud_phonemes = (
                [lexicon.NIQQUD_PHONEMES.get(niqqud, "") for niqqud in cur[1]]
                if not skip_diacritics
                else []
            )            
            
            cur_phonemes.extend(niqqud_phonemes)
            # Ensure the stress is at the beginning of the syllable
            cur_phonemes.sort(key=lambda x: x != 'ˈ')
            phonemes.extend(cur_phonemes)
            

            if not next:
                cur_syllable[0] += cur[0] + cur[1]
                cur_syllable[1] += ''.join(cur_phonemes)
                syllables.append(cur_syllable)
            elif not prev:
                cur_syllable = [cur[0] + cur[1], ''.join(cur_phonemes)]

            elif len(re.findall('[א-ת]', cur_syllable[0])) >= 2 and has_vowel(cur_syllable[1]) and cur[1]:
                syllables.append(cur_syllable)
                cur_syllable = [cur[0] + cur[1], ''.join(cur_phonemes)]

            elif not has_vowel(cur_phonemes):                
                cur_syllable[0] += cur[0] + cur[1]
                cur_syllable[1] += ''.join(cur_phonemes)

            elif not has_vowel(cur_syllable[1]):
                cur_syllable[0] += cur[0] + cur[1]
                cur_syllable[1] += ''.join(cur_phonemes)
            else:
                syllables.append(cur_syllable)
                cur_syllable = [cur[0] + cur[1], ''.join(cur_phonemes)]
            i += skip_offset + 1
            
        return syllables
