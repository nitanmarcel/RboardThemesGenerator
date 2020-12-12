import os
from colorsys import rgb_to_hls, hls_to_rgb, rgb_to_hsv
from webcolors import rgb_to_hex
from uuid import uuid4


def generate_groups(lst, N):
    return [lst[n:n + N] for n in range(0, len(lst), N)]


def adjust_color_lightness(r, g, b, factor):
    h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    l = max(min(l * factor, 1.0), 0.0)
    r, g, b = hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)


def darken_color(r, g, b, factor=0.1):
    return adjust_color_lightness(r, g, b, 1 - factor)


def sort_colors(palette):
    palette.sort(key=lambda rgb: rgb_to_hsv(*rgb))
    return palette


def generate_id(lenght=20):
    return uuid4().hex[:lenght]  # + ''.join(str(random.randint(0,10)) for x in range(6))

def clear_tmpdir():
    for folderName, subfolders, filenames in os.walk("tmp/"):
        for filename in filenames:
            if not filename.endswith(".gitkeep"):
                filePath = os.path.join(folderName, filename)
                os.remove(filePath)
