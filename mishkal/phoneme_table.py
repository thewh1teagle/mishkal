from .lexicon.symbols import LetterSymbol
from .lexicon.letters import Letters

STRESS = "'"
SECOND_STRESS = ','

PHONEME_TABLE = {
    # Letters
    Letters.ALEF: 'ʔ',
    Letters.BET: 'v',
    Letters.GIMEL: 'g',
    Letters.DALET: 'd',
    Letters.HEY: 'h',
    Letters.VAV: 'v',
    Letters.ZAYIN: 'z',
    Letters.CHET: 'x',
    Letters.TET: 't',
    Letters.YOD: 'j',
    Letters.KAF: 'x',
    Letters.LAMED: 'l',
    Letters.MEM: 'm',
    Letters.NUN: 'n',
    Letters.SAMECH: 's',
    Letters.AYIN: '?',
    Letters.PEY: 'f',
    Letters.TZADI: 'ts',
    Letters.QOF: 'k',
    Letters.RESH: 'r',
    Letters.SHIN: 'ʃ',
    Letters.TAV: 't',
    
    # Final.value letters
    Letters.FINAL_KAF: 'x',
    Letters.FINAL_PEY: 'f',
    Letters.FINAL_TZADI: 'ts',
    Letters.FINAL_NUN: 'n',
    Letters.FINAL_MEM: 'm',
    
    # Symbols
    LetterSymbol.hataf_segol: 'e',          # HATAF SEGOL
    LetterSymbol.hataf_patah: 'a',          # HATAF PATAH
    
    LetterSymbol.patah: 'a',                # PATAH
    LetterSymbol.hataf_qamats: 'a',         # HATAF QAMATS
    LetterSymbol.qamats: 'a',               # QAMATS
    LetterSymbol.qamats_qatan: 'o',         # QAMATS QATAN
    LetterSymbol.holam: 'o',                # HOLAM
    LetterSymbol.holam_haser_for_vav: 'o',  # HOLAM HASER FOR VAV
    LetterSymbol.hiriq: 'i',                # HIRIQ
    LetterSymbol.tsere: 'e',                # TSERE
    LetterSymbol.hataf_segol: 'e',          # HATAF SEGOL
    LetterSymbol.segol: 'e',                # SEGOL
    LetterSymbol.qubuts: 'u',               # QUBUTS
    
    
    LetterSymbol.sheva: '',                 # Handled in core
    LetterSymbol.dagesh_or_mapiq: '',       # Handled in core
    LetterSymbol.shin_dot: '',              # Handled in core
    LetterSymbol.sin_dot: '',               # Handled in core
    LetterSymbol.geresh: '',                # Handled in core
    LetterSymbol.geresh_en: '',             # Handled in core
}

