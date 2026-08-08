#!/usr/bin/env python3
"""Build the Warm-Ivory Night-Garden artwork used by the Programmable profile."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "profile"
SOURCE_DIR = ASSET_DIR / "source"
QA_DIR = ROOT / ".artifacts" / "profile"

LEFT_PLANT_SOURCE = SOURCE_DIR / "programmable-botanical-left-v2.webp"
RIGHT_PLANT_SOURCE = SOURCE_DIR / "programmable-botanical-right-v2.webp"
PROGRAMMABLE_MARK = SOURCE_DIR / "programmable-loop-mark-warm-ivory.png"
GITHUB_MARK = SOURCE_DIR / "github-mark-official.png"
BUTTON_FONT = SOURCE_DIR / "fonts" / "InstrumentSans-Medium.ttf"
AVATAR = ASSET_DIR / "programmable-github-avatar-warm-ivory-4096.png"

HERO_GIF = ASSET_DIR / "programmable-night-garden.gif"
HERO_STILL = ASSET_DIR / "programmable-night-garden.jpg"
BUILDER_STILL = ASSET_DIR / "programmable-builder-skill.jpg"
ECOSYSTEM_STILL = ASSET_DIR / "programmable-profile-ecosystem.jpg"
SOCIAL_PREVIEW = ASSET_DIR / "programmable-github-social-preview.jpg"
CLAUDE_BUTTON = ASSET_DIR / "open-in-claude-code-night.png"
ANY_AGENT_BUTTON = ASSET_DIR / "copy-for-any-agent-night.png"
MANIFEST = ASSET_DIR / "animation-manifest.json"

HERO_SIZE = (1400, 560)
BUILDER_SIZE = (1400, 560)
ECOSYSTEM_SIZE = (1400, 560)
SOCIAL_PREVIEW_SIZE = (1280, 640)
BUTTON_SIZE = (600, 156)
FRAME_COUNT = 16
FRAME_DURATION_MS = 360

CANVAS = (1, 1, 3)
WARM_IVORY = (248, 240, 233)
COOL_WHITE = (229, 238, 255)

# The same sparse point-star logic as the website. These are dots, never crosses.
STATIC_STARS = [
    (3.0, 18.0, 0.7, 0.54),
    (9.0, 39.0, 0.65, 0.46),
    (14.0, 8.0, 0.65, 0.40),
    (19.0, 24.0, 0.7, 0.52),
    (29.0, 16.0, 0.65, 0.42),
    (37.0, 27.0, 0.7, 0.48),
    (47.0, 9.0, 0.65, 0.44),
    (61.0, 19.0, 0.7, 0.44),
    (69.0, 29.0, 0.65, 0.50),
    (77.0, 7.0, 0.7, 0.46),
    (87.0, 36.0, 0.65, 0.42),
    (96.0, 17.0, 0.7, 0.52),
    (6.0, 54.0, 0.6, 0.36),
    (12.0, 25.0, 0.6, 0.38),
    (23.0, 34.0, 0.6, 0.34),
    (32.0, 6.0, 0.6, 0.34),
    (43.0, 29.0, 0.6, 0.38),
    (52.0, 20.0, 0.6, 0.34),
    (58.0, 12.0, 0.6, 0.36),
    (72.0, 31.0, 0.6, 0.34),
    (82.0, 33.5, 0.6, 0.36),
    (91.0, 11.0, 0.6, 0.38),
    (94.0, 47.0, 0.6, 0.34),
    (99.0, 29.0, 0.6, 0.36),
]

TWINKLE_STARS = [
    (7.5, 12.5, 1.0, 0.1),
    (89.6, 14.8, 1.0, 0.7),
    (16.8, 31.2, 1.4, 0.35),
    (76.4, 21.5, 1.0, 0.9),
    (94.1, 38.6, 1.3, 0.2),
    (7.5, 50.7, 0.9, 0.58),
    (26.2, 8.1, 1.0, 0.78),
    (54.8, 11.7, 1.0, 0.42),
    (68.7, 7.4, 1.4, 0.03),
    (94.5, 52.3, 0.9, 0.66),
    (21.7, 43.8, 1.0, 0.28),
    (72.2, 30.4, 1.0, 0.82),
    (2.6, 6.5, 0.8, 0.48),
    (84.1, 4.7, 1.2, 0.16),
    (90.8, 27.4, 0.9, 0.54),
    (30.8, 38.6, 1.2, 0.94),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def trim_alpha(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bounds = rgba.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("Expected a visible alpha asset")
    return rgba.crop(bounds)


def resize_to_height(image: Image.Image, height: int) -> Image.Image:
    width = round(image.width * height / image.height)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def resize_to_width(image: Image.Image, width: int) -> Image.Image:
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def with_opacity(image: Image.Image, opacity: float) -> Image.Image:
    rgba = image.convert("RGBA")
    rgba.putalpha(rgba.getchannel("A").point(lambda value: round(value * opacity)))
    return rgba


def load_programmable_mark(height: int) -> Image.Image:
    source = trim_alpha(Image.open(PROGRAMMABLE_MARK))
    mark = Image.new("RGBA", source.size, (*WARM_IVORY, 0))
    mark.putalpha(source.getchannel("A"))
    return resize_to_height(mark, height)


def load_github_mark(height: int) -> Image.Image:
    """Turn GitHub's official black-on-white source into a Warm-Ivory mark with alpha."""
    source = Image.open(GITHUB_MARK).convert("RGB")
    alpha = ImageOps.invert(ImageOps.grayscale(source))
    alpha = alpha.point(lambda value: 0 if value < 4 else min(255, round(value * 1.08)))
    mark = Image.new("RGBA", source.size, (*WARM_IVORY, 0))
    mark.putalpha(alpha)
    return resize_to_height(trim_alpha(mark), height)


def load_plant(path: Path, width: int, opacity: float) -> Image.Image:
    plant = Image.open(path).convert("RGBA")
    plant = ImageEnhance.Color(plant).enhance(1.18)
    plant = ImageEnhance.Brightness(plant).enhance(1.04)
    return with_opacity(resize_to_width(plant, width), opacity)


def paste_mark_with_glow(
    canvas: Image.Image,
    mark: Image.Image,
    center: tuple[int, int],
    glow_color: tuple[int, int, int] = WARM_IVORY,
    glow_strength: float = 0.08,
    glow_blur: int = 18,
) -> None:
    x = round(center[0] - mark.width / 2)
    y = round(center[1] - mark.height / 2)
    padding = 42
    padded_size = (mark.width + padding * 2, mark.height + padding * 2)
    padded_alpha = Image.new("L", padded_size, 0)
    padded_alpha.paste(mark.getchannel("A"), (padding, padding))
    glow_alpha = padded_alpha.filter(ImageFilter.GaussianBlur(glow_blur))
    glow = Image.new("RGBA", padded_size, (*glow_color, 0))
    glow.putalpha(glow_alpha.point(lambda value: round(value * glow_strength)))
    canvas.alpha_composite(glow, (x - padding, y - padding))
    canvas.alpha_composite(mark, (x, y))


def add_ground_glow(canvas: Image.Image, strength: float = 1.0) -> None:
    width, height = canvas.size
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    draw.ellipse(
        (round(width * 0.16), round(height * 0.78), round(width * 0.84), round(height * 1.34)),
        fill=(191, 125, 218, round(82 * strength)),
    )
    draw.ellipse(
        (round(width * -0.10), round(height * 0.82), round(width * 0.30), round(height * 1.28)),
        fill=(184, 107, 205, round(34 * strength)),
    )
    draw.ellipse(
        (round(width * 0.70), round(height * 0.82), round(width * 1.10), round(height * 1.28)),
        fill=(115, 94, 181, round(34 * strength)),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(max(20, round(height * 0.12))))
    canvas.alpha_composite(glow)


def add_star_field(canvas: Image.Image, frame: int = 0) -> None:
    width, height = canvas.size
    stars = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(stars)

    for index, (x_pct, y_pct, radius, opacity) in enumerate(STATIC_STARS):
        x = round(width * x_pct / 100)
        y = round(height * y_pct / 100)
        pixel_radius = max(0.75, radius * width / 1400 * 1.4)
        color = WARM_IVORY if index % 3 else COOL_WHITE
        alpha = round(255 * opacity)
        draw.ellipse((x - pixel_radius, y - pixel_radius, x + pixel_radius, y + pixel_radius), fill=(*color, alpha))

    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for index, (x_pct, y_pct, radius, phase) in enumerate(TWINKLE_STARS):
        theta = math.tau * ((frame / FRAME_COUNT + phase) % 1.0)
        pulse = ((math.sin(theta) + 1) / 2) ** (5 if index % 3 else 8)
        alpha = round(32 + pulse * 205)
        scale = 0.78 + pulse * 0.58
        x = round(width * x_pct / 100)
        y = round(height * y_pct / 100)
        pixel_radius = max(0.85, radius * width / 1400 * scale * 1.35)
        color = COOL_WHITE if index % 4 == 1 else WARM_IVORY
        draw.ellipse((x - pixel_radius, y - pixel_radius, x + pixel_radius, y + pixel_radius), fill=(*color, alpha))
        if pulse > 0.45:
            glow_radius = pixel_radius * 2.4
            glow_draw.ellipse(
                (x - glow_radius, y - glow_radius, x + glow_radius, y + glow_radius),
                fill=(*color, round(45 * pulse)),
            )

    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(2.2)))
    canvas.alpha_composite(stars)


def plant_angles(frame: int) -> tuple[float, float]:
    theta = math.tau * frame / FRAME_COUNT
    left = 0.18 + math.sin(theta - 1.18) * 1.10 + math.sin(theta * 2 + 0.42) * 0.24
    right = -0.12 + math.sin(theta + 1.46) * 1.25 + math.sin(theta * 3 - 0.31) * 0.21
    return left, right


def paste_plants(canvas: Image.Image, frame: int, plant_width: int, opacity: float) -> None:
    left = load_plant(LEFT_PLANT_SOURCE, plant_width, opacity)
    right = load_plant(RIGHT_PLANT_SOURCE, plant_width, opacity)
    left_angle, right_angle = plant_angles(frame)

    left = left.rotate(
        left_angle,
        resample=Image.Resampling.BICUBIC,
        center=(round(left.width * 0.41), round(left.height * 0.972)),
        expand=False,
        fillcolor=(0, 0, 0, 0),
    )
    right = right.rotate(
        right_angle,
        resample=Image.Resampling.BICUBIC,
        center=(round(right.width * 0.68), round(right.height * 0.972)),
        expand=False,
        fillcolor=(0, 0, 0, 0),
    )

    width, height = canvas.size
    bottom_overlap = max(8, round(height * 0.035))
    canvas.alpha_composite(left, (-round(plant_width * 0.08), height - left.height + bottom_overlap))
    canvas.alpha_composite(right, (width - right.width + round(plant_width * 0.09), height - right.height + bottom_overlap))


def build_scene(
    size: tuple[int, int],
    frame: int = 0,
    plant_width: int | None = None,
    plant_opacity: float = 0.94,
    ground_strength: float = 1.0,
) -> Image.Image:
    canvas = Image.new("RGBA", size, (*CANVAS, 255))
    add_ground_glow(canvas, ground_strength)
    add_star_field(canvas, frame)
    if plant_width is not None:
        paste_plants(canvas, frame, plant_width, plant_opacity)
    return canvas


def save_jpeg(image: Image.Image, path: Path, quality: int = 92) -> None:
    image.convert("RGB").save(path, quality=quality, optimize=True, progressive=True)


def fit_label_font(text: str, max_width: int, initial_size: int = 30) -> ImageFont.FreeTypeFont:
    size = initial_size
    while size >= 24:
        font = ImageFont.truetype(BUTTON_FONT, size)
        bounds = font.getbbox(text)
        if bounds[2] - bounds[0] <= max_width:
            return font
        size -= 1
    raise RuntimeError(f"Button label is too long: {text}")


def build_action_button(label: str, path: Path, frame: int) -> None:
    canvas = build_scene(BUTTON_SIZE, frame=frame, ground_strength=0.72)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (2, 2, BUTTON_SIZE[0] - 3, BUTTON_SIZE[1] - 3),
        radius=26,
        outline=(*WARM_IVORY, 74),
        width=2,
    )

    button_mark = load_programmable_mark(40)
    paste_mark_with_glow(canvas, button_mark, (51, BUTTON_SIZE[1] // 2), glow_strength=0.07, glow_blur=10)

    font = fit_label_font(label, 400)
    bounds = draw.textbbox((0, 0), label, font=font)
    text_height = bounds[3] - bounds[1]
    draw.text(
        (104, round((BUTTON_SIZE[1] - text_height) / 2 - bounds[1])),
        label,
        font=font,
        fill=(*WARM_IVORY, 255),
    )

    arrow_font = ImageFont.truetype(BUTTON_FONT, 40)
    arrow_bounds = draw.textbbox((0, 0), "→", font=arrow_font)
    arrow_height = arrow_bounds[3] - arrow_bounds[1]
    draw.text(
        (BUTTON_SIZE[0] - 58, round((BUTTON_SIZE[1] - arrow_height) / 2 - arrow_bounds[1])),
        "→",
        font=arrow_font,
        fill=(*WARM_IVORY, 224),
    )
    canvas.save(path, optimize=True)


def build_static_assets() -> None:
    builder = build_scene(BUILDER_SIZE, frame=4, plant_width=286)
    paste_mark_with_glow(builder, load_programmable_mark(174), (572, 244))
    paste_mark_with_glow(
        builder,
        load_github_mark(154),
        (828, 244),
        glow_color=WARM_IVORY,
        glow_strength=0.07,
    )
    save_jpeg(builder, BUILDER_STILL)

    ecosystem = build_scene(ECOSYSTEM_SIZE, frame=8, plant_width=250, ground_strength=0.88)
    paste_mark_with_glow(ecosystem, load_programmable_mark(140), (700, 240), glow_strength=0.06)
    save_jpeg(ecosystem, ECOSYSTEM_STILL)

    social = build_scene(SOCIAL_PREVIEW_SIZE, frame=12, plant_width=276)
    paste_mark_with_glow(social, load_programmable_mark(208), (492, 292))
    paste_mark_with_glow(
        social,
        load_github_mark(180),
        (788, 292),
        glow_color=WARM_IVORY,
        glow_strength=0.07,
    )
    save_jpeg(social, SOCIAL_PREVIEW, quality=91)
    if SOCIAL_PREVIEW.stat().st_size >= 1_000_000:
        raise RuntimeError("Repository social preview must stay below GitHub's 1 MB limit")

    build_action_button("Open in Claude Code", CLAUDE_BUTTON, frame=3)
    build_action_button("Prompt for any coding agent", ANY_AGENT_BUTTON, frame=11)


def build_hero_frames() -> list[Image.Image]:
    mark = load_programmable_mark(166)
    frames: list[Image.Image] = []
    for frame in range(FRAME_COUNT):
        canvas = build_scene(HERO_SIZE, frame=frame, plant_width=286)
        paste_mark_with_glow(canvas, mark, (HERO_SIZE[0] // 2, 244))
        frames.append(canvas.convert("RGB"))
    return frames


def global_palette(frames: list[Image.Image], colors: int = 192) -> Image.Image:
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


def save_gif(frames: list[Image.Image], path: Path) -> None:
    palette = global_palette(frames)
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
    picks = [0, 4, 8, 12]
    thumb_width = 700
    thumb_height = round(frames[0].height * thumb_width / frames[0].width)
    sheet = Image.new("RGB", (thumb_width * 2, thumb_height * 2), CANVAS)
    for index, frame_index in enumerate(picks):
        sheet.paste(
            frames[frame_index].resize((thumb_width, thumb_height), Image.Resampling.LANCZOS),
            ((index % 2) * thumb_width, (index // 2) * thumb_height),
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)


def assert_static_center(frames: list[Image.Image]) -> None:
    box = (610, 145, 790, 345)
    hashes = [hashlib.sha256(frame.crop(box).tobytes()).hexdigest() for frame in frames]
    if len(set(hashes)) != 1:
        raise RuntimeError("The protected Warm-Ivory logo area changed between frames")


def assert_brand_sources() -> None:
    mark = Image.open(PROGRAMMABLE_MARK).convert("RGBA")
    opaque = [pixel[:3] for pixel in mark.getdata() if pixel[3] >= 250]
    exact_warm_ivory = sum(color == WARM_IVORY for color in opaque)
    if not opaque or exact_warm_ivory / len(opaque) < 0.97:
        raise RuntimeError("Programmable mark core must be Warm Ivory")
    avatar = Image.open(AVATAR).convert("RGBA")
    if avatar.getpixel((0, 0))[:3] != (0, 0, 0):
        raise RuntimeError("GitHub avatar must retain its pure-black canvas")


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    assert_brand_sources()
    build_static_assets()

    hero_frames = build_hero_frames()
    save_gif(hero_frames, HERO_GIF)
    save_jpeg(hero_frames[0], HERO_STILL, quality=93)

    encoded_hero = decode_gif(HERO_GIF)
    assert_static_center(encoded_hero)
    save_contact_sheet(encoded_hero, QA_DIR / "night-garden-contact-sheet.png")

    manifest = {
        "brand": {
            "canvas": "#010103",
            "warmIvory": "#f8f0e9",
            "canonicalLogo": str(PROGRAMMABLE_MARK.relative_to(ROOT)),
            "avatar": str(AVATAR.relative_to(ROOT)),
            "sourceSha256": {
                str(PROGRAMMABLE_MARK.relative_to(ROOT)): sha256(PROGRAMMABLE_MARK),
                str(LEFT_PLANT_SOURCE.relative_to(ROOT)): sha256(LEFT_PLANT_SOURCE),
                str(RIGHT_PLANT_SOURCE.relative_to(ROOT)): sha256(RIGHT_PLANT_SOURCE),
                str(AVATAR.relative_to(ROOT)): sha256(AVATAR),
            },
        },
        "hero": {
            "sources": [
                str(LEFT_PLANT_SOURCE.relative_to(ROOT)),
                str(RIGHT_PLANT_SOURCE.relative_to(ROOT)),
            ],
            "gif": str(HERO_GIF.relative_to(ROOT)),
            "still": str(HERO_STILL.relative_to(ROOT)),
            "dimensions": list(HERO_SIZE),
            "frames": FRAME_COUNT,
            "frameDurationMs": FRAME_DURATION_MS,
            "motion": [
                "Two painted plant groups sway independently from anchored roots",
                "Round microstars twinkle in staggered phases without crosses or spatial drift",
                "The camera, canvas and Warm-Ivory Programmable mark stay fixed",
            ],
        },
        "builder": {
            "canonicalLogos": [
                str(PROGRAMMABLE_MARK.relative_to(ROOT)),
                str(GITHUB_MARK.relative_to(ROOT)),
            ],
            "still": str(BUILDER_STILL.relative_to(ROOT)),
            "dimensions": list(BUILDER_SIZE),
        },
        "ecosystem": {
            "canonicalLogo": str(PROGRAMMABLE_MARK.relative_to(ROOT)),
            "still": str(ECOSYSTEM_STILL.relative_to(ROOT)),
            "dimensions": list(ECOSYSTEM_SIZE),
        },
        "socialPreview": {
            "canonicalLogos": [
                str(PROGRAMMABLE_MARK.relative_to(ROOT)),
                str(GITHUB_MARK.relative_to(ROOT)),
            ],
            "still": str(SOCIAL_PREVIEW.relative_to(ROOT)),
            "dimensions": list(SOCIAL_PREVIEW_SIZE),
            "maxBytes": 1_000_000,
        },
        "actions": {
            "font": str(BUTTON_FONT.relative_to(ROOT)),
            "dimensions": list(BUTTON_SIZE),
            "buttons": [
                str(CLAUDE_BUTTON.relative_to(ROOT)),
                str(ANY_AGENT_BUTTON.relative_to(ROOT)),
            ],
        },
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
