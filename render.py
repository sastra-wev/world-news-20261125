"""Pressroom: the small drawing toolkit behind the one-page newspaper.

Everything in this module is generic page furniture -- type handling,
word wrapping, rules, stamps and simple chart marks.  It knows nothing
about today's stories; main.py brings the news and arranges the page
with these tools.  Only Pillow is used, and every operation is a pure
function of its inputs, so a page built with it is byte-stable.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Ink and paper
# ---------------------------------------------------------------------------

PAPER = (244, 239, 227)        # warm newsprint
CARD = (252, 249, 240)         # lighter stock for raised panels
INK = (26, 24, 22)             # near-black body ink
FADED = (108, 101, 91)         # aged grey for furniture text
CRIMSON = (172, 30, 38)        # the one loud colour on the page
MIDNIGHT = (17, 34, 66)        # night sky / chart field
GOLD = (198, 148, 44)
EARTH = (96, 71, 45)
EARTH_DARK = (63, 45, 29)
WATER = (56, 108, 168)
BRICK = (148, 119, 95)
MORTAR = (104, 82, 60)
SMOKE = (206, 204, 198)

# ---------------------------------------------------------------------------
# Type cupboard.  Each entry is a family in the order we prefer to find it.
# ---------------------------------------------------------------------------

_TYPE_CUPBOARD = {
    "serif": (
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ),
    "serif-bold": (
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    ),
    "serif-italic": (
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ),
    "sans": (
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ),
    "sans-bold": (
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ),
}


class Pressroom:
    """One sheet of paper plus the tools to set type and draw on it."""

    def __init__(self, width, height, ground=PAPER):
        self.width = width
        self.height = height
        self.img = Image.new("RGB", (width, height), ground)
        self.pen = ImageDraw.Draw(self.img)
        self._type_cache = {}

    # -- type ------------------------------------------------------------

    def type(self, kind, size):
        """Return (and cache) a font of the named kind at the given size."""
        key = (kind, size)
        if key not in self._type_cache:
            face = None
            for path in _TYPE_CUPBOARD[kind]:
                try:
                    face = ImageFont.truetype(path, size)
                    break
                except OSError:
                    continue
            if face is None:  # last resort: PIL's built-in bitmap face
                face = ImageFont.load_default()
            self._type_cache[key] = face
        return self._type_cache[key]

    def measure(self, text, font):
        return self.pen.textlength(text, font=font)

    def fit(self, text, kind, start, limit):
        """Largest size <= start at which text still fits limit pixels."""
        size = start
        while size > 8:
            if self.measure(text, self.type(kind, size)) <= limit:
                break
            size -= 1
        return self.type(kind, size)

    # -- setting type ------------------------------------------------------

    def wrap(self, text, font, limit):
        """Greedy word wrap: split text into lines no wider than limit."""
        lines = []
        current = ""
        for word in text.split():
            trial = word if not current else current + " " + word
            if self.measure(trial, font) <= limit:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def set_block(self, x, y, text, font, limit, leading, ink=INK):
        """Set a wrapped paragraph with its top-left corner at (x, y)."""
        for line in self.wrap(text, font, limit):
            self.pen.text((x, y), line, font=font, fill=ink)
            y += leading
        return y

    def set_centered(self, cx, y, text, font, ink=INK):
        w = self.measure(text, font)
        self.pen.text((cx - w / 2, y), text, font=font, fill=ink)

    def set_right(self, x_right, y, text, font, ink=INK):
        w = self.measure(text, font)
        self.pen.text((x_right - w, y), text, font=font, fill=ink)

    # -- page furniture ----------------------------------------------------

    def rule(self, x0, x1, y, weight=2, ink=INK):
        self.pen.rectangle([x0, y, x1, y + weight - 1], fill=ink)

    def frame(self, x, y, w, h, fill=None, edge=None, weight=1):
        if fill is not None:
            self.pen.rectangle([x, y, x + w - 1, y + h - 1], fill=fill)
        if edge is not None:
            self.pen.rectangle([x, y, x + w - 1, y + h - 1],
                               outline=edge, width=weight)

    def paste_scene(self, scene, x, y):
        """Glue a separately drawn picture onto the page at (x, y)."""
        self.img.paste(scene, (x, y))
        # Pasting replaces the draw target's pixels; refresh the pen.
        self.pen = ImageDraw.Draw(self.img)

    # -- ornaments -----------------------------------------------------------

    def rubber_stamp(self, cx, cy, text, size, ink, angle=-11, pad=10):
        """A rotated, outlined stamp centred on (cx, cy)."""
        font = self.type("sans-bold", size)
        tw = int(self.measure(text, font))
        th = size + 2 * pad
        layer = Image.new("RGBA", (tw + 2 * pad + 8, th + 8), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.rectangle([3, 3, layer.width - 4, layer.height - 4],
                    outline=ink + (255,), width=4)
        d.text(((layer.width - tw) / 2, pad + 2), text, font=font,
               fill=ink + (255,))
        spun = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
        self.img.paste(spun, (int(cx - spun.width / 2),
                              int(cy - spun.height / 2)), spun)
        self.pen = ImageDraw.Draw(self.img)

    def barber_pole(self, x, y, length, thick, angle_deg, stripe=26,
                    first=(200, 44, 48), second=(246, 244, 238)):
        """A red-and-white striped barrier arm, drawn already rotated."""
        import math
        layer = Image.new("RGBA", (length, thick), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        pos = 0
        flip = False
        while pos < length:
            d.rectangle([pos, 0, min(pos + stripe, length) - 1, thick - 1],
                        fill=(first if not flip else second) + (255,))
            pos += stripe
            flip = not flip
        d.rectangle([0, 0, length - 1, thick - 1], outline=(30, 30, 30, 255))
        spun = layer.rotate(angle_deg, expand=True, resample=Image.BICUBIC)
        self.img.paste(spun, (int(x), int(y)), spun)
        self.pen = ImageDraw.Draw(self.img)
        return math.radians(angle_deg)

    def brickwork(self, x, y, w, h, course=16, brick=46):
        """Courses of bricks filling the box (x, y, w, h)."""
        row = 0
        yy = y
        while yy < y + h:
            offset = 0 if row % 2 == 0 else brick // 2
            xx = x - offset
            while xx < x + w:
                self.pen.rectangle(
                    [max(xx, x), yy, min(xx + brick - 2, x + w - 1),
                     min(yy + course - 2, y + h - 1)], fill=BRICK)
                xx += brick
            yy += course
            row += 1
        self.pen.rectangle([x, y, x + w - 1, y + h - 1], outline=MORTAR)

    def downtrend(self, x, y, w, h, ink, label=None, label_ink=None):
        """A jagged falling market line inside the box, with a label."""
        pts = [(0.02, 0.16), (0.16, 0.10), (0.30, 0.30), (0.44, 0.26),
               (0.58, 0.44), (0.70, 0.40), (0.83, 0.58), (0.97, 0.86)]
        coords = [(x + fx * w, y + fy * h) for fx, fy in pts]
        self.pen.line(coords, fill=ink, width=4)
        for px, py in coords:
            self.pen.ellipse([px - 3, py - 3, px + 3, py + 3], fill=ink)
        ax, ay = coords[-1]
        self.pen.polygon([(ax, ay), (ax - 13, ay - 9), (ax - 4, ay - 14)],
                         fill=ink)
        if label:
            font = self.type("sans-bold", 15)
            lx = x + w - self.measure(label, font) - 8
            self.pen.text((lx, y + 6), label, font=font,
                          fill=label_ink or ink)


def scene_canvas(w, h, ground):
    """A blank off-page picture and its own little pressroom."""
    sheet = Pressroom(w, h, ground)
    return sheet
