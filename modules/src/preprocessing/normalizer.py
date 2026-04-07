import re
import unicodedata

class MalayalamNormalizer:
    def __init__(self):
        # Malayalam Unicode Block: 0D00–0D7F
        # Chillus typically require ZWJ (U+200D), so we must be careful not to strip valid formations.
        self.zwj = '\u200d'
        self.zwnj = '\u200c'

    def normalize(self, text: str) -> str:
        if not isinstance(text, str):
            return ""

        # Step 1: Unicode Standardization (NFC) [cite: 39]
        text = unicodedata.normalize('NFC', text)

        # Step 2: Artifact Removal [cite: 40]
        # Remove ZWNJ completely. Remove ZWJ only if it's NOT part of a chillu.
        # (Simplified for implementation: standardizing chillus to atomic characters if using modern Unicode)
        text = text.replace(self.zwnj, '')
        
        # Step 3: Whitespace Cleanup [cite: 41]
        text = re.sub(r'\s+', ' ', text)
        
        # Step 4: Punctuation Normalization [cite: 42]
        # Separate punctuation from words to prevent it from attaching to semantic tokens
        text = re.sub(r'([.,!?।॥])', r' \1 ', text)
        
        # Note: Deliberately preserving English characters and digits to support code-switching[cite: 44, 45, 46].
        return text.strip()

if __name__ == "__main__":
    norm = MalayalamNormalizer()
    print("Normalizer initialized. Test:", norm.normalize("മലയാളം   പഠിക്കാം!"))