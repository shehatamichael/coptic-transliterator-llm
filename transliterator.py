#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Coptic to Latin transliterator that doesn't use Pynini
"""

import re
import unicodedata


class CopticTransliterator:
    def __init__(self):
        # Basic character mappings
        self.char_map = {
            "ⲁ": "a",
            "Ⲁ": "A",
            "ⲃ": "b",
            "Ⲃ": "B",
            "ⲅ": "g",
            "Ⲅ": "G",
            "ⲇ": "d",
            "Ⲇ": "D",
            "ⲉ": "e",
            "Ⲉ": "E",
            "ⲋ": "f",
            "Ⲋ": "F",
            "ⲍ": "z",
            "Ⲍ": "Z",
            "ⲏ": "i",
            "Ⲏ": "I",
            "ⲑ": "th",
            "Ⲑ": "TH",
            "ⲓ": "i",
            "Ⲓ": "I",
            "ⲕ": "k",
            "Ⲕ": "K",
            "ⲗ": "l",
            "Ⲗ": "L",
            "ⲙ": "m",
            "Ⲙ": "M",
            "ⲛ": "n",
            "Ⲛ": "N",
            "ⲝ": "x",
            "Ⲝ": "X",
            "ⲟ": "o",
            "Ⲟ": "O",
            "ⲡ": "p",
            "Ⲡ": "P",
            "ⲣ": "r",
            "Ⲣ": "R",
            "ⲥ": "s",
            "Ⲥ": "S",
            "ⲧ": "t",
            "Ⲧ": "T",
            "ⲩ": "u",
            "Ⲩ": "U",
            "ⲫ": "ph",
            "Ⲫ": "PH",
            "ⲭ": "ch",
            "Ⲭ": "CH",
            "ⲯ": "ps",
            "Ⲯ": "PS",
            "ⲱ": "o",
            "Ⲱ": "O",
            "ϣ": "sh",
            "Ϣ": "SH",
            "ϥ": "f",
            "Ϥ": "F",
            "ϧ": "kh",
            "Ϧ": "KH",
            "ϩ": "h",
            "Ϩ": "H",
            "ϫ": "j",
            "Ϫ": "J",
            "ϭ": "ky",
            "Ϭ": "KY",
            "ϯ": "ti",
            "Ϯ": "TI",
        }

    def translit(self, text):
        """
        Transliterate Coptic text to Latin script
        """
        # Normalize input to decompose combining characters
        text = unicodedata.normalize("NFKD", text)
        # Remove combining diacritics (e.g., supralinear stroke)
        text = "".join(c for c in text if not unicodedata.combining(c))
        # Apply contextual rules first (similar to original pynini rules)
        result = self._apply_contextual_rules(text.lower())

        # Apply basic character mappings
        for coptic_char, latin_char in self.char_map.items():
            result = result.replace(coptic_char.lower(), latin_char.lower())

        # Replace any remaining unmapped Coptic characters with a placeholder or warning
        unmapped = "".join(c for c in result if ord(c) >= 0x2C80 and ord(c) <= 0x2CFF)
        if unmapped:
            print(f"Warning: Unmapped Coptic characters found: {unmapped}")
        return result

    def _apply_contextual_rules(self, text):
        """
        Apply context-sensitive transliteration rules
        """
        # Alpha contextual rules
        text = re.sub(r"ⲁ(?=ⲥ\b)", "æ", text)  # ⲁ -> æ before ⲥ at word boundary
        text = re.sub(r"ⲁ(?=\b)", "ə", text)  # ⲁ -> ə at word boundary
        text = re.sub(r"ⲁ", "ɑː", text)  # ⲁ -> ɑː elsewhere

        # Veeta (ⲃ) contextual rules
        text = re.sub(r"ⲃ(?=ⲓⲙ\b)", "b", text)  # ⲃ -> b before ⲓⲙ at word boundary
        text = re.sub(r"ⲃ(?=ⲧ\b)", "v", text)  # ⲃ -> v before ⲧ at word boundary
        text = re.sub(r"ⲃ(?=[ⲁⲟⲱⲓⲏⲉ])", "v", text)  # ⲃ -> v before vowels
        text = re.sub(r"ⲃ(?=ⲣ)", "b", text)  # ⲃ -> b before ⲣ
        text = re.sub(r"ⲃ(?=ⲥ)", "b", text)  # ⲃ -> b before ⲥ
        text = re.sub(r"ⲃ(?=\b)", "b", text)  # ⲃ -> b at word boundary

        # Gamma (ⲅ) contextual rules
        text = re.sub(r"ⲅ(?=ⲅ)", "n", text)  # ⲅ -> n before ⲅ
        text = re.sub(r"ⲅ(?=ⲓ)", "g", text)  # ⲅ -> g before ⲓ
        text = re.sub(r"ⲅ(?=ⲉ)", "g", text)  # ⲅ -> g before ⲉ
        text = re.sub(r"ⲅ", "gh", text)  # ⲅ -> gh elsewhere

        # Eeta (ⲏ) contextual rules
        text = re.sub(r"ⲉ(ⲏ)", r"ey", text)  # ⲉⲏ -> ey

        # Ei contextual rules
        text = re.sub(r"ⲉ(?=ⲟ)", "eɪ", text)  # ⲉ -> eɪ before ⲟ
        text = re.sub(r"ⲏ", "ee", text)  # ⲏ -> ee (general case)

        # Multi-character sequences
        text = re.sub(r"ⲕⲕ", "kk", text)
        text = re.sub(r"ⲙⲙ", "mm", text)
        text = re.sub(r"ⲛⲛ", "nn", text)
        text = re.sub(r"ⲟⲓⲁ", "ia", text)
        text = re.sub(r"ⲟⲩⲱ", "o'o", text)

        return text


# Create instance for easy use
transliterator = CopticTransliterator()


def translit(text):
    return transliterator.translit(text)


# Example usage
if __name__ == "__main__":
    # Test with some Coptic text
    test_text = "ⲁⲛⲟⲕ ⲟⲩⲛ ⲟⲩⲙⲁⲓⲛⲟⲩⲧⲉ"
    print(f"Original: {test_text}")
    print(f"Transliterated: {translit(test_text)}")
