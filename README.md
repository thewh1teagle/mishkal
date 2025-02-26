# Mishkal

Grapheme to phoneme in Hebrew

Convert Hebrew text into IPA for TTS systems and learning.

## Features

- Convert text with niqqud to modern spoken phonemes
- (WIP) Accurate lightweight niqqud model
- Expand dates into text with niqqud
- Expand numbers into text with niqqud
- (WIP) Mixed English in Hebrew
- Dictionaries with words, symbols, emojies


## Limitiation

The following hard to predict even from text with niqqud.

- Shva nah and nah
- Stress (Atmaha / Milre / Milra. same thing.)
- Kamatz Katan (rarely used)

## Install
```console
pip install mishkal-hebrew
```

## Play

See [Phonemize with Hebrew Space](https://huggingface.co/spaces/thewh1teagle/phonemize-in-hebrew)

## Examples
```python
from mishkal import phonemize
phonemes = phonemize('שָׁלוֹם עוֹלָם') 
print(phonemes) # ʃalom olam
```

See [examples](examples)

To understand the research and development journey behind Mishkal, check out the full story on [Medium](https://medium.com/@thewh1teagle/hebrew-tts-its-not-easy-7f57a7842d57).

## Docs

- Dictionaries prioritized based on `gold`, `silver`, `bronze`.
- Hebrew niqqud is normalized and deduplicated phonetically (simplified)
- Most of the Hebrew rules are happen in `phonemize.py`
- Input chars: `!"'(),-.:` and `0x5B0` to `0x5E0` (normalized later)
- Output chars: `!"'(),-.:?abdefghijklmnoprsttstʃuvxzʃʒˈˌ`

#### Niqqud deduplication

Hataf segol -> Tsere

Segol -> Tsere

Hataf patah -> patah

Hataf qamatz -> patah

Qamats -> Patah

Qamats katan -> Holam

Hebrew geresh -> Regular `'` (apostrophe)

#### Niqqud set and symbols

`Teres`, `Patah`, `Holam`, `Vav Holam` (`ו`), `Dagesh` (`בכפךף`), `Shin dot` (`ש`), `Sin dot` (`ש`), `'` (apostrophe eg. `ג'ירפה`)

We're left with: `Tsere, Patah, Holam` (and of course `Shin dot`, `Sin dot`, `Vav holam`

#### Hebrew phonemes

Constants

`b` - Bet

`v` - Vet, Vav

`g` - Gimel

`dʒ` - Gimel with geresh, Zain with geresh

`d` - Dalet

`h` - He

`z` - Zain

`x` - Het, Haf

`t` - Taf, Tet

`j` - Yod

`k` - Kuf, Kaf

`l` - Lamed

`m` - Mem

`n` - Nun

`s` - Sin, Samekh

`f` - Fei

`p` - Pei dgusha

`ts` - tsadik

`tʃ` - Tsadik with geresh

`r` - Resh

`ʃ` - Shin

Vowels

`a` - Shamar

`e` - Shemer

`i` - Shimer

`o` - Shomer

`u` - Shumar

Symbols

`ˈ` - stress (0x2C8) visually looks like apostrophe

`ˌ` - secondary stress (0x2CC) visually looks like comma

See [Unicode Hebrew table](https://en.wikipedia.org/wiki/Unicode_and_HTML_for_the_Hebrew_alphabet#Compact_table)
