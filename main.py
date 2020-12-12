import argparse
import getpass
import os
import zipfile

import randomcolor
from cairosvg import svg2png

from utils import utils, types


def main(hue=None, luminosity="dark", count=500, seed=None):
    utils.clear_tmpdir()
    print("Generating")
    color_generator = randomcolor.RandomColor(seed=seed)
    rand_color = color_generator.generate(hue=hue, luminosity=luminosity, count=count * 3, format_="rgbArray")
    groups = utils.generate_groups(rand_color, 3)
    palette_groups = []
    for palette in groups:
        sorted_palette = utils.sort_colors(palette)
        palette_groups.append([types.Color(x[0], x[1], x[2]) for x in sorted_palette])

    sheet = ""
    sheet_b = ""
    metadata = ""
    preview = ""

    with open("files/generated.css", "r") as f:
        sheet = f.read()
    with open("files/generated_border.css", "r") as f:
        sheet_b = f.read()
    with open("files/metadata.json", "r") as f:
        metadata = f.read()
    with open("files/preview.svg", "r") as f:
        preview = f.read()

    for palette in palette_groups:
        c1 = palette[0].hex
        c2 = palette[1].hex
        c3 = palette[2].hex
        palette[2].darken_color(factor=0.1)
        c4 = palette[2].hex
        palette[1].darken_color(factor=0.1)
        c5 = palette[1].hex

        c1_id = "%c1%"
        c2_id = "%c2%"
        c3_id = "%c3%"
        c4_id = "%c4%"
        c5_id = "%c5%"
        gen_id = "%genID%"
        with open("tmp/generated.css", "w+") as f:
            f.write(
                sheet.replace(c1_id, c1).replace(c2_id, c2).replace(c3_id, c3).replace(c4_id, c4).replace(c5_id, c5))
        with open("tmp/generated_border.css", "w+") as f:
            f.write(sheet_b.replace(c1_id, c1).replace(c3_id, c3))
        with open("tmp/metadata.json", "w+") as f:
            f.write(metadata.replace(gen_id, utils.generate_id(5)).replace("%username%", getpass.getuser()).replace(
                "%isLight%", "true" if luminosity in ["bright", "light"] else "false"))

        svg = preview.replace(c1_id, c1).replace(c2_id, c2).replace(c3_id, c3)

        file_id = utils.generate_id(8)
        with zipfile.ZipFile(f"tmp/0x{file_id}.zip", "w") as zipObj:
            for folderName, subfolders, filenames in os.walk("tmp/"):
                for filename in filenames:
                    if filename.endswith(".css") or filename.endswith(".json"):
                        if not filename.endswith(".gitkeep"):
                            filePath = os.path.join(folderName, filename)
                            zipObj.write(filePath, os.path.basename(filePath))

        svg2png(bytestring=svg, write_to=f"tmp/0x{file_id}")

    print("Packing Themes")
    pack_id = utils.generate_id(10)
    with zipfile.ZipFile(f"out/Gen{pack_id}.pack", "w") as zipObj:
        for folderName, subfolders, filenames in os.walk("tmp/"):
            for filename in filenames:
                if not filename.endswith(".css") and not filename.endswith(".json") and not filename.endswith(".gitkeep"):
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath, os.path.basename(filePath))

    utils.clear_tmpdir()
    print(f"Generated {count} themes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hue",
                        help="Controls the hue of the generated color. You can pass a string representing a color name: red, orange, yellow, green, blue, purple, pink and monochrome are currently supported.")
    parser.add_argument("-l", "--luminosity",
                        help="Controls the luminosity of the generated color. You can specify a string containing bright, light or dark.")
    parser.add_argument("-c", "--count", help="An integer which specifies the number of themes to generate", type=int)
    parser.add_argument("-s", "--seed",
                        help="An integer or string which when passed will cause randomColor to return the same color each time.")

    args = parser.parse_args()
    hue = None
    luminosity = None
    seed = args.seed
    count = args.count or 500
    if args.hue is not None and args.hue in ["red", "orange", "yellow", "purple", "pink", "monochrome"]:
        hue = args.hue
    if args.luminosity is not None and args.luminosity in ["bright", "light", "dark"]:
        luminosity = args.luminosity
    main(hue, luminosity, count, seed)
