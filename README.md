# Pixel Fonts
These are pixel art fonts I have created for a variety of purposes.

Files:
- .bdf files: Output of FontForge to be converted to TTF by bdf2ttf.py or used in embedded devices
- .ttf files: Output of bdf2ttf.py for general use

## Terminology

- Condensed - Each glyph is up to 70%-80% of the grid width
- Monospace - These fonts are "Condensed" sized but every glyph is the same width
- Ultra Condensed - Each glyph is up to 50%-60% of the grid width
- True - These fonts are within the specified size by having no descent value. These fonts are better suited for embedded devices.


## Icons
Starting July 8, 2024, icons are now embedded in fonts with the specified resolution., making use of the Private Use Area blocks of Unicode.

Icons that represent existing emoji are to use code points of such emoji. Custom icons are to be stored at U+E700 to U+E7FF.

What fonts use icons and what codepoints they are assigned are defined in config.json

