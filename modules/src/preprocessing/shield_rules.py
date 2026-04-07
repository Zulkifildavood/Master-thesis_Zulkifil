import re

class MorphologicalShield:
    def __init__(self):
        self.boundary_marker = '▁' # U+2581 [cite: 96]
        self.min_stem_length = 3     # Enforcing minimum stem constraint [cite: 128]
        
        # Priority rules (Longest-match first) [cite: 123, 124]
        self.nominal_suffixes = [
            r'(കള്|മാര്‍)$',           # Plurals (-kal, -maar) [cite: 86]
            r'(ില്‍|ക്കല്‍)$',         # Locative (-il, -kal) [cite: 84]
            r'(ുടെ|ന്റെ)$',          # Genitive (-ute, -nte) [cite: 84]
            r'(ക്ക്|ഇന്|ന്|ഉ)$',   # Dative (-kku, -inu, -nu, -u) [cite: 84]
            r'(എ|യെ)$'               # Accusative (-e, -ye) [cite: 84]
        ]
        
        self.verbal_suffixes = [
            r'(ിട്ടില്ല)$',            # Negative compound (-ittilla) [cite: 90, 125]
            r'(ില്ല|ആത്ത)$',          # Negative clitics (-illa, -aatt) [cite: 89]
            r'(ഉന്നു)$',             # Present (-unnu) [cite: 88]
            r'(തു|ഇ)$',              # Past (-tu, -i) [cite: 88]
            r'(ഉം|ഊ)$'               # Future (-um, -uu) [cite: 88]
        ]

    def apply_shield(self, word: str) -> str:
        """Applies boundary insertion based on prioritized regex rules."""
        # Check nominal suffixes
        for suffix in self.nominal_suffixes:
            match = re.search(suffix, word)
            if match:
                stem = word[:match.start()]
                if len(stem) >= self.min_stem_length:
                    return f"{stem}{self.boundary_marker}{match.group(1)}"
        
        # Check verbal suffixes
        for suffix in self.verbal_suffixes:
            match = re.search(suffix, word)
            if match:
                stem = word[:match.start()]
                if len(stem) >= self.min_stem_length:
                    return f"{stem}{self.boundary_marker}{match.group(1)}"
                    
        return word

    def process_sequence(self, text: str) -> str:
        words = text.split()
        shielded_words = [self.apply_shield(w) for w in words]
        return " ".join(shielded_words)