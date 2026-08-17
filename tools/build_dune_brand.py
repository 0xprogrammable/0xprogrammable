#!/usr/bin/env python3
"""Build the Programmable Dune hero from the approved MidJourney ecosystem art.

The illustration and exact Programmable mark stay fixed. Only small circular
stars in the black sky change luminance, keeping the dashboard calm while the
brand still feels alive.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from build_profile_v4 import (
    ECOSYSTEM_SOURCE,
    PROGRAMMABLE_MARK,
    alpha_trim,
    paste_centered,
    replace_generated_sky,
)


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "profile"
OUTPUT = ASSET_DIR / "programmable-dune-analytics-night-garden-v1.gif"
POSTER = ASSET_DIR / "programmable-dune-analytics-night-garden-v1.jpg"
MANIFEST = ASSET_DIR / "programmable-dune-analytics-night-garden-v1.json"
QA_DIR = ROOT / ".artifacts" / "dune-v1"

SIZE = (1600, 533)
FRAME_COUNT = 20
FRAME_DURATION_MS = 300
SKY_HEIGHT = 245
LOGO_CENTER = (800, 104)
LOGO_HEIGHT = 116
LOGO_EXCLUSION = (720, 28, 880, 184)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def white_programmable_mark(height: int) -> Image.Image:
    source = alpha_trim(Image.open(PROGRAMMABLE_MARK))
    width = round(source.width * height / source.height)
    alpha = source.getchannel("A").resize((width, height), Image.Resampling.LANCZOS)
    mark = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    mark.putalpha(alpha)
    return mark


def is_inside_logo(x: int, y: int) -> bool:
    left, top, right, bottom = LOGO_EXCLUSION
    return left <= x <= right and top <= y <= bottom


def is_point_white(pixel: tuple[int, int, int, int]) -> bool:
    red, green, blue, alpha = pixel
    return alpha > 220 and min(red, green, blue) > 138 and max(red, green, blue) - min(red, green, blue) < 52


def surrounding_black_ratio(image: Image.Image, bounds: tuple[int, int, int, int]) -> float:
    left, top, right, bottom = bounds
    black = 0
    total = 0
    for y in range(max(0, top - 5), min(SKY_HEIGHT, bottom + 6)):
        for x in range(max(0, left - 5), min(image.width, right + 6)):
            if left <= x <= right and top <= y <= bottom:
                continue
            red, green, blue, _ = image.getpixel((x, y))
            total += 1
            black += max(red, green, blue) < 36
    return black / total if total else 0.0


def detect_stars(image: Image.Image) -> list[dict[str, float]]:
    visited: set[tuple[int, int]] = set()
    pixels = image.load()
    stars: list[dict[str, float]] = []

    for y in range(SKY_HEIGHT):
        for x in range(image.width):
            if (x, y) in visited or is_inside_logo(x, y) or not is_point_white(pixels[x, y]):
                continue

            queue = deque([(x, y)])
            visited.add((x, y))
            component: list[tuple[int, int]] = []
            while queue:
                current_x, current_y = queue.popleft()
                component.append((current_x, current_y))
                for delta_x, delta_y in (
                    (-1, 0),
                    (1, 0),
                    (0, -1),
                    (0, 1),
                    (-1, -1),
                    (1, -1),
                    (-1, 1),
                    (1, 1),
                ):
                    next_x = current_x + delta_x
                    next_y = current_y + delta_y
                    if not (0 <= next_x < image.width and 0 <= next_y < SKY_HEIGHT):
                        continue
                    if (next_x, next_y) in visited or is_inside_logo(next_x, next_y):
                        continue
                    if is_point_white(pixels[next_x, next_y]):
                        visited.add((next_x, next_y))
                        queue.append((next_x, next_y))

            left = min(point[0] for point in component)
            right = max(point[0] for point in component)
            top = min(point[1] for point in component)
            bottom = max(point[1] for point in component)
            width = right - left + 1
            height = bottom - top + 1
            if not 1 <= len(component) <= 72 or width > 12 or height > 12:
                continue
            if surrounding_black_ratio(image, (left, top, right, bottom)) < 0.74:
                continue

            center_x = sum(point[0] for point in component) / len(component)
            center_y = sum(point[1] for point in component) / len(component)
            radius = max(0.75, min(2.45, max(width, height) * 0.44))
            stars.append(
                {
                    "x": center_x,
                    "y": center_y,
                    "radius": radius,
                    "phase": ((round(center_x) * 29 + round(center_y) * 47) % FRAME_COUNT) / FRAME_COUNT,
                    "period": 0.86 + ((round(center_x) * 7 + round(center_y) * 17) % 41) / 100,
                    "left": left,
                    "top": top,
                    "right": right,
                    "bottom": bottom,
                }
            )

    return stars


def clean_sky(base: Image.Image, stars: list[dict[str, float]]) -> Image.Image:
    clean = base.copy()
    draw = ImageDraw.Draw(clean)
    for star in stars:
        draw.rectangle(
            (
                int(star["left"]) - 2,
                int(star["top"]) - 2,
                int(star["right"]) + 2,
                int(star["bottom"]) + 2,
            ),
            fill=(0, 0, 0, 255),
        )
    return clean


def render_frame(clean: Image.Image, stars: list[dict[str, float]], index: int) -> Image.Image:
    frame = clean.copy()
    sharp = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    glow = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    sharp_draw = ImageDraw.Draw(sharp)
    glow_draw = ImageDraw.Draw(glow)
    progress = index / FRAME_COUNT

    for star_index, star in enumerate(stars):
        theta = math.tau * ((progress / star["period"] + star["phase"]) % 1.0)
        pulse = ((math.sin(theta) + 1.0) / 2.0) ** 2.2
        opacity = 70 + round(pulse * 185)
        radius = star["radius"] * (0.86 + pulse * (0.34 if star_index % 11 else 0.54))
        x = star["x"]
        y = star["y"]
        sharp_draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(255, 255, 255, opacity))
        if pulse > 0.88 and star_index % 7 == 0:
            glow_radius = radius * 1.85
            glow_draw.ellipse(
                (x - glow_radius, y - glow_radius, x + glow_radius, y + glow_radius),
                fill=(236, 243, 255, round((pulse - 0.88) / 0.12 * 34)),
            )

    frame.alpha_composite(glow.filter(ImageFilter.GaussianBlur(1.1)))
    frame.alpha_composite(sharp)
    return frame.convert("RGB")


def main() -> None:
    base = ImageOps.fit(
        Image.open(ECOSYSTEM_SOURCE).convert("RGB"),
        SIZE,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.48),
    )
    base = replace_generated_sky(base, seed=90817, star_count=154)
    paste_centered(base, white_programmable_mark(LOGO_HEIGHT), LOGO_CENTER)

    stars = detect_stars(base)
    if len(stars) < 90:
        raise RuntimeError(f"Detected only {len(stars)} point stars; expected at least 90")

    clean = clean_sky(base, stars)
    frames_rgb = [render_frame(clean, stars, index) for index in range(FRAME_COUNT)]
    frames_rgb[0].save(POSTER, quality=94, optimize=True, progressive=True)

    palette = frames_rgb[0].quantize(colors=160, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    frames = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames_rgb]
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
        disposal=1,
    )

    QA_DIR.mkdir(parents=True, exist_ok=True)
    for frame_index in (0, 6, 12, 18):
        frames_rgb[frame_index].save(QA_DIR / f"dune-frame-{frame_index:02d}.png", optimize=True)

    manifest = {
        "source": ECOSYSTEM_SOURCE.relative_to(ROOT).as_posix(),
        "sourceSha256": sha256(ECOSYSTEM_SOURCE),
        "midjourneyJob": "b79ea563-3261-4d5f-980e-4fb301418444",
        "midjourneyIndex": 2,
        "midjourneyMoodboardId": "7488121925059739690",
        "output": OUTPUT.relative_to(ROOT).as_posix(),
        "outputSha256": sha256(OUTPUT),
        "poster": POSTER.relative_to(ROOT).as_posix(),
        "posterSha256": sha256(POSTER),
        "dimensions": list(SIZE),
        "frameCount": FRAME_COUNT,
        "frameDurationMs": FRAME_DURATION_MS,
        "loopDurationMs": FRAME_COUNT * FRAME_DURATION_MS,
        "detectedPointStars": len(stars),
        "motion": "Only small white circular point stars change luminance.",
        "logoAndGarden": "Static in every frame.",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    print(f"gifBytes={OUTPUT.stat().st_size}")


if __name__ == "__main__":
    main()
