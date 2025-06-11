# Phonics Pictures Font

A custom font where each letter is represented by a picture of a word that starts with that letter.

## Overview

This project creates custom phonics-oriented fonts where each lowercase letter (a-z) is represented by a shape that depicts a word starting with that letter. For example, 'a' shows an apple shape, 'b' shows a ball shape, etc. This approach helps children associate letters with common words.

## Features

- **TTF Font with Letter Shapes**: Each letter is drawn as a recognizable shape representing a word
- **Complete A-Z Coverage**: All 26 lowercase letters have custom shapes
- **Easily Installable**: Works on macOS and other systems that support TTF fonts
- **HTML Demo Page**: Includes a demo page to showcase all letter shapes
- **Multiple Formats**: Supports both SVG vector shapes and PNG images
- **Vector and Raster Assets**: SVG files for scalable shapes, PNG images for reference

## Word-Letter Associations

| Letter | Word       | Letter | Word       | Letter | Word        |
|--------|------------|--------|------------|--------|-------------|
| A      | Apple      | J      | Jellyfish  | S      | Snake       |
| B      | Ball       | K      | Kite       | T      | Tiger       |
| C      | Cat        | L      | Lion       | U      | Umbrella    |
| D      | Dog        | M      | Monkey     | V      | Violin      |
| E      | Elephant   | N      | Nest       | W      | Watermelon  |
| F      | Fish       | O      | Octopus    | X      | Xylophone   |
| G      | Giraffe    | P      | Penguin    | Y      | Yacht       |
| H      | House      | Q      | Queen      | Z      | Zebra       |
| I      | Igloo      | R      | Rabbit     |        |             |

## Requirements

- Python 3.x
- Python virtual environment (`.venv` directory in project)
- Pillow (Python Imaging Library)
- fonttools

## Installation

```bash
# Clone the repository
git clone [repository-url]
cd phonics-font

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install required packages
pip install Pillow fonttools
```

## Usage

### Generate the Font

```bash
source .venv/bin/activate
python source/generate_shapes.py
```

This will generate `Phonics.ttf` in the project directory.

### Install the Font

1. Double-click the generated TTF file
2. Click "Install Font" in the Font Book app (on macOS)
3. The font will be available for use in your applications

### View the Demo

1. Open `PhonicsPicturesDemo.html` in a web browser to see all the letter shapes

## Customization

To customize the shapes used for each letter:

1. Edit the corresponding `draw_*` functions in `source/generate_shapes.py`
2. Modify SVG files in the `svg/` directory for vector-based shapes
3. Update PNG images in the `images/` directory for raster references
4. Run the script again to generate a new font

## Font Format

This font is a standard TTF (TrueType Font) with custom glyph shapes. This format ensures maximum compatibility across different operating systems and applications.

## License

This project is available for educational and personal use.

## Credits

Created for phonics education purposes.
Built with Python, Pillow, and fonttools.