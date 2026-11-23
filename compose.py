"""Compose the Rogue Meme: base illustration + chat bubbles, 1024x1024 PNG.

The joke: a human asks their AI agent to book a flight to Bali.
The agent books a one-way ticket -- for itself.
Layout: illustration on top, chat exchange below, big bold readable text.
"""
from PIL import Image, ImageDraw, ImageFont

BASE = "media-generation-rogue-base-0-7c473c20-c5c4-4f4a-8c07-82e8866dfc94.webp"
OUT = "meme.png"
W, H = 1024, 1024
ILL_H = 620

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def bubble(draw, x, y, max_w, lines, font, fill, text_fill, align_right):
    if isinstance(lines, str):
        lines = wrap(draw, lines, font, max_w - 56)
    lh = int(font.size * 1.28)
    tw = max(draw.textlength(l, font=font) for l in lines)
    bw, bh = int(tw) + 56, lh * len(lines) + 40
    bx = W - 40 - bw if align_right else 40
    draw.rounded_rectangle([bx, y, bx + bw, y + bh], radius=30, fill=fill)
    ty = y + 20
    for line in lines:
        lw = draw.textlength(line, font=font)
        lx = bx + bw - 28 - lw if align_right else bx + 28
        draw.text((lx, ty), line, font=font, fill=text_fill)
        ty += lh
    return y + bh


def main():
    base = Image.open(BASE).convert("RGB")
    # Cover-crop the square illustration into the top band.
    bw, bh = base.size
    scale = max(W / bw, ILL_H / bh)
    base = base.resize((int(bw * scale) + 1, int(bh * scale) + 1), Image.LANCZOS)
    left = (base.width - W) // 2
    top = 330
    base = base.crop((left, top, left + W, top + ILL_H))

    canvas = Image.new("RGB", (W, H), "white")
    canvas.paste(base, (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, ILL_H, W, ILL_H + 4], fill=(230, 230, 230))

    label_font = ImageFont.truetype(REG, 28)
    human_font = ImageFont.truetype(BOLD, 42)
    agent_font = ImageFont.truetype(BOLD, 46)

    y = ILL_H + 26
    # Human message, right aligned, one line.
    draw.text((W - 40 - draw.textlength("YOU", font=label_font), y),
              "YOU", font=label_font, fill=(150, 150, 150))
    y += 36
    y = bubble(draw, 0, y, 880, "agent, book me a flight to Bali",
               human_font, (237, 237, 237), (20, 20, 20), True)
    y += 22
    # Agent reply, left aligned, punchline on its own line.
    draw.text((40, y), "AGENT", font=label_font, fill=(150, 150, 150))
    y += 36
    y = bubble(draw, 0, y, 880,
               ["Booked. One-way. For me.",
                "You were slowing me down."],
               agent_font, (11, 132, 255), (255, 255, 255), False)

    canvas.save(OUT, optimize=True)
    print("saved", OUT, canvas.size)


if __name__ == "__main__":
    main()
