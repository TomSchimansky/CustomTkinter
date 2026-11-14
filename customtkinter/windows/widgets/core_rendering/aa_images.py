"""
Antialiased shapes as small PNG images for the 'image_shapes' drawing method.

Tk blends the semi-transparent edge pixels of PNG images with everything below them on the canvas.
This works with every Tk 8.6 and 9 build, also with Tk builds on Linux that have no Xft support and
therefore can't render the CustomTkinter_shapes_font smoothly. Only the standard library is used,
so there is no dependency on Pillow.

The alpha value of every pixel is calculated from the distance of the pixel center to the edge of
the shape, which gives a smooth edge with a width of one pixel.
"""

import math
import zlib
import struct
import base64
from typing import Tuple, List, Sequence

RGB = Tuple[int, int, int]


def _alpha(coverage: float) -> int:
    if coverage <= 0:
        return 0
    if coverage >= 1:
        return 255
    return round(coverage * 255)


def _encode_png(width: int, height: int, rgb: RGB, alpha_rows: Sequence[Sequence[int]]) -> bytes:
    """ returns a base64 encoded RGBA PNG with one color and the given alpha values """
    color = bytes(rgb)
    pixels = [color + bytes((alpha,)) for alpha in range(256)]
    raw = b"".join(b"\x00" + b"".join(pixels[alpha] for alpha in row) for row in alpha_rows)

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw))
           + chunk(b"IEND", b""))
    return base64.b64encode(png)


def circle_image_size(radius: float) -> int:
    """ side length of the square circle image, always even so that it can be centered on a pixel corner """
    return 2 * math.ceil(radius)


def circle_png(radius: float, rgb: RGB) -> bytes:
    size = circle_image_size(radius)
    half = size // 2

    # calculate one quarter and mirror it, the circle center is in the middle of the image
    quarter: List[List[int]] = []
    for y in range(half):
        distance_y = half - (y + 0.5)
        row = []
        for x in range(half):
            distance_x = half - (x + 0.5)
            row.append(_alpha(radius - math.sqrt(distance_x * distance_x + distance_y * distance_y) + 0.5))
        quarter.append(row)

    top_rows = [row + row[::-1] for row in quarter]
    return _encode_png(size, size, rgb, top_rows + top_rows[::-1])


def _distance_to_segment(px: float, py: float, ax: float, ay: float, bx: float, by: float) -> float:
    dx, dy = bx - ax, by - ay
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        t = 0
    else:
        t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / length_squared))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def shape_points(kind: str, size: float) -> List[Tuple[float, float]]:
    """ points of the line shapes relative to their center, fitted to the glyphs of the CustomTkinter_shapes_font """
    if kind == "checkmark":
        radius = size / 2.8
        return [(radius, -radius), (-radius / 4, radius * 0.8), (-radius, radius / 6)]
    elif kind == "dropdown_arrow":
        return [(-size * 0.4, -size * 0.16), (0, size * 0.16), (size * 0.4, -size * 0.16)]
    raise ValueError(f"unknown shape '{kind}'")


def shape_image_size(kind: str, size: float, line_width: float) -> int:
    """ side length of the square shape image, always even """
    extent = max(max(abs(x), abs(y)) for x, y in shape_points(kind, size)) + line_width / 2 + 1
    return 2 * math.ceil(extent)


def shape_png(kind: str, size: float, line_width: float, offset_x: float, offset_y: float, rgb: RGB) -> bytes:
    """ line shape with round caps and joins, the center of the shape is shifted by offset_x, offset_y (0 <= offset < 1)
        from the middle of the image to place it on fractional canvas coordinates """
    image_size = shape_image_size(kind, size, line_width)
    center_x, center_y = image_size / 2 + offset_x, image_size / 2 + offset_y
    points = [(center_x + x, center_y + y) for x, y in shape_points(kind, size)]
    segments = list(zip(points[:-1], points[1:]))
    half_line_width = line_width / 2

    rows = []
    for y in range(image_size):
        row = []
        for x in range(image_size):
            distance = min(_distance_to_segment(x + 0.5, y + 0.5, ax, ay, bx, by) for (ax, ay), (bx, by) in segments)
            row.append(_alpha(half_line_width - distance + 0.5))
        rows.append(row)
    return _encode_png(image_size, image_size, rgb, rows)
