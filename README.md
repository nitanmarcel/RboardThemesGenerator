# Rboard Themes Generator
A small funny themes generator for [Rboard Themes](https://forum.xda-developers.com/t/module-rboard-themes-more-themes-for-gboard.3840354/)

## Installation

```shell
git clone https://github.com/nitanmarcel/RboardThemesGenerator
python3 -m pip install -r requirements.txt
python3 main.py --count 100 # For 100 themes
```

### Usage

```shell
usage: main.py [-h] [--hue HUE] [-l LUMINOSITY] [-c COUNT] [-s SEED]

optional arguments:
  -h, --help            show this help message and exit
  --hue HUE             Controls the hue of the generated color. You can pass a string representing a color name: red, orange, yellow, green, blue, purple, pink
                        and monochrome are currently supported.
  -l LUMINOSITY, --luminosity LUMINOSITY
                        Controls the luminosity of the generated color. You can specify a string containing bright, light or dark.
  -c COUNT, --count COUNT
                        An integer which specifies the number of themes to generate
  -s SEED, --seed SEED  An integer or string which when passed will cause randomColor to return the same color each time.
```

