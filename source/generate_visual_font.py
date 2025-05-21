#!/usr/bin/env python3
import os
import string
import tempfile
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Configuration
FONT_NAME = "PhonicsPicturesVisual"
OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
TEMP_DIR = os.path.join(OUTPUT_DIR, "temp")
SVG_DIR = os.path.join(TEMP_DIR, "svg")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{FONT_NAME}.ttf")
IMAGE_SIZE = (500, 500)

# Ensure directories exist
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(SVG_DIR, exist_ok=True)

def create_font_generator_script():
    """Create a FontForge Python script to generate the font"""
    script_path = os.path.join(TEMP_DIR, "generate_font.py")
    
    with open(script_path, "w") as f:
        f.write(f"""#!/usr/bin/env python3
import fontforge
import os
import sys

# Font information
font = fontforge.font()
font.fontname = "{FONT_NAME}"
font.familyname = "{FONT_NAME}"
font.fullname = "{FONT_NAME}"
font.copyright = "Created with FontForge"
font.encoding = "UnicodeFull"
font.em = 1000

# Set character width and height
svg_dir = "{SVG_DIR}"

# Create glyphs for a-z
for i in range(26):
    char = chr(ord('a') + i)
    code = ord(char)
    svg_path = os.path.join(svg_dir, f"{{char}}.svg")
    
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
font.generate("{OUTPUT_FILE}")
print(f"Font saved to {OUTPUT_FILE}")
""")
    
    return script_path

def trace_image_to_svg(image_path, svg_path):
    """Convert a PNG image to SVG using potrace (must be installed)"""
    # First, create temporary files for the BMP conversion
    with tempfile.NamedTemporaryFile(delete=False, suffix='.ppm') as temp_ppm:
        temp_ppm_path = temp_ppm.name
    
    # Convert PNG to PPM (bitmap format potrace can read)
    img = Image.open(image_path).convert('RGB')
    img.save(temp_ppm_path)
    
    # Use potrace to convert to SVG
    try:
        subprocess.run(['potrace', temp_ppm_path, '-s', '-o', svg_path], check=True)
        print(f"Converted {image_path} to {svg_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {image_path} to SVG: {e}")
    except FileNotFoundError:
        print("potrace is not installed. Please install potrace.")
        # Create a fallback simple SVG with a rectangle
        with open(svg_path, 'w') as f:
            f.write(f'''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="500pt" height="500pt" viewBox="0 0 500 500" preserveAspectRatio="xMidYMid meet">
<g transform="translate(0.000000,500.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none">
<path d="M500 2500 l0 -2000 2000 0 2000 0 0 2000 0 2000 -2000 0 -2000 0 0 -2000z"/>
</g>
</svg>''')
    
    # Clean up
    try:
        os.unlink(temp_ppm_path)
    except:
        pass
    
def create_simple_svg_files():
    """Create simplified SVG files from the PNG images"""
    for letter in string.ascii_lowercase:
        img_path = os.path.join(IMAGES_DIR, f"{letter}.png")
        svg_path = os.path.join(SVG_DIR, f"{letter}.svg")
        
        if os.path.exists(img_path):
            # Create a simple SVG with the letter's outline
            trace_image_to_svg(img_path, svg_path)
        else:
            print(f"Image not found for letter '{letter}'")

def install_potrace():
    """Check if potrace is installed and provide instructions if not"""
    try:
        result = subprocess.run(['which', 'potrace'], capture_output=True, text=True)
        if result.returncode == 0:
            print("potrace is already installed.")
            return True
        else:
            print("potrace is not installed. Attempting to provide instructions...")
            
            # Check if homebrew is installed
            brew_result = subprocess.run(['which', 'brew'], capture_output=True, text=True)
            if brew_result.returncode == 0:
                print("\nTo install potrace, run the following command:")
                print("brew install potrace")
            else:
                print("\nTo install potrace:")
                print("1. First install Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
                print("2. Then install potrace: brew install potrace")
            
            return False
    except Exception as e:
        print(f"Error checking for potrace: {e}")
        return False

def create_alternative_svg():
    """Create simplified SVG representations for letters without potrace"""
    for letter in string.ascii_lowercase:
        img_path = os.path.join(IMAGES_DIR, f"{letter}.png")
        svg_path = os.path.join(SVG_DIR, f"{letter}.svg")
        
        if os.path.exists(img_path):
            # Create a simple SVG with shapes
            with open(svg_path, 'w') as f:
                # Calculate a letter-specific hue based on its position
                hue = (ord(letter) - ord('a')) * (360/26)
                
                f.write(f'''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="500pt" height="500pt" viewBox="0 0 500 500" preserveAspectRatio="xMidYMid meet">
<g transform="translate(0.000000,500.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none">
<path d="M1000 2500 c0 -1000 0 -1000 1000 -1000 1000 0 1000 0 1000 1000 0 1000 0 1000 -1000 1000 -1000 0 -1000 0 -1000 -1000z m1800 0 c0 -700 0 -700 -700 -700 -700 0 -700 0 -700 700 0 700 0 700 700 700 700 0 700 0 700 -700z"/>
<path d="M1500 2500 c0 -500 0 -500 500 -500 500 0 500 0 500 500 0 500 0 500 -500 500 -500 0 -500 0 -500 -500z"/>
<text x="2500" y="1750" transform="scale(1,-1)" font-family="Arial" font-size="500" text-anchor="middle">{letter.upper()}</text>
</g>
</svg>''')
                
            print(f"Created alternative SVG for '{letter}'")
        else:
            print(f"Image not found for letter '{letter}'")

def main():
    print("Creating a visual phonics font from images...")
    
    # First check if potrace is installed
    has_potrace = install_potrace()
    
    # Create SVG versions of our letter images
    if has_potrace:
        create_simple_svg_files()
    else:
        print("\nUsing alternative SVG creation method...")
        create_alternative_svg()
    
    # Create a FontForge script to generate the font
    script_path = create_font_generator_script()
    
    # Try to run the FontForge script
    try:
        # First try the 'fontforge' command
        try:
            subprocess.run(['fontforge', '-script', script_path], check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            # If that doesn't work, try the Mac OS X FontForge.app location
            fontforge_app = '/Applications/FontForge.app/Contents/MacOS/FontForge'
            if os.path.exists(fontforge_app):
                subprocess.run([fontforge_app, '-script', script_path], check=True)
            else:
                raise FileNotFoundError("FontForge not found")
                
        print(f"\nFont created successfully at {OUTPUT_FILE}")
        print("To install the font:")
        print("1. Double-click the font file in Finder")
        print("2. Click 'Install Font' in the Font Book preview")
        
    except FileNotFoundError:
        print("\nFontForge not found. Please install FontForge to generate the font.")
        print("You can install FontForge using Homebrew:")
        print("  brew install fontforge")
        print("Or download it from https://fontforge.org/en-US/")
        
        # Create an HTML display as a fallback
        html_path = os.path.join(OUTPUT_DIR, f"{FONT_NAME}.html")
        create_html_fallback(html_path)
        
        print("\nAs an alternative, an HTML preview has been created:")
        print(f"  {html_path}")
    
    except Exception as e:
        print(f"\nError generating font: {e}")
        print("Creating HTML fallback display instead...")
        
        # Create an HTML display as a fallback
        html_path = os.path.join(OUTPUT_DIR, f"{FONT_NAME}.html")
        create_html_fallback(html_path)
        
        print(f"HTML preview created at {html_path}")

def create_html_fallback(html_path):
    """Create an HTML file that displays the letter images"""
    with open(html_path, 'w') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Phonics Picture Font</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            text-align: center;
        }
        .letter-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .letter-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .letter-image {
            width: 150px;
            height: 150px;
            object-fit: contain;
        }
        .letter-label {
            margin-top: 10px;
            font-size: 24px;
            font-weight: bold;
        }
        .word-label {
            color: #555;
        }
        .text-sample {
            font-size: 24px;
            line-height: 1.5;
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        .text-sample p {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>Phonics Picture Font</h1>
    
    <div class="letter-grid">
""")
        
        # Add each letter with its image
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
        
        for letter, word in sorted(sample_images.items()):
            image_path = f"images/{letter}.png"
            f.write(f"""
        <div class="letter-card">
            <img src="{image_path}" alt="{letter}" class="letter-image">
            <div class="letter-label">{letter.upper()}</div>
            <div class="word-label">{word}</div>
        </div>
""")
            
        # Add examples
        f.write("""
    </div>
    
    <h2>Example Sentences</h2>
    <div class="text-sample">
        <p>
            Using images as letters, we can create sentences like:<br>
            <span id="example-1"></span>
        </p>
        
        <p>
            Or try this pangram:<br>
            <span id="example-2"></span>
        </p>
    </div>

    <script>
        // Create image replacement function
        function replaceTextWithImages(elementId, text) {
            const element = document.getElementById(elementId);
            let html = '';
            
            for (let i = 0; i < text.length; i++) {
                const char = text[i].toLowerCase();
                if (char >= 'a' && char <= 'z') {
                    html += `<img src="images/${char}.png" alt="${char}" style="height: 40px; vertical-align: middle;">`;
                } else {
                    html += text[i];
                }
            }
            
            element.innerHTML = html;
        }
        
        // Replace example texts
        replaceTextWithImages('example-1', 'The quick brown fox');
        replaceTextWithImages('example-2', 'The quick brown fox jumps over the lazy dog');
    </script>
</body>
</html>
""")

if __name__ == "__main__":
    main()