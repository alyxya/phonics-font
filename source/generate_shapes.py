#!/usr/bin/env python3
import os
import string
import math
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables import _c_m_a_p
from fontTools.ttLib.tables.O_S_2f_2 import Panose

class FlippedPen:
    """A pen wrapper that flips y-coordinates vertically"""
    def __init__(self, pen, font_size=1000):
        self.pen = pen
        self.font_size = font_size
    
    def flip_y(self, y):
        """Flip y-coordinate around the center of the font"""
        return self.font_size - y
    
    def moveTo(self, pt):
        x, y = pt
        self.pen.moveTo((x, self.flip_y(y)))
    
    def lineTo(self, pt):
        x, y = pt
        self.pen.lineTo((x, self.flip_y(y)))
    
    def closePath(self):
        self.pen.closePath()
    
    def glyph(self):
        return self.pen.glyph()

# Configuration
FONT_NAME = "Phonics"
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
    font['maxp'].maxPoints = 500  # Set reasonable defaults
    font['maxp'].maxContours = 50
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

def draw_apple(pen):
    """Draw an apple shape for 'a'"""
    # Apple shape
    radius = 400
    cx, cy = 500, 500
    
    # Main apple body (circle)
    pen.moveTo((cx, cy - radius))
    
    # Create a circle approximation using line segments
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        pen.lineTo((x, y))
    
    pen.closePath()
    
    # Stem
    stem_width = 50
    stem_height = 150
    pen.moveTo((cx - stem_width/2, cy - radius))
    pen.lineTo((cx - stem_width/2, cy - radius - stem_height))
    pen.lineTo((cx + stem_width/2, cy - radius - stem_height))
    pen.lineTo((cx + stem_width/2, cy - radius))
    pen.closePath()
    
    # Leaf (simplified)
    pen.moveTo((cx + stem_width, cy - radius - stem_height/2))
    pen.lineTo((cx + stem_width + 150, cy - radius - stem_height))
    pen.lineTo((cx + stem_width + 150, cy - radius - stem_height/3))
    pen.lineTo((cx + stem_width, cy - radius))
    pen.closePath()

def draw_ball(pen):
    """Draw a ball shape for 'b'"""
    # Ball (circle with lines)
    radius = 400
    cx, cy = 500, 500
    
    # Main ball (circle)
    pen.moveTo((cx + radius, cy))
    
    # Create a circle approximation using line segments
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        pen.lineTo((x, y))
    
    pen.closePath()
    
    # Horizontal curve line
    pen.moveTo((cx - radius/2, cy))
    pen.lineTo((cx + radius/2, cy))
    pen.closePath()
    
    # Vertical curve line
    pen.moveTo((cx, cy - radius/2))
    pen.lineTo((cx, cy + radius/2))
    pen.closePath()
    
    # Diagonal line 1
    pen.moveTo((cx - radius/3, cy - radius/3))
    pen.lineTo((cx + radius/3, cy + radius/3))
    pen.closePath()
    
    # Diagonal line 2
    pen.moveTo((cx - radius/3, cy + radius/3))
    pen.lineTo((cx + radius/3, cy - radius/3))
    pen.closePath()

def draw_cat(pen):
    """Draw a cat shape for 'c'"""
    # Cat face with ears
    radius = 350
    cx, cy = 500, 500
    
    # Cat face (circle)
    pen.moveTo((cx + radius, cy))
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Left ear (triangle)
    ear_size = 200
    pen.moveTo((cx - radius/2, cy - radius/2))
    pen.lineTo((cx - radius - ear_size/2, cy - radius - ear_size))
    pen.lineTo((cx, cy - radius))
    pen.closePath()
    
    # Right ear (triangle)
    pen.moveTo((cx + radius/2, cy - radius/2))
    pen.lineTo((cx + radius + ear_size/2, cy - radius - ear_size))
    pen.lineTo((cx, cy - radius))
    pen.closePath()
    
    # Left eye
    eye_size = 80
    pen.moveTo((cx - radius/3, cy - radius/5))
    pen.lineTo((cx - radius/3 - eye_size, cy - radius/5))
    pen.lineTo((cx - radius/3 - eye_size, cy - radius/5 - eye_size))
    pen.lineTo((cx - radius/3, cy - radius/5 - eye_size))
    pen.closePath()
    
    # Right eye
    pen.moveTo((cx + radius/3, cy - radius/5))
    pen.lineTo((cx + radius/3 + eye_size, cy - radius/5))
    pen.lineTo((cx + radius/3 + eye_size, cy - radius/5 - eye_size))
    pen.lineTo((cx + radius/3, cy - radius/5 - eye_size))
    pen.closePath()
    
    # Nose (triangle)
    nose_size = 60
    pen.moveTo((cx, cy + radius/5))
    pen.lineTo((cx - nose_size, cy + radius/5 + nose_size))
    pen.lineTo((cx + nose_size, cy + radius/5 + nose_size))
    pen.closePath()
    
    # Mouth (simplified whiskers)
    whisker_length = 150
    pen.moveTo((cx - nose_size, cy + radius/5 + nose_size))
    pen.lineTo((cx - nose_size - whisker_length, cy + radius/5 + 1.5*nose_size))
    pen.closePath()
    
    pen.moveTo((cx + nose_size, cy + radius/5 + nose_size))
    pen.lineTo((cx + nose_size + whisker_length, cy + radius/5 + 1.5*nose_size))
    pen.closePath()

def draw_dog(pen):
    """Draw a dog shape for 'd'"""
    # Dog head with floppy ears
    radius = 350
    cx, cy = 500, 500
    
    # Dog face (circle)
    pen.moveTo((cx + radius, cy))
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Left ear (floppy)
    ear_width = 200
    ear_height = 350
    pen.moveTo((cx - radius/2, cy - radius/2))
    pen.lineTo((cx - radius - ear_width, cy - radius/2))
    pen.lineTo((cx - radius - ear_width, cy))
    pen.lineTo((cx - radius, cy + ear_height/2))
    pen.lineTo((cx - radius/2, cy))
    pen.closePath()
    
    # Right ear (floppy)
    pen.moveTo((cx + radius/2, cy - radius/2))
    pen.lineTo((cx + radius + ear_width, cy - radius/2))
    pen.lineTo((cx + radius + ear_width, cy))
    pen.lineTo((cx + radius, cy + ear_height/2))
    pen.lineTo((cx + radius/2, cy))
    pen.closePath()
    
    # Left eye (oval)
    eye_radius = 60
    pen.moveTo((cx - radius/3 + eye_radius, cy - radius/4))
    segments = 16
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx - radius/3 + eye_radius * math.cos(angle)
        y = cy - radius/4 + eye_radius * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Right eye (oval)
    pen.moveTo((cx + radius/3 + eye_radius, cy - radius/4))
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + radius/3 + eye_radius * math.cos(angle)
        y = cy - radius/4 + eye_radius * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Nose (rounded rectangle)
    nose_width = 150
    nose_height = 100
    pen.moveTo((cx - nose_width/2, cy + radius/4))
    pen.lineTo((cx + nose_width/2, cy + radius/4))
    pen.lineTo((cx + nose_width/2, cy + radius/4 + nose_height))
    pen.lineTo((cx - nose_width/2, cy + radius/4 + nose_height))
    pen.closePath()

def draw_elephant(pen):
    """Draw an elephant shape for 'e'"""
    # Elephant head with trunk
    head_radius = 300
    cx, cy = 500, 500
    
    # Elephant head (circle)
    pen.moveTo((cx + head_radius, cy))
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + head_radius * math.cos(angle)
        y = cy + head_radius * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Left ear (large semicircle)
    ear_radius = 250
    pen.moveTo((cx - head_radius, cy))
    for i in range(0, 13):  # Half circle
        angle = math.pi * i / 12
        x = cx - head_radius + ear_radius * math.cos(angle + math.pi/2)
        y = cy + ear_radius * math.sin(angle + math.pi/2)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Right ear (large semicircle)
    pen.moveTo((cx + head_radius, cy))
    for i in range(0, 13):  # Half circle
        angle = math.pi * i / 12
        x = cx + head_radius + ear_radius * math.cos(angle - math.pi/2)
        y = cy + ear_radius * math.sin(angle - math.pi/2)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Trunk
    trunk_width = 100
    trunk_length = 450
    pen.moveTo((cx - trunk_width/2, cy + head_radius/2))
    pen.lineTo((cx + trunk_width/2, cy + head_radius/2))
    pen.lineTo((cx + trunk_width/2, cy + head_radius + trunk_length))
    pen.lineTo((cx - trunk_width/2, cy + head_radius + trunk_length))
    pen.closePath()
    
    # Eyes
    eye_size = 50
    pen.moveTo((cx - head_radius/3, cy - head_radius/3))
    pen.lineTo((cx - head_radius/3 + eye_size, cy - head_radius/3))
    pen.lineTo((cx - head_radius/3 + eye_size, cy - head_radius/3 + eye_size))
    pen.lineTo((cx - head_radius/3, cy - head_radius/3 + eye_size))
    pen.closePath()
    
    pen.moveTo((cx + head_radius/3, cy - head_radius/3))
    pen.lineTo((cx + head_radius/3 + eye_size, cy - head_radius/3))
    pen.lineTo((cx + head_radius/3 + eye_size, cy - head_radius/3 + eye_size))
    pen.lineTo((cx + head_radius/3, cy - head_radius/3 + eye_size))
    pen.closePath()

def draw_fish(pen):
    """Draw a fish shape for 'f'"""
    # Fish (oval with tail)
    body_width = 400
    body_height = 250
    cx, cy = 450, 500
    
    # Fish body (oval)
    pen.moveTo((cx + body_width/2, cy))
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + body_width/2 * math.cos(angle)
        y = cy + body_height/2 * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Tail fin (triangle)
    tail_size = 200
    pen.moveTo((cx + body_width/2, cy - body_height/4))
    pen.lineTo((cx + body_width/2 + tail_size, cy - body_height))
    pen.lineTo((cx + body_width/2 + tail_size, cy + body_height))
    pen.lineTo((cx + body_width/2, cy + body_height/4))
    pen.closePath()
    
    # Eye
    eye_size = 40
    pen.moveTo((cx - body_width/4, cy - body_height/4))
    pen.lineTo((cx - body_width/4 + eye_size, cy - body_height/4))
    pen.lineTo((cx - body_width/4 + eye_size, cy - body_height/4 + eye_size))
    pen.lineTo((cx - body_width/4, cy - body_height/4 + eye_size))
    pen.closePath()
    
    # Dorsal fin
    fin_width = 100
    fin_height = 120
    pen.moveTo((cx, cy - body_height/2))
    pen.lineTo((cx + fin_width, cy - body_height/2 - fin_height))
    pen.lineTo((cx - fin_width, cy - body_height/2 - fin_height))
    pen.closePath()

def draw_giraffe(pen):
    """Draw a giraffe shape for 'g'"""
    # Giraffe (long neck and head)
    cx, cy = 500, 500
    head_size = 150
    neck_width = 100
    neck_length = 400
    
    # Giraffe head (oval)
    pen.moveTo((cx + head_size/2, cy - neck_length))
    segments = 16
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + head_size/2 * math.cos(angle)
        y = cy - neck_length + head_size/1.5 * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Neck
    pen.moveTo((cx - neck_width/2, cy))
    pen.lineTo((cx + neck_width/2, cy))
    pen.lineTo((cx + neck_width/2, cy - neck_length + head_size/2))
    pen.lineTo((cx - neck_width/2, cy - neck_length + head_size/2))
    pen.closePath()
    
    # Ears
    ear_size = 40
    pen.moveTo((cx - head_size/2, cy - neck_length))
    pen.lineTo((cx - head_size/2 - ear_size, cy - neck_length - ear_size))
    pen.lineTo((cx - head_size/2, cy - neck_length - ear_size))
    pen.closePath()
    
    pen.moveTo((cx + head_size/2, cy - neck_length))
    pen.lineTo((cx + head_size/2 + ear_size, cy - neck_length - ear_size))
    pen.lineTo((cx + head_size/2, cy - neck_length - ear_size))
    pen.closePath()
    
    # Eye
    eye_size = 20
    pen.moveTo((cx - head_size/4, cy - neck_length - head_size/4))
    pen.lineTo((cx - head_size/4 + eye_size, cy - neck_length - head_size/4))
    pen.lineTo((cx - head_size/4 + eye_size, cy - neck_length - head_size/4 + eye_size))
    pen.lineTo((cx - head_size/4, cy - neck_length - head_size/4 + eye_size))
    pen.closePath()
    
    # Giraffe spots (several circles)
    spot_size = 50
    for i in range(5):
        x = cx - neck_width/4 + (i % 2) * neck_width/2
        y = cy - i * neck_length/5 - neck_length/10
        pen.moveTo((x + spot_size/2, y))
        for j in range(1, 9):
            angle = 2 * math.pi * j / 8
            px = x + spot_size/2 * math.cos(angle)
            py = y + spot_size/2 * math.sin(angle)
            pen.lineTo((px, py))
        pen.closePath()

def draw_house(pen):
    """Draw a house shape for 'h'"""
    # House (square with triangular roof)
    cx, cy = 500, 500
    house_width = 600
    house_height = 400
    roof_height = 250
    
    # House body (square)
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
    door_width = 150
    door_height = 250
    pen.moveTo((cx - door_width/2, cy + house_height))
    pen.lineTo((cx + door_width/2, cy + house_height))
    pen.lineTo((cx + door_width/2, cy + house_height - door_height))
    pen.lineTo((cx - door_width/2, cy + house_height - door_height))
    pen.closePath()
    
    # Window (left)
    window_size = 120
    pen.moveTo((cx - house_width/4 - window_size/2, cy + house_height/3))
    pen.lineTo((cx - house_width/4 + window_size/2, cy + house_height/3))
    pen.lineTo((cx - house_width/4 + window_size/2, cy + house_height/3 + window_size))
    pen.lineTo((cx - house_width/4 - window_size/2, cy + house_height/3 + window_size))
    pen.closePath()
    
    # Window (right)
    pen.moveTo((cx + house_width/4 - window_size/2, cy + house_height/3))
    pen.lineTo((cx + house_width/4 + window_size/2, cy + house_height/3))
    pen.lineTo((cx + house_width/4 + window_size/2, cy + house_height/3 + window_size))
    pen.lineTo((cx + house_width/4 - window_size/2, cy + house_height/3 + window_size))
    pen.closePath()

def draw_igloo(pen):
    """Draw an igloo shape for 'i'"""
    # Igloo (dome with entrance)
    cx, cy = 500, 500
    width = 600
    height = 350
    entrance_width = 200
    entrance_height = 150
    
    # Main dome (half circle)
    pen.moveTo((cx - width/2, cy))
    for i in range(0, 13):  # Half circle
        angle = math.pi * i / 12
        x = cx + width/2 * math.cos(angle + math.pi)
        y = cy + height * math.sin(angle + math.pi)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Snow blocks (horizontal lines)
    block_height = 50
    for y_pos in range(int(cy), int(cy - height), -int(block_height)):
        pen.moveTo((cx - width/2, y_pos))
        pen.lineTo((cx + width/2, y_pos))
        pen.closePath()
    
    # Entrance cutout
    pen.moveTo((cx - entrance_width/2, cy))
    pen.lineTo((cx + entrance_width/2, cy))
    pen.lineTo((cx + entrance_width/2, cy - entrance_height))
    pen.lineTo((cx - entrance_width/2, cy - entrance_height))
    pen.closePath()
    
    # Dot above (typical for letter 'i')
    dot_size = 80
    pen.moveTo((cx - dot_size/2, cy - height - 100))
    pen.lineTo((cx + dot_size/2, cy - height - 100))
    pen.lineTo((cx + dot_size/2, cy - height - 100 - dot_size))
    pen.lineTo((cx - dot_size/2, cy - height - 100 - dot_size))
    pen.closePath()

def draw_jellyfish(pen):
    """Draw a jellyfish shape for 'j'"""
    # Jellyfish (bell with tentacles)
    cx, cy = 500, 400
    bell_width = 300
    bell_height = 250
    tentacle_length = 400
    
    # Bell (half-circle)
    pen.moveTo((cx - bell_width/2, cy))
    for i in range(0, 13):  # Half circle
        angle = math.pi * i / 12
        x = cx + bell_width/2 * math.cos(angle + math.pi)
        y = cy + bell_height * math.sin(angle + math.pi)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Tentacles (multiple lines)
    num_tentacles = 7
    for i in range(num_tentacles):
        offset = bell_width * (i / (num_tentacles - 1) - 0.5)
        
        # Add some variation to tentacle length
        variation = 0.8 + 0.4 * (i % 3) / 2
        
        # Wavy tentacle
        pen.moveTo((cx + offset, cy))
        
        # Create a wavy line
        wave_width = 30
        segments = 6
        for j in range(1, segments + 1):
            # Alternate left and right for wave effect
            x_offset = wave_width * (-1 if j % 2 == 0 else 1)
            y_pos = cy + j * (tentacle_length * variation) / segments
            pen.lineTo((cx + offset + x_offset, y_pos))
        
        pen.closePath()
    
    # Dot above (typical for letter 'j')
    dot_size = 80
    pen.moveTo((cx - dot_size/2, cy - bell_height - 100))
    pen.lineTo((cx + dot_size/2, cy - bell_height - 100))
    pen.lineTo((cx + dot_size/2, cy - bell_height - 100 - dot_size))
    pen.lineTo((cx - dot_size/2, cy - bell_height - 100 - dot_size))
    pen.closePath()

def draw_kite(pen):
    """Draw a kite shape for 'k'"""
    # Kite (diamond with tail)
    cx, cy = 500, 400
    kite_width = 400
    kite_height = 600
    tail_length = 350
    
    # Kite body (diamond)
    pen.moveTo((cx, cy - kite_height/2))
    pen.lineTo((cx + kite_width/2, cy))
    pen.lineTo((cx, cy + kite_height/2))
    pen.lineTo((cx - kite_width/2, cy))
    pen.closePath()
    
    # Kite cross-spars
    pen.moveTo((cx - kite_width/2, cy))
    pen.lineTo((cx + kite_width/2, cy))
    pen.closePath()
    
    pen.moveTo((cx, cy - kite_height/2))
    pen.lineTo((cx, cy + kite_height/2))
    pen.closePath()
    
    # Kite tail (zigzag)
    tail_segments = 3
    segment_length = tail_length / tail_segments
    zig_width = 50
    
    pen.moveTo((cx, cy + kite_height/2))
    for i in range(1, tail_segments + 1):
        # Zigzag left and right
        x_offset = zig_width * (-1 if i % 2 == 0 else 1)
        y_pos = cy + kite_height/2 + i * segment_length
        pen.lineTo((cx + x_offset, y_pos))
    
    pen.closePath()
    
    # Kite string
    pen.moveTo((cx, cy - kite_height/2))
    pen.lineTo((cx - kite_width/2 - 100, cy + kite_height/2 + tail_length))
    pen.closePath()

def draw_lion(pen):
    """Draw a lion shape for 'l'"""
    # Lion (head with mane)
    cx, cy = 500, 500
    head_radius = 300
    mane_size = 150
    
    # Lion head (circle)
    pen.moveTo((cx + head_radius, cy))
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + head_radius * math.cos(angle)
        y = cy + head_radius * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Mane (spiky circle around head)
    mane_spikes = 16
    for i in range(mane_spikes):
        angle = 2 * math.pi * i / mane_spikes
        inner_x = cx + head_radius * math.cos(angle)
        inner_y = cy + head_radius * math.sin(angle)
        outer_x = cx + (head_radius + mane_size) * math.cos(angle)
        outer_y = cy + (head_radius + mane_size) * math.sin(angle)
        
        pen.moveTo((inner_x, inner_y))
        pen.lineTo((outer_x, outer_y))
        pen.closePath()
    
    # Eyes
    eye_size = 60
    pen.moveTo((cx - head_radius/3, cy - head_radius/5))
    pen.lineTo((cx - head_radius/3 - eye_size, cy - head_radius/5))
    pen.lineTo((cx - head_radius/3 - eye_size, cy - head_radius/5 - eye_size))
    pen.lineTo((cx - head_radius/3, cy - head_radius/5 - eye_size))
    pen.closePath()
    
    pen.moveTo((cx + head_radius/3, cy - head_radius/5))
    pen.lineTo((cx + head_radius/3 + eye_size, cy - head_radius/5))
    pen.lineTo((cx + head_radius/3 + eye_size, cy - head_radius/5 - eye_size))
    pen.lineTo((cx + head_radius/3, cy - head_radius/5 - eye_size))
    pen.closePath()
    
    # Nose (triangle)
    nose_size = 50
    pen.moveTo((cx, cy + head_radius/5))
    pen.lineTo((cx - nose_size, cy + head_radius/5 + nose_size))
    pen.lineTo((cx + nose_size, cy + head_radius/5 + nose_size))
    pen.closePath()
    
    # Mouth (curved line)
    pen.moveTo((cx - nose_size, cy + head_radius/5 + nose_size))
    pen.lineTo((cx, cy + head_radius/5 + nose_size*2))
    pen.lineTo((cx + nose_size, cy + head_radius/5 + nose_size))
    pen.closePath()

def draw_monkey(pen):
    """Draw a monkey shape for 'm'"""
    # Monkey (head with ears)
    cx, cy = 500, 500
    head_radius = 300
    ear_size = 150
    
    # Monkey head (circle)
    pen.moveTo((cx + head_radius, cy))
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + head_radius * math.cos(angle)
        y = cy + head_radius * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Left ear (circle)
    ear_cx = cx - head_radius * 0.7
    ear_cy = cy - head_radius * 0.7
    pen.moveTo((ear_cx + ear_size, ear_cy))
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = ear_cx + ear_size * math.cos(angle)
        y = ear_cy + ear_size * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Right ear (circle)
    ear_cx = cx + head_radius * 0.7
    ear_cy = cy - head_radius * 0.7
    pen.moveTo((ear_cx + ear_size, ear_cy))
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = ear_cx + ear_size * math.cos(angle)
        y = ear_cy + ear_size * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Eyes
    eye_size = 60
    pen.moveTo((cx - head_radius/3, cy - head_radius/5))
    pen.lineTo((cx - head_radius/3 - eye_size, cy - head_radius/5))
    pen.lineTo((cx - head_radius/3 - eye_size, cy - head_radius/5 - eye_size))
    pen.lineTo((cx - head_radius/3, cy - head_radius/5 - eye_size))
    pen.closePath()
    
    pen.moveTo((cx + head_radius/3, cy - head_radius/5))
    pen.lineTo((cx + head_radius/3 + eye_size, cy - head_radius/5))
    pen.lineTo((cx + head_radius/3 + eye_size, cy - head_radius/5 - eye_size))
    pen.lineTo((cx + head_radius/3, cy - head_radius/5 - eye_size))
    pen.closePath()
    
    # Nose (oval)
    nose_width = 100
    nose_height = 70
    pen.moveTo((cx, cy + head_radius/5))
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + nose_width/2 * math.cos(angle)
        y = cy + head_radius/5 + nose_height/2 * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Mouth (curved line)
    mouth_width = 200
    pen.moveTo((cx - mouth_width/2, cy + head_radius/3))
    pen.lineTo((cx, cy + head_radius/2))
    pen.lineTo((cx + mouth_width/2, cy + head_radius/3))
    pen.closePath()

def draw_nest(pen):
    """Draw a nest shape for 'n'"""
    # Nest (bowl with eggs)
    cx, cy = 500, 500
    nest_width = 500
    nest_height = 200
    
    # Nest base (half-ellipse)
    pen.moveTo((cx - nest_width/2, cy))
    segments = 12
    for i in range(0, segments + 1):
        angle = math.pi * i / segments
        x = cx + nest_width/2 * math.cos(angle + math.pi)
        y = cy + nest_height * math.sin(angle + math.pi)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Nest texture (twigs)
    num_twigs = 20
    twig_length = 80
    
    for i in range(num_twigs):
        angle = math.pi * (i / num_twigs + 0.5)
        start_x = cx + (nest_width/2 - 20) * math.cos(angle + math.pi)
        start_y = cy + (nest_height - 20) * math.sin(angle + math.pi)
        
        # Twig direction varies slightly
        end_angle = angle + (0.1 * (i % 3 - 1))
        end_x = start_x + twig_length * math.cos(end_angle)
        end_y = start_y + twig_length * math.sin(end_angle)
        
        pen.moveTo((start_x, start_y))
        pen.lineTo((end_x, end_y))
        pen.closePath()
    
    # Eggs in nest (3 small ovals)
    egg_size = 70
    egg_positions = [
        (cx - egg_size, cy - egg_size/2),
        (cx, cy - egg_size),
        (cx + egg_size, cy - egg_size/2)
    ]
    
    for egg_cx, egg_cy in egg_positions:
        pen.moveTo((egg_cx + egg_size/2, egg_cy))
        segments = 16
        for i in range(1, segments + 1):
            angle = 2 * math.pi * i / segments
            x = egg_cx + egg_size/2 * math.cos(angle)
            y = egg_cy + egg_size/1.5 * math.sin(angle)
            pen.lineTo((x, y))
        pen.closePath()

def draw_octopus(pen):
    """Draw an octopus shape for 'o'"""
    # Octopus (head with tentacles)
    cx, cy = 500, 400
    head_radius = 250
    tentacle_length = 400
    
    # Octopus head (circle)
    pen.moveTo((cx + head_radius, cy))
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + head_radius * math.cos(angle)
        y = cy + head_radius * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Eyes
    eye_size = 60
    eye_distance = 100
    
    # Left eye
    pen.moveTo((cx - eye_distance/2, cy - head_radius/4))
    pen.lineTo((cx - eye_distance/2 - eye_size, cy - head_radius/4))
    pen.lineTo((cx - eye_distance/2 - eye_size, cy - head_radius/4 - eye_size))
    pen.lineTo((cx - eye_distance/2, cy - head_radius/4 - eye_size))
    pen.closePath()
    
    # Right eye
    pen.moveTo((cx + eye_distance/2, cy - head_radius/4))
    pen.lineTo((cx + eye_distance/2 + eye_size, cy - head_radius/4))
    pen.lineTo((cx + eye_distance/2 + eye_size, cy - head_radius/4 - eye_size))
    pen.lineTo((cx + eye_distance/2, cy - head_radius/4 - eye_size))
    pen.closePath()
    
    # Tentacles (8 wavy lines)
    num_tentacles = 8
    for i in range(num_tentacles):
        angle = 2 * math.pi * i / num_tentacles + math.pi/num_tentacles
        start_x = cx + head_radius * math.cos(angle)
        start_y = cy + head_radius * math.sin(angle)
        
        # Create wavy tentacle
        pen.moveTo((start_x, start_y))
        
        # Wavy line with 4 segments
        prev_x, prev_y = start_x, start_y
        for j in range(1, 5):
            # Calculate segment end
            segment_length = tentacle_length / 4
            direct_x = start_x + tentacle_length * math.cos(angle)
            direct_y = start_y + tentacle_length * math.sin(angle)
            
            # Add some wave effect perpendicular to tentacle direction
            perp_angle = angle + math.pi/2
            wave_size = 50 * (-1 if j % 2 == 0 else 1)
            
            segment_x = start_x + (j * segment_length * math.cos(angle)) + (wave_size * math.cos(perp_angle))
            segment_y = start_y + (j * segment_length * math.sin(angle)) + (wave_size * math.sin(perp_angle))
            
            pen.lineTo((segment_x, segment_y))
        
        pen.closePath()

def draw_penguin(pen):
    """Draw a penguin shape for 'p'"""
    # Penguin (body with head)
    cx, cy = 500, 500
    body_width = 300
    body_height = 500
    head_size = 200
    
    # Body (oval)
    pen.moveTo((cx, cy - body_height/2))
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + body_width/2 * math.cos(angle)
        y = cy + body_height/2 * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # White belly (partial oval)
    belly_width = body_width * 0.7
    belly_height = body_height * 0.6
    pen.moveTo((cx - belly_width/2, cy))
    pen.lineTo((cx + belly_width/2, cy))
    
    for i in range(1, segments//2 + 1):
        angle = math.pi * i / (segments//2)
        x = cx + belly_width/2 * math.cos(angle)
        y = cy + belly_height/2 * math.sin(angle)
        pen.lineTo((x, y))
    
    pen.closePath()
    
    # Head (circle on top of body)
    head_cx = cx
    head_cy = cy - body_height/2 - head_size/2
    
    pen.moveTo((head_cx + head_size/2, head_cy))
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = head_cx + head_size/2 * math.cos(angle)
        y = head_cy + head_size/2 * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Eyes
    eye_size = 30
    eye_distance = 70
    
    # Left eye
    pen.moveTo((head_cx - eye_distance/2, head_cy - head_size/6))
    pen.lineTo((head_cx - eye_distance/2 - eye_size, head_cy - head_size/6))
    pen.lineTo((head_cx - eye_distance/2 - eye_size, head_cy - head_size/6 - eye_size))
    pen.lineTo((head_cx - eye_distance/2, head_cy - head_size/6 - eye_size))
    pen.closePath()
    
    # Right eye
    pen.moveTo((head_cx + eye_distance/2, head_cy - head_size/6))
    pen.lineTo((head_cx + eye_distance/2 + eye_size, head_cy - head_size/6))
    pen.lineTo((head_cx + eye_distance/2 + eye_size, head_cy - head_size/6 - eye_size))
    pen.lineTo((head_cx + eye_distance/2, head_cy - head_size/6 - eye_size))
    pen.closePath()
    
    # Beak (triangle)
    beak_size = 50
    pen.moveTo((head_cx, head_cy))
    pen.lineTo((head_cx - beak_size, head_cy + beak_size))
    pen.lineTo((head_cx + beak_size, head_cy + beak_size))
    pen.closePath()
    
    # Feet (small triangles at bottom)
    feet_width = 80
    feet_height = 40
    
    # Left foot
    pen.moveTo((cx - body_width/4, cy + body_height/2))
    pen.lineTo((cx - body_width/4 - feet_width/2, cy + body_height/2 + feet_height))
    pen.lineTo((cx - body_width/4 + feet_width/2, cy + body_height/2 + feet_height))
    pen.closePath()
    
    # Right foot
    pen.moveTo((cx + body_width/4, cy + body_height/2))
    pen.lineTo((cx + body_width/4 - feet_width/2, cy + body_height/2 + feet_height))
    pen.lineTo((cx + body_width/4 + feet_width/2, cy + body_height/2 + feet_height))
    pen.closePath()

def draw_queen(pen):
    """Draw a queen shape for 'q'"""
    # Queen (crown with face)
    cx, cy = 500, 500
    crown_width = 400
    crown_height = 300
    face_radius = 250
    
    # Crown base (rectangle)
    pen.moveTo((cx - crown_width/2, cy - crown_height))
    pen.lineTo((cx + crown_width/2, cy - crown_height))
    pen.lineTo((cx + crown_width/2, cy))
    pen.lineTo((cx - crown_width/2, cy))
    pen.closePath()
    
    # Crown points (triangles)
    num_points = 5
    point_height = 150
    
    for i in range(num_points):
        point_x = cx - crown_width/2 + crown_width * i / (num_points - 1)
        
        pen.moveTo((point_x, cy - crown_height))
        pen.lineTo((point_x - crown_width/num_points/2, cy - crown_height - point_height))
        pen.lineTo((point_x + crown_width/num_points/2, cy - crown_height - point_height))
        pen.closePath()
    
    # Face (circle)
    pen.moveTo((cx + face_radius, cy + face_radius))
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + face_radius * math.cos(angle)
        y = cy + face_radius * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Eyes
    eye_size = 60
    eye_distance = 120
    
    # Left eye
    pen.moveTo((cx - eye_distance/2, cy + face_radius/3))
    pen.lineTo((cx - eye_distance/2 - eye_size, cy + face_radius/3))
    pen.lineTo((cx - eye_distance/2 - eye_size, cy + face_radius/3 - eye_size))
    pen.lineTo((cx - eye_distance/2, cy + face_radius/3 - eye_size))
    pen.closePath()
    
    # Right eye
    pen.moveTo((cx + eye_distance/2, cy + face_radius/3))
    pen.lineTo((cx + eye_distance/2 + eye_size, cy + face_radius/3))
    pen.lineTo((cx + eye_distance/2 + eye_size, cy + face_radius/3 - eye_size))
    pen.lineTo((cx + eye_distance/2, cy + face_radius/3 - eye_size))
    pen.closePath()
    
    # Smile (curved line)
    smile_width = 200
    pen.moveTo((cx - smile_width/2, cy + face_radius/2))
    pen.lineTo((cx, cy + face_radius/2 + 50))
    pen.lineTo((cx + smile_width/2, cy + face_radius/2))
    pen.closePath()

def draw_rabbit(pen):
    """Draw a rabbit shape for 'r'"""
    # Rabbit (head with long ears)
    cx, cy = 500, 550
    head_radius = 250
    ear_width = 100
    ear_height = 400
    
    # Rabbit head (circle)
    pen.moveTo((cx + head_radius, cy))
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + head_radius * math.cos(angle)
        y = cy + head_radius * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Left ear
    pen.moveTo((cx - head_radius/3, cy - head_radius/2))
    pen.lineTo((cx - head_radius/3 - ear_width/2, cy - head_radius - ear_height))
    pen.lineTo((cx - head_radius/3 + ear_width/2, cy - head_radius - ear_height))
    pen.lineTo((cx - head_radius/3, cy - head_radius/2))
    pen.closePath()
    
    # Right ear
    pen.moveTo((cx + head_radius/3, cy - head_radius/2))
    pen.lineTo((cx + head_radius/3 - ear_width/2, cy - head_radius - ear_height))
    pen.lineTo((cx + head_radius/3 + ear_width/2, cy - head_radius - ear_height))
    pen.lineTo((cx + head_radius/3, cy - head_radius/2))
    pen.closePath()
    
    # Eyes
    eye_size = 50
    eye_distance = 120
    
    # Left eye
    pen.moveTo((cx - eye_distance/2, cy - head_radius/5))
    pen.lineTo((cx - eye_distance/2 - eye_size, cy - head_radius/5))
    pen.lineTo((cx - eye_distance/2 - eye_size, cy - head_radius/5 - eye_size))
    pen.lineTo((cx - eye_distance/2, cy - head_radius/5 - eye_size))
    pen.closePath()
    
    # Right eye
    pen.moveTo((cx + eye_distance/2, cy - head_radius/5))
    pen.lineTo((cx + eye_distance/2 + eye_size, cy - head_radius/5))
    pen.lineTo((cx + eye_distance/2 + eye_size, cy - head_radius/5 - eye_size))
    pen.lineTo((cx + eye_distance/2, cy - head_radius/5 - eye_size))
    pen.closePath()
    
    # Nose (small circle)
    nose_size = 40
    pen.moveTo((cx + nose_size, cy))
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + nose_size * math.cos(angle)
        y = cy + nose_size * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Mouth (three lines forming whiskers)
    whisker_length = 120
    
    # Middle line
    pen.moveTo((cx, cy + nose_size))
    pen.lineTo((cx, cy + nose_size + 40))
    pen.closePath()
    
    # Left whiskers
    pen.moveTo((cx - nose_size, cy + nose_size/2))
    pen.lineTo((cx - nose_size - whisker_length, cy + nose_size/2 - 20))
    pen.closePath()
    
    pen.moveTo((cx - nose_size, cy + nose_size/2))
    pen.lineTo((cx - nose_size - whisker_length, cy + nose_size/2 + 20))
    pen.closePath()
    
    # Right whiskers
    pen.moveTo((cx + nose_size, cy + nose_size/2))
    pen.lineTo((cx + nose_size + whisker_length, cy + nose_size/2 - 20))
    pen.closePath()
    
    pen.moveTo((cx + nose_size, cy + nose_size/2))
    pen.lineTo((cx + nose_size + whisker_length, cy + nose_size/2 + 20))
    pen.closePath()

def draw_snake(pen):
    """Draw a snake shape for 's'"""
    # Snake (S-curve with head)
    cx, cy = 500, 500
    snake_width = 120
    length_factor = 800
    head_size = 180
    
    # S-curve shape
    points = []
    num_points = 50
    
    for i in range(num_points + 1):
        t = i / num_points
        # Parametric equation for S-curve
        x = cx + (length_factor/3) * math.sin(2 * math.pi * t)
        y = cy + (length_factor/2) * (t - 0.5)
        points.append((x, y))
    
    # Main snake body
    for i in range(len(points) - 1):
        # Create rectangle segment between consecutive points
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        
        # Direction vector between points
        dx, dy = x2 - x1, y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        
        # Normalized perpendicular vector
        if length > 0:
            nx, ny = -dy/length, dx/length
        else:
            nx, ny = 0, 1
            
        # Create rectangle corners
        half_width = snake_width/2
        
        # Use perpendicular vector to create width
        corner1 = (x1 + nx * half_width, y1 + ny * half_width)
        corner2 = (x1 - nx * half_width, y1 - ny * half_width)
        corner3 = (x2 - nx * half_width, y2 - ny * half_width)
        corner4 = (x2 + nx * half_width, y2 + ny * half_width)
        
        # Draw segment
        pen.moveTo(corner1)
        pen.lineTo(corner2)
        pen.lineTo(corner3)
        pen.lineTo(corner4)
        pen.closePath()
    
    # Snake head
    head_x, head_y = points[0]
    
    # Approximating the angle of the head based on first segments
    dx = points[2][0] - points[0][0]
    dy = points[2][1] - points[0][1]
    head_angle = math.atan2(dy, dx)
    
    # Draw head (oval oriented in the direction of travel)
    pen.moveTo((head_x + head_size/2 * math.cos(head_angle), 
               head_y + head_size/2 * math.sin(head_angle)))
    
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        # Rotate the ellipse to match snake direction
        x = head_x + (head_size/2 * math.cos(angle) * math.cos(head_angle) - 
                     head_size/3 * math.sin(angle) * math.sin(head_angle))
        y = head_y + (head_size/2 * math.cos(angle) * math.sin(head_angle) + 
                     head_size/3 * math.sin(angle) * math.cos(head_angle))
        pen.lineTo((x, y))
    pen.closePath()
    
    # Eyes
    eye_size = 20
    eye_offset = 40
    
    # Left eye (relative to head direction)
    eye_angle = head_angle + math.pi/4
    eye_x = head_x + eye_offset * math.cos(head_angle) + eye_offset * math.cos(eye_angle)
    eye_y = head_y + eye_offset * math.sin(head_angle) + eye_offset * math.sin(eye_angle)
    
    pen.moveTo((eye_x + eye_size, eye_y))
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = eye_x + eye_size * math.cos(angle)
        y = eye_y + eye_size * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Right eye (relative to head direction)
    eye_angle = head_angle - math.pi/4
    eye_x = head_x + eye_offset * math.cos(head_angle) + eye_offset * math.cos(eye_angle)
    eye_y = head_y + eye_offset * math.sin(head_angle) + eye_offset * math.sin(eye_angle)
    
    pen.moveTo((eye_x + eye_size, eye_y))
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = eye_x + eye_size * math.cos(angle)
        y = eye_y + eye_size * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()

def draw_tiger(pen):
    """Draw a tiger shape for 't'"""
    # Tiger (head with stripes)
    cx, cy = 500, 500
    head_radius = 300
    ear_size = 100
    
    # Tiger head (circle)
    pen.moveTo((cx + head_radius, cy))
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + head_radius * math.cos(angle)
        y = cy + head_radius * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Left ear (triangle)
    pen.moveTo((cx - head_radius/2, cy - head_radius/2))
    pen.lineTo((cx - head_radius - ear_size, cy - head_radius - ear_size))
    pen.lineTo((cx - ear_size, cy - head_radius - ear_size/2))
    pen.closePath()
    
    # Right ear (triangle)
    pen.moveTo((cx + head_radius/2, cy - head_radius/2))
    pen.lineTo((cx + head_radius + ear_size, cy - head_radius - ear_size))
    pen.lineTo((cx + ear_size, cy - head_radius - ear_size/2))
    pen.closePath()
    
    # Eyes
    eye_size = 60
    eye_distance = 150
    
    # Left eye
    pen.moveTo((cx - eye_distance/2, cy - head_radius/5))
    pen.lineTo((cx - eye_distance/2 - eye_size, cy - head_radius/5))
    pen.lineTo((cx - eye_distance/2 - eye_size, cy - head_radius/5 - eye_size))
    pen.lineTo((cx - eye_distance/2, cy - head_radius/5 - eye_size))
    pen.closePath()
    
    # Right eye
    pen.moveTo((cx + eye_distance/2, cy - head_radius/5))
    pen.lineTo((cx + eye_distance/2 + eye_size, cy - head_radius/5))
    pen.lineTo((cx + eye_distance/2 + eye_size, cy - head_radius/5 - eye_size))
    pen.lineTo((cx + eye_distance/2, cy - head_radius/5 - eye_size))
    pen.closePath()
    
    # Nose (triangle)
    nose_size = 40
    pen.moveTo((cx, cy + head_radius/5))
    pen.lineTo((cx - nose_size, cy + head_radius/5 + nose_size))
    pen.lineTo((cx + nose_size, cy + head_radius/5 + nose_size))
    pen.closePath()
    
    # Mouth (curved line)
    pen.moveTo((cx - nose_size, cy + head_radius/5 + nose_size))
    pen.lineTo((cx, cy + head_radius/5 + nose_size*2))
    pen.lineTo((cx + nose_size, cy + head_radius/5 + nose_size))
    pen.closePath()
    
    # Tiger stripes (several curved lines)
    num_stripes = 7
    stripe_width = 30
    
    for i in range(num_stripes):
        stripe_angle = math.pi/8 + i * math.pi/(num_stripes-1)
        stripe_length = head_radius * 1.6
        
        start_x = cx + (head_radius * 0.6) * math.cos(stripe_angle)
        start_y = cy + (head_radius * 0.6) * math.sin(stripe_angle)
        
        end_x = cx + stripe_length * math.cos(stripe_angle)
        end_y = cy + stripe_length * math.sin(stripe_angle)
        
        # Draw stripe as narrow rectangle
        perp_angle = stripe_angle + math.pi/2
        perp_x = stripe_width/2 * math.cos(perp_angle)
        perp_y = stripe_width/2 * math.sin(perp_angle)
        
        pen.moveTo((start_x + perp_x, start_y + perp_y))
        pen.lineTo((start_x - perp_x, start_y - perp_y))
        pen.lineTo((end_x - perp_x, end_y - perp_y))
        pen.lineTo((end_x + perp_x, end_y + perp_y))
        pen.closePath()

def draw_umbrella(pen):
    """Draw an umbrella shape for 'u'"""
    # Umbrella with handle
    cx, cy = 500, 350
    radius = 400
    handle_length = 500
    handle_width = 30
    
    # Umbrella canopy (half circle)
    pen.moveTo((cx - radius, cy))
    for i in range(0, 13):  # Half circle
        angle = math.pi * i / 12
        x = cx + radius * math.cos(angle + math.pi)
        y = cy + radius * math.sin(angle + math.pi)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Handle
    pen.moveTo((cx - handle_width/2, cy))
    pen.lineTo((cx + handle_width/2, cy))
    pen.lineTo((cx + handle_width/2, cy + handle_length))
    pen.lineTo((cx - handle_width/2, cy + handle_length))
    pen.closePath()
    
    # J-hook handle end
    hook_size = 100
    pen.moveTo((cx, cy + handle_length))
    pen.lineTo((cx + hook_size, cy + handle_length))
    pen.lineTo((cx + hook_size, cy + handle_length - hook_size))
    pen.lineTo((cx + hook_size - handle_width, cy + handle_length - hook_size))
    pen.lineTo((cx + hook_size - handle_width, cy + handle_length - handle_width))
    pen.lineTo((cx, cy + handle_length - handle_width))
    pen.closePath()
    
    # Umbrella ribs
    for i in range(5):
        angle = math.pi * i / 4
        pen.moveTo((cx, cy))
        pen.lineTo((cx + radius * math.cos(angle + math.pi), cy + radius * math.sin(angle + math.pi)))
        pen.closePath()

def draw_violin(pen):
    """Draw a violin shape for 'v'"""
    # Violin with bow
    cx, cy = 500, 500
    body_width = 250
    body_height = 450
    neck_width = 50
    neck_length = 250
    
    # Violin body (stylized figure 8)
    top_radius = body_width/2
    bottom_radius = body_width/2.2
    waist_width = body_width * 0.7
    
    # Upper bout
    pen.moveTo((cx - top_radius, cy - body_height/4))
    pen.lineTo((cx - waist_width/2, cy))
    pen.lineTo((cx - bottom_radius, cy + body_height/4))
    
    # Bottom bout curve
    segments = 12
    for i in range(0, segments + 1):
        angle = math.pi * i / segments - math.pi/2
        x = cx + bottom_radius * math.cos(angle)
        y = cy + body_height/4 + bottom_radius * math.sin(angle)
        pen.lineTo((x, y))
    
    # Upper right side
    pen.lineTo((cx + waist_width/2, cy))
    pen.lineTo((cx + top_radius, cy - body_height/4))
    
    # Top bout curve
    for i in range(0, segments + 1):
        angle = math.pi * i / segments + math.pi/2
        x = cx + top_radius * math.cos(angle)
        y = cy - body_height/4 + top_radius * math.sin(angle)
        pen.lineTo((x, y))
    
    pen.closePath()
    
    # Neck
    pen.moveTo((cx - neck_width/2, cy - body_height/4 - top_radius))
    pen.lineTo((cx + neck_width/2, cy - body_height/4 - top_radius))
    pen.lineTo((cx + neck_width/2, cy - body_height/4 - top_radius - neck_length))
    pen.lineTo((cx - neck_width/2, cy - body_height/4 - top_radius - neck_length))
    pen.closePath()
    
    # Scroll (simplified)
    scroll_size = 70
    pen.moveTo((cx - scroll_size/2, cy - body_height/4 - top_radius - neck_length))
    pen.lineTo((cx + scroll_size/2, cy - body_height/4 - top_radius - neck_length))
    pen.lineTo((cx + scroll_size/2, cy - body_height/4 - top_radius - neck_length - scroll_size))
    pen.lineTo((cx - scroll_size/2, cy - body_height/4 - top_radius - neck_length - scroll_size))
    pen.closePath()
    
    # F-holes (simplified)
    f_hole_width = 20
    f_hole_height = 100
    f_hole_distance = 100
    
    # Left f-hole
    pen.moveTo((cx - f_hole_distance/2, cy))
    pen.lineTo((cx - f_hole_distance/2 - f_hole_width, cy))
    pen.lineTo((cx - f_hole_distance/2 - f_hole_width, cy + f_hole_height))
    pen.lineTo((cx - f_hole_distance/2, cy + f_hole_height))
    pen.closePath()
    
    # Right f-hole
    pen.moveTo((cx + f_hole_distance/2, cy))
    pen.lineTo((cx + f_hole_distance/2 + f_hole_width, cy))
    pen.lineTo((cx + f_hole_distance/2 + f_hole_width, cy + f_hole_height))
    pen.lineTo((cx + f_hole_distance/2, cy + f_hole_height))
    pen.closePath()
    
    # Bow (curved line)
    bow_length = 700
    bow_width = 20
    bow_curve = 100
    
    # Calculate control points for a curved bow
    pen.moveTo((cx - bow_length/2, cy - body_height/2))
    pen.lineTo((cx, cy - body_height/2 - bow_curve))
    pen.lineTo((cx + bow_length/2, cy - body_height/2))
    pen.closePath()

def draw_watermelon(pen):
    """Draw a watermelon shape for 'w'"""
    # Watermelon (half circle with seeds)
    cx, cy = 500, 500
    radius = 400
    rind_thickness = 50
    
    # Main watermelon shape (half circle)
    pen.moveTo((cx - radius, cy))
    
    # Draw the curved part
    segments = 12
    for i in range(0, segments + 1):
        angle = math.pi * i / segments
        x = cx + radius * math.cos(angle + math.pi)
        y = cy + radius * math.sin(angle + math.pi)
        pen.lineTo((x, y))
    
    pen.closePath()
    
    # Rind (inner half circle)
    inner_radius = radius - rind_thickness
    pen.moveTo((cx - inner_radius, cy))
    
    for i in range(0, segments + 1):
        angle = math.pi * i / segments
        x = cx + inner_radius * math.cos(angle + math.pi)
        y = cy + inner_radius * math.sin(angle + math.pi)
        pen.lineTo((x, y))
        
    pen.closePath()
    
    # Seeds (scattered oval shapes)
    seed_count = 12
    seed_width = 30
    seed_height = 50
    
    # Create a grid of seeds
    for i in range(seed_count):
        # Calculate position in a grid pattern with some randomization
        grid_x = (i % 4) - 1.5  # -1.5, -0.5, 0.5, 1.5
        grid_y = (i // 4) - 1   # -1, 0, 1
        
        # Add some variation to seed positions
        offset_x = (i % 3 - 1) * 30
        offset_y = ((i + 1) % 3 - 1) * 30
        
        seed_x = cx + grid_x * inner_radius/2 + offset_x
        seed_y = cy + grid_y * inner_radius/2 + offset_y
        
        # Draw seed (oval)
        pen.moveTo((seed_x + seed_width/2, seed_y))
        for j in range(1, segments + 1):
            angle = 2 * math.pi * j / segments
            x = seed_x + seed_width/2 * math.cos(angle)
            y = seed_y + seed_height/2 * math.sin(angle)
            pen.lineTo((x, y))
        pen.closePath()

def draw_xylophone(pen):
    """Draw a xylophone shape for 'x'"""
    # Xylophone (series of bars)
    cx, cy = 500, 500
    width = 600
    height = 400
    num_bars = 8
    
    # Calculate bar dimensions
    bar_width = width - 100
    bar_height = height / (num_bars * 1.5)
    bar_spacing = height / num_bars
    
    # Draw bars (decreasing in width as they go down)
    for i in range(num_bars):
        y_pos = cy - height/2 + i * bar_spacing
        
        # Each bar gets progressively shorter
        current_width = bar_width * (num_bars - i) / num_bars
        
        pen.moveTo((cx - current_width/2, y_pos))
        pen.lineTo((cx + current_width/2, y_pos))
        pen.lineTo((cx + current_width/2, y_pos + bar_height))
        pen.lineTo((cx - current_width/2, y_pos + bar_height))
        pen.closePath()
    
    # Draw mallets (crossed to make an 'X' shape)
    mallet_length = width * 0.7
    mallet_width = 20
    mallet_head = 50
    
    # First mallet (diagonal top-left to bottom-right)
    angle = math.pi/4
    dx = math.cos(angle) * mallet_length/2
    dy = math.sin(angle) * mallet_length/2
    
    pen.moveTo((cx - dx, cy - dy))
    pen.lineTo((cx + dx, cy + dy))
    pen.closePath()
    
    # Second mallet (diagonal top-right to bottom-left)
    angle = -math.pi/4
    dx = math.cos(angle) * mallet_length/2
    dy = math.sin(angle) * mallet_length/2
    
    pen.moveTo((cx + dx, cy - dy))
    pen.lineTo((cx - dx, cy + dy))
    pen.closePath()
    
    # Mallet heads (circles at the ends)
    head_positions = [
        (cx - dx, cy - dy),
        (cx + dx, cy + dy),
        (cx + dx, cy - dy),
        (cx - dx, cy + dy)
    ]
    
    for head_x, head_y in head_positions:
        pen.moveTo((head_x + mallet_head/2, head_y))
        segments = 16
        for i in range(1, segments + 1):
            angle = 2 * math.pi * i / segments
            x = head_x + mallet_head/2 * math.cos(angle)
            y = head_y + mallet_head/2 * math.sin(angle)
            pen.lineTo((x, y))
        pen.closePath()

def draw_yacht(pen):
    """Draw a yacht shape for 'y'"""
    # Yacht (sailboat)
    cx, cy = 500, 500
    hull_width = 500
    hull_height = 150
    mast_height = 400
    sail_width = 300
    
    # Hull (boat bottom)
    pen.moveTo((cx - hull_width/2, cy))
    pen.lineTo((cx + hull_width/2, cy))
    pen.lineTo((cx + hull_width/3, cy + hull_height))
    pen.lineTo((cx - hull_width/3, cy + hull_height))
    pen.closePath()
    
    # Mast (vertical pole)
    mast_width = 20
    pen.moveTo((cx - mast_width/2, cy))
    pen.lineTo((cx + mast_width/2, cy))
    pen.lineTo((cx + mast_width/2, cy - mast_height))
    pen.lineTo((cx - mast_width/2, cy - mast_height))
    pen.closePath()
    
    # Main sail (triangle)
    pen.moveTo((cx, cy - mast_height))
    pen.lineTo((cx, cy))
    pen.lineTo((cx + sail_width, cy - mast_height/2))
    pen.closePath()
    
    # Jib sail (small triangle at front)
    jib_height = mast_height * 0.6
    pen.moveTo((cx, cy - jib_height))
    pen.lineTo((cx, cy))
    pen.lineTo((cx - sail_width/2, cy - jib_height/3))
    pen.closePath()
    
    # Water (wavy line)
    wave_width = hull_width * 1.5
    wave_height = 50
    num_waves = 6
    segment_width = wave_width / num_waves
    
    pen.moveTo((cx - wave_width/2, cy + hull_height + wave_height))
    
    for i in range(num_waves + 1):
        x = cx - wave_width/2 + i * segment_width
        # Alternate up and down to create waves
        y = cy + hull_height + wave_height/2 + (wave_height/2 if i % 2 == 0 else -wave_height/2)
        pen.lineTo((x, y))
    
    pen.closePath()

def draw_zebra(pen):
    """Draw a zebra shape for 'z'"""
    # Zebra (horse-like shape with stripes)
    cx, cy = 500, 500
    body_length = 500
    body_height = 250
    head_size = 200
    leg_length = 300
    
    # Body (oval)
    pen.moveTo((cx - body_length/2, cy))
    segments = 24
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + body_length/2 * math.cos(angle)
        y = cy + body_height/2 * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Head (oval at front of body)
    head_angle = -math.pi/6  # Slightly angled down
    head_cx = cx - body_length/2 - head_size/3
    head_cy = cy - body_height/4
    
    pen.moveTo((head_cx + head_size/2 * math.cos(head_angle), 
               head_cy + head_size/2 * math.sin(head_angle)))
    
    for i in range(1, segments + 1):
        angle = 2 * math.pi * i / segments
        # Rotate and stretch the ellipse
        x = head_cx + (head_size/2 * math.cos(angle) * math.cos(head_angle) - 
                     head_size/3 * math.sin(angle) * math.sin(head_angle))
        y = head_cy + (head_size/2 * math.cos(angle) * math.sin(head_angle) + 
                     head_size/3 * math.sin(angle) * math.cos(head_angle))
        pen.lineTo((x, y))
    pen.closePath()
    
    # Ears (triangles)
    ear_size = 60
    ear_cx = head_cx - head_size/4
    ear_cy = head_cy - head_size/2
    
    # Left ear
    pen.moveTo((ear_cx, ear_cy))
    pen.lineTo((ear_cx - ear_size, ear_cy - ear_size))
    pen.lineTo((ear_cx + ear_size, ear_cy - ear_size))
    pen.closePath()
    
    # Legs (four rectangles)
    leg_width = 40
    leg_positions = [
        (cx - body_length/4, cy + body_height/2),  # Front left
        (cx - body_length/4 + leg_width*3, cy + body_height/2),  # Front right
        (cx + body_length/4 - leg_width*3, cy + body_height/2),  # Back left
        (cx + body_length/4, cy + body_height/2)   # Back right
    ]
    
    for leg_x, leg_y in leg_positions:
        pen.moveTo((leg_x - leg_width/2, leg_y))
        pen.lineTo((leg_x + leg_width/2, leg_y))
        pen.lineTo((leg_x + leg_width/2, leg_y + leg_length))
        pen.lineTo((leg_x - leg_width/2, leg_y + leg_length))
        pen.closePath()
    
    # Tail (thin rectangle with tuft)
    tail_width = 20
    tail_length = 200
    tuft_size = 60
    
    pen.moveTo((cx + body_length/2, cy))
    pen.lineTo((cx + body_length/2 + tail_width/2, cy))
    pen.lineTo((cx + body_length/2 + tail_width/2, cy + tail_length))
    pen.lineTo((cx + body_length/2 - tail_width/2, cy + tail_length))
    pen.closePath()
    
    # Tuft (small oval at end of tail)
    tuft_cx = cx + body_length/2
    tuft_cy = cy + tail_length
    
    pen.moveTo((tuft_cx + tuft_size/2, tuft_cy))
    for i in range(1, segments//2 + 1):
        angle = 2 * math.pi * i / segments
        x = tuft_cx + tuft_size/2 * math.cos(angle)
        y = tuft_cy + tuft_size/2 * math.sin(angle)
        pen.lineTo((x, y))
    pen.closePath()
    
    # Zebra stripes (several rectangles across body)
    num_stripes = 12
    stripe_width = 30
    
    for i in range(num_stripes):
        stripe_x = cx - body_length/2 + body_length * i / num_stripes
        
        pen.moveTo((stripe_x, cy - body_height/2))
        pen.lineTo((stripe_x + stripe_width, cy - body_height/2))
        pen.lineTo((stripe_x + stripe_width, cy + body_height/2))
        pen.lineTo((stripe_x, cy + body_height/2))
        pen.closePath()

def add_letter_glyphs_to_font(font):
    """Add glyphs to the font for each letter with shapes representing words"""
    # Dictionary mapping letters to drawing functions
    letter_shapes = {
        'a': draw_apple,
        'b': draw_ball,
        'c': draw_cat,
        'd': draw_dog,
        'e': draw_elephant,
        'f': draw_fish,
        'g': draw_giraffe,
        'h': draw_house,
        'i': draw_igloo,
        'j': draw_jellyfish,
        'k': draw_kite,
        'l': draw_lion,
        'm': draw_monkey,
        'n': draw_nest,
        'o': draw_octopus,
        'p': draw_penguin,
        'q': draw_queen,
        'r': draw_rabbit,
        's': draw_snake,
        't': draw_tiger,
        'u': draw_umbrella,
        'v': draw_violin,
        'w': draw_watermelon,
        'x': draw_xylophone,
        'y': draw_yacht,
        'z': draw_zebra,
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
    flipped_pen = FlippedPen(pen, FONT_SIZE)
    flipped_pen.moveTo((100, 100))
    flipped_pen.lineTo((900, 100))
    flipped_pen.lineTo((900, 900))
    flipped_pen.lineTo((100, 900))
    flipped_pen.closePath()
    font['glyf']['.notdef'] = flipped_pen.glyph()
    font['hmtx'].metrics['.notdef'] = (FONT_SIZE, 0)
    
    # Add glyphs for each lowercase letter
    for i, letter in enumerate(string.ascii_lowercase):
        unicode_value = ord(letter)
        glyph_name = f"uni{unicode_value:04X}"
        
        # Create a glyph with a letter-specific shape
        pen = TTGlyphPen(glyphSet=font.getGlyphSet())
        flipped_pen = FlippedPen(pen, FONT_SIZE)
        
        if letter in letter_shapes:
            # Use a specific drawing function for this letter
            letter_shapes[letter](flipped_pen)
            print(f"Added custom shape for '{letter}' (Unicode: {unicode_value})")
        else:
            # For letters without specific shapes, create a simple generic shape
            center_x, center_y = FONT_SIZE/2, FONT_SIZE/2
            radius = FONT_SIZE * 0.4
            
            # Create a basic shape (circle with the letter inside)
            flipped_pen.moveTo((center_x + radius, center_y))
            segments = 24
            for j in range(1, segments + 1):
                angle = 2 * math.pi * j / segments
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                flipped_pen.lineTo((x, y))
            flipped_pen.closePath()
            
            # Add letter identifier (simple approximation)
            letter_lines = []
            
            if letter == 'i':
                # i - vertical line with dot
                letter_lines = [
                    [(center_x, center_y - radius/2), (center_x, center_y + radius/2)],
                    [(center_x - radius/5, center_y - radius*0.8), (center_x + radius/5, center_y - radius*0.8)]
                ]
            elif letter == 'j':
                # j - hook with dot
                letter_lines = [
                    [(center_x, center_y - radius/2), (center_x, center_y + radius/2)],
                    [(center_x, center_y + radius/2), (center_x - radius/3, center_y + radius/2 + radius/3)],
                    [(center_x - radius/5, center_y - radius*0.8), (center_x + radius/5, center_y - radius*0.8)]
                ]
            elif letter == 'k':
                # k - vertical with two diagonals
                letter_lines = [
                    [(center_x - radius/3, center_y - radius/2), (center_x - radius/3, center_y + radius/2)],
                    [(center_x - radius/3, center_y), (center_x + radius/3, center_y - radius/2)],
                    [(center_x - radius/3, center_y), (center_x + radius/3, center_y + radius/2)]
                ]
            elif letter == 'l':
                # l - vertical line
                letter_lines = [
                    [(center_x, center_y - radius/2), (center_x, center_y + radius/2)]
                ]
            elif letter == 'm':
                # m - simplified m
                letter_lines = [
                    [(center_x - radius/2, center_y + radius/2), (center_x - radius/2, center_y - radius/2)],
                    [(center_x - radius/2, center_y - radius/2), (center_x, center_y + radius/4)],
                    [(center_x, center_y + radius/4), (center_x + radius/2, center_y - radius/2)],
                    [(center_x + radius/2, center_y - radius/2), (center_x + radius/2, center_y + radius/2)]
                ]
            elif letter == 'n':
                # n - simplified n
                letter_lines = [
                    [(center_x - radius/3, center_y + radius/2), (center_x - radius/3, center_y - radius/2)],
                    [(center_x - radius/3, center_y - radius/2), (center_x + radius/3, center_y + radius/2)],
                    [(center_x + radius/3, center_y + radius/2), (center_x + radius/3, center_y - radius/2)]
                ]
            elif letter == 'o':
                # o - inner circle
                inner_radius = radius * 0.6
                pen.moveTo((center_x + inner_radius, center_y))
                for j in range(1, segments + 1):
                    angle = 2 * math.pi * j / segments
                    x = center_x + inner_radius * math.cos(angle)
                    y = center_y + inner_radius * math.sin(angle)
                    flipped_pen.lineTo((x, y))
                pen.closePath()
            elif letter == 'p':
                # p - simplified p
                letter_lines = [
                    [(center_x - radius/3, center_y + radius/2), (center_x - radius/3, center_y - radius/2)],
                    [(center_x - radius/3, center_y - radius/2), (center_x + radius/3, center_y - radius/2)],
                    [(center_x + radius/3, center_y - radius/2), (center_x + radius/3, center_y)],
                    [(center_x + radius/3, center_y), (center_x - radius/3, center_y)]
                ]
            elif letter == 'q':
                # q - circle with tail
                inner_radius = radius * 0.5
                pen.moveTo((center_x + inner_radius, center_y))
                for j in range(1, segments + 1):
                    angle = 2 * math.pi * j / segments
                    x = center_x + inner_radius * math.cos(angle)
                    y = center_y + inner_radius * math.sin(angle)
                    flipped_pen.lineTo((x, y))
                pen.closePath()
                
                # Tail
                pen.moveTo((center_x + inner_radius*0.7, center_y + inner_radius*0.7))
                pen.lineTo((center_x + radius/2, center_y + radius/2))
                pen.closePath()
            elif letter == 'r':
                # r - simplified r
                letter_lines = [
                    [(center_x - radius/3, center_y + radius/2), (center_x - radius/3, center_y - radius/2)],
                    [(center_x - radius/3, center_y - radius/3), (center_x, center_y - radius/2)],
                    [(center_x, center_y - radius/2), (center_x + radius/3, center_y - radius/3)]
                ]
            elif letter == 's':
                # s - simplified s
                letter_lines = [
                    [(center_x + radius/3, center_y - radius/2), (center_x - radius/3, center_y - radius/2)],
                    [(center_x - radius/3, center_y - radius/2), (center_x - radius/3, center_y)],
                    [(center_x - radius/3, center_y), (center_x + radius/3, center_y)],
                    [(center_x + radius/3, center_y), (center_x + radius/3, center_y + radius/2)],
                    [(center_x + radius/3, center_y + radius/2), (center_x - radius/3, center_y + radius/2)]
                ]
            elif letter == 't':
                # t - simplified t
                letter_lines = [
                    [(center_x, center_y - radius/2), (center_x, center_y + radius/2)],
                    [(center_x - radius/3, center_y - radius/4), (center_x + radius/3, center_y - radius/4)]
                ]
            elif letter == 'v':
                # v - simplified v
                letter_lines = [
                    [(center_x - radius/3, center_y - radius/2), (center_x, center_y + radius/2)],
                    [(center_x, center_y + radius/2), (center_x + radius/3, center_y - radius/2)]
                ]
            elif letter == 'w':
                # w - simplified w
                letter_lines = [
                    [(center_x - radius/2, center_y - radius/2), (center_x - radius/4, center_y + radius/2)],
                    [(center_x - radius/4, center_y + radius/2), (center_x, center_y - radius/4)],
                    [(center_x, center_y - radius/4), (center_x + radius/4, center_y + radius/2)],
                    [(center_x + radius/4, center_y + radius/2), (center_x + radius/2, center_y - radius/2)]
                ]
            elif letter == 'x':
                # x - simplified x
                letter_lines = [
                    [(center_x - radius/3, center_y - radius/2), (center_x + radius/3, center_y + radius/2)],
                    [(center_x - radius/3, center_y + radius/2), (center_x + radius/3, center_y - radius/2)]
                ]
            elif letter == 'y':
                # y - simplified y
                letter_lines = [
                    [(center_x - radius/3, center_y - radius/2), (center_x, center_y)],
                    [(center_x, center_y), (center_x + radius/3, center_y - radius/2)],
                    [(center_x, center_y), (center_x, center_y + radius/2)]
                ]
            elif letter == 'z':
                # z - simplified z
                letter_lines = [
                    [(center_x - radius/3, center_y - radius/2), (center_x + radius/3, center_y - radius/2)],
                    [(center_x + radius/3, center_y - radius/2), (center_x - radius/3, center_y + radius/2)],
                    [(center_x - radius/3, center_y + radius/2), (center_x + radius/3, center_y + radius/2)]
                ]
            
            # Draw letter lines
            for line in letter_lines:
                flipped_pen.moveTo(line[0])
                flipped_pen.lineTo(line[1])
                flipped_pen.closePath()
                
            print(f"Added generic shape for '{letter}' (Unicode: {unicode_value})")
        
        font['glyf'][glyph_name] = flipped_pen.glyph()
        font['hmtx'].metrics[glyph_name] = (FONT_SIZE, 0)
        
        # Map the Unicode character to this glyph
        for cmap in font['cmap'].tables:
            cmap.cmap[unicode_value] = glyph_name
    
    # Update the font metrics
    font['maxp'].numGlyphs = len(glyph_order)
    font['hhea'].numberOfHMetrics = len(font['hmtx'].metrics)
    
    return font

def main():
    print("Creating a phonics font with letter-specific shapes...")
    
    # Create a basic font
    font = create_empty_font()
    
    # Add glyphs for each letter
    font = add_letter_glyphs_to_font(font)
    
    # Save the font
    try:
        font.save(OUTPUT_FILE)
        print(f"Font saved to {OUTPUT_FILE}")
        print("You can now install this font on your Mac by:")
        print("1. Double-clicking the font file")
        print("2. Clicking 'Install Font' in the Font Book app")
        print("\nThis font contains shapes representing words for each letter:")
        print("a - apple shape")
        print("b - ball shape")
        print("c - cat shape")
        print("d - dog shape")
        print("e - elephant shape")
        print("f - fish shape")
        print("g - giraffe shape")
        print("h - house shape")
        print("i - igloo shape")
        print("j - jellyfish shape")
        print("k - kite shape")
        print("l - lion shape")
        print("m - monkey shape")
        print("n - nest shape")
        print("o - octopus shape")
        print("p - penguin shape")
        print("q - queen shape")
        print("r - rabbit shape")
        print("s - snake shape")
        print("t - tiger shape")
        print("u - umbrella shape")
        print("v - violin shape")
        print("w - watermelon shape")
        print("x - xylophone shape")
        print("y - yacht shape")
        print("z - zebra shape")
    except Exception as e:
        print(f"Error saving font: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()