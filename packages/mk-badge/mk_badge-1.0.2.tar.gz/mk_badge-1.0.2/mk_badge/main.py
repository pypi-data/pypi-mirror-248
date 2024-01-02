"""
mk_badge
Copyright (C) 2019 LoveIsGrief

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import io
import sys

import cairo
from importlib import resources

from mk_badge import SplitButton, ButtonSideConfig, FontConfig


def _main(args):
    button = SplitButton(
        ButtonSideConfig(
            args.text[0],
            stroke_color=args.left_stroke_color, text_color=args.left_text_color, fill_color=args.left_fill_color
        ),
        ButtonSideConfig(
            args.text[1],
            stroke_color=args.right_stroke_color, text_color=args.right_text_color, fill_color=args.right_fill_color
        ),
        FontConfig(args.font, args.font_size),
        args.border_radius, spaces_between=args.spaces,
        padding=args.padding
    )

    output = args.filename
    if not output:
        output = io.BytesIO()
    width, height = button.calc_dimensions()
    with cairo.SVGSurface(output, width, height) as surface:
        context = cairo.Context(surface)
        context.set_line_width(1)

        button.draw(context, width, height)

    # Output to stdout if no filename was passed
    if isinstance(output, io.BytesIO):
        output.seek(0)
        sys.stdout.buffer.write(output.read())


def main():
    import argparse

    def rgb_color(arg):
        try:
            r, g, b = [(int(val) % 256) / 255 for val in arg.split(",")]
            return r, g, b
        except:
            raise argparse.ArgumentTypeError("RGB = 3 values, separated by a comma and each 0-255")

    parser = argparse.ArgumentParser(
        "mk_badge",
        description="Makes SVG badges like the ones made by travis-ci to show the status of a build."
                    "The size of the button will be calculated from provided options",
    )

    version = resources.files("mk_badge").joinpath("VERSION").read_bytes().decode()
    parser.add_argument(
        "-v", "--version", action="version",
        version="%(prog)s " + version,
        help="Prints the version"
    )

    for position in ("left", "right"):
        group = parser.add_argument_group("%s_text" % position)
        group.add_argument(
            "--%s-text-color" % position,
            default="0,0,0",
            type=rgb_color,
            help="The RGB text color of the %s text. Default is 0,0,0"
        )
        group.add_argument(
            "--%s-fill-color" % position,
            default="255,255,255",
            type=rgb_color,
            help="The RGB color used to fill the the %s split of the button. Default is 255,255,255"
        )
        group.add_argument(
            "--%s-stroke-color" % position,
            default="0,0,0",
            type=rgb_color,
            help="The RGB color used to stroke the the %s split of the button. Default is 0,0,0"
        )

    font_group = parser.add_argument_group("font", "options for the font")
    font_group.add_argument("--font", default="Arial", help="The actual font to use")
    font_group.add_argument("--font-size", default="14", type=int, help="How big the font should be")

    parser.add_argument("-p", "--padding",
                        default="10",
                        type=int, help="How many pixels should be added around the text")
    parser.add_argument("-s", "--spaces",
                        default="3",
                        type=int, help="How many pixels should be added around the text")
    parser.add_argument("-b", "--border-radius",
                        default="10",
                        type=int, help="The curvature of the button")
    parser.add_argument("-f", "--filename",
                        help="Where to store the SVG")
    parser.add_argument("text", nargs=2, help="The left and right text")

    _main(parser.parse_args())


if __name__ == '__main__':
    main()
