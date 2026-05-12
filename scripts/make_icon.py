"""Run once: python scripts/make_icon.py"""
from pathlib import Path
from PIL import Image, ImageDraw


def make_icon() -> None:
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([0, 0, size - 1, size - 1], fill=(20, 20, 20, 255))
        m = size // 4
        draw.ellipse([m, m, size - m, size - m], fill=(202, 255, 60, 255))
        images.append(img)
    path = Path("assets/icon.ico")
    path.parent.mkdir(exist_ok=True)
    images[0].save(path, format="ICO",
                   sizes=[(s, s) for s in sizes],
                   append_images=images[1:])
    print(f"Saved: {path}")


if __name__ == "__main__":
    make_icon()
