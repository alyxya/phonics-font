#!/usr/bin/env python3
import os
import string
import math
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables import _c_m_a_p
from fontTools.ttLib.tables.O_S_2f_2 import Panose

# Configuration
FONT_NAME = "PhonicsPicturesShapes"
OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{FONT_NAME}.ttf")
FONT_SIZE = 1000  # Units per em

# Ensure directories exist
os.makedirs(IMAGES_DIR, exist_ok=True)

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
    font['maxp'].maxPoints = 100  # Set reasonable defaults
    font['maxp'].maxContours = 10
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
    font['OS/2'].sxHeight = 500
    font['OS/2'].sCapHeight = 700
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

def draw_apple(pen, x, y, width, height):
    """Draw an apple shape for 'a'"""
    # Draw apple body (circle)
    cx, cy = x + width/2, y + height/2
    radius = min(width, height) * 0.4
    
    # Main apple body
    pen.moveTo((cx, cy - radius))
    
    # Use an approximation of a circle with Bezier curves
    # Top right quadrant
    pen.qCurveTo((cx + radius/2, cy - radius), (cx + radius, cy - radius/2), (cx + radius, cy))
    # Bottom right quadrant
    pen.qCurveTo((cx + radius, cy + radius/2), (cx + radius/2, cy + radius), (cx, cy + radius))
    # Bottom left quadrant
    pen.qCurveTo((cx - radius/2, cy + radius), (cx - radius, cy + radius/2), (cx - radius, cy))
    # Top left quadrant
    pen.qCurveTo((cx - radius, cy - radius/2), (cx - radius/2, cy - radius), (cx, cy - radius))
    
    pen.closePath()
    
    # Draw stem
    stem_width = width * 0.05
    stem_height = height * 0.15
    pen.moveTo((cx - stem_width/2, cy - radius))
    pen.lineTo((cx - stem_width/2, cy - radius - stem_height))
    pen.lineTo((cx + stem_width/2, cy - radius - stem_height))
    pen.lineTo((cx + stem_width/2, cy - radius))
    pen.closePath()
    
    # Draw leaf
    leaf_width = width * 0.15
    leaf_height = height * 0.2
    pen.moveTo((cx + stem_width/2, cy - radius - stem_height*0.7))
    pen.qCurveTo((cx + leaf_width/2, cy - radius - stem_height - leaf_height/2), 
                 (cx + leaf_width, cy - radius - stem_height), 
                 (cx + leaf_width, cy - radius - stem_height*0.5))
    pen.qCurveTo((cx + leaf_width, cy - radius), 
                 (cx + stem_width, cy - radius), 
                 (cx + stem_width/2, cy - radius - stem_height*0.5))
    pen.closePath()

def draw_ball(pen, x, y, width, height):
    """Draw a ball shape for 'b'"""
    # Draw a circle with some lines to make it look like a ball
    cx, cy = x + width/2, y + height/2
    radius = min(width, height) * 0.4
    
    # Main ball circle
    points = 24
    for i in range(points):
        angle = 2 * math.pi * i / points
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        if i == 0:
            pen.moveTo((px, py))
        else:
            pen.lineTo((px, py))
    pen.closePath()
    
    # Add some curved lines to make it look like a ball
    # Horizontal curve
    pen.moveTo((cx - radius * 0.7, cy))
    pen.qCurveTo((cx - radius * 0.3, cy + radius * 0.3), 
                 (cx + radius * 0.3, cy + radius * 0.3), 
                 (cx + radius * 0.7, cy))
    pen.closePath()
    
    # Vertical curve
    pen.moveTo((cx, cy - radius * 0.7))
    pen.qCurveTo((cx - radius * 0.3, cy - radius * 0.3), 
                 (cx - radius * 0.3, cy + radius * 0.3), 
                 (cx, cy + radius * 0.7))
    pen.closePath()

def draw_cat(pen, x, y, width, height):
    """Draw a cat shape for 'c'"""
    # Draw a cat face with pointy ears
    cx, cy = x + width/2, y + height/2
    radius = min(width, height) * 0.35
    
    # Cat face (circle)
    points = 24
    for i in range(points):
        angle = 2 * math.pi * i / points
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        if i == 0:
            pen.moveTo((px, py))
        else:
            pen.lineTo((px, py))
    pen.closePath()
    
    # Left ear
    ear_size = radius * 0.6
    pen.moveTo((cx - radius * 0.7, cy - radius * 0.3))
    pen.lineTo((cx - radius - ear_size, cy - radius - ear_size))
    pen.lineTo((cx - radius * 0.3, cy - radius * 0.7))
    pen.closePath()
    
    # Right ear
    pen.moveTo((cx + radius * 0.7, cy - radius * 0.3))
    pen.lineTo((cx + radius + ear_size, cy - radius - ear_size))
    pen.lineTo((cx + radius * 0.3, cy - radius * 0.7))
    pen.closePath()
    
    # Eyes
    eye_radius = radius * 0.15
    # Left eye
    pen.moveTo((cx - radius * 0.3, cy - radius * 0.1))
    pen.qCurveTo((cx - radius * 0.3 + eye_radius, cy - radius * 0.1), 
                 (cx - radius * 0.3 + eye_radius, cy - radius * 0.1 + eye_radius),
                 (cx - radius * 0.3, cy - radius * 0.1 + eye_radius * 2))
    pen.qCurveTo((cx - radius * 0.3 - eye_radius, cy - radius * 0.1 + eye_radius), 
                 (cx - radius * 0.3 - eye_radius, cy - radius * 0.1),
                 (cx - radius * 0.3, cy - radius * 0.1))
    pen.closePath()
    
    # Right eye
    pen.moveTo((cx + radius * 0.3, cy - radius * 0.1))
    pen.qCurveTo((cx + radius * 0.3 + eye_radius, cy - radius * 0.1), 
                 (cx + radius * 0.3 + eye_radius, cy - radius * 0.1 + eye_radius),
                 (cx + radius * 0.3, cy - radius * 0.1 + eye_radius * 2))
    pen.qCurveTo((cx + radius * 0.3 - eye_radius, cy - radius * 0.1 + eye_radius), 
                 (cx + radius * 0.3 - eye_radius, cy - radius * 0.1),
                 (cx + radius * 0.3, cy - radius * 0.1))
    pen.closePath()
    
    # Nose
    pen.moveTo((cx, cy + radius * 0.1))
    pen.lineTo((cx + radius * 0.1, cy + radius * 0.2))
    pen.lineTo((cx - radius * 0.1, cy + radius * 0.2))
    pen.closePath()
    
    # Mouth
    pen.moveTo((cx, cy + radius * 0.2))
    pen.lineTo((cx, cy + radius * 0.3))
    pen.closePath()
    
    pen.moveTo((cx, cy + radius * 0.3))
    pen.qCurveTo((cx + radius * 0.2, cy + radius * 0.4), 
                 (cx + radius * 0.3, cy + radius * 0.3),
                 (cx + radius * 0.3, cy + radius * 0.3))
    pen.closePath()
    
    pen.moveTo((cx, cy + radius * 0.3))
    pen.qCurveTo((cx - radius * 0.2, cy + radius * 0.4), 
                 (cx - radius * 0.3, cy + radius * 0.3),
                 (cx - radius * 0.3, cy + radius * 0.3))
    pen.closePath()

def draw_dog(pen, x, y, width, height):
    """Draw a dog shape for 'd'"""
    # Draw a dog head with floppy ears
    cx, cy = x + width/2, y + height/2
    radius = min(width, height) * 0.35
    
    # Dog face (circle)
    points = 24
    for i in range(points):
        angle = 2 * math.pi * i / points
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        if i == 0:
            pen.moveTo((px, py))
        else:
            pen.lineTo((px, py))
    pen.closePath()
    
    # Left ear (floppy)
    ear_width = radius * 0.4
    ear_height = radius * 0.8
    pen.moveTo((cx - radius * 0.7, cy - radius * 0.3))
    pen.qCurveTo((cx - radius - ear_width, cy - radius * 0.2), 
                 (cx - radius - ear_width, cy + ear_height),
                 (cx - radius * 0.5, cy + ear_height * 0.6))
    pen.qCurveTo((cx - radius * 0.3, cy + radius * 0.3), 
                 (cx - radius * 0.4, cy),
                 (cx - radius * 0.7, cy - radius * 0.3))
    pen.closePath()
    
    # Right ear (floppy)
    pen.moveTo((cx + radius * 0.7, cy - radius * 0.3))
    pen.qCurveTo((cx + radius + ear_width, cy - radius * 0.2), 
                 (cx + radius + ear_width, cy + ear_height),
                 (cx + radius * 0.5, cy + ear_height * 0.6))
    pen.qCurveTo((cx + radius * 0.3, cy + radius * 0.3), 
                 (cx + radius * 0.4, cy),
                 (cx + radius * 0.7, cy - radius * 0.3))
    pen.closePath()
    
    # Eyes
    eye_radius = radius * 0.1
    # Left eye
    pen.moveTo((cx - radius * 0.25, cy - radius * 0.1))
    for i in range(12):
        angle = 2 * math.pi * i / 12
        px = cx - radius * 0.25 + eye_radius * math.cos(angle)
        py = cy - radius * 0.1 + eye_radius * math.sin(angle)
        if i == 0:
            pen.moveTo((px, py))
        else:
            pen.lineTo((px, py))
    pen.closePath()
    
    # Right eye
    pen.moveTo((cx + radius * 0.25, cy - radius * 0.1))
    for i in range(12):
        angle = 2 * math.pi * i / 12
        px = cx + radius * 0.25 + eye_radius * math.cos(angle)
        py = cy - radius * 0.1 + eye_radius * math.sin(angle)
        if i == 0:
            pen.moveTo((px, py))
        else:
            pen.lineTo((px, py))
    pen.closePath()
    
    # Nose
    nose_size = radius * 0.15
    pen.moveTo((cx, cy + radius * 0.1))
    pen.lineTo((cx + nose_size, cy + radius * 0.25))
    pen.lineTo((cx - nose_size, cy + radius * 0.25))
    pen.closePath()

def draw_elephant(pen, x, y, width, height):
    """Draw an elephant shape for 'e'"""
    # Draw an elephant head with trunk
    cx, cy = x + width/2, y + height/2
    radius = min(width, height) * 0.3
    
    # Elephant head (oval)
    head_width = radius * 1.5
    head_height = radius * 1.2
    
    # Draw head
    points = 24
    for i in range(points):
        angle = 2 * math.pi * i / points
        px = cx + head_width * math.cos(angle)
        py = cy + head_height * math.sin(angle)
        if i == 0:
            pen.moveTo((px, py))
        else:
            pen.lineTo((px, py))
    pen.closePath()
    
    # Left ear
    ear_width = head_width * 0.8
    ear_height = head_height * 0.9
    pen.moveTo((cx - head_width * 0.7, cy - head_height * 0.2))
    pen.qCurveTo((cx - head_width - ear_width, cy - ear_height), 
                 (cx - head_width - ear_width, cy + ear_height * 0.5),
                 (cx - head_width * 0.5, cy + head_height * 0.2))
    pen.qCurveTo((cx - head_width * 0.3, cy), 
                 (cx - head_width * 0.5, cy - head_height * 0.2),
                 (cx - head_width * 0.7, cy - head_height * 0.2))
    pen.closePath()
    
    # Right ear
    pen.moveTo((cx + head_width * 0.7, cy - head_height * 0.2))
    pen.qCurveTo((cx + head_width + ear_width, cy - ear_height), 
                 (cx + head_width + ear_width, cy + ear_height * 0.5),
                 (cx + head_width * 0.5, cy + head_height * 0.2))
    pen.qCurveTo((cx + head_width * 0.3, cy), 
                 (cx + head_width * 0.5, cy - head_height * 0.2),
                 (cx + head_width * 0.7, cy - head_height * 0.2))
    pen.closePath()
    
    # Trunk
    trunk_width = radius * 0.25
    trunk_length = radius * 1.6
    pen.moveTo((cx - trunk_width, cy + head_height * 0.3))
    pen.qCurveTo((cx - trunk_width * 0.5, cy + head_height * 0.5), 
                 (cx - trunk_width * 2, cy + head_height + trunk_length * 0.5),
                 (cx, cy + head_height + trunk_length))
    pen.qCurveTo((cx + trunk_width * 2, cy + head_height + trunk_length * 0.5), 
                 (cx + trunk_width * 0.5, cy + head_height * 0.5),
                 (cx + trunk_width, cy + head_height * 0.3))
    pen.closePath()
    
    # Eyes
    eye_radius = radius * 0.1
    # Left eye
    pen.moveTo((cx - head_width * 0.3, cy - head_height * 0.2))
    for i in range(12):
        angle = 2 * math.pi * i / 12
        px = cx - head_width * 0.3 + eye_radius * math.cos(angle)
        py = cy - head_height * 0.2 + eye_radius * math.sin(angle)
        if i == 0:
            pen.moveTo((px, py))
        else:
            pen.lineTo((px, py))
    pen.closePath()
    
    # Right eye
    pen.moveTo((cx + head_width * 0.3, cy - head_height * 0.2))
    for i in range(12):
        angle = 2 * math.pi * i / 12
        px = cx + head_width * 0.3 + eye_radius * math.cos(angle)
        py = cy - head_height * 0.2 + eye_radius * math.sin(angle)
        if i == 0:
            pen.moveTo((px, py))
        else:
            pen.lineTo((px, py))
    pen.closePath()

def draw_fish(pen, x, y, width, height):
    """Draw a fish shape for 'f'"""
    cx, cy = x + width/2, y + height/2
    body_length = min(width, height) * 0.6
    body_height = body_length * 0.4
    
    # Fish body (oval)
    points = 24
    for i in range(points):
        angle = 2 * math.pi * i / points
        px = cx + body_length * math.cos(angle)
        py = cy + body_height * math.sin(angle)
        if i == 0:
            pen.moveTo((px, py))
        else:
            pen.lineTo((px, py))
    pen.closePath()
    
    # Tail fin
    tail_width = body_length * 0.4
    tail_height = body_height * 1.5
    pen.moveTo((cx + body_length, cy))
    pen.lineTo((cx + body_length + tail_width, cy - tail_height/2))
    pen.lineTo((cx + body_length + tail_width, cy + tail_height/2))
    pen.closePath()
    
    # Eye
    eye_radius = body_height * 0.2
    pen.moveTo((cx - body_length * 0.5, cy - body_height * 0.3))
    for i in range(12):
        angle = 2 * math.pi * i / 12
        px = cx - body_length * 0.5 + eye_radius * math.cos(angle)
        py = cy - body_height * 0.3 + eye_radius * math.sin(angle)
        if i == 0:
            pen.moveTo((px, py))
        else:
            pen.lineTo((px, py))
    pen.closePath()

def draw_house(pen, x, y, width, height):
    """Draw a house shape for 'h'"""
    cx, cy = x + width/2, y + height/2
    house_width = width * 0.6
    house_height = height * 0.5
    roof_height = height * 0.25
    
    # House body (rectangle)
    pen.moveTo((cx - house_width/2, cy))
    pen.lineTo((cx + house_width/2, cy))
    pen.lineTo((cx + house_width/2, cy + house_height))
    pen.lineTo((cx - house_width/2, cy + house_height))
    pen.closePath()
    
    # Roof (triangle)
    pen.moveTo((cx - house_width/2, cy))
    pen.lineTo((cx, cy - roof_height))
    pen.lineTo((cx + house_width/2, cy))
    pen.closePath()
    
    # Door
    door_width = house_width * 0.25
    door_height = house_height * 0.6
    pen.moveTo((cx - door_width/2, cy + house_height))
    pen.lineTo((cx + door_width/2, cy + house_height))
    pen.lineTo((cx + door_width/2, cy + house_height - door_height))
    pen.lineTo((cx - door_width/2, cy + house_height - door_height))
    pen.closePath()
    
    # Window
    window_size = house_width * 0.15
    pen.moveTo((cx + house_width/4, cy + house_height/4))
    pen.lineTo((cx + house_width/4 + window_size, cy + house_height/4))
    pen.lineTo((cx + house_width/4 + window_size, cy + house_height/4 + window_size))
    pen.lineTo((cx + house_width/4, cy + house_height/4 + window_size))
    pen.closePath()

def draw_umbrella(pen, x, y, width, height):
    """Draw an umbrella for 'u'"""
    cx, cy = x + width/2, y + height/2
    radius = min(width, height) * 0.4
    handle_length = radius * 1.5
    
    # Umbrella canopy (semi-circle)
    points = 13  # Half of a full circle
    for i in range(points):
        angle = math.pi * i / (points-1)
        px = cx + radius * math.cos(angle)
        py = cy - radius * math.sin(angle)  # Flip to make upside-down
        if i == 0:
            pen.moveTo((px, py))
        else:
            pen.lineTo((px, py))
    pen.closePath()
    
    # Handle
    handle_width = radius * 0.05
    pen.moveTo((cx, cy))
    pen.lineTo((cx, cy + handle_length))
    pen.lineTo((cx + handle_width, cy + handle_length))
    pen.lineTo((cx + handle_width, cy))
    pen.closePath()
    
    # Curved handle end
    pen.moveTo((cx, cy + handle_length))
    pen.qCurveTo((cx + handle_width * 3, cy + handle_length), 
                 (cx + handle_width * 4, cy + handle_length - handle_width * 4),
                 (cx + handle_width * 4, cy + handle_length - handle_width * 4))
    pen.lineTo((cx + handle_width * 4 - handle_width, cy + handle_length - handle_width * 4))
    pen.qCurveTo((cx + handle_width * 3 - handle_width, cy + handle_length - handle_width), 
                 (cx, cy + handle_length - handle_width),
                 (cx, cy + handle_length - handle_width))
    pen.closePath()
    
    # Ribs of the umbrella
    for i in range(5):
        angle = math.pi * i / 4
        end_x = cx + radius * math.cos(angle)
        end_y = cy - radius * math.sin(angle)
        pen.moveTo((cx, cy))
        pen.lineTo((end_x, end_y))
        pen.closePath()

def draw_letter_glyphs_to_font(font):
    """Add glyphs to the font for each letter with shapes representing words"""
    # Dictionary mapping letters to drawing functions
    letter_shapes = {
        'a': draw_apple,
        'b': draw_ball,
        'c': draw_cat,
        'd': draw_dog,
        'e': draw_elephant,
        'f': draw_fish,
        'h': draw_house,
        'u': draw_umbrella,
        # Add more shapes here...
    }
    
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
    pen.moveTo((100, 100))
    pen.lineTo((900, 100))
    pen.lineTo((900, 900))
    pen.lineTo((100, 900))
    pen.closePath()
    font['glyf']['.notdef'] = pen.glyph()
    font['hmtx'].metrics['.notdef'] = (FONT_SIZE, 0)
    
    # Add glyphs for each lowercase letter
    for i, letter in enumerate(string.ascii_lowercase):
        unicode_value = ord(letter)
        glyph_name = f"uni{unicode_value:04X}"
        
        # Create a glyph with a letter-specific shape
        pen = TTGlyphPen(glyphSet=font.getGlyphSet())
        
        if letter in letter_shapes:
            # Use a specific drawing function for this letter
            letter_shapes[letter](pen, 100, 100, 800, 800)
        else:
            # For letters without specific shapes, create a generic shape
            # based on the letter position in the alphabet
            pattern_type = (ord(letter) - ord('a')) % 5
            center_x, center_y = FONT_SIZE/2, FONT_SIZE/2
            radius = FONT_SIZE * 0.4
            
            if pattern_type == 0:
                # Draw a square
                pen.moveTo((center_x - radius, center_y - radius))
                pen.lineTo((center_x + radius, center_y - radius))
                pen.lineTo((center_x + radius, center_y + radius))
                pen.lineTo((center_x - radius, center_y + radius))
                pen.closePath()
            elif pattern_type == 1:
                # Draw a triangle
                pen.moveTo((center_x, center_y - radius))
                pen.lineTo((center_x + radius, center_y + radius))
                pen.lineTo((center_x - radius, center_y + radius))
                pen.closePath()
            elif pattern_type == 2:
                # Draw a diamond
                pen.moveTo((center_x, center_y - radius))
                pen.lineTo((center_x + radius, center_y))
                pen.lineTo((center_x, center_y + radius))
                pen.lineTo((center_x - radius, center_y))
                pen.closePath()
            elif pattern_type == 3:
                # Draw a pentagon
                num_points = 5
                for j in range(num_points):
                    angle = 2 * math.pi * j / num_points - math.pi/2
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    if j == 0:
                        pen.moveTo((x, y))
                    else:
                        pen.lineTo((x, y))
                pen.closePath()
            else:
                # Draw a hexagon
                num_points = 6
                for j in range(num_points):
                    angle = 2 * math.pi * j / num_points
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    if j == 0:
                        pen.moveTo((x, y))
                    else:
                        pen.lineTo((x, y))
                pen.closePath()
            
            # Add the letter to make it recognizable
            letter_scale = 0.5
            letter_x = center_x - radius * letter_scale
            letter_y = center_y - radius * letter_scale
            letter_width = radius * letter_scale * 2
            letter_height = radius * letter_scale * 2
            
            # Approximate the letter shape (very simplified)
            if letter == 'g':
                # g - circle with a tail
                circle_radius = letter_width / 2
                pen.moveTo((letter_x + circle_radius, letter_y))
                for j in range(20):
                    angle = 2 * math.pi * j / 20
                    x = letter_x + circle_radius + circle_radius * math.cos(angle)
                    y = letter_y + circle_radius + circle_radius * math.sin(angle)
                    pen.lineTo((x, y))
                pen.closePath()
                
                # Tail
                pen.moveTo((letter_x + circle_radius, letter_y + letter_height))
                pen.lineTo((letter_x + circle_radius, letter_y + letter_height + letter_height * 0.4))
                pen.lineTo((letter_x + letter_width * 0.7, letter_y + letter_height + letter_height * 0.4))
                pen.closePath()
            elif letter == 'i':
                # i - vertical line with a dot
                pen.moveTo((center_x - radius * 0.05, center_y - radius * 0.3))
                pen.lineTo((center_x + radius * 0.05, center_y - radius * 0.3))
                pen.lineTo((center_x + radius * 0.05, center_y + radius * 0.3))
                pen.lineTo((center_x - radius * 0.05, center_y + radius * 0.3))
                pen.closePath()
                
                # Dot
                dot_radius = radius * 0.07
                pen.moveTo((center_x + dot_radius, center_y - radius * 0.4))
                for j in range(12):
                    angle = 2 * math.pi * j / 12
                    x = center_x + dot_radius * math.cos(angle)
                    y = center_y - radius * 0.4 + dot_radius * math.sin(angle)
                    pen.lineTo((x, y))
                pen.closePath()
            elif letter == 'j':
                # j - hook with a dot
                pen.moveTo((center_x, center_y - radius * 0.3))
                pen.qCurveTo((center_x + radius * 0.3, center_y - radius * 0.3),
                            (center_x + radius * 0.3, center_y),
                            (center_x + radius * 0.3, center_y + radius * 0.3))
                pen.qCurveTo((center_x + radius * 0.3, center_y + radius * 0.5),
                            (center_x, center_y + radius * 0.5),
                            (center_x - radius * 0.1, center_y + radius * 0.3))
                pen.closePath()
                
                # Dot
                dot_radius = radius * 0.07
                pen.moveTo((center_x + dot_radius, center_y - radius * 0.4))
                for j in range(12):
                    angle = 2 * math.pi * j / 12
                    x = center_x + dot_radius * math.cos(angle)
                    y = center_y - radius * 0.4 + dot_radius * math.sin(angle)
                    pen.lineTo((x, y))
                pen.closePath()
            elif letter == 'k':
                # k - vertical line with angled lines
                pen.moveTo((center_x - radius * 0.3, center_y - radius * 0.4))
                pen.lineTo((center_x - radius * 0.2, center_y - radius * 0.4))
                pen.lineTo((center_x - radius * 0.2, center_y + radius * 0.4))
                pen.lineTo((center_x - radius * 0.3, center_y + radius * 0.4))
                pen.closePath()
                
                # Diagonal lines
                pen.moveTo((center_x - radius * 0.2, center_y))
                pen.lineTo((center_x + radius * 0.3, center_y - radius * 0.4))
                pen.lineTo((center_x + radius * 0.3 + radius * 0.1, center_y - radius * 0.4 + radius * 0.1))
                pen.lineTo((center_x - radius * 0.2 + radius * 0.1, center_y + radius * 0.1))
                pen.closePath()
                
                pen.moveTo((center_x - radius * 0.2, center_y))
                pen.lineTo((center_x + radius * 0.3, center_y + radius * 0.4))
                pen.lineTo((center_x + radius * 0.3 - radius * 0.1, center_y + radius * 0.4 + radius * 0.1))
                pen.lineTo((center_x - radius * 0.2 - radius * 0.1, center_y + radius * 0.1))
                pen.closePath()
            
            # For other letters, no additional decoration, as they'll be replaced later
            
        font['glyf'][glyph_name] = pen.glyph()
        font['hmtx'].metrics[glyph_name] = (FONT_SIZE, 0)
        
        # Map the Unicode character to this glyph
        for cmap in font['cmap'].tables:
            cmap.cmap[unicode_value] = glyph_name
        
        print(f"Added shape glyph for '{letter}' (Unicode: {unicode_value})")
    
    # Update the font metrics
    font['maxp'].numGlyphs = len(glyph_order)
    font['hhea'].numberOfHMetrics = len(font['hmtx'].metrics)
    
    return font

def main():
    print("Creating a phonics font with letter-specific shapes...")
    
    # Create a basic font
    font = create_empty_font()
    
    # Add glyphs for each letter
    font = draw_letter_glyphs_to_font(font)
    
    # Save the font
    try:
        font.save(OUTPUT_FILE)
        print(f"Font saved to {OUTPUT_FILE}")
        print("You can now install this font on your Mac by:")
        print("1. Double-clicking the font file")
        print("2. Clicking 'Install Font' in the Font Book app")
        print("\nThis font contains shapes representing words for each letter.")
        print("Some examples:")
        print("a - apple shape")
        print("b - ball shape")
        print("c - cat shape")
        print("d - dog shape")
        print("e - elephant shape")
        print("f - fish shape")
        print("h - house shape")
        print("u - umbrella shape")
        print("\nMore letter shapes can be added in the future.")
    except Exception as e:
        print(f"Error saving font: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()