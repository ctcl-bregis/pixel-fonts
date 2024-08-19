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
Each icon directory has subdirectories

- emoji - Icons that represent existing emoji
- logos - Icons that represent online services and companies
- system - Made specifically for use in embedded devices such as the OLED display on MediaCow Touch 2.

### Embedded Icons in Fonts
Fonts that share the same resolution as an icon pack are to have icons embedded in the font.

Icons that represent existing emoji are to use code points of such emoji. Custom icons are to be stored at U+E700 to U+E7FF.

What fonts use icons and what codepoints they are assigned are defined in config.json

