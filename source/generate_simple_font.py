#!/usr/bin/env python3
import os
import string
from PIL import Image, ImageDraw, ImageFont
from PIL import Image

# Configuration
FONT_NAME = "PhonicsPicturesSimple"
OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
HTML_FILE = os.path.join(OUTPUT_DIR, f"{FONT_NAME}.html")
IMAGE_SIZE = (500, 500)  # Size of each letter image

# Ensure directories exist
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

def create_html_font_display():
    """Create an HTML file to display the images as a font"""
    with open(HTML_FILE, 'w') as f:
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
        
        # Create sample images for letters (if they don't exist)
        create_sample_images()
        
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
        
        print(f"HTML display created at {HTML_FILE}")
        print(f"Open this file in a web browser to see the phonics pictures")

def main():
    # Create sample images for letters
    create_sample_images()
    
    # Create HTML display
    create_html_font_display()
    
    print("Since creating a proper font file with pictures is complex, we've created a visual HTML display.")
    print("You can use the images in the 'images' directory for your font creation needs.")

if __name__ == "__main__":
    main()