"""
Dictionaries are tab separated key value words
"""
from pathlib import Path
import json
import re

files = Path(__file__).parent.glob('*.json')

class Dictionary:
    def __init__(self):        
        self.dict = {}
        self.load_dictionaries()


    def load_dictionaries(self):
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                parsed = json.load(f)
                self.dict.update(parsed)
            

    def expand(self, text: str) -> str:
        """
        TODO: if key doesn't have diacritics expand even diacritized words
        """
        for key, value in self.dict.items():
            text = re.sub(re.escape(key), value, text)
        return text