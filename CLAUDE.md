# Phonics Font Project

## Project Overview
This is a phonics-oriented font project that creates custom TTF fonts where each letter (a-z) is represented by pictorial shapes of words starting with that letter. The project helps children associate letters with common words through visual representation.

## Project Structure
- `/source/` - Python scripts for generating different font variants
- `/svg/` - SVG files for each letter (a-z)
- `/images/` - PNG images for each letter (a-z) 
- `/temp/` - Temporary files and alternate versions
- `*.ttf` - Generated font files
- `*.html` - Demo pages for showcasing fonts

## Available Font Variants
- `PhonicsPictures.ttf` - Main phonics font
- `PhonicsPicturesShapes.ttf` - Shapes variant
- `PhonicsPicturesVisible.ttf` - Visible variant

## Key Scripts
- `generate_font.py` - Main font generation script
- `generate_shapes.py` - Generates shapes font variant
- `generate_simple_font.py` - Simple font generation
- `generate_visible_font.py` - Visible font variant
- `generate_visual_font.py` - Visual font variant
- `generate_svg_font.py` - SVG-based font generation
- `generate_color_font.py` - Color font generation
- `generate_bitmap_font.py` - Bitmap font generation

## Dependencies
- Python 3.x
- Pillow (PIL)
- fonttools
- Virtual environment in `.venv/`

## Common Commands
```bash
# Activate virtual environment
source .venv/bin/activate

# Generate main shapes font
python source/generate_shapes.py

# Generate other variants
python source/generate_font.py
python source/generate_visible_font.py
python source/generate_visual_font.py
```

## Letter-Word Associations
Each letter represents a word:
A=Apple, B=Ball, C=Cat, D=Dog, E=Elephant, F=Fish, G=Giraffe, H=House, I=Igloo, J=Jellyfish, K=Kite, L=Lion, M=Monkey, N=Nest, O=Octopus, P=Penguin, Q=Queen, R=Rabbit, S=Snake, T=Tiger, U=Umbrella, V=Violin, W=Watermelon, X=Xylophone, Y=Yacht, Z=Zebra

## Testing
View generated fonts using the HTML demo files:
- `PhonicsPicturesDemo.html`
- `PhonicsPicturesSimple.html` 
- `PhonicsPicturesVisual.html`

## Development Notes
- Font generation uses Python's Pillow library for image processing
- fonttools library handles TTF font creation
- SVG files provide vector-based letter shapes
- Images provide raster-based alternatives