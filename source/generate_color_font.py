#!/usr/bin/env python3
import os
import string
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import _c_m_a_p
from fontTools.ttLib.tables import _h_e_a_d
from fontTools.ttLib.tables import _h_h_e_a
from fontTools.ttLib.tables import _h_m_t_x
from fontTools.ttLib.tables import _m_a_x_p
from fontTools.ttLib.tables import _n_a_m_e
from fontTools.ttLib.tables import _O_S_2
from fontTools.ttLib.tables import _p_o_s_t
from fontTools.ttLib.tables._c_b_d_t import CBDT
from fontTools.ttLib.tables._c_b_l_c import CBLC
import struct
import math

# Configuration
FONT_NAME = "PhonicsPicturesColor"
OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{FONT_NAME}.ttf")
FONT_SIZE = 1000  # Units per em
IMAGE_SIZE = (500, 500)  # Size of each letter image

# Ensure images directory exists
os.makedirs(IMAGES_DIR, exist_ok=True)

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

def create_font_with_cbdt():
    """Create a new font with CBDT/CBLC tables for color bitmap support"""
    font = TTFont()
    
    # Add required tables
    font['head'] = newTable('head')
    font['head'].tableVersion = 1.0
    font['head'].fontRevision = 1.0
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
    # Many other fields omitted for simplicity
    
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
    cmap_format4 = _c_m_a_p.CmapSubtable.newSubtable(4)
    cmap_format4.platformID = 3
    cmap_format4.platEncID = 1
    cmap_format4.language = 0
    cmap_format4.cmap = {}  # Will be populated later
    font['cmap'].tables = [cmap_format4]
    
    # Create empty CBDT and CBLC tables for color bitmap support
    font['CBDT'] = newTable('CBDT')
    font['CBDT'].version = 3  # Version 3 for CBDT
    font['CBDT'].strikeData = []
    
    font['CBLC'] = newTable('CBLC')
    font['CBLC'].version = 3  # Version 3 for CBLC
    font['CBLC'].strikes = []
    
    return font

def add_bitmap_glyphs_to_font(font, letters, images_dir):
    """Add bitmap glyphs to the font using CBDT/CBLC tables"""
    from PIL import Image
    import io
    
    # Prepare structures for CBDT/CBLC tables
    cbdt_strike_data = {}
    cblc_strike = {
        'ppemX': 72,  # Pixels per em X
        'ppemY': 72,  # Pixels per em Y
        'bitDepth': 32,  # 32 bit RGBA
        'flags': 0,
        'subtables': []
    }
    
    # Map for glyph IDs
    glyph_id_map = {}
    next_glyph_id = 0
    
    # First, add a required .notdef glyph
    glyph_id_map['.notdef'] = next_glyph_id
    font['hmtx'].metrics['.notdef'] = (FONT_SIZE, 0)
    next_glyph_id += 1
    
    # Create a subtable in CBLC for the bitmap strike
    subtable = {
        'firstGlyphIndex': 1,  # Start after .notdef
        'lastGlyphIndex': len(letters),
        'additionalOffsetToIndexSubtable': 0,  # Will be calculated later
        'indexFormat': 1,
        'imageFormat': 17,  # Format 17: PNG with alpha
        'imageDataOffset': 0,  # Will be calculated later
        'glyphIdArray': [],
        'glyphOffsets': []
    }
    
    glyph_bitmap_data = []
    
    # Process each letter
    for letter in letters:
        unicode_value = ord(letter)
        glyph_name = f"uni{unicode_value:04X}"
        image_path = os.path.join(images_dir, f"{letter}.png")
        
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            continue
        
        try:
            img = Image.open(image_path)
            
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Get image dimensions
            width, height = img.size
            
            # Store glyph ID
            glyph_id = next_glyph_id
            glyph_id_map[glyph_name] = glyph_id
            next_glyph_id += 1
            
            # Add to cmap
            for subtable in font['cmap'].tables:
                subtable.cmap[unicode_value] = glyph_name
            
            # Add width information
            font['hmtx'].metrics[glyph_name] = (width, 0)
            
            # Save image as PNG in memory
            png_data = io.BytesIO()
            img.save(png_data, format='PNG')
            png_data = png_data.getvalue()
            
            # Store bitmap data
            bitmap_data = {
                'glyphID': glyph_id,
                'imageData': png_data
            }
            glyph_bitmap_data.append(bitmap_data)
            
            # Add to subtable glyph array
            subtable['glyphIdArray'].append(glyph_id)
            
            print(f"Added bitmap glyph for '{letter}' (Unicode: {unicode_value})")
            
        except Exception as e:
            print(f"Error adding bitmap glyph for '{letter}': {e}")
    
    # Store the bitmap data
    offset = 0
    for bitmap in glyph_bitmap_data:
        # Store offset
        subtable['glyphOffsets'].append(offset)
        # Actual CBDT data (PNG format)
        cbdt_strike_data[bitmap['glyphID']] = {
            'imageData': bitmap['imageData']
        }
        offset += len(bitmap['imageData'])
    
    # Add final offset
    subtable['glyphOffsets'].append(offset)
    
    # Add subtable to CBLC strike
    cblc_strike['subtables'].append(subtable)
    
    # Attach to font CBLC/CBDT tables
    font['CBLC'].strikes = [cblc_strike]
    font['CBDT'].strikeData = [cbdt_strike_data]
    
    # Update font metrics
    font['hhea'].numberOfHMetrics = len(font['hmtx'].metrics)
    font['maxp'].numGlyphs = next_glyph_id
    
    return font

def main():
    # Create sample images for letters
    create_sample_images()
    
    # Create font with CBDT/CBLC tables for color bitmap support
    font = create_font_with_cbdt()
    
    # Add bitmap glyphs for all lowercase letters
    letters = string.ascii_lowercase
    font = add_bitmap_glyphs_to_font(font, letters, IMAGES_DIR)
    
    # Save the font
    try:
        font.save(OUTPUT_FILE)
        print(f"Color bitmap font saved to {OUTPUT_FILE}")
        print("Note: This font uses CBDT/CBLC tables for color bitmap support.")
        print("It may only work in certain applications that support these tables.")
    except Exception as e:
        print(f"Error saving font: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()