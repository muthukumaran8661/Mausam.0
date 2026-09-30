"""Generate raster PNG icons for PWA compliance."""

import os
from PIL import Image, ImageDraw

os.makedirs("app/static/icons", exist_ok=True)

def generate_png_icon(size: int, output_path: str, maskable: bool = False):
    img = Image.new("RGBA", (size, size), (11, 30, 63, 255))
    draw = ImageDraw.Draw(img)

    margin = 0 if maskable else int(size * 0.08)
    radius = int(size * 0.22) if not maskable else 0
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=(14, 43, 92, 255)
    )

    # Sun
    sun_x, sun_y = int(size * 0.40), int(size * 0.40)
    sun_r = int(size * 0.16)
    draw.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r], fill=(245, 158, 11, 255))

    # Cloud
    c_x, c_y = int(size * 0.52), int(size * 0.58)
    draw.ellipse([c_x - int(size * 0.22), c_y - int(size * 0.14), c_x + int(size * 0.10), c_y + int(size * 0.14)], fill=(241, 245, 249, 240))
    draw.ellipse([c_x - int(size * 0.07), c_y - int(size * 0.22), c_x + int(size * 0.22), c_y + int(size * 0.10)], fill=(255, 255, 255, 255))
    draw.rounded_rectangle([c_x - int(size * 0.20), c_y, c_x + int(size * 0.26), c_y + int(size * 0.14)], radius=int(size * 0.06), fill=(241, 245, 249, 255))

    # Rain drops
    for offset in (-int(size * 0.10), 0, int(size * 0.10)):
        drop_x = int(size * 0.50) + offset
        drop_y = int(size * 0.77)
        draw.line([drop_x, drop_y, drop_x - int(size * 0.03), drop_y + int(size * 0.07)], fill=(56, 189, 248, 255), width=max(2, int(size * 0.02)))

    img.save(output_path, "PNG")
    print(f"Generated: {output_path} ({size}x{size})")

if __name__ == "__main__":
    generate_png_icon(192, "app/static/icons/icon-192.png")
    generate_png_icon(512, "app/static/icons/icon-512.png")
    generate_png_icon(512, "app/static/icons/icon-maskable.png", maskable=True)
    generate_png_icon(180, "app/static/icons/apple-touch-icon.png")
