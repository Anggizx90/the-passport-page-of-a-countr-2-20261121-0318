#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Writes /output/entry.png: one uncaptioned open passport spread for the
invented Republic of Caldris — a North Atlantic island nation, capital
Port Anselm. Left page: data page with a code-drawn portrait, holder
details and a machine-readable strip. Right page: arrival/departure
stamps from the two neighbouring countries (Kestrelia and Vordania)
plus a visa-condition box and a harbour-tax fee stamp.

Every date is consistent: issued 02 JUN 2025, expires 01 JUN 2035;
every stamp falls between those dates, arrivals precede departures.
Deterministic: no randomness, no network, Pillow only.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

FD = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FD, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")
MONO = os.path.join(FD, "DejaVuSansMono.ttf")
MONO_B = os.path.join(FD, "DejaVuSansMono-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text(draw, xy, s, f, fill, anchor="la"):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)


def centered(draw, cx, y, s, f, fill):
    draw.text((cx, y), s, font=f, fill=fill, anchor="ma")


def mrz_check(s):
    """ICAO 9303 check digit: weights 7,3,1; < = 0, A-Z = 10-35."""
    vals = {}
    for i in range(10):
        vals[str(i)] = i
    for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        vals[c] = 10 + i
    vals["<"] = 0
    total = 0
    for i, ch in enumerate(s):
        total += vals[ch] * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    doc = "4829137<<"  # 9-char document-number field
    line1 = "P<CDRVOSS<<ELIN<MARA"
    line1 = line1 + "<" * (44 - len(line1))
    dob = "920314"
    exp = "350601"
    pers = "<" * 14
    body = (
        doc + mrz_check(doc)
        + "CDR"
        + dob + mrz_check(dob)
        + "F"
        + exp + mrz_check(exp)
        + pers + mrz_check(pers)
    )
    line2 = body + mrz_check(body)
    assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
    return line1, line2


def draw_crest(draw, cx, cy, r, ink):
    """Small state emblem: ring, gull wings, star, waves."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ink, width=2)
    draw.ellipse([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4],
                 outline=ink, width=1)
    # gull: two swept arcs
    draw.arc([cx - r + 8, cy - 8, cx - 2, cy + 12], 200, 340, fill=ink, width=2)
    draw.arc([cx + 2, cy - 8, cx + r - 8, cy + 12], 200, 340, fill=ink, width=2)
    # star above
    s = 5
    draw.polygon([(cx, cy - r + 12), (cx + 2, cy - r + 17), (cx + s, cy - r + 17),
                  (cx + 3, cy - r + 21), (cx + 4, cy - r + 26), (cx, cy - r + 23),
                  (cx - 4, cy - r + 26), (cx - 3, cy - r + 21), (cx - s, cy - r + 17),
                  (cx - 2, cy - r + 17)], fill=ink)
    # waves below
    for dy in (10, 16):
        draw.arc([cx - r + 10, cy + dy - 5, cx + r - 10, cy + dy + 5],
                 0, 180, fill=ink, width=2)


def draw_portrait(size):
    """Stylised, dignified portrait of the holder: a lighthouse keeper
    in her early thirties, dark hair in a bun, navy high-collar uniform."""
    pw, ph = size
    img = Image.new("RGB", (pw, ph), (58, 96, 110))
    d = ImageDraw.Draw(img)
    # backdrop: pale sky gradient bands + faint horizon (the sea)
    for y in range(ph):
        t = y / ph
        d.line([(0, y), (pw, y)],
               fill=(int(58 + 60 * t), int(96 + 55 * t), int(110 + 45 * t)))
    # distant lighthouse on the horizon, left
    lx = 22
    d.rectangle([lx, 118, lx + 10, 150], fill=(235, 230, 215))
    d.polygon([(lx - 2, 118), (lx + 12, 118), (lx + 5, 108)], fill=(150, 40, 40))
    d.rectangle([lx + 2, 112, lx + 8, 118], fill=(250, 240, 180))
    d.line([(0, 150), (pw, 150)], fill=(210, 220, 215), width=2)
    # sea band
    d.rectangle([0, 150, pw, ph], fill=(46, 84, 96))
    for yy in (158, 168, 180):
        d.line([(8, yy), (pw - 8, yy)], fill=(90, 130, 140), width=1)
    cx = pw // 2
    # shoulders / navy uniform
    d.polygon([(cx - 62, ph), (cx - 52, 168), (cx - 26, 152),
               (cx + 26, 152), (cx + 52, 168), (cx + 62, ph)],
              fill=(28, 42, 66))
    # collar + brass button + epaulette hint
    d.polygon([(cx - 26, 152), (cx, 178), (cx + 26, 152), (cx, 166)],
              fill=(38, 56, 84))
    d.ellipse([cx - 3, 176, cx + 3, 182], fill=(198, 164, 90))
    d.line([(cx - 52, 168), (cx - 34, 158)], fill=(198, 164, 90), width=2)
    d.line([(cx + 52, 168), (cx + 34, 158)], fill=(198, 164, 90), width=2)
    # neck
    d.rectangle([cx - 11, 138, cx + 11, 156], fill=(214, 176, 142))
    d.polygon([(cx - 11, 138), (cx + 11, 138), (cx + 14, 152), (cx - 14, 152)],
              fill=(198, 158, 124))
    # face
    d.ellipse([cx - 27, 78, cx + 27, 140], fill=(226, 188, 152))
    # hair: dark brown, parted, swept back + bun
    d.pieslice([cx - 31, 66, cx + 31, 122], 180, 360, fill=(58, 38, 28))
    d.polygon([(cx - 30, 96), (cx - 24, 76), (cx - 12, 70), (cx - 22, 92)],
              fill=(58, 38, 28))
    d.polygon([(cx + 30, 96), (cx + 24, 76), (cx + 12, 70), (cx + 22, 92)],
              fill=(58, 38, 28))
    d.ellipse([cx - 12, 58, cx + 12, 76], fill=(58, 38, 28))  # bun
    d.arc([cx - 12, 58, cx + 12, 76], 0, 360, fill=(40, 26, 18), width=1)
    # brows, eyes, nose, mouth — calm, direct gaze
    d.line([(cx - 18, 104), (cx - 7, 102)], fill=(58, 38, 28), width=2)
    d.line([(cx + 7, 102), (cx + 18, 104)], fill=(58, 38, 28), width=2)
    for ex in (-13, 13):
        d.ellipse([cx + ex - 5, 106, cx + ex + 5, 112], fill=(250, 246, 238))
        d.ellipse([cx + ex - 2, 107, cx + ex + 2, 111], fill=(52, 44, 38))
    d.line([(cx, 112), (cx - 1, 122), (cx + 2, 123)], fill=(190, 148, 116), width=2)
    d.line([(cx - 7, 130), (cx + 7, 130)], fill=(164, 96, 84), width=2)
    # soft shading on the face edge
    d.arc([cx - 27, 78, cx + 27, 140], 300, 60, fill=(200, 160, 128), width=2)
    return img


def make_stamp(country, kind, date, place, color, angle, size=(216, 116)):
    """One ink stamp, drawn on its own layer and rotated slightly."""
    w, h = size
    layer = Image.new("RGBA", (w + 30, h + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = 15, 15, 15 + w, 15 + h
    ink = color + (215,)
    faint = color + (150,)
    d.rounded_rectangle([x0, y0, x1, y1], radius=8, outline=ink, width=3)
    d.rounded_rectangle([x0 + 5, y0 + 5, x1 - 5, y1 - 5], radius=6,
                        outline=faint, width=1)
    cx = (x0 + x1) // 2
    d.text((cx, y0 + 10), country, font=font(SANS_B, 19), fill=ink, anchor="ma")
    d.line([(x0 + 14, y0 + 36), (x1 - 14, y0 + 36)], fill=faint, width=1)
    d.text((cx, y0 + 42), kind, font=font(SANS_B, 24), fill=ink, anchor="ma")
    d.text((cx, y0 + 70), date, font=font(SANS_B, 16), fill=ink, anchor="ma")
    d.text((cx, y0 + 90), place, font=font(SANS, 11), fill=faint, anchor="ma")
    return layer.rotate(angle, resample=Image.BICUBIC, expand=False)


def main():
    img = Image.new("RGB", (W, H), (32, 48, 44))
    d = ImageDraw.Draw(img)
    # desk: deep green leather with vignette
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)],
               fill=(int(38 - 10 * t), int(58 - 12 * t), int(52 - 10 * t)))
    for x in range(0, W, 7):
        d.line([(x, 0), (x, H)], fill=(36, 56, 50), width=1)
    # soft shadow under the open book
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([18, 128, 1006, 892], radius=6, fill=(0, 0, 0, 90))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)

    # ---- the open spread ----
    LX0, LY0, LX1, LY1 = 24, 136, 500, 884   # left page
    RX0, RY0, RX1, RY1 = 524, 136, 1000, 884  # right page
    cream_l = (244, 238, 224)
    cream_r = (242, 235, 218)
    d.rectangle([LX0, LY0, LX1, LY1], fill=cream_l)
    d.rectangle([RX0, RY0, RX1, RY1], fill=cream_r)
    # page edges / gutter
    d.rectangle([LX0, LY0, LX1, LY1], outline=(120, 105, 80), width=2)
    d.rectangle([RX0, RY0, RX1, RY1], outline=(120, 105, 80), width=2)
    d.rectangle([LX1 - 2, LY0, LX1 + 2, LY1], fill=(150, 135, 105))
    d.rectangle([RX0 - 2, RY0, RX0 + 2, RY1], fill=(150, 135, 105))
    d.line([(LX1, LY0), (LX1, LY1)], fill=(90, 75, 55), width=1)
    # faint guilloche arcs on both pages
    for page_x0, page_x1 in ((LX0, LX1), (RX0, RY0)):
        pass
    for cx in range(LX0 + 30, LX1, 60):
        d.arc([cx - 40, LY0 + 8, cx + 40, LY0 + 88], 0, 180,
              fill=(225, 216, 195), width=1)
    for cx in range(RX0 + 30, RX1, 60):
        d.arc([cx - 40, RY0 + 8, cx + 40, RY0 + 88], 0, 180,
              fill=(222, 212, 190), width=1)
    # faint diagonal watermark on right page
    wm = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wm)
    wd.text((762, 520), "CALDRIS", font=font(SERIF_B, 64),
            fill=(90, 110, 100, 26), anchor="mm")
    wm = wm.rotate(-24, center=(762, 520), resample=Image.BICUBIC)
    img.paste(Image.alpha_composite(img.convert("RGBA"), wm).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)

    ink = (28, 38, 52)
    label = (110, 100, 80)
    accent = (24, 74, 92)

    # ================= LEFT PAGE: DATA PAGE =================
    draw_crest(d, 262, 178, 26, accent)
    centered(d, 262, 208, "REPUBLIC OF CALDRIS", font(SERIF_B, 21), ink)
    centered(d, 262, 234, "PASSPORT  ·  PASSEPORT", font(SANS_B, 11), accent)
    d.line([(48, 256), (476, 256)], fill=accent, width=2)
    d.line([(48, 259), (476, 259)], fill=accent, width=1)

    # portrait
    portrait = draw_portrait((150, 190))
    img.paste(portrait, (48, 272))
    d.rectangle([48, 272, 198, 462], outline=(90, 80, 60), width=2)
    d.line([(48, 462), (198, 462)], fill=(90, 80, 60), width=1)
    centered(d, 123, 466, "PORTRAIT · PHOTO", font(SANS, 8), label)

    # fields right of portrait
    fx, fw = 214, 262
    fields_right = [
        ("TYPE / TYPE", "P"),
        ("COUNTRY CODE / CODE", "CDR"),
        ("PASSPORT No. / No.", "CDR4829137"),
        ("SURNAME / NOM", "VOSS"),
        ("GIVEN NAMES / PRÉNOMS", "ELIN MARA"),
        ("NATIONALITY / NATIONALITÉ", "CALDRISH"),
        ("DATE OF BIRTH / NÉ(E) LE", "14 MAR 1992"),
    ]
    y = 272
    for lab, val in fields_right:
        text(d, (fx, y), lab, font(SANS, 9), label)
        text(d, (fx, y + 11), val, font(SANS_B, 14), ink)
        y += 30
    # rule under the right-hand block
    d.line([(fx, 272 + 7 * 30 - 6), (476, 272 + 7 * 30 - 6)],
           fill=(190, 178, 150), width=1)

    # fields below portrait
    y = 500
    fields_low = [
        ("PLACE OF BIRTH / LIEU DE NAISSANCE", "PORT ANSELM, CALDRIS"),
        ("SEX / SEXE", "F      ·      OCCUPATION / PROFESSION:  LIGHTKEEPER"),
        ("DATE OF ISSUE / DÉLIVRÉ LE", "02 JUN 2025"),
        ("DATE OF EXPIRY / EXPIRE LE", "01 JUN 2035"),
        ("AUTHORITY / AUTORITÉ", "PORT ANSELM PASSPORT OFFICE"),
    ]
    for lab, val in fields_low:
        text(d, (48, y), lab, font(SANS, 9), label)
        text(d, (48, y + 11), val, font(SANS_B, 14), ink)
        y += 30
    # signature
    y += 2
    d.line([(48, y + 22), (300, y + 22)], fill=ink, width=1)
    text(d, (48, y), "Elin Mara Voss", font(SERIF, 20), ink)
    text(d, (48, y + 26), "HOLDER'S SIGNATURE / SIGNATURE DU TITULAIRE",
         font(SANS, 8), label)
    # small note tying holder to the country
    text(d, (320, y), "OCCUPATION ON FILE:", font(SANS, 8), label)
    text(d, (320, y + 11), "LIGHTKEEPER,", font(SANS_B, 11), ink)
    text(d, (320, y + 24), "NORTH LIGHT, PORT ANSELM", font(SANS_B, 11), ink)

    # MRZ band
    d.rectangle([40, 792, 484, 856], fill=(232, 226, 208))
    d.rectangle([40, 792, 484, 856], outline=(150, 138, 110), width=1)
    l1, l2 = mrz_lines()
    text(d, (48, 800), l1, font(MONO, 14), ink)
    text(d, (48, 824), l2, font(MONO, 14), ink)
    text(d, (48, 866), "CDR4829137", font(SANS, 9), label)
    text(d, (476, 866), "P. 12", font(SANS, 9), label, anchor="ra")

    # ================= RIGHT PAGE: VISAS / STAMPS =================
    centered(d, 762, 158, "VISAS", font(SERIF_B, 20), ink)
    centered(d, 762, 184, "ARRIVALS AND DEPARTURES · ENTRÉES ET SORTIES",
             font(SANS, 9), label)
    d.line([(548, 206), (976, 206)], fill=accent, width=2)
    d.line([(548, 209), (976, 209)], fill=accent, width=1)

    stamps = [
        ("KESTRELIA", "ARRIVAL", "18 AUG 2025", "HARBOR GATE · FERRY", (31, 78, 156), -3),
        ("KESTRELIA", "DEPARTURE", "24 AUG 2025", "HARBOR GATE · FERRY", (31, 78, 156), 2),
        ("VORDANIA", "ARRIVAL", "09 NOV 2025", "NORTH PASS · ROAD", (42, 107, 58), 3),
        ("VORDANIA", "DEPARTURE", "21 NOV 2025", "NORTH PASS · ROAD", (42, 107, 58), -2),
        ("KESTRELIA", "ARRIVAL", "12 FEB 2026", "FERRY TERMINAL", (31, 78, 156), -2),
        ("KESTRELIA", "DEPARTURE", "19 FEB 2026", "FERRY TERMINAL", (31, 78, 156), 3),
    ]
    positions = [(548, 226), (760, 226), (548, 356), (760, 356), (548, 486), (760, 486)]
    base = img.convert("RGBA")
    for (country, kind, date, place, color, angle), (sx, sy) in zip(stamps, positions):
        st = make_stamp(country, kind, date, place, color, angle)
        base.alpha_composite(st, (sx - 8, sy - 8))
    img = base.convert("RGB")
    d = ImageDraw.Draw(img)

    # ---- telling detail: visa-condition box + fee stamp ----
    by = 622
    d.rectangle([548, by, 976, 772], outline=(24, 74, 92), width=2)
    d.rectangle([548, by, 976, 648], fill=(24, 74, 92))
    text(d, (562, by + 7), "CONDITION OF ENTRY — KESTRELIA",
         font(SANS_B, 13), (244, 238, 224))
    lines = [
        "30-day stay. No employment. A return ferry must be",
        "booked before entry; the fare is payable in caldr (CLD)",
        "only. Overstay is fined 5 CLD a day at Harbor Gate.",
    ]
    y = 658
    for ln in lines:
        text(d, (562, y), ln, font(SANS, 12), ink)
        y += 17
    text(d, (562, 716), "FEE: 12 CLD HARBOUR TAX — PAID AT ISSUE",
         font(SANS_B, 11), (120, 40, 40))
    text(d, (562, 736), "This passport is the property of the Republic of Caldris.",
         font(SANS, 10), label)
    # purple fee stamp overlapping the box corner
    fee = Image.new("RGBA", (260, 84), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fee)
    fd.rounded_rectangle([4, 4, 256, 80], radius=6,
                         outline=(122, 44, 122, 220), width=3)
    fd.text((130, 12), "HARBOUR TAX PAID", font=font(SANS_B, 15),
            fill=(122, 44, 122, 230), anchor="ma")
    fd.text((130, 34), "12 CLD  ·  02 JUN 2025", font=font(SANS_B, 14),
            fill=(122, 44, 122, 230), anchor="ma")
    fd.text((130, 56), "PORT ANSELM", font=font(SANS, 10),
            fill=(122, 44, 122, 190), anchor="ma")
    fee = fee.rotate(-8, resample=Image.BICUBIC, expand=True)
    img_rgba = img.convert("RGBA")
    img_rgba.alpha_composite(fee, (712, 786))
    img = img_rgba.convert("RGB")
    d = ImageDraw.Draw(img)

    # footer
    text(d, (548, 866), "32 PAGES", font(SANS, 9), label)
    text(d, (976, 866), "P. 13", font(SANS, 9), label, anchor="ra")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT}: {img.size}, {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
