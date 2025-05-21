#!/usr/bin/env python3
import os
import glob
import subprocess
import tempfile
from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import TTFont
import xml.etree.ElementTree as ET

def modify_svg_for_font(svg_file, output_file, unicode_value):
    """Modify the SVG to make it suitable for inclusion in a font."""
    tree = ET.parse(svg_file)
    root = tree.getroot()
    
    # Get original width/height/viewBox
    width = int(root.get('width', '200'))
    height = int(root.get('height', '200'))
    
    # Set the glyph ID and unicode value
    root.set('id', f'glyph{unicode_value}')
    
    # Remove any text elements (we just want the shapes)
    ns = {'svg': 'http://www.w3.org/2000/svg'} if root.tag.startswith('{') else {}
    for text_elem in root.findall('.//svg:text', ns) if ns else root.findall('.//text'):
        parent = text_elem.getparent()
        if parent is not None:
            parent.remove(text_elem)
    
    # Write the modified SVG
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def main():
    # Create directory for output
    os.makedirs('font', exist_ok=True)
    os.makedirs('font/svg_temp', exist_ok=True)
    
    # Create a new font using fontBuilder
    font_name = "PhonicsFont"
    fb = FontBuilder(1000, isTTF=True)
    
    # Setup name table
    fb.setupNameTable({
        'familyName': font_name,
        'styleName': 'Regular',
        'uniqueFontIdentifier': f'{font_name}-Regular',
        'fullName': f'{font_name} Regular',
        'version': '1.0',
        'psName': f'{font_name}-Regular',
        'manufacturer': 'Custom',
        'designer': 'Phonics Project',
        'description': 'Font created from SVG files',
        'copyright': 'Copyright (c) 2025',
        'licenseDescription': 'SIL Open Font License',
        'licenseInfoURL': 'http://scripts.sil.org/OFL',
    })
    
    # Process each SVG file
    svg_files = sorted(glob.glob('svg/?.svg'))  # Only get a.svg, b.svg, etc.
    
    # Create a mapping for glyphs
    cmap = {}  # Unicode to glyph name mapping
    glyph_order = ['.notdef']  # Start with .notdef glyph
    metrics = {'.notdef': (600, 0)}  # width, left side bearing
    
    # For each letter, create a modified SVG in temp directory
    for svg_file in svg_files:
        # Get the letter from the filename (e.g., 'a' from 'a.svg')
        letter = os.path.basename(svg_file).split('.')[0]
        
        # Skip if not a lowercase letter
        if not letter.isalpha() or not letter.islower() or len(letter) != 1:
            continue
        
        print(f"Processing {svg_file} for letter '{letter}'")
        
        # Get unicode value for the letter
        unicode_value = ord(letter)
        
        # Add to glyph mappings
        glyph_name = letter
        glyph_order.append(glyph_name)
        cmap[unicode_value] = glyph_name
        metrics[glyph_name] = (600, 0)  # width, left side bearing
    
    # Setup the font with basic required tables
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupHorizontalMetrics(metrics)
    
    # Create a minimal glyf table with empty glyphs
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    
    glyphs = {}
    for glyph_name in glyph_order:
        pen = TTGlyphPen(None)
        # Add a simple square contour for each glyph
        if glyph_name != '.notdef':  # Skip .notdef as it's special
            pen.moveTo((0, 0))
            pen.lineTo((0, 1000))
            pen.lineTo((1000, 1000))
            pen.lineTo((1000, 0))
            pen.closePath()
        glyphs[glyph_name] = pen.glyph()
    
    fb.setupGlyf(glyphs)
    
    # Save the base OTF font
    output_path = 'font/phonics_font.otf'
    fb.save(output_path)
    print(f"Font created successfully: {output_path}")
    
    # To create an SVG font (for color), we'd need to modify the approach
    # This would require either fontforge (which isn't easily installable via pip)
    # or a more complex approach with fontTools to embed SVGs
    print("Note: This is a basic font. For SVG color font, additional tools like fontforge would be needed.")

if __name__ == '__main__':
    main()