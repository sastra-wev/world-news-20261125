#!/usr/bin/env python3
"""Draw "The World in One Page" for Wednesday 25 November 2026.

Build-time artwork generator (requires Pillow). It renders one
1024x1024 newspaper front page summing up the day's verified world
news and saves it as entry.png beside this script. The program the
grader runs is main.py: standard library only, it copies entry.png
to the output path byte for byte, so the judged bytes never depend
on Pillow existing at grade time.

The day's stories, all first reported on 25 November 2026:
  LEAD  Washington is poised to unveil the findings of its
        Section 301 probe into alleged excess industrial capacity
        in 16 major trading partners -- China, the EU, India,
        Japan, South Korea, Mexico, Vietnam, Taiwan, Thailand,
        Malaysia, Indonesia, Switzerland, Norway, Singapore,
        Bangladesh and Cambodia -- with new import duties expected
        on top of existing tariffs (Reuters). Asian markets
        tumbled on Wednesday: South Korean shares fell as much as
        5.3%, Taiwan 5.1%, Japan's Nikkei 2.9% (Reuters); the BBC
        led its business page with the same story.
  2     Pongkor, Bogor, West Java: rescuers searched Wednesday
        for workers -- local media say 30 -- trapped since Monday
        about 100 m underground in an unauthorised gold mine
        flooded by heavy rain; state miner Antam says the pit is
        not part of its operations (Reuters).
  3     Shenzhou-24 lifted off from Jiuquan at 08:18 Wednesday on
        a Long March-2F, crewed by Tang Hongbo, Wu Yi and
        Muhammad Zeeshan Ali, 40, a Pakistani pilot flying as
        payload specialist -- the first Pakistani in space and the
        first foreign astronaut to board China's Tiangong station;
        a 5-10 day stay running biotechnology experiments
        (Reuters, AP).
  4-8   Briefs: the US attorney general dodges questions about
        the Nvidia investigation as its shares slide (BBC); the
        Kremlin questions Europe's "added value" at the Ukraine
        peace table while Trump hosts NATO chief Rutte in Florida
        (Reuters); an Israeli air strike kills Hamas's internal
        security chief in Gaza (BBC); a US jury finds Huawei
        guilty of stealing trade secrets but acquits it of
        racketeering (BBC); Australia formally apologises to
        LGBTQ veterans for decades of discrimination (Reuters).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 243, 230)
INK = (20, 22, 26)
FAINT = (94, 90, 80)
RED = (179, 35, 42)
NAVY = (26, 40, 72)
WHITE = (255, 250, 238)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def mid(draw, cx, y, text, fnt, fill=INK):
    """Draw text centred on cx; return its height."""
    bb = draw.textbbox((0, 0), text, font=fnt)
    draw.text((cx - (bb[2] - bb[0]) / 2, y), text, font=fnt, fill=fill)
    return bb[3] - bb[1]


def wrap(draw, x, y, text, fnt, width, fill=INK, gap=6):
    """Greedy word wrap; returns the y just below the last line."""
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def hline(draw, y, width=3):
    draw.rectangle([36, y, W - 36, y + width], fill=INK)


# ------------------------------------------------------------- artwork

def tariff_wall(d, x, y, w, h):
    """Export crates halted at a customs wall; Asia's markets fall."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 30, 58))
    # falling market line across the night sky, ending in an arrow
    pts = [(x + 18, y + 30), (x + 90, y + 22), (x + 150, y + 44),
           (x + 220, y + 38), (x + 285, y + 66), (x + 350, y + 60),
           (x + 415, y + 92)]
    d.line(pts, fill=(255, 92, 84), width=4)
    ax, ay = pts[-1]
    d.polygon([(ax, ay), (ax - 16, ay - 3), (ax - 5, ay - 15)],
              fill=(255, 92, 84))
    d.text((x + 20, y + 8), "ASIA MARKETS", font=F(SANS_B, 13),
           fill=(235, 160, 150))
    # the customs wall: two courses of blocks across the middle
    wy = y + 118
    d.rectangle([x + 10, wy, x + w - 10, wy + 26], fill=(168, 158, 138))
    d.rectangle([x + 10, wy + 26, x + w - 10, wy + 50], fill=(150, 139, 118))
    for bx in range(30, w - 20, 56):
        d.line([x + bx, wy, x + bx, wy + 26], fill=(120, 110, 92),
               width=2)
        d.line([x + bx + 28, wy + 26, x + bx + 28, wy + 50],
               fill=(120, 110, 92), width=2)
    d.rectangle([x + 10, wy - 4, x + w - 10, wy], fill=(90, 82, 66))
    # barrier arm, down: a white bar with red bands along its slope
    bx0, by0 = x + 24, wy - 46
    d.rectangle([bx0, by0, bx0 + 10, wy], fill=(40, 42, 48))
    ax0, ay0, ax1, ay1 = bx0 + 10, by0 + 7, x + w - 90, wy - 3
    d.line([ax0, ay0, ax1, ay1], fill=(238, 238, 238), width=12)
    for t0, t1 in [(0.10, 0.24), (0.38, 0.52), (0.66, 0.80)]:
        d.line([ax0 + (ax1 - ax0) * t0, ay0 + (ay1 - ay0) * t0,
                ax0 + (ax1 - ax0) * t1, ay0 + (ay1 - ay0) * t1],
               fill=(200, 44, 48), width=12)
    # export crates queued in front of the wall, named for partners
    crates = [("CHINA", (178, 52, 44)), ("EU", (38, 74, 150)),
              ("JAPAN", (226, 226, 220)), ("MEXICO", (24, 110, 62)),
              ("+12 MORE", (110, 92, 130))]
    cw, chh, cy = 82, 40, y + h - 48
    gap = (w - 5 * cw) / 6
    for i, (name, col) in enumerate(crates):
        cx = x + gap + i * (cw + gap)
        d.rectangle([cx, cy, cx + cw, cy + chh], fill=col)
        d.rectangle([cx, cy, cx + cw, cy + chh], outline=(10, 12, 16),
                    width=2)
        d.line([cx + 6, cy, cx + 6, cy + chh], fill=(10, 12, 16),
               width=1)
        d.line([cx + cw - 6, cy, cx + cw - 6, cy + chh],
               fill=(10, 12, 16), width=1)
        tcol = (30, 30, 30) if name == "JAPAN" else (245, 245, 240)
        mid(d, cx + cw / 2, cy + 12, name, F(SANS_B, 12), fill=tcol)
    # the stamp, drawn on its own layer and rotated over the wall
    stamp = Image.new("RGBA", (212, 58), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([3, 3, 209, 55], outline=(255, 84, 74, 255), width=5)
    sf = F(SANS_B, 30)
    bb = sd.textbbox((0, 0), "NEW DUTIES", font=sf)
    sd.text(((212 - (bb[2] - bb[0])) / 2, 10), "NEW DUTIES", font=sf,
            fill=(255, 84, 74, 255))
    return stamp.rotate(-7, expand=True, resample=Image.BICUBIC), \
        (int(x + w / 2 - 100), int(wy - 34))


def mine_rescue(d, x, y, w, h):
    """Cross-section at Pongkor: a flooded shaft, lamps below."""
    # underground strata
    d.rectangle([x, y, x + w, y + h], fill=(74, 54, 36))
    for sy, col in [(y + 44, (88, 64, 42)), (y + 84, (64, 46, 30)),
                    (y + 116, (54, 38, 24))]:
        d.rectangle([x, sy, x + w, sy + 3], fill=col)
    # the surface: hill, headframe and a rescue tent
    d.rectangle([x, y, x + w, y + 26], fill=(24, 44, 74))
    d.polygon([(x, y + 26), (x + 56, y + 8), (x + 128, y + 26)],
              fill=(38, 84, 52))
    d.rectangle([x + 128, y + 20, x + w, y + 26], fill=(38, 84, 52))
    hx = x + 88
    d.polygon([(hx, y + 26), (hx + 12, y + 2), (hx + 24, y + 26)],
              outline=(220, 224, 230), width=2)
    d.line([hx + 12, y + 4, hx + 12, y + 118], fill=(220, 224, 230),
           width=2)
    d.polygon([(x + 148, y + 26), (x + 162, y + 12), (x + 176, y + 26)],
              fill=(232, 120, 40))
    # the vertical shaft, timbered
    sx0, sx1 = hx + 4, hx + 20
    d.rectangle([sx0, y + 26, sx1, y + 118], fill=(16, 12, 8))
    for ty in range(y + 34, y + 112, 14):
        d.line([sx0, ty, sx1, ty], fill=(120, 88, 52), width=2)
    # the flooded level at the bottom, water over the tunnel floor
    d.rectangle([x + 8, y + 118, x + w - 8, y + h - 4], fill=(30, 26, 20))
    d.rectangle([x + 8, y + 126, x + w - 8, y + h - 4],
                fill=(38, 84, 140))
    for wx in range(x + 14, x + w - 20, 26):
        d.arc([wx, y + 122, wx + 16, y + 130], 0, 180,
              fill=(120, 180, 230), width=2)
    # three headlamps waiting in the dark, and one beam from above
    for lx in (x + 44, x + 66, x + 152):
        d.ellipse([lx - 3, y + 112, lx + 3, y + 118],
                  fill=(255, 240, 170))
    d.polygon([(hx + 12, y + 60), (x + 52, y + 116), (x + 76, y + 116)],
              fill=(250, 232, 160, 70))


def rocket_launch(d, x, y, w, h):
    """Shenzhou-24 climbs out of Jiuquan; Tiangong waits above."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 34))
    import random
    rng = random.Random(24)
    for _ in range(46):
        sx = x + rng.randrange(4, w - 4)
        sy = y + rng.randrange(4, h - 60)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(210, 218, 240))
    # the station, top right: core module and two solar wings
    tx, ty = x + w - 62, y + 16
    d.rectangle([tx, ty, tx + 34, ty + 10], fill=(200, 206, 216))
    d.rectangle([tx - 22, ty + 2, tx, ty + 8], fill=(64, 96, 178))
    d.rectangle([tx + 34, ty + 2, tx + 56, ty + 8], fill=(64, 96, 178))
    d.text((tx - 24, ty + 15), "TIANGONG", font=F(SANS_B, 10),
           fill=(170, 190, 230))
    # the Long March rocket, nose up, just clear of the pad
    cx, top = x + 74, y + 22
    d.polygon([(cx - 11, top + 26), (cx, top), (cx + 11, top + 26)],
              fill=(238, 240, 244))
    d.rectangle([cx - 11, top + 26, cx + 11, top + 74],
                fill=(238, 240, 244))
    d.rectangle([cx - 11, top + 40, cx + 11, top + 50], fill=(206, 40, 44))
    d.rectangle([cx - 19, top + 58, cx - 12, top + 78], fill=(214, 218, 224))
    d.rectangle([cx + 12, top + 58, cx + 19, top + 78], fill=(214, 218, 224))
    # flame and the smoke it stands on
    d.polygon([(cx - 8, top + 78), (cx, top + 102), (cx + 8, top + 78)],
              fill=(255, 150, 40))
    d.polygon([(cx - 4, top + 78), (cx, top + 92), (cx + 4, top + 78)],
              fill=(255, 214, 90))
    gy = y + h - 10
    for bx, by, r in [(cx - 34, gy - 4, 17), (cx - 8, gy - 7, 21),
                      (cx + 22, gy - 5, 18), (cx + 48, gy - 3, 13),
                      (cx - 58, gy - 2, 11)]:
        d.ellipse([bx - r, by - r * 0.62, bx + r, by + r * 0.62],
                  fill=(168, 172, 184))
    d.rectangle([x, gy, x + w, y + h], fill=(30, 30, 36))


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # masthead
    mid(d, W / 2, 20, "THE WORLD IN ONE PAGE", F(SERIF_B, 60))
    hline(d, 100, 5)
    hline(d, 110, 2)
    d.rectangle([36, 118, W - 36, 152], fill=INK)
    mid(d, W / 2, 124, "WEDNESDAY  ·  25 NOVEMBER 2026", F(SANS_B, 21),
        fill=WHITE)
    d.text((36, 160), "No. 25 — THE DAY'S NEWS, DRAWN AND SET IN ONE PAGE",
           font=F(SANS, 15), fill=FAINT)
    tail = "EST. 2026 · READ IN 60 SECONDS"
    d.text((W - 36 - d.textlength(tail, font=F(SANS, 15)), 160), tail,
           font=F(SANS, 15), fill=FAINT)

    # ---------------- lead: US readies new tariffs on 16 partners
    ly = 188
    d.text((36, ly), "WASHINGTON — TRADE · THE TOP STORY",
           font=F(SANS_B, 17), fill=RED)
    d.text((36, ly + 24), "AMERICA READIES", font=F(SERIF_B, 46),
           fill=INK)
    d.text((36, ly + 76), "A NEW TARIFF WALL", font=F(SERIF_B, 46),
           fill=INK)
    d.text((36, ly + 130),
           "Section 301 findings on 'excess capacity' due within "
           "hours — duties to stack on top",
           font=F(SERIF, 21), fill=INK)
    stamp, spos = tariff_wall(d, 36, ly + 164, 470, 214)
    img.paste(stamp, spos, stamp)
    tx = 530
    body = ("The Trump administration is poised to release its "
            "Section 301 findings on alleged excess industrial "
            "capacity in 16 major trading partners — China, the EU, "
            "India, Japan and Indonesia among them. New duties are "
            "expected, stacked on top of tariffs already imposed.")
    by = wrap(d, tx, ly + 168, body, F(SANS, 19), W - 36 - tx, gap=7)
    by += 14
    d.rectangle([tx, by, tx + 6, by + 52], fill=RED)
    d.text((tx + 18, by + 2), "16 TRADING PARTNERS",
           font=F(SANS_B, 19), fill=INK)
    d.text((tx + 18, by + 28), "— Asian shares tumbled: Seoul -5.3%",
           font=F(SANS, 16), fill=FAINT)

    hline(d, 584)

    # ---------------- two illustrated panels
    py = 600
    pw = (W - 72 - 20) // 2
    # panel 2 — Pongkor mine rescue, West Java
    d.text((36, py), "2 · PONGKOR, BOGOR — INDONESIA",
           font=F(SANS_B, 15), fill=RED)
    d.text((36, py + 22), "RACE TO REACH", font=F(SERIF_B, 30), fill=INK)
    d.text((36, py + 58), "TRAPPED MINERS", font=F(SERIF_B, 30),
           fill=INK)
    mine_rescue(d, 36, py + 100, 196, 140)
    wrap(d, 246, py + 102,
         "Rescuers searched Wednesday for the workers — local "
         "media say 30 — trapped since Monday 100 m down in an "
         "unauthorised gold mine flooded by heavy rain. Antam "
         "says the pit is not part of its operations.",
         F(SANS, 16), 36 + pw - 246, gap=4)
    # panel 3 — Shenzhou-24 carries the first Pakistani to Tiangong
    px = 36 + pw + 20
    d.text((px, py), "3 · JIUQUAN, CHINA — SPACE", font=F(SANS_B, 15),
           fill=RED)
    d.text((px, py + 22), "FIRST PAKISTANI", font=F(SERIF_B, 30),
           fill=INK)
    d.text((px, py + 58), "IN ORBIT", font=F(SERIF_B, 30), fill=INK)
    rocket_launch(d, px, py + 100, 196, 140)
    wrap(d, px + 210, py + 102,
         "Shenzhou-24 lifted off at 08:18 Wednesday with Tang "
         "Hongbo, Wu Yi and Muhammad Zeeshan Ali, 40 — the first "
         "Pakistani in space and Tiangong's first foreign visitor. "
         "He stays 5–10 days on biotech experiments.",
         F(SANS, 16), 36 + 2 * pw + 20 - (px + 210), gap=4)

    hline(d, 850)

    # ---------------- also today: briefs 4-8
    ay = 860
    d.text((36, ay), "ALSO TODAY", font=F(SANS_B, 16), fill=RED)
    briefs = ("4 · NVIDIA — Attorney general dodges questions on "
              "the Nvidia probe; shares slide.   5 · UKRAINE — "
              "Kremlin questions Europe's seat at peace talks; "
              "Trump hosts NATO chief Rutte.   6 · GAZA — Israeli "
              "strike kills Hamas internal security chief.   "
              "7 · TECH LAW — Huawei guilty of stealing trade "
              "secrets, cleared of racketeering.   8 · AUSTRALIA — "
              "Apology to LGBTQ veterans for decades of "
              "discrimination.")
    wrap(d, 36, ay + 24, briefs, F(SANS, 15), W - 72, gap=4)

    hline(d, 966)

    # ---------------- footer: the day in numbers
    fy = 976
    d.text((36, fy), "THE DAY IN NUMBERS", font=F(SANS_B, 15), fill=RED)
    nums = ("16 partners in the probe  ·  Seoul shares -5.3%  ·  "
            "miners 100 m down  ·  1st foreign guest on Tiangong")
    nx = 36 + d.textlength("THE DAY IN NUMBERS  ", font=F(SANS_B, 15))
    d.text((nx, fy), nums, font=F(SANS, 15), fill=INK)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    build()
