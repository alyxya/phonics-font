#!/usr/bin/env python3
import fontforge
import os
import sys

# Font information
font = fontforge.font()
font.fontname = "PhonicsPicturesVisual"
font.familyname = "PhonicsPicturesVisual"
font.fullname = "PhonicsPicturesVisual"
font.copyright = "Created with FontForge"
font.encoding = "UnicodeFull"
font.em = 1000

# Set character width and height
svg_dir = "/Users/jamesshi/Desktop/phonics-font/temp/svg"

# Create glyphs for a-z
for i in range(26):
    char = chr(ord('a') + i)
    code = ord(char)
    svg_path = os.path.join(svg_dir, f"{char}.svg")
    
    if os.path.exists(svg_path):
        # Create glyph for this character
        glyph = font.createChar(code)
        glyph.importOutlines(svg_path)
        
        # Set width and alignment
        glyph.width = 1000
        
        # Correct placement/scaling
        glyph.autoHint()
        glyph.autoInstr()

# Generate the font file
font.generate("/Users/jamesshi/Desktop/phonics-font/PhonicsPicturesVisual.ttf")
print(f"Font saved to /Users/jamesshi/Desktop/phonics-font/PhonicsPicturesVisual.ttf")
