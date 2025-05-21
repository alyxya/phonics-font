#!/usr/bin/env python3
import os
import string
import io
import base64
import struct
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
import xml.etree.ElementTree as ET

# Configuration
FONT_NAME = "PhonicsPicturesSVG"
OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
SVG_DIR = os.path.join(OUTPUT_DIR, "svg")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{FONT_NAME}.ttf")
FONT_SIZE = 1000  # Units per em
IMAGE_SIZE = (500, 500)  # Size of each letter image

# Ensure directories exist
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(SVG_DIR, exist_ok=True)

def create_sample_images():
    """Create sample images for each letter if they don't exist"""
    sample_images = {
        'a': 'apple',
        'b': 'ball',
        'c': 'cat',
        'd': 'dog',
        'e': 'elephant',
        'f': 'fish',
        'g': 'giraffe',
        'h': 'house',
        'i': 'igloo',
        'j': 'jellyfish',
        'k': 'kite',
        'l': 'lion',
        'm': 'monkey',
        'n': 'nest',
        'o': 'octopus',
        'p': 'penguin',
        'q': 'queen',
        'r': 'rabbit',
        's': 'snake',
        't': 'tiger',
        'u': 'umbrella',
        'v': 'violin',
        'w': 'watermelon',
        'x': 'xylophone',
        'y': 'yacht',
        'z': 'zebra'
    }

    for letter, word in sample_images.items():
        img_path = os.path.join(IMAGES_DIR, f"{letter}.png")
        if not os.path.exists(img_path):
            # Create a sample colored image with the word
            img = Image.new('RGBA', IMAGE_SIZE, color=(255, 255, 255, 0))
            
            # Generate a hue based on the letter's position in the alphabet
            hue = (ord(letter) - ord('a')) * (360/26)  # Spread colors across hue range
            r, g, b = hsv_to_rgb(hue/360, 0.8, 0.9)
            
            # Draw a colored circle with the letter
            draw = ImageDraw.Draw(img)
            
            # Draw colored circle
            circle_radius = min(IMAGE_SIZE) // 2 - 10
            circle_center = (IMAGE_SIZE[0] // 2, IMAGE_SIZE[1] // 2)
            draw.ellipse(
                (
                    circle_center[0] - circle_radius, 
                    circle_center[1] - circle_radius,
                    circle_center[0] + circle_radius, 
                    circle_center[1] + circle_radius
                ), 
                fill=(int(r*255), int(g*255), int(b*255), 255)
            )
            
            # Add the letter and word
            try:
                # Try to use a system font
                font = ImageFont.truetype("Arial", 120)
            except IOError:
                # Fallback to default
                font = ImageFont.load_default()
                
            # Draw the letter
            letter_pos = (IMAGE_SIZE[0] // 2, IMAGE_SIZE[1] // 2 - 50)
            draw.text(letter_pos, letter.upper(), fill=(255, 255, 255, 255), font=font, anchor="mm")
            
            # Draw the word
            word_pos = (IMAGE_SIZE[0] // 2, IMAGE_SIZE[1] // 2 + 70)
            small_font = ImageFont.truetype("Arial", 60) if font != ImageFont.load_default() else ImageFont.load_default()
            draw.text(word_pos, word, fill=(0, 0, 0, 255), font=small_font, anchor="mm")
            
            # Save the image
            img.save(img_path)
            print(f"Created sample image for '{letter}' ({word})")

def hsv_to_rgb(h, s, v):
    """Convert HSV color space to RGB color space"""
    if s == 0.0:
        return v, v, v
    
    i = int(h * 6)
    f = (h * 6) - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    i %= 6
    
    if i == 0:
        return v, t, p
    elif i == 1:
        return q, v, p
    elif i == 2:
        return p, v, t
    elif i == 3:
        return p, q, v
    elif i == 4:
        return t, p, v
    else:
        return v, p, q

def convert_images_to_svg():
    """Convert all PNG images to SVG format with embedded images"""
    svg_files = {}
    
    for letter in string.ascii_lowercase:
        img_path = os.path.join(IMAGES_DIR, f"{letter}.png")
        svg_path = os.path.join(SVG_DIR, f"{letter}.svg")
        
        if not os.path.exists(img_path):
            print(f"Image file does not exist: {img_path}")
            continue
        
        # Read image and get dimensions
        with Image.open(img_path) as img:
            width, height = img.size
            
            # Create SVG with embedded image
            svg = ET.Element("svg", {
                "xmlns": "http://www.w3.org/2000/svg",
                "xmlns:xlink": "http://www.w3.org/1999/xlink",
                "width": str(width),
                "height": str(height),
                "viewBox": f"0 0 {width} {height}"
            })
            
            # Convert PNG to base64 for embedding
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            
            # Add image to SVG
            ET.SubElement(svg, "image", {
                "width": str(width),
                "height": str(height),
                "xlink:href": f"data:image/png;base64,{img_base64}"
            })
            
            # Write SVG to file
            tree = ET.ElementTree(svg)
            with open(svg_path, "wb") as f:
                tree.write(f, encoding="utf-8", xml_declaration=True)
            
            # Store SVG document
            with open(svg_path, "rb") as f:
                svg_content = f.read()
                svg_files[letter] = svg_content
                
            print(f"Converted {img_path} to {svg_path}")
    
    return svg_files

def create_basic_font():
    """Create a basic TTF font with empty glyphs"""
    font = TTFont()
    
    # Add required tables
    font['head'] = newTable('head')
    font['head'].tableVersion = 1.0
    font['head'].fontRevision = 1.0
    font['head'].checkSumAdjustment = 0  # Will be recalculated when the font is saved
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
    font['hhea'].numberOfHMetrics = 0  # Will update later
    
    # Create hmtx table
    font['hmtx'] = newTable('hmtx')
    font['hmtx'].metrics = {}
    
    # Create maxp table
    font['maxp'] = newTable('maxp')
    font['maxp'].tableVersion = 0x00010000
    font['maxp'].numGlyphs = 0  # Will update later
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
    familyName = FONT_NAME
    styleName = "Regular"
    uniqueID = f"{familyName}.{styleName}"
    fullName = f"{familyName} {styleName}"
    version = "Version 1.0"
    
    nameStrings = {
        1: familyName,    # Font Family name
        2: styleName,     # Font Subfamily name
        3: uniqueID,      # Unique font identifier
        4: fullName,      # Full font name
        5: version,       # Version string
        6: familyName,    # PostScript name
    }
    
    for nameID, nameString in nameStrings.items():
        for platformID, encodingID, languageID in [(3, 1, 0x409)]:  # Windows English
            font['name'].setName(nameString, nameID, platformID, encodingID, languageID)
    
    # Create OS/2 table
    font['OS/2'] = newTable('OS/2')
    font['OS/2'].version = 4
    font['OS/2'].usWeightClass = 400
    font['OS/2'].usWidthClass = 5
    font['OS/2'].fsType = 0
    
    # Required fields for OS/2 table
    font['OS/2'].xAvgCharWidth = 500
    font['OS/2'].usBreakChar = 32  # space
    font['OS/2'].usDefaultChar = 0  # .notdef
    font['OS/2'].sTypoAscender = int(FONT_SIZE * 0.8)
    font['OS/2'].sTypoDescender = int(FONT_SIZE * -0.2)
    font['OS/2'].sTypoLineGap = 0
    font['OS/2'].usWinAscent = int(FONT_SIZE * 0.8)
    font['OS/2'].usWinDescent = int(FONT_SIZE * 0.2)
    
    # CodePage ranges - required for Windows
    font['OS/2'].ulCodePageRange1 = 0x00000001  # Latin 1
    font['OS/2'].ulCodePageRange2 = 0
    
    # Unicode ranges
    font['OS/2'].ulUnicodeRange1 = 0x00000001  # Basic Latin
    font['OS/2'].ulUnicodeRange2 = 0
    font['OS/2'].ulUnicodeRange3 = 0
    font['OS/2'].ulUnicodeRange4 = 0
    
    # Panose - needs to be a proper structure
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
    
    # Vendor ID
    font['OS/2'].achVendID = 'PYFT'  # Python FontTools
    
    # Font selection flags
    font['OS/2'].fsSelection = 0
    
    # sFamilyClass (font classification)
    font['OS/2'].sFamilyClass = 0
    
    # Required metrics for OS/2 table version 2 and above
    font['OS/2'].sxHeight = 0
    font['OS/2'].sCapHeight = 0
    font['OS/2'].usDefaultChar = 0
    font['OS/2'].usBreakChar = 32  # space
    font['OS/2'].usMaxContext = 0
    
    # The min/max values, assuming a square design for all glyphs
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
    
    # Create post table
    font['post'] = newTable('post')
    font['post'].formatType = 3.0
    font['post'].italicAngle = 0
    font['post'].underlinePosition = -75
    font['post'].underlineThickness = 50
    font['post'].isFixedPitch = 0
    font['post'].minMemType42 = 0
    font['post'].maxMemType42 = 0
    font['post'].minMemType1 = 0
    font['post'].maxMemType1 = 0
    
    # Create cmap table
    font['cmap'] = newTable('cmap')
    font['cmap'].tableVersion = 0
    from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
    cmap_format4 = CmapSubtable.newSubtable(4)
    cmap_format4.platformID = 3
    cmap_format4.platEncID = 1
    cmap_format4.language = 0
    cmap_format4.cmap = {}  # Will be populated later
    font['cmap'].tables = [cmap_format4]
    
    # Create empty glyf and loca tables
    font['glyf'] = newTable('glyf')
    font['glyf'].glyphs = {}
    font['loca'] = newTable('loca')
    
    return font

def add_empty_glyphs_to_font(font, letters):
    """Add empty placeholder glyphs for each letter"""
    # Initialize glyph order and map
    glyph_order = ['.notdef']
    glyph_id_map = {'.notdef': 0}
    
    # Set the glyph order first
    for letter in letters:
        unicode_value = ord(letter)
        glyph_name = f"uni{unicode_value:04X}"
        glyph_order.append(glyph_name)
        glyph_id_map[glyph_name] = len(glyph_order) - 1
    
    # Set the glyph order in the font
    font.setGlyphOrder(glyph_order)
    
    # Add a required .notdef glyph
    pen = TTGlyphPen(glyphSet=font.getGlyphSet())
    pen.moveTo((50, 50))
    pen.lineTo((450, 50))
    pen.lineTo((450, 450))
    pen.lineTo((50, 450))
    pen.closePath()
    font['glyf']['.notdef'] = pen.glyph()
    font['hmtx'].metrics['.notdef'] = (500, 0)
    
    # Add empty glyphs for each letter
    for letter in letters:
        unicode_value = ord(letter)
        glyph_name = f"uni{unicode_value:04X}"
        
        # Create a simple rectangle glyph as placeholder
        pen = TTGlyphPen(glyphSet=font.getGlyphSet())
        pen.moveTo((50, 50))
        pen.lineTo((450, 50))
        pen.lineTo((450, 450))
        pen.lineTo((50, 450))
        pen.closePath()
        
        font['glyf'][glyph_name] = pen.glyph()
        font['hmtx'].metrics[glyph_name] = (500, 0)
        
        # Map Unicode code point to glyph
        for cmap in font['cmap'].tables:
            cmap.cmap[unicode_value] = glyph_name
    
    # Update font metrics
    font['maxp'].numGlyphs = len(glyph_order)
    font['hhea'].numberOfHMetrics = len(font['hmtx'].metrics)
    
    return font, glyph_id_map

def add_svg_table(font, glyph_id_map, svg_files):
    """Add SVG table to the font"""
    from fontTools.ttLib.tables.S_V_G_ import table_S_V_G_
    
    # Create SVG table
    svg_table = table_S_V_G_()
    svg_table.docList = []
    svg_table.colorPalettes = None
    
    # Add SVG documents for each letter
    for letter, svg_data in svg_files.items():
        unicode_value = ord(letter)
        glyph_name = f"uni{unicode_value:04X}"
        
        if glyph_name in glyph_id_map:
            glyph_id = glyph_id_map[glyph_name]
            
            # Add SVG document to table
            svg_table.docList.append((glyph_id, glyph_id, svg_data))
            print(f"Added SVG for '{letter}' (GlyphID: {glyph_id})")
    
    # Sort documents by glyph ID
    svg_table.docList.sort(key=lambda doc: doc[0])
    
    # Add table to font
    font['SVG '] = svg_table
    
    return font

def main():
    # Create sample images for letters
    create_sample_images()
    
    # Convert images to SVG format
    svg_files = convert_images_to_svg()
    
    # Create basic font
    font = create_basic_font()
    
    # Add empty glyphs for each letter
    font, glyph_id_map = add_empty_glyphs_to_font(font, string.ascii_lowercase)
    
    # Add SVG table with color glyphs
    font = add_svg_table(font, glyph_id_map, svg_files)
    
    # Save the font
    try:
        font.save(OUTPUT_FILE)
        print(f"SVG color font saved to {OUTPUT_FILE}")
        print("Note: This font uses SVG table for color support.")
        print("It will work in modern browsers and applications that support SVG fonts.")
    except Exception as e:
        print(f"Error saving font: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()