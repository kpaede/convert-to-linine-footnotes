import re
import sys
from pathlib import Path

def convert_to_inline(md_text: str) -> str:
    # Schritt 1: Alle Fußnoten-Definitionen am Ende erfassen
    footnote_pattern = re.compile(r'^\[\^(\d+)\]:\s*(.+)$', re.MULTILINE)
    footnotes = {m.group(1): m.group(2).strip() for m in footnote_pattern.finditer(md_text)}

    # Schritt 2: Fußnoten-Referenzen im Text ersetzen
    def replacer(match):
        key = match.group(1)
        return f"^[{footnotes.get(key, '')}]"

    text_without_defs = footnote_pattern.sub('', md_text)  # Definitionen entfernen
    result = re.sub(r'\[\^(\d+)\]', replacer, text_without_defs)
    return result.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Verwendung: python convert_footnotes.py datei.md")
        sys.exit(1)

    infile = Path(sys.argv[1])
    text = infile.read_text(encoding="utf-8")
    converted = convert_to_inline(text)

    outfile = infile.with_name(infile.stem + "_inline.md")
    outfile.write_text(converted, encoding="utf-8")
    print(f"Konvertiert gespeichert in: {outfile}")
