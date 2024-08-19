# Pixel Fonts - CTCL 2022-2024
# Purpose: Build script for all fonts and icons
# Created: July 7, 2024
# Modified: July 12, 2024

import io
import json
import os
import shutil

import bdfparser
import drawsvg
import fontforge

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def replace_right(text, old, new, count=-1):
    return text[::-1].replace(old[::-1], new[::-1], count)[::-1]

def piskelc2svg(filepath, newfilepath):
    with open(filepath) as f:
        content = f.readlines()

    width = int(content[3].split(" ")[2])
    height = int(content[4].split(" ")[2])

    data = "".join(content[10:]).replace("\n", "").split("}")[0].split(", ")
    data = [pix[2:] for pix in data]
    # Data is exported for little-endian CPU architectures and must be "reversed"
    tmp = []
    for pix in data:
        ba = bytearray.fromhex(pix)
        ba.reverse()
        tmp.append(ba.hex())
    data = tmp

    rows = chunks(data, width)

    d = drawsvg.Drawing(width * 64, height * 64)

    ypos = 0
    xpos = 0
    for y in rows:
        for x in y:
            color = f"#{x[:-2]}"
            opacity = int(x[-2:], 16) / 256
            if opacity > 0:
                d.append(drawsvg.Rectangle(xpos, ypos, 64, 64, fill = color, fill_opacity = opacity))
            xpos += 64
        xpos = 0
        ypos += 64

    d.save_svg(newfilepath)

    os.system(f"inkscape --export-type=svg --export-plain-svg --export-overwrite -g --batch-process {newfilepath} --verb='EditSelectAll;SelectionUnion;FileSave'")

def bdf2vecs(path, output, exts):
    bdffont = bdfparser.Font(path)
    glyphs = bdffont.glyphs

    ttffont = fontforge.font()
    ttffont.encoding = "UnicodeFull"
    ttffont.fontname = bdffont.props["font_name"]
    ttffont.familyname = bdffont.props["face_name"]
    ttffont.fullname = bdffont.headers["fontname"]
    ttffont.ascent = 64 * int(bdffont.props["font_ascent"])
    ttffont.descent = 64 * int(bdffont.props["font_descent"])

    svgglyphs = {}
    for x, y in glyphs.items():
        glyph = bdffont.glyphbycp(y[1])

        glyph_width = glyph.meta["dwx0"]
        glyph_height = int(bdffont.props["pixel_size"])

        if glyph_width > 1:
            rows = []
            for i in range((glyph_height - glyph.meta["bbh"]) - int(bdffont.props["font_descent"]) - glyph.meta["bbyoff"]):
                rows.append("0" * glyph.meta["dwx0"])       

            for datarow in glyph.meta["hexdata"]:
                if datarow == "00":
                    rows.append("0" * glyph.meta["dwx0"])
                else:
                    rows.append(("0" * glyph.meta["bbxoff"]) + str(bin(int(datarow, 16))[2:]).rjust(len(datarow) * 4, "0"))

            d = drawsvg.Drawing(glyph.meta["dwx0"] * 64, glyph_height * 64)
            ypos = 0
            xpos = 0
            notempty = False
            for row in rows:
                for pix in row:
                    if pix == "1":
                        notempty = True
                        d.append(drawsvg.Rectangle(xpos, ypos, 64, 64, fill = "#000000", fill_opacity = 255))
                    xpos += 64
                xpos = 0
                ypos += 64
        

            d.save_svg("/dev/shm/" + y[0] + ".svg")

            g = ttffont.createMappedChar(y[1])
            if notempty:
                g.importOutlines("/dev/shm/" + str(y[0]) + ".svg", ('removeoverlap', 'correctdir'))
            g.width = 64 * (int(glyph.meta["dwx0"]))
            g.removeOverlap()

            for ext in exts:
                ttffont.generate(f"{output}.{ext}")

with open("config.json") as f:
    cfg = dict(json.loads(f.read()))

#if os.path.exists("build/"):
#    shutil.rmtree("build/")

if not os.path.exists("build/"):
    os.mkdir("build/")

for iconset in cfg["icons"]["list"]:
    filelist = [f for f in os.listdir(iconset) if os.path.isfile(os.path.join(iconset, f))]
    filelist = [f for f in filelist if f.endswith(".c")]

    if not os.path.exists(f"build/{iconset}"):
        os.mkdir(f"build/{iconset}/")

    #for icon in filelist:
    #    piskelc2svg(f"{iconset}/{icon}", f"build/{iconset}/" + icon[:-2] + ".svg")

    
for (name, data) in cfg["fonts"].items():
    if not os.path.exists(f"build/{name}"):
        os.mkdir(f"build/{name}")

    for (variant, path) in data["variants"].items(): 
        sfd = fontforge.open(f"{name}/{path}")

        if len(sfd.bitmapSizes) == 1:
            bmpres = sfd.bitmapSizes[0]
        elif len(sfd.bitmapSizes) > 1: 
            print(f"Error: font variant {variant} has more than one bitmap strike resolution, skipping")
            continue
        elif len(sfd.bitmapSizes) < 1:
            print(f"Error: font variant {variant} does not have any bitmap strikes, skipping")
            continue

        sfd.generate(f"build/{name}/{name}-{variant}.bdf", str(bmpres)) 
        os.rename(f"build/{name}/{name}-{variant}-{bmpres}.bdf", f"build/{name}/{name}-{variant}.bdf")
        bdf2vecs(f"build/{name}/{name}-{variant}.bdf", f"build/{name}/{name}-{variant}", cfg["vecs"])


            


