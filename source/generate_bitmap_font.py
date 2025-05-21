#!/usr/bin/env python3
import os
import string
from PIL import Image
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._g_l_y_f import Glyph
from fontTools.ttLib.tables import _c_m_a_p
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables import _h_e_a_d, _h_h_e_a, _h_m_t_x, _m_a_x_p, _n_a_m_e, _p_o_s_t
from fontTools.ttLib.tables.O_S_2f_2 import table_O_S_2f_2
import struct
import io

# Configuration
FONT_NAME = "PhonicsPictures"
OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{FONT_NAME}.ttf")
FONT_SIZE = 1000  # Units per em
IMAGE_SIZE = (500, 500)  # Size of each letter image

def create_empty_font():
    """Create an empty font with all required tables"""
    font = TTFont()
    
    # Create head table
    font['head'] = newTable('head')
    font['head'].checkSumAdjustment = 0
    font['head'].tableVersion = 1.0
    font['head'].fontRevision = 1.0
    font['head'].magicNumber = 0x5F0F3CF5
    font['head'].flags = 0
    font['head'].unitsPerEm = FONT_SIZE
    font['head'].created = 0
    font['head'].modified = 0
    font['head'].xMin = 0
    font['head'].yMin = 0
    font['head'].xMax = FONT_SIZE
    font['head'].yMax = FONT_SIZE
    font['head'].macStyle = 0
    font['head'].lowestRecPPEM = 8
    font['head'].fontDirectionHint = 2
    font['head'].indexToLocFormat = 0
    font['head'].glyphDataFormat = 0
    
    # Create hhea table
    font['hhea'] = newTable('hhea')
    font['hhea'].tableVersion = 0x00010000
    font['hhea'].ascent = int(FONT_SIZE * 0.8)
    font['hhea'].descent = int(FONT_SIZE * -0.2)
    font['hhea'].lineGap = 0
    font['hhea'].advanceWidthMax = FONT_SIZE
    font['hhea'].minLeftSideBearing = 0
    font['hhea'].minRightSideBearing = 0
    font['hhea'].xMaxExtent = FONT_SIZE
    font['hhea'].caretSlopeRise = 1
    font['hhea'].caretSlopeRun = 0
    font['hhea'].caretOffset = 0
    font['hhea'].reserved0 = 0
    font['hhea'].reserved1 = 0
    font['hhea'].reserved2 = 0
    font['hhea'].reserved3 = 0
    font['hhea'].metricDataFormat = 0
    font['hhea'].numberOfHMetrics = 0  # Will be updated later
    
    # Create hmtx table (horizontal metrics)
    font['hmtx'] = newTable('hmtx')
    font['hmtx'].metrics = {}
    
    # Create maxp table (maximum profile)
    font['maxp'] = newTable('maxp')
    font['maxp'].tableVersion = 0x00010000
    font['maxp'].numGlyphs = 0
    font['maxp'].maxPoints = 0
    font['maxp'].maxContours = 0
    font['maxp'].maxCompositePoints = 0
    font['maxp'].maxCompositeContours = 0
    font['maxp'].maxZones = 2
    font['maxp'].maxTwilightPoints = 0
    font['maxp'].maxStorage = 0
    font['maxp'].maxFunctionDefs = 0
    font['maxp'].maxInstructionDefs = 0
    font['maxp'].maxStackElements = 0
    font['maxp'].maxSizeOfInstructions = 0
    font['maxp'].maxComponentElements = 0
    font['maxp'].maxComponentDepth = 0
    
    # Create name table
    font['name'] = newTable('name')
    
    # Add name records
    nameStrings = {
        1: FONT_NAME,  # Font Family name
        2: "Regular",  # Font Subfamily name
        3: f"{FONT_NAME}:Regular",  # Unique font identifier
        4: f"{FONT_NAME} Regular",  # Full font name
        5: "Version 1.0",  # Version string
        6: f"{FONT_NAME}-Regular",  # PostScript name
    }
    
    for nameID, nameString in nameStrings.items():
        font['name'].setName(nameString, nameID, 3, 1, 0x409)  # Windows, Unicode, English
    
    # Create OS/2 table
    font['OS/2'] = newTable('OS/2')
    font['OS/2'].version = 4
    font['OS/2'].xAvgCharWidth = 500
    font['OS/2'].usWeightClass = 400
    font['OS/2'].usWidthClass = 5
    font['OS/2'].fsType = 0
    
    # Unicode ranges
    font['OS/2'].ulUnicodeRange1 = 1  # Basic Latin
    font['OS/2'].ulUnicodeRange2 = 0
    font['OS/2'].ulUnicodeRange3 = 0
    font['OS/2'].ulUnicodeRange4 = 0
    
    # Code page ranges
    font['OS/2'].ulCodePageRange1 = 0x00000001  # Latin 1
    font['OS/2'].ulCodePageRange2 = 0
    
    # Metrics
    font['OS/2'].sTypoAscender = font['hhea'].ascent
    font['OS/2'].sTypoDescender = font['hhea'].descent
    font['OS/2'].sTypoLineGap = font['hhea'].lineGap
    font['OS/2'].usWinAscent = font['hhea'].ascent
    font['OS/2'].usWinDescent = -font['hhea'].descent
    
    # Vendor ID
    font['OS/2'].achVendID = "PYFT"  # Python FontTools
    
    # Font classification
    font['OS/2'].sFamilyClass = 0
    
    # Panose classification
    from fontTools.ttLib.tables.O_S_2f_2 import Panose
    font['OS/2'].panose = Panose()
    font['OS/2'].panose.bFamilyType = 0
    font['OS/2'].panose.bSerifStyle = 0
    font['OS/2'].panose.bWeight = 0
    font['OS/2'].panose.bProportion = 0
    font['OS/2'].panose.bContrast = 0
    font['OS/2'].panose.bStrokeVariation = 0
    font['OS/2'].panose.bArmStyle = 0
    font['OS/2'].panose.bLetterForm = 0
    font['OS/2'].panose.bMidline = 0
    font['OS/2'].panose.bXHeight = 0
    
    # Subscript/superscript metrics
    font['OS/2'].ySubscriptXSize = int(FONT_SIZE * 0.65)
    font['OS/2'].ySubscriptYSize = int(FONT_SIZE * 0.65)
    font['OS/2'].ySubscriptXOffset = 0
    font['OS/2'].ySubscriptYOffset = int(FONT_SIZE * 0.075)
    font['OS/2'].ySuperscriptXSize = int(FONT_SIZE * 0.65)
    font['OS/2'].ySuperscriptYSize = int(FONT_SIZE * 0.65)
    font['OS/2'].ySuperscriptXOffset = 0
    font['OS/2'].ySuperscriptYOffset = int(FONT_SIZE * 0.35)
    font['OS/2'].yStrikeoutSize = int(FONT_SIZE * 0.05)
    font['OS/2'].yStrikeoutPosition = int(FONT_SIZE * 0.3)
    
    # Selection flags
    font['OS/2'].fsSelection = 0
    
    # Required for version 2 and above
    font['OS/2'].sxHeight = 0
    font['OS/2'].sCapHeight = 0
    font['OS/2'].usDefaultChar = 0
    font['OS/2'].usBreakChar = 32  # space
    font['OS/2'].usMaxContext = 0
    
    # Create post table (PostScript)
    font['post'] = newTable('post')
    font['post'].formatType = 3.0
    font['post'].italicAngle = 0
    font['post'].underlinePosition = -int(FONT_SIZE * 0.075)
    font['post'].underlineThickness = int(FONT_SIZE * 0.05)
    font['post'].isFixedPitch = 0
    font['post'].minMemType42 = 0
    font['post'].maxMemType42 = 0
    font['post'].minMemType1 = 0
    font['post'].maxMemType1 = 0
    
    # Create cmap table (character to glyph mapping)
    font['cmap'] = newTable('cmap')
    font['cmap'].tableVersion = 0
    
    # Create a format 4 cmap subtable
    cmap_format4 = _c_m_a_p.CmapSubtable.newSubtable(4)
    cmap_format4.platformID = 3  # Windows
    cmap_format4.platEncID = 1   # Unicode BMP
    cmap_format4.language = 0    # Default language
    cmap_format4.cmap = {}       # Empty mapping to start
    font['cmap'].tables = [cmap_format4]
    
    # Create empty glyf and loca tables
    font['glyf'] = newTable('glyf')
    font['glyf'].glyphs = {}
    font['loca'] = newTable('loca')
    
    return font

def add_glyphs_to_font(font):
    """Add glyphs to the font for each letter"""
    # Set up a list for the glyph order
    glyph_order = ['.notdef']  # Start with .notdef
    
    # Build the full glyph order first
    for letter in string.ascii_lowercase:
        unicode_value = ord(letter)
        glyph_name = f"uni{unicode_value:04X}"
        glyph_order.append(glyph_name)
    
    # Set the glyph order in the font first
    font.setGlyphOrder(glyph_order)
    
    # Create a simple .notdef glyph (empty square)
    pen = TTGlyphPen(glyphSet=font.getGlyphSet())
    pen.moveTo((50, 50))
    pen.lineTo((450, 50))
    pen.lineTo((450, 450))
    pen.lineTo((50, 450))
    pen.closePath()
    font['glyf']['.notdef'] = pen.glyph()
    font['hmtx'].metrics['.notdef'] = (500, 0)
    
    # Add glyphs for each lowercase letter
    for letter in string.ascii_lowercase:
        unicode_value = ord(letter)
        glyph_name = f"uni{unicode_value:04X}"
        
        # Create a simple square glyph
        pen = TTGlyphPen(glyphSet=font.getGlyphSet())
        pen.moveTo((0, 0))
        pen.lineTo((FONT_SIZE, 0))
        pen.lineTo((FONT_SIZE, FONT_SIZE))
        pen.lineTo((0, FONT_SIZE))
        pen.closePath()
        
        font['glyf'][glyph_name] = pen.glyph()
        font['hmtx'].metrics[glyph_name] = (FONT_SIZE, 0)
        
        # Map the Unicode character to this glyph
        for cmap in font['cmap'].tables:
            cmap.cmap[unicode_value] = glyph_name
        
        print(f"Added glyph for '{letter}' (Unicode: {unicode_value})")
    
    # Update the font metrics
    font['maxp'].numGlyphs = len(glyph_order)
    font['hhea'].numberOfHMetrics = len(font['hmtx'].metrics)
    
    return font

def main():
    # Create a basic font
    font = create_empty_font()
    
    # Add glyphs for each letter
    font = add_glyphs_to_font(font)
    
    # Save the font
    try:
        font.save(OUTPUT_FILE)
        print(f"Font saved to {OUTPUT_FILE}")
        print("You can now install this font on your Mac by:")
        print("1. Double-clicking the font file")
        print("2. Clicking 'Install Font' in the Font Book app")
    except Exception as e:
        print(f"Error saving font: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()