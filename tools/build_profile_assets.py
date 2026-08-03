#!/usr/bin/env python3
"""Build the restrained paper-stop-motion artwork used by the profile README."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "profile"
SOURCE_DIR = ASSET_DIR / "source"
QA_DIR = ROOT / ".artifacts" / "profile"

HERO_SOURCE = SOURCE_DIR / "programmable-profile-ecosystem-source.png"
BUILDER_SOURCE = SOURCE_DIR / "programmable-builder-source.png"
PROGRAMMABLE_MARK = SOURCE_DIR / "programmable-loop-mark.png"
GITHUB_MARK = SOURCE_DIR / "github-mark-official.png"

HERO_GIF = ASSET_DIR / "programmable-profile-ecosystem.gif"
HERO_STILL = ASSET_DIR / "programmable-profile-ecosystem.jpg"
BUILDER_GIF = ASSET_DIR / "programmable-builder-skill.gif"
BUILDER_STILL = ASSET_DIR / "programmable-builder-skill.jpg"
MANIFEST = ASSET_DIR / "animation-manifest.json"

HERO_SIZE = (1400, 560)
BUILDER_SIZE = (1400, 520)
FRAME_COUNT = 12
FRAME_DURATION_MS = 340

PINK = (232, 121, 190, 214)
PALE_PINK = (247, 174, 206, 196)
SAGE = (142, 151, 112, 174)
BLUE = (120, 145, 200, 166)
GOLD = (218, 176, 97, 158)


def fit_cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Resize and center-crop an image without stretching it."""
    target_width, target_height = size
    scale = max(target_width / image.width, target_height / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_width) // 2
    top = (resized.height - target_height) // 2
    return resized.crop((left, top, left + target_width, top + target_height)).convert("RGBA")


def trim_alpha(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bounds = rgba.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("Expected a visible mark")
    return rgba.crop(bounds)


def resize_to_height(image: Image.Image, height: int) -> Image.Image:
    width = round(image.width * height / image.height)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def load_programmable_mark(height: int) -> Image.Image:
    return resize_to_height(trim_alpha(Image.open(PROGRAMMABLE_MARK)), height)


def load_github_mark(height: int) -> Image.Image:
    """Turn GitHub's white-backed source mark into a clean transparent mark."""
    source = Image.open(GITHUB_MARK).convert("RGB")
    gray = ImageOps.grayscale(source)
    alpha = ImageOps.invert(gray).point(lambda value: 0 if value < 8 else value)
    mark = Image.new("RGBA", source.size, (24, 23, 23, 0))
    mark.putalpha(alpha)
    return resize_to_height(trim_alpha(mark), height)


def paste_center(canvas: Image.Image, artwork: Image.Image, center: tuple[int, int]) -> None:
    x = round(center[0] - artwork.width / 2)
    y = round(center[1] - artwork.height / 2)
    canvas.alpha_composite(artwork, (x, y))


def paper_petal(
    size: int,
    color: tuple[int, int, int, int],
    angle: float,
) -> Image.Image:
    """Draw one small, antialiased paper petal with a painted center vein."""
    scale = 4
    width = size * scale
    height = round(size * 1.75) * scale
    petal = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(petal)
    cx = width // 2
    points = [
        (cx, 1),
        (round(width * 0.88), round(height * 0.42)),
        (cx, height - 1),
        (round(width * 0.12), round(height * 0.42)),
    ]
    draw.polygon(points, fill=color)
    vein = tuple(max(0, channel - 30) for channel in color[:3]) + (round(color[3] * 0.42),)
    draw.line((cx, round(height * 0.18), cx, round(height * 0.82)), fill=vein, width=scale)
    petal = petal.resize((size, round(size * 1.75)), Image.Resampling.LANCZOS)
    return petal.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)


def stepped_state(frame: int) -> int:
    return frame


def add_petals(
    canvas: Image.Image,
    frame: int,
    specs: list[tuple[float, float, int, int, int, float, tuple[int, int, int, int], int]],
) -> None:
    """Place independently timed cut-paper petals in discrete stop-motion steps."""
    state = stepped_state(frame)
    for index, (px, py, amp_x, amp_y, size, base_angle, color, phase) in enumerate(specs):
        theta = ((state + phase) % 12) * math.tau / 12
        x = round(px * canvas.width + math.sin(theta) * amp_x)
        y = round(py * canvas.height + math.cos(theta * (1 + (index % 2) * 0.5)) * amp_y)
        angle = base_angle + round(math.sin(theta + index) * 8)
        petal = paper_petal(size, color, angle)
        canvas.alpha_composite(petal, (x - petal.width // 2, y - petal.height // 2))


def add_paper_dust(canvas: Image.Image, frame: int, specs: list[tuple[float, float, int]]) -> None:
    """Add sparse, stepped pollen dots without moving the paper texture."""
    state = stepped_state(frame)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for index, (px, py, phase) in enumerate(specs):
        theta = ((state + phase) % 12) * math.tau / 12
        x = round(px * canvas.width + math.sin(theta) * (3 + index % 3))
        y = round(py * canvas.height + math.cos(theta) * (2 + index % 2))
        radius = 1 + ((state + phase) % 3 == 0)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(221, 172, 104, 120))
    canvas.alpha_composite(layer)


HERO_PETALS = [
    (0.085, 0.205, 9, 7, 11, -18, PALE_PINK, 0),
    (0.155, 0.115, 7, 5, 8, 32, SAGE, 3),
    (0.255, 0.245, 10, 6, 9, -44, PINK, 7),
    (0.745, 0.190, 8, 7, 9, 36, GOLD, 2),
    (0.845, 0.110, 7, 5, 8, -25, SAGE, 6),
    (0.930, 0.220, 10, 8, 11, 42, PALE_PINK, 9),
]

BUILDER_PETALS = [
    (0.090, 0.195, 8, 6, 9, -22, PALE_PINK, 1),
    (0.205, 0.125, 7, 5, 7, 31, SAGE, 4),
    (0.795, 0.125, 7, 5, 7, -31, SAGE, 7),
    (0.910, 0.195, 8, 6, 9, 22, PALE_PINK, 10),
]


def build_hero_frames() -> list[Image.Image]:
    base = fit_cover(Image.open(HERO_SOURCE), HERO_SIZE)
    mark = load_programmable_mark(252)
    frames: list[Image.Image] = []
    for frame in range(FRAME_COUNT):
        canvas = base.copy()
        add_petals(canvas, frame, HERO_PETALS)
        add_paper_dust(
            canvas,
            frame,
            [(0.115, 0.33, 0), (0.205, 0.30, 4), (0.795, 0.29, 7), (0.885, 0.34, 10)],
        )
        # The canonical mark is always pasted last and never animated.
        paste_center(canvas, mark, (HERO_SIZE[0] // 2, 256))
        frames.append(canvas.convert("RGB"))
    return frames


def build_builder_frames() -> list[Image.Image]:
    base = fit_cover(Image.open(BUILDER_SOURCE), BUILDER_SIZE)
    programmable = load_programmable_mark(188)
    github = load_github_mark(148)
    frames: list[Image.Image] = []
    for frame in range(FRAME_COUNT):
        canvas = base.copy()
        add_petals(canvas, frame, BUILDER_PETALS)
        add_paper_dust(
            canvas,
            frame,
            [(0.300, 0.42, 1), (0.330, 0.37, 4), (0.670, 0.37, 7), (0.700, 0.42, 10)],
        )
        # Both official marks remain pixel-identical throughout the loop.
        paste_center(canvas, programmable, (605, 242))
        paste_center(canvas, github, (795, 242))
        frames.append(canvas.convert("RGB"))
    return frames


def global_palette(frames: list[Image.Image], colors: int) -> Image.Image:
    sample_width = 280
    sample_height = round(frames[0].height * sample_width / frames[0].width)
    columns = 4
    rows = math.ceil(len(frames) / columns)
    atlas = Image.new("RGB", (sample_width * columns, sample_height * rows))
    for index, frame in enumerate(frames):
        atlas.paste(
            frame.resize((sample_width, sample_height), Image.Resampling.BILINEAR),
            ((index % columns) * sample_width, (index // columns) * sample_height),
        )
    return atlas.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)


def save_gif(frames: list[Image.Image], path: Path, colors: int = 176) -> None:
    palette = global_palette(frames, colors)
    quantized = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    quantized[0].save(
        path,
        save_all=True,
        append_images=quantized[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
        disposal=1,
    )


def decode_gif(path: Path) -> list[Image.Image]:
    encoded = Image.open(path)
    decoded: list[Image.Image] = []
    for frame_index in range(encoded.n_frames):
        encoded.seek(frame_index)
        decoded.append(encoded.convert("RGB"))
    return decoded


def save_contact_sheet(frames: list[Image.Image], path: Path) -> None:
    picks = [round(index * (len(frames) - 1) / 5) for index in range(6)]
    thumb_width = 350
    thumb_height = round(frames[0].height * thumb_width / frames[0].width)
    sheet = Image.new("RGB", (thumb_width * len(picks), thumb_height), (250, 244, 237))
    for column, frame_index in enumerate(picks):
        sheet.paste(
            frames[frame_index].resize((thumb_width, thumb_height), Image.Resampling.LANCZOS),
            (column * thumb_width, 0),
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)


def crop_hashes(frames: list[Image.Image], box: tuple[int, int, int, int]) -> list[str]:
    return [hashlib.sha256(frame.crop(box).tobytes()).hexdigest() for frame in frames]


def assert_static_center(frames: list[Image.Image], box: tuple[int, int, int, int], label: str) -> None:
    hashes = crop_hashes(frames, box)
    if len(set(hashes)) != 1:
        raise RuntimeError(f"{label} protected logo area changed between frames")


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)

    hero_frames = build_hero_frames()
    builder_frames = build_builder_frames()
    save_gif(hero_frames, HERO_GIF, colors=184)
    save_gif(builder_frames, BUILDER_GIF, colors=176)
    hero_frames[0].save(HERO_STILL, quality=92, optimize=True, progressive=True)
    builder_frames[0].save(BUILDER_STILL, quality=92, optimize=True, progressive=True)

    encoded_hero = decode_gif(HERO_GIF)
    encoded_builder = decode_gif(BUILDER_GIF)
    assert_static_center(encoded_hero, (560, 105, 840, 410), "Hero")
    assert_static_center(encoded_builder, (500, 125, 900, 360), "Builder")
    save_contact_sheet(encoded_hero, QA_DIR / "hero-contact-sheet.png")
    save_contact_sheet(encoded_builder, QA_DIR / "builder-contact-sheet.png")

    manifest = {
        "hero": {
            "source": str(HERO_SOURCE.relative_to(ROOT)),
            "canonicalLogo": str(PROGRAMMABLE_MARK.relative_to(ROOT)),
            "gif": str(HERO_GIF.relative_to(ROOT)),
            "still": str(HERO_STILL.relative_to(ROOT)),
            "dimensions": list(HERO_SIZE),
            "frames": FRAME_COUNT,
            "frameDurationMs": FRAME_DURATION_MS,
            "motion": [
                "Independent cut-paper petals and sparse pollen move in visible steps",
                "The paper field, floral painting and canonical Programmable mark stay fixed",
                "No camera movement, warping, morphing, text or generated logos",
            ],
        },
        "builder": {
            "source": str(BUILDER_SOURCE.relative_to(ROOT)),
            "canonicalLogo": str(PROGRAMMABLE_MARK.relative_to(ROOT)),
            "githubLogo": str(GITHUB_MARK.relative_to(ROOT)),
            "gif": str(BUILDER_GIF.relative_to(ROOT)),
            "still": str(BUILDER_STILL.relative_to(ROOT)),
            "dimensions": list(BUILDER_SIZE),
            "frames": FRAME_COUNT,
            "frameDurationMs": FRAME_DURATION_MS,
            "motion": [
                "Independent cut-paper petals and sparse pollen move around the two official marks",
                "Both marks remain fixed and pixel-identical throughout the loop",
                "No computer scene, camera movement, warping, morphing or embedded text",
            ],
        },
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
