#!/usr/bin/env python3
"""Build the animated GitHub profile cover from the approved MidJourney master.

The garden, logo and composition stay fixed. Only small white point stars in
the black sky change luminance, so the GIF does not introduce the unstable
flower movement or typography drift that generative video would add.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "profile"
SOURCE = ASSET_DIR / "programmable-github-profile-night-garden-v3.png"
OUTPUT = ASSET_DIR / "programmable-github-profile-night-garden-v4.gif"
MANIFEST = ASSET_DIR / "profile-v4-manifest.json"
QA_DIR = ROOT / ".artifacts" / "profile-v4"

BUILDER_SOURCE = ASSET_DIR / "source" / "programmable-builder-night-garden-midjourney-v4.png"
ECOSYSTEM_SOURCE = ASSET_DIR / "source" / "programmable-ecosystem-night-garden-midjourney-v4.png"
PROGRAMMABLE_MARK = ASSET_DIR / "source" / "programmable-loop-mark-warm-ivory.png"
GITHUB_MARK = ASSET_DIR / "source" / "github-mark-official.png"
BUILDER_OUTPUT = ASSET_DIR / "programmable-builder-skill-v4.jpg"
ECOSYSTEM_OUTPUT = ASSET_DIR / "programmable-profile-ecosystem-v4.jpg"
SOCIAL_PREVIEW = ASSET_DIR / "programmable-github-social-preview.jpg"

SIZE = (1400, 700)
FRAME_COUNT = 32
FRAME_DURATION_MS = 200
SKY_HEIGHT = 300
LOGO_EXCLUSION = (585, 58, 815, 285)
CHAPTER_SIZE = (1400, 560)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_neutral_white(pixel: tuple[int, int, int, int]) -> bool:
    red, green, blue, alpha = pixel
    return alpha > 220 and min(red, green, blue) > 214 and max(red, green, blue) - min(red, green, blue) < 34


def is_inside_logo(x: int, y: int) -> bool:
    left, top, right, bottom = LOGO_EXCLUSION
    return left <= x <= right and top <= y <= bottom


def surrounding_black_ratio(image: Image.Image, bounds: tuple[int, int, int, int]) -> float:
    left, top, right, bottom = bounds
    margin = 5
    sample_left = max(0, left - margin)
    sample_top = max(0, top - margin)
    sample_right = min(image.width - 1, right + margin)
    sample_bottom = min(SKY_HEIGHT - 1, bottom + margin)
    black = 0
    total = 0
    for y in range(sample_top, sample_bottom + 1):
        for x in range(sample_left, sample_right + 1):
            if left <= x <= right and top <= y <= bottom:
                continue
            red, green, blue, _ = image.getpixel((x, y))
            total += 1
            black += max(red, green, blue) < 34
    return black / total if total else 0.0


def detect_stars(image: Image.Image) -> list[dict[str, float]]:
    width, _ = image.size
    visited: set[tuple[int, int]] = set()
    stars: list[dict[str, float]] = []
    pixels = image.load()

    for y in range(SKY_HEIGHT):
        for x in range(width):
            if (x, y) in visited or is_inside_logo(x, y) or not is_neutral_white(pixels[x, y]):
                continue

            queue = deque([(x, y)])
            visited.add((x, y))
            component: list[tuple[int, int]] = []
            while queue:
                current_x, current_y = queue.popleft()
                component.append((current_x, current_y))
                for delta_x, delta_y in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
                    next_x = current_x + delta_x
                    next_y = current_y + delta_y
                    if not (0 <= next_x < width and 0 <= next_y < SKY_HEIGHT):
                        continue
                    if (next_x, next_y) in visited or is_inside_logo(next_x, next_y):
                        continue
                    if is_neutral_white(pixels[next_x, next_y]):
                        visited.add((next_x, next_y))
                        queue.append((next_x, next_y))

            left = min(point[0] for point in component)
            right = max(point[0] for point in component)
            top = min(point[1] for point in component)
            bottom = max(point[1] for point in component)
            component_width = right - left + 1
            component_height = bottom - top + 1
            if not 1 <= len(component) <= 92 or component_width > 14 or component_height > 14:
                continue
            if surrounding_black_ratio(image, (left, top, right, bottom)) < 0.72:
                continue

            center_x = sum(point[0] for point in component) / len(component)
            center_y = sum(point[1] for point in component) / len(component)
            diameter = max(component_width, component_height)
            radius = max(0.85, min(4.2, diameter * 0.56))
            phase = ((round(center_x) * 37 + round(center_y) * 71) % FRAME_COUNT) / FRAME_COUNT
            period = 0.72 + ((round(center_x) * 13 + round(center_y) * 19) % 37) / 100
            stars.append(
                {
                    "x": center_x,
                    "y": center_y,
                    "radius": radius,
                    "phase": phase,
                    "period": period,
                    "left": left,
                    "top": top,
                    "right": right,
                    "bottom": bottom,
                }
            )

    return stars


def make_clean_base(source: Image.Image, stars: list[dict[str, float]]) -> Image.Image:
    clean = source.copy()
    draw = ImageDraw.Draw(clean)
    for star in stars:
        padding = 2
        draw.rectangle(
            (
                int(star["left"]) - padding,
                int(star["top"]) - padding,
                int(star["right"]) + padding,
                int(star["bottom"]) + padding,
            ),
            fill=(0, 0, 0, 255),
        )
    return clean


def render_frame(clean: Image.Image, stars: list[dict[str, float]], frame_index: int) -> Image.Image:
    frame = clean.copy()
    sharp = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    soft = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    sharp_draw = ImageDraw.Draw(sharp)
    soft_draw = ImageDraw.Draw(soft)

    progress = frame_index / FRAME_COUNT
    for index, star in enumerate(stars):
        theta = math.tau * ((progress / star["period"] + star["phase"]) % 1.0)
        pulse = (math.sin(theta) + 1.0) / 2.0
        pulse = pulse**2.4
        opacity = 72 + round(pulse * 183)
        scale = 0.88 + pulse * (0.32 if index % 7 else 0.52)
        radius = star["radius"] * scale
        x = star["x"]
        y = star["y"]
        sharp_draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(255, 255, 255, opacity))
        if pulse > 0.82 and index % 5 == 0:
            soft_radius = radius * 2.15
            soft_draw.ellipse(
                (x - soft_radius, y - soft_radius, x + soft_radius, y + soft_radius),
                fill=(236, 243, 255, round((pulse - 0.82) / 0.18 * 48)),
            )

    frame.alpha_composite(soft.filter(ImageFilter.GaussianBlur(1.6)))
    frame.alpha_composite(sharp)
    return frame.convert("RGB")


def sky_mask(image: Image.Image) -> Image.Image:
    """Return the black sky connected to the image's upper edge, closing point-star holes."""
    rgb = image.convert("RGB")
    width, height = rgb.size
    candidate = Image.new("L", rgb.size, 0)
    candidate_pixels = candidate.load()
    rgb_pixels = rgb.load()
    for y in range(round(height * 0.56)):
        for x in range(width):
            if max(rgb_pixels[x, y]) < 44:
                candidate_pixels[x, y] = 255

    visited: set[tuple[int, int]] = set()
    queue: deque[tuple[int, int]] = deque()
    for x in range(width):
        if candidate_pixels[x, 0] == 255:
            visited.add((x, 0))
            queue.append((x, 0))

    while queue:
        x, y = queue.popleft()
        for next_x, next_y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if not (0 <= next_x < width and 0 <= next_y < height):
                continue
            if (next_x, next_y) in visited or candidate_pixels[next_x, next_y] != 255:
                continue
            visited.add((next_x, next_y))
            queue.append((next_x, next_y))

    connected = Image.new("L", rgb.size, 0)
    connected_pixels = connected.load()
    for x, y in visited:
        connected_pixels[x, y] = 255

    # Fill the small colored star holes while retaining the overall tree line.
    return connected.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.MinFilter(15))


def replace_generated_sky(image: Image.Image, seed: int, star_count: int) -> Image.Image:
    """Replace generated starbursts or colored points with a pure black point-star sky."""
    canvas = image.convert("RGBA")
    rgb = image.convert("RGB")
    width, height = image.size
    pixels = rgb.load()
    visited: set[tuple[int, int]] = set()
    point_centers: list[tuple[float, float, float]] = []
    scan_height = round(height * 0.48)

    def bright_point(x: int, y: int) -> bool:
        red, green, blue = pixels[x, y]
        return max(red, green, blue) > 118 and (min(red, green, blue) > 72 or max(red, green, blue) - min(red, green, blue) > 42)

    def local_black_ratio(bounds: tuple[int, int, int, int]) -> float:
        left, top, right, bottom = bounds
        black = 0
        total = 0
        for sample_y in range(max(0, top - 6), min(scan_height, bottom + 7)):
            for sample_x in range(max(0, left - 6), min(width, right + 7)):
                if left <= sample_x <= right and top <= sample_y <= bottom:
                    continue
                total += 1
                black += max(pixels[sample_x, sample_y]) < 42
        return black / total if total else 0.0

    for y in range(scan_height):
        for x in range(width):
            if (x, y) in visited or not bright_point(x, y):
                continue
            queue = deque([(x, y)])
            visited.add((x, y))
            component: list[tuple[int, int]] = []
            while queue:
                current_x, current_y = queue.popleft()
                component.append((current_x, current_y))
                for delta_x, delta_y in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
                    next_x = current_x + delta_x
                    next_y = current_y + delta_y
                    if not (0 <= next_x < width and 0 <= next_y < scan_height):
                        continue
                    if (next_x, next_y) in visited or not bright_point(next_x, next_y):
                        continue
                    visited.add((next_x, next_y))
                    queue.append((next_x, next_y))

            left = min(point[0] for point in component)
            right = max(point[0] for point in component)
            top = min(point[1] for point in component)
            bottom = max(point[1] for point in component)
            component_width = right - left + 1
            component_height = bottom - top + 1
            if not 1 <= len(component) <= 160 or component_width > 18 or component_height > 18:
                continue
            if local_black_ratio((left, top, right, bottom)) < 0.68:
                continue
            center_x = sum(point[0] for point in component) / len(component)
            center_y = sum(point[1] for point in component) / len(component)
            radius = max(0.75, min(2.2, max(component_width, component_height) * 0.42))
            point_centers.append((center_x, center_y, radius))

    clean_draw = ImageDraw.Draw(canvas)
    for center_x, center_y, radius in point_centers:
        padding = max(2, math.ceil(radius * 1.8))
        clean_draw.rectangle(
            (center_x - padding, center_y - padding, center_x + padding, center_y + padding),
            fill=(0, 0, 0, 255),
        )

    rng = random.Random(seed)
    star_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(star_layer)
    for index, (x, y, radius) in enumerate(point_centers):
        tone = (255, 255, 255) if index % 4 else (236, 243, 255)
        opacity = 170 + (index * 29 % 82)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*tone, opacity))

    placed = len(point_centers)
    attempts = 0
    while placed < star_count and attempts < star_count * 80:
        attempts += 1
        x = rng.randrange(14, image.width - 14)
        y = rng.randrange(8, round(image.height * 0.46))
        neighborhood = [pixels[check_x, check_y] for check_y in range(max(0, y - 3), min(height, y + 4)) for check_x in range(max(0, x - 3), min(width, x + 4))]
        if not neighborhood or sum(max(pixel) < 36 for pixel in neighborhood) / len(neighborhood) < 0.94:
            continue
        radius = rng.choice((0.7, 0.8, 0.9, 1.0, 1.15, 1.35))
        opacity = rng.randrange(128, 246)
        tone = rng.choice(((255, 255, 255), (236, 243, 255), (248, 248, 244)))
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*tone, opacity))
        placed += 1

    canvas.alpha_composite(star_layer)
    return canvas


def alpha_trim(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bounds = rgba.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("Expected a visible mark")
    return rgba.crop(bounds)


def white_programmable_mark(height: int) -> Image.Image:
    source = alpha_trim(Image.open(PROGRAMMABLE_MARK))
    width = round(source.width * height / source.height)
    alpha = source.getchannel("A").resize((width, height), Image.Resampling.LANCZOS)
    mark = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    mark.putalpha(alpha)
    return mark


def white_github_mark(height: int) -> Image.Image:
    source = Image.open(GITHUB_MARK).convert("RGB")
    alpha = ImageOps.invert(ImageOps.grayscale(source))
    alpha = alpha.point(lambda value: 0 if value < 5 else value)
    rgba = Image.new("RGBA", source.size, (255, 255, 255, 0))
    rgba.putalpha(alpha)
    trimmed = alpha_trim(rgba)
    width = round(trimmed.width * height / trimmed.height)
    return trimmed.resize((width, height), Image.Resampling.LANCZOS)


def paste_centered(canvas: Image.Image, image: Image.Image, center: tuple[int, int]) -> None:
    canvas.alpha_composite(image, (round(center[0] - image.width / 2), round(center[1] - image.height / 2)))


def build_chapter_assets() -> dict[str, dict[str, object]]:
    builder = ImageOps.fit(
        Image.open(BUILDER_SOURCE).convert("RGB"),
        CHAPTER_SIZE,
        method=Image.Resampling.LANCZOS,
    )
    builder = replace_generated_sky(builder, seed=70726, star_count=108)
    paste_centered(builder, white_programmable_mark(102), (640, 107))
    paste_centered(builder, white_github_mark(88), (760, 107))
    builder.convert("RGB").save(BUILDER_OUTPUT, quality=94, optimize=True, progressive=True)

    ecosystem = ImageOps.fit(
        Image.open(ECOSYSTEM_SOURCE).convert("RGB"),
        CHAPTER_SIZE,
        method=Image.Resampling.LANCZOS,
    )
    ecosystem = replace_generated_sky(ecosystem, seed=49157, star_count=124)
    ecosystem.convert("RGB").save(ECOSYSTEM_OUTPUT, quality=94, optimize=True, progressive=True)

    social_preview = ImageOps.fit(
        Image.open(SOURCE).convert("RGB"),
        (1280, 640),
        method=Image.Resampling.LANCZOS,
    )
    social_preview.save(SOCIAL_PREVIEW, quality=94, optimize=True, progressive=True)

    return {
        "builder": {
            "source": BUILDER_SOURCE.relative_to(ROOT).as_posix(),
            "sourceSha256": sha256(BUILDER_SOURCE),
            "midjourneyJob": "ae75b291-c01f-4b44-a0f8-b1bb7081c84a",
            "midjourneyIndex": 2,
            "output": BUILDER_OUTPUT.relative_to(ROOT).as_posix(),
            "outputSha256": sha256(BUILDER_OUTPUT),
            "dimensions": list(CHAPTER_SIZE),
        },
        "ecosystem": {
            "source": ECOSYSTEM_SOURCE.relative_to(ROOT).as_posix(),
            "sourceSha256": sha256(ECOSYSTEM_SOURCE),
            "midjourneyJob": "b79ea563-3261-4d5f-980e-4fb301418444",
            "midjourneyIndex": 2,
            "output": ECOSYSTEM_OUTPUT.relative_to(ROOT).as_posix(),
            "outputSha256": sha256(ECOSYSTEM_OUTPUT),
            "dimensions": list(CHAPTER_SIZE),
        },
        "socialPreview": {
            "source": SOURCE.relative_to(ROOT).as_posix(),
            "output": SOCIAL_PREVIEW.relative_to(ROOT).as_posix(),
            "outputSha256": sha256(SOCIAL_PREVIEW),
            "dimensions": [1280, 640],
        },
    }


def main() -> None:
    source = Image.open(SOURCE).convert("RGBA").resize(SIZE, Image.Resampling.LANCZOS)
    stars = detect_stars(source)
    if len(stars) < 55:
        raise RuntimeError(f"Detected only {len(stars)} stars; expected at least 55")

    clean = make_clean_base(source, stars)
    rgb_frames = [render_frame(clean, stars, frame) for frame in range(FRAME_COUNT)]

    # One shared palette keeps the flowers and logo bit-identical between frames.
    palette = rgb_frames[0].quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    frames = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in rgb_frames]
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
    for frame_index in (0, 8, 16, 24):
        rgb_frames[frame_index].save(QA_DIR / f"hero-frame-{frame_index:02d}.png", optimize=True)

    chapter_assets = build_chapter_assets()
    manifest = {
        "source": SOURCE.relative_to(ROOT).as_posix(),
        "sourceSha256": sha256(SOURCE),
        "output": OUTPUT.relative_to(ROOT).as_posix(),
        "outputSha256": sha256(OUTPUT),
        "dimensions": list(SIZE),
        "frameCount": FRAME_COUNT,
        "frameDurationMs": FRAME_DURATION_MS,
        "loopDurationMs": FRAME_COUNT * FRAME_DURATION_MS,
        "detectedPointStars": len(stars),
        "motion": "Only detected white circular point stars in the black sky change luminance.",
        "logoAndGarden": "Static in every frame.",
        "chapterAssets": chapter_assets,
        "midjourneyMoodboard": "Programmable Night Garden",
        "midjourneyMoodboardId": "7488121925059739690",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    print(f"bytes={OUTPUT.stat().st_size}")


if __name__ == "__main__":
    main()
