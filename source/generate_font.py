#!/usr/bin/env python3
import os
import string
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables._g_l_y_f import Glyph
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
import math

# Configuration
FONT_NAME = "PhonicsPictures"
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
            img = Image.new('RGB', IMAGE_SIZE, color=(255, 255, 255))
            
            # Generate a hue based on the letter's position in the alphabet
            hue = (ord(letter) - ord('a')) * (360/26)  # Spread colors across hue range
            r, g, b = hsv_to_rgb(hue/360, 0.8, 0.9)
            
            # Draw a colored circle with the letter
            from PIL import ImageDraw, ImageFont
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
                fill=(int(r*255), int(g*255), int(b*255))
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
            draw.text(letter_pos, letter.upper(), fill=(255, 255, 255), font=font, anchor="mm")
            
            # Draw the word
            word_pos = (IMAGE_SIZE[0] // 2, IMAGE_SIZE[1] // 2 + 70)
            small_font = ImageFont.truetype("Arial", 60) if font != ImageFont.load_default() else ImageFont.load_default()
            draw.text(word_pos, word, fill=(0, 0, 0), font=small_font, anchor="mm")
            
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

def create_empty_font():
    """Create a new empty TTFont"""
    font = TTFont()
    font.flavor = None
    
    # Add required tables
    font['head'] = TTFont().getTableClass('head')()
    font['head'].unitsPerEm = FONT_SIZE
    font['head'].xMin = 0
    font['head'].yMin = 0
    font['head'].xMax = FONT_SIZE
    font['head'].yMax = FONT_SIZE
    
    font['hhea'] = TTFont().getTableClass('hhea')()
    font['hhea'].ascent = int(FONT_SIZE * 0.8)
    font['hhea'].descent = int(FONT_SIZE * -0.2)
    
    font['hmtx'] = TTFont().getTableClass('hmtx')()
    font['maxp'] = TTFont().getTableClass('maxp')()
    font['post'] = TTFont().getTableClass('post')()
    font['cmap'] = TTFont().getTableClass('cmap')()
    
    # Create empty glyf table
    font['glyf'] = TTFont().getTableClass('glyf')()
    font['loca'] = TTFont().getTableClass('loca')()
    
    # Create OS/2 table
    font['OS/2'] = TTFont().getTableClass('OS/2')()
    
    # Create name table 
    font['name'] = TTFont().getTableClass('name')()
    nameRecord = font['name'].setName(FONT_NAME, 1, 3, 1, 1033)  # Family name
    nameRecord = font['name'].setName(FONT_NAME, 2, 3, 1, 1033)  # Style name
    nameRecord = font['name'].setName(f"{FONT_NAME} Regular", 4, 3, 1, 1033)  # Full name
    
    # Initialize defaults for required tables
    font['maxp'].numGlyphs = 0
    
    return font

def add_glyph_from_image(font, unicode_value, image_path):
    """Add a glyph to the font from an image"""
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return False
    
    try:
        img = Image.open(image_path)
        
        # Scale the image to fit in the font
        width, height = img.size
        scale = min(FONT_SIZE / width, FONT_SIZE / height) * 0.8
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Create a simple rectangular glyph that will be referenced in COLR/CPAL tables later
        pen = TTGlyphPen(None)
        pen.moveTo((0, 0))
        pen.lineTo((new_width, 0))
        pen.lineTo((new_width, new_height))
        pen.lineTo((0, new_height))
        pen.closePath()
        
        # Add the glyph to the font
        glyph_name = f"uni{unicode_value:04X}"
        font['glyf'][glyph_name] = pen.glyph()
        
        # Update the hmtx table with glyph metrics
        font['hmtx'].metrics[glyph_name] = (new_width, 0)
        
        # Map the Unicode code point to this glyph
        if not font['cmap'].tables:
            cmap_format4 = CmapSubtable.newSubtable(4)
            font['cmap'].tables.append(cmap_format4)
        
        for subtable in font['cmap'].tables:
            subtable.cmap[unicode_value] = glyph_name
        
        # Increment the number of glyphs
        font['maxp'].numGlyphs += 1
        
        return True
        
    except Exception as e:
        print(f"Error adding glyph for Unicode {unicode_value}: {e}")
        return False

def main():
    # Create sample images for letters (you can replace these with your own images)
    create_sample_images()
    
    # Create an empty font
    font = create_empty_font()
    
    # Add a required .notdef glyph
    pen = TTGlyphPen(None)
    pen.moveTo((50, 50))
    pen.lineTo((450, 50))
    pen.lineTo((450, 450))
    pen.lineTo((50, 450))
    pen.closePath()
    font['glyf']['.notdef'] = pen.glyph()
    font['hmtx'].metrics['.notdef'] = (500, 0)
    font['maxp'].numGlyphs += 1
    
    # Add a glyph for each letter
    for letter in string.ascii_lowercase:
        unicode_value = ord(letter)
        image_path = os.path.join(IMAGES_DIR, f"{letter}.png")
        if add_glyph_from_image(font, unicode_value, image_path):
            print(f"Added glyph for '{letter}' (Unicode: {unicode_value})")
    
    # Save the font
    try:
        font.save(OUTPUT_FILE)
        print(f"Font saved to {OUTPUT_FILE}")
        print("Note: This is a basic font. The images are converted to simple outlines.")
        print("For full color support, you would need a more advanced approach.")
    except Exception as e:
        print(f"Error saving font: {e}")

if __name__ == "__main__":
    main()