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

## Available Font Files
- `Phonics.ttf` - Main phonics font with letter shapes

## Key Scripts
- `generate_shapes.py` - Main font generation script that creates shapes font

## Dependencies
- Python 3.x
- Pillow (PIL)
- fonttools
- Virtual environment in `.venv/`

## Common Commands
```bash
# Activate virtual environment (if using one)
source .venv/bin/activate

# Generate the phonics font
python source/generate_shapes.py
```

## Letter-Word Associations
Each letter represents a word:
A=Apple, B=Ball, C=Cat, D=Dog, E=Elephant, F=Fish, G=Giraffe, H=House, I=Igloo, J=Jellyfish, K=Kite, L=Lion, M=Monkey, N=Nest, O=Octopus, P=Penguin, Q=Queen, R=Rabbit, S=Snake, T=Tiger, U=Umbrella, V=Violin, W=Watermelon, X=Xylophone, Y=Yacht, Z=Zebra

## Testing
View the generated font using the HTML demo file:
- `PhonicsDemo.html`

## Development Notes
- Font generation uses Python's Pillow library for image processing
- fonttools library handles TTF font creation
- SVG files in `/svg/` provide vector-based letter shapes
- PNG images in `/images/` provide raster-based references
- Each letter (a-z) has corresponding SVG and PNG files
