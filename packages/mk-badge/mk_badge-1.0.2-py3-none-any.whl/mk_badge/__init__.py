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

from collections import namedtuple

import cairo

Point = namedtuple("Point", ["x", "y"])
Connector = namedtuple("Connector", ["x", "y", "func", "pre_args"])


class Path:

    def __init__(self, context):
        """
        :type context: cairo.Context
        """
        self.point_ops = []
        self.context = context
        self.close = False

        self.fill = False
        self.fill_source = None
        self.fill_color_t = (0, 0, 0)

        self.stroke = True
        self.stroke_source = None
        self.stroke_color_t = (0, 0, 0)

    def add_point(self, x, y, func="line_to", pre_args=tuple()):
        self.point_ops.append(Connector(x, y, func, pre_args))

    def __enter__(self):
        self.context.new_path()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._draw()
        if self.close:
            self.context.close_path()

        self._fill()
        self._stroke()

    def _fill(self):
        if not self.fill:
            return

        self._set_source("fill")

        if self.stroke:
            self.context.fill_preserve()
        else:
            self.context.fill()

    def _stroke(self):
        if not self.stroke:
            return

        self._set_source("stroke")

        self.context.stroke()

    def _set_source(self, _type):
        source = getattr(self, "%s_source" % _type)
        color_t = getattr(self, "%s_color_t" % _type)

        if source:
            self.context.set_source(source)
        elif color_t:
            if len(color_t) == 3:
                self.context.set_source_rgb(*color_t)
            elif len(color_t) == 3:
                self.context.set_source_rgb(*color_t)
            else:
                raise ValueError("Provide a tuple of length 3 or 4 for the color of %s" % _type)

    def _draw(self):
        for op in self.point_ops:
            func = getattr(self.context, op.func)
            func(*(op.pre_args + (op.x, op.y)))


class ButtonSideConfig:
    def __init__(self, text, text_color=(0, 0, 0), stroke_color=(0, 0, 0), fill_color=(1, 1, 1)):
        self.text = text
        self.text_color = text_color
        self.stroke_color = stroke_color
        self.fill_color = fill_color


FontConfig = namedtuple("FontConfig", [
    "font",
    "size"
])


class SplitButton:
    """
    A button with a left and right text, split in two by a slash "/" (in that manner)
    """

    def __init__(self,
                 left_config, right_config, font_config, border_radius,
                 padding=10,
                 spaces_between=3):
        """
        @type left_config:  ButtonSideConfig
        @type right_config: ButtonSideConfig
        @type font_config: FontConfig
        @type border_radius: int
        @param padding: Padding around the text in the button
        @type padding: int
        @param spaces_between: The number of spaces between the left and right text
        @type spaces_between: int
        """
        self.left_config = left_config
        self.right_config = right_config
        self.font_config = font_config
        self.radius = border_radius
        self.padding = padding
        self.spaces_between = spaces_between

        self.text = self.left_config.text + " " * self.spaces_between + self.right_config.text

    def calc_dimensions(self):
        """
        Calculate the dimensions of the text + its padding that will be used as the dimensions of the button
        @rtype float, float
        """
        width = 0
        height = 0
        with cairo.SVGSurface(None, width, height) as surface:
            context = cairo.Context(surface)
            self._contextualize_font(context)
            extents = context.text_extents(self.text)
            width = extents.width
            height = extents.height

        total_padding = self.padding * 2

        return width + total_padding, height + total_padding

    def draw(self, context, width, height):
        """
        Draw the button into a given context.

        @type context: cairo.Context
        @type width: float
        @type height: float
        """
        self._contextualize_font(context)
        text = self.text

        # Split like a slash (/) through the button
        left_width = context.text_extents(self.left_config.text + ".").width + self.padding
        right_width = context.text_extents(self.right_config.text + ".").width + self.padding
        split_top = 1 - (right_width / width)
        split_bottom = left_width / width

        # Left button
        with Path(context) as left:
            left.close = True
            left.fill = True
            left.stroke_color_t = self.left_config.stroke_color
            left.fill_color_t = self.left_config.fill_color

            left.add_point(0, height - self.radius, "move_to")
            left.add_point(self.radius, height, "curve_to", (
                0, height,
                0, height,
            ))
            left.add_point(width * split_bottom, height)
            left.add_point(width * split_top, 0)
            left.add_point(self.radius, 0)
            left.add_point(0, self.radius, "curve_to", (
                0, 0,
                0, 0,
            ))

        # Left button
        with Path(context) as right:
            right.close = True
            right.fill = True
            right.stroke_color_t = self.right_config.stroke_color
            right.fill_color_t = self.right_config.fill_color

            right.add_point(width * split_bottom, height, "move_to")
            right.add_point(width - self.radius, height)
            right.add_point(width, height - self.radius, "curve_to", (
                width, height,
                width, height,
            ))

            right.add_point(width, self.radius)
            right.add_point(width - self.radius, 0, "curve_to", (
                width, 0,
                width, 0,
            ))
            right.add_point(width * split_top, 0)

        context.move_to(self.padding, height - self._find_text_rel_y())

        context.set_source_rgb(*self.left_config.text_color)
        context.show_text(self.left_config.text)
        context.show_text(" " * self.spaces_between)

        context.set_source_rgb(*self.right_config.text_color)
        context.show_text(self.right_config.text)

    def _find_text_rel_y(self):
        """
        Finds y to center the text horizontally in the button

        This is necessary because the coordinate used to determine where the text will be written
         makes a horizontal line upon which letters will be written.
        Letter that go below that line mean that coordinate is not the lowest point of the text!

        So, here we create a path from text and get the lowest most point.
        Using that and the padding, we now know where to position out text
        :return:
        :rtype:
        """
        with cairo.SVGSurface(None, 1000, 1000) as surface:
            context = cairo.Context(surface)
            self._contextualize_font(context)

            # Draw text at origin so we won't need any additionally transformations
            #  to find the lowest point
            context.new_path()
            context.move_to(0, 0)
            context.text_path(self.text)
            m = 0

            # Only these two provide an x and y tuple
            # Curves have a 6-tuple
            # https://pycairo.readthedocs.io/en/latest/reference/enums.html#cairo.PathDataType
            acceptable_type = (cairo.PATH_MOVE_TO, cairo.PATH_LINE_TO)

            # Copy-flat should get rid of curve types
            for type, points in context.copy_path_flat():
                if type in acceptable_type:
                    m = max(m, points[1])
            return self.padding + m

    def _contextualize_font(self, context):
        """
        Applies the font config in the context

        @type context: cairo.Context
        """
        context.set_font_size(self.font_config.size)
        context.select_font_face(self.font_config.font)
