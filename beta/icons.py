"""Draws the Reef Key mark and writes the icon set.

The mark is a key whose bow is a ring and whose teeth read as the notches on a
test strip, sitting over two lines of water. Drawn at 8x and downsampled, so
the edges are clean without needing an SVG rasteriser.
"""
from PIL import Image, ImageDraw

INK = (6, 11, 16)
CARD = (13, 21, 28)
CYAN = (47, 224, 198)

S = 1024
F = 4                      # supersample factor
W = S * F


def wave(d, y, amp, width, colour, alpha):
    """A smooth swell across the tile, drawn as a polyline so the crests join
    cleanly rather than meeting at the flat ends of separate arcs."""
    import math
    pts = []
    steps = 400
    for i in range(steps + 1):
        x = W * i / float(steps)
        pts.append((x, y + amp * math.sin(2 * math.pi * (x / (W / 2.0)))))
    d.line(pts, fill=colour + (alpha,), width=width, joint='curve')


def build(size):
    img = Image.new('RGBA', (W, W), CARD + (255,))
    d = ImageDraw.Draw(img, 'RGBA')

    # a little depth: the ground darkens towards the bottom of the tile
    for i in range(W):
        t = i / float(W)
        shade = tuple(int(CARD[c] + (INK[c] - CARD[c]) * t) for c in range(3))
        d.line([(0, i), (W, i)], fill=shade + (255,))

    # water
    wave(d, W * 0.745, W * 0.034, int(W * 0.022), CYAN, 150)
    wave(d, W * 0.865, W * 0.030, int(W * 0.019), CYAN, 80)

    # key: ring bow
    cx, cy = W * 0.5, W * 0.315
    r = W * 0.168
    lw = int(W * 0.064)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=CYAN + (255,), width=lw)

    # stem
    top = cy + r - lw * 0.35
    bot = W * 0.745
    d.rounded_rectangle([cx - lw / 2.0, top, cx + lw / 2.0, bot],
                        radius=lw / 2.0, fill=CYAN + (255,))

    # teeth, stepping shorter down the stem
    for frac, length in ((0.575, 0.130), (0.685, 0.096)):
        y = W * frac
        d.rounded_rectangle([cx - lw / 2.0, y - lw / 2.0,
                             cx + W * length, y + lw / 2.0],
                            radius=lw / 2.0, fill=CYAN + (255,))

    return img.resize((size, size), Image.LANCZOS).convert('RGB')


for name, size in [('icon-1024.png', 1024), ('icon-512.png', 512),
                   ('apple-touch-icon.png', 180), ('icon-192.png', 192)]:
    build(size).save('/mnt/user-data/outputs/' + name, 'PNG')
    print('%-22s %dx%d' % (name, size, size))
