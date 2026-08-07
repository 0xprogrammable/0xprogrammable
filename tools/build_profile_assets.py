#!/usr/bin/env python3
"""Build the night-garden artwork used by the Programmable profile README."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "profile"
SOURCE_DIR = ASSET_DIR / "source"
QA_DIR = ROOT / ".artifacts" / "profile"

NIGHT_SKY_SOURCE = SOURCE_DIR / "programmable-night-sky-source.png"
NIGHT_BOTANICAL_SOURCE = SOURCE_DIR / "programmable-night-botanical-source.png"
BUILDER_BACKGROUND_SOURCE = SOURCE_DIR / "programmable-builder-night-background-source.png"
ECOSYSTEM_BACKGROUND_SOURCE = SOURCE_DIR / "programmable-ecosystem-night-background-source.png"
PROGRAMMABLE_MARK = SOURCE_DIR / "programmable-loop-mark.png"
GITHUB_MARK = SOURCE_DIR / "github-mark-official.png"
BUTTON_FONT = SOURCE_DIR / "fonts" / "InstrumentSans-Medium.ttf"

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
FRAME_COUNT = 12
FRAME_DURATION_MS = 400


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
    """Turn the official black-on-white GitHub source into a white mark with alpha."""
    source = Image.open(GITHUB_MARK).convert("RGB")
    alpha = ImageOps.invert(ImageOps.grayscale(source))
    alpha = alpha.point(lambda value: 0 if value < 4 else min(255, round(value * 1.08)))
    mark = Image.new("RGBA", source.size, (248, 249, 252, 0))
    mark.putalpha(alpha)
    return resize_to_height(trim_alpha(mark), height)


def paste_mark_with_glow(
    canvas: Image.Image,
    mark: Image.Image,
    center: tuple[int, int],
    glow_color: tuple[int, int, int] = (238, 119, 193),
    glow_strength: float = 0.22,
    glow_blur: int = 22,
) -> None:
    """Keep the exact mark fixed while adding a restrained static paper halo."""
    x = round(center[0] - mark.width / 2)
    y = round(center[1] - mark.height / 2)
    padding = 52
    padded_size = (mark.width + padding * 2, mark.height + padding * 2)
    padded_alpha = Image.new("L", padded_size, 0)
    padded_alpha.paste(mark.getchannel("A"), (padding, padding))
    glow_alpha = padded_alpha.filter(ImageFilter.GaussianBlur(glow_blur))
    glow = Image.new("RGBA", padded_size, (*glow_color, 0))
    glow.putalpha(glow_alpha.point(lambda value: round(value * glow_strength)))
    canvas.alpha_composite(glow, (x - padding, y - padding))
    canvas.alpha_composite(mark, (x, y))


def save_jpeg(image: Image.Image, path: Path, quality: int = 91) -> None:
    image.convert("RGB").save(path, quality=quality, optimize=True, progressive=True)


def fit_label_font(text: str, max_width: int, initial_size: int = 36) -> ImageFont.FreeTypeFont:
    size = initial_size
    while size >= 24:
        font = ImageFont.truetype(BUTTON_FONT, size)
        bounds = font.getbbox(text)
        if bounds[2] - bounds[0] <= max_width:
            return font
        size -= 1
    raise RuntimeError(f"Button label is too long: {text}")


def build_action_button(background: Path, label: str, path: Path) -> None:
    canvas = fit_cover(Image.open(background), BUTTON_SIZE)
    canvas = Image.alpha_composite(canvas, Image.new("RGBA", BUTTON_SIZE, (2, 5, 20, 58)))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (2, 2, BUTTON_SIZE[0] - 3, BUTTON_SIZE[1] - 3),
        radius=28,
        outline=(239, 130, 188, 210),
        width=3,
    )

    button_mark = load_programmable_mark(54)
    paste_mark_with_glow(canvas, button_mark, (56, BUTTON_SIZE[1] // 2), glow_strength=0.16, glow_blur=12)

    font = fit_label_font(label, 430)
    bounds = draw.textbbox((0, 0), label, font=font)
    text_height = bounds[3] - bounds[1]
    draw.text((100, round((BUTTON_SIZE[1] - text_height) / 2 - bounds[1])), label, font=font, fill=(249, 250, 255, 255))

    arrow_font = ImageFont.truetype(BUTTON_FONT, 42)
    arrow = "→"
    arrow_bounds = draw.textbbox((0, 0), arrow, font=arrow_font)
    arrow_height = arrow_bounds[3] - arrow_bounds[1]
    draw.text(
        (BUTTON_SIZE[0] - 58, round((BUTTON_SIZE[1] - arrow_height) / 2 - arrow_bounds[1])),
        arrow,
        font=arrow_font,
        fill=(239, 130, 188, 255),
    )
    canvas.save(path, optimize=True)


def build_static_assets() -> None:
    """Build the two night banners and the repository social-preview card."""
    builder = fit_cover(Image.open(BUILDER_BACKGROUND_SOURCE), BUILDER_SIZE)
    programmable = load_programmable_mark(224)
    github = load_github_mark(208)
    paste_mark_with_glow(builder, programmable, (578, 244))
    paste_mark_with_glow(
        builder,
        github,
        (822, 244),
        glow_color=(236, 241, 255),
        glow_strength=0.18,
        glow_blur=20,
    )
    save_jpeg(builder, BUILDER_STILL)

    ecosystem = fit_cover(Image.open(ECOSYSTEM_BACKGROUND_SOURCE), ECOSYSTEM_SIZE)
    ecosystem_mark = load_programmable_mark(205)
    paste_mark_with_glow(ecosystem, ecosystem_mark, (700, 242), glow_strength=0.20)
    save_jpeg(ecosystem, ECOSYSTEM_STILL)

    social = fit_cover(Image.open(ECOSYSTEM_BACKGROUND_SOURCE), SOCIAL_PREVIEW_SIZE)
    social_programmable = load_programmable_mark(270)
    social_github = load_github_mark(250)
    paste_mark_with_glow(social, social_programmable, (492, 298), glow_strength=0.24)
    paste_mark_with_glow(
        social,
        social_github,
        (788, 298),
        glow_color=(236, 241, 255),
        glow_strength=0.20,
        glow_blur=22,
    )
    save_jpeg(social, SOCIAL_PREVIEW, quality=89)

    if SOCIAL_PREVIEW.stat().st_size >= 1_000_000:
        raise RuntimeError("Repository social preview must stay below GitHub's 1 MB limit")

    build_action_button(BUILDER_BACKGROUND_SOURCE, "Open in Claude Code", CLAUDE_BUTTON)
    build_action_button(ECOSYSTEM_BACKGROUND_SOURCE, "Prompt for Codex + other agents", ANY_AGENT_BUTTON)


# Head-only masks let the painted flowers sway while the camera, stems and paper stay fixed.
# Each tuple is: (left, top, right, bottom, x amplitude, angle amplitude, phase).
FLOWER_MOTIONS = [
    (98, 382, 232, 482, 4.0, 1.15, 0),
    (244, 414, 313, 482, 2.5, 1.35, 3),
    (1022, 440, 1178, 556, 4.0, 1.10, 6),
    (1160, 380, 1232, 456, 2.5, 1.30, 9),
]


def flower_mask(
    botanical: Image.Image,
    sky: Image.Image,
    box: tuple[int, int, int, int],
) -> Image.Image:
    """Isolate painted pixels from the matching sky inside a feathered oval."""
    diff = ImageChops.difference(botanical.crop(box).convert("RGB"), sky.crop(box).convert("RGB"))
    gray = ImageOps.grayscale(diff)
    contrast = gray.point(lambda value: 0 if value < 9 else min(255, (value - 9) * 12))
    contrast = contrast.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2))

    oval = Image.new("L", contrast.size, 0)
    ImageDraw.Draw(oval).ellipse((2, 2, oval.width - 3, oval.height - 3), fill=255)
    oval = oval.filter(ImageFilter.GaussianBlur(4))
    return ImageChops.multiply(contrast, oval)


def prepare_flower_layers(
    botanical: Image.Image,
    sky: Image.Image,
) -> tuple[Image.Image, list[tuple[Image.Image, tuple[int, int, int, int], float, float, int]], Image.Image]:
    """Remove four flower heads from the base and return movable painted layers."""
    fixed = botanical.copy()
    union = Image.new("L", botanical.size, 0)
    layers: list[tuple[Image.Image, tuple[int, int, int, int], float, float, int]] = []

    for left, top, right, bottom, x_amp, angle_amp, phase in FLOWER_MOTIONS:
        box = (left, top, right, bottom)
        mask = flower_mask(botanical, sky, box)
        flower = botanical.crop(box)
        flower.putalpha(mask)
        fixed.paste(sky.crop(box), (left, top), mask)
        union.paste(ImageChops.lighter(union.crop(box), mask), (left, top))
        layers.append((flower, box, x_amp, angle_amp, phase))

    return fixed, layers, union


def build_hero_frames() -> tuple[list[Image.Image], Image.Image]:
    botanical = fit_cover(Image.open(NIGHT_BOTANICAL_SOURCE), HERO_SIZE)
    sky = fit_cover(Image.open(NIGHT_SKY_SOURCE), HERO_SIZE)
    base, flowers, mask = prepare_flower_layers(botanical, sky)
    mark = load_programmable_mark(226)
    frames: list[Image.Image] = []

    for frame in range(FRAME_COUNT):
        canvas = base.copy()
        for flower, box, x_amp, angle_amp, phase in flowers:
            theta = ((frame + phase) % FRAME_COUNT) * math.tau / FRAME_COUNT
            x_offset = round(math.sin(theta) * x_amp)
            y_offset = round((1 - math.cos(theta)) * 0.55)
            angle = math.sin(theta) * angle_amp
            moved = flower.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
            canvas.alpha_composite(moved, (box[0] + x_offset, box[1] + y_offset))

        # The canonical mark and its halo are always pasted last and never animated.
        paste_mark_with_glow(canvas, mark, (HERO_SIZE[0] // 2, 263))
        frames.append(canvas.convert("RGB"))

    return frames, mask


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


def save_gif(frames: list[Image.Image], path: Path) -> None:
    palette = global_palette(frames, 256)
    # A shared palette without error-diffusion keeps every non-moving pixel identical.
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
    picks = [0, 3, 6, 9]
    thumb_width = 700
    thumb_height = round(frames[0].height * thumb_width / frames[0].width)
    sheet = Image.new("RGB", (thumb_width * 2, thumb_height * 2), (9, 13, 35))
    for index, frame_index in enumerate(picks):
        sheet.paste(
            frames[frame_index].resize((thumb_width, thumb_height), Image.Resampling.LANCZOS),
            ((index % 2) * thumb_width, (index // 2) * thumb_height),
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

    build_static_assets()

    hero_frames, flower_mask_image = build_hero_frames()
    save_gif(hero_frames, HERO_GIF)
    hero_frames[0].save(HERO_STILL, quality=92, optimize=True, progressive=True)

    encoded_hero = decode_gif(HERO_GIF)
    assert_static_center(encoded_hero, (565, 130, 835, 400), "Hero")
    save_contact_sheet(encoded_hero, QA_DIR / "night-garden-contact-sheet.png")
    flower_mask_image.save(QA_DIR / "night-garden-flower-mask.png", optimize=True)

    manifest = {
        "hero": {
            "sources": [
                str(NIGHT_SKY_SOURCE.relative_to(ROOT)),
                str(NIGHT_BOTANICAL_SOURCE.relative_to(ROOT)),
            ],
            "canonicalLogo": str(PROGRAMMABLE_MARK.relative_to(ROOT)),
            "gif": str(HERO_GIF.relative_to(ROOT)),
            "still": str(HERO_STILL.relative_to(ROOT)),
            "dimensions": list(HERO_SIZE),
            "frames": FRAME_COUNT,
            "frameDurationMs": FRAME_DURATION_MS,
            "motion": [
                "Four painted flower heads move in small stepped sways",
                "The camera, night sky, stems and canonical Programmable mark stay fixed",
                "No warping, morphing, text, generated logos or global color cycling",
            ],
        },
        "builder": {
            "source": str(BUILDER_BACKGROUND_SOURCE.relative_to(ROOT)),
            "canonicalLogos": [
                str(PROGRAMMABLE_MARK.relative_to(ROOT)),
                str(GITHUB_MARK.relative_to(ROOT)),
            ],
            "still": str(BUILDER_STILL.relative_to(ROOT)),
            "dimensions": list(BUILDER_SIZE),
            "composition": "Optically balanced Programmable and white GitHub marks in a moonlit garden",
        },
        "ecosystem": {
            "source": str(ECOSYSTEM_BACKGROUND_SOURCE.relative_to(ROOT)),
            "canonicalLogo": str(PROGRAMMABLE_MARK.relative_to(ROOT)),
            "still": str(ECOSYSTEM_STILL.relative_to(ROOT)),
            "dimensions": list(ECOSYSTEM_SIZE),
            "composition": "A quiet night-garden clearing with the Programmable mark",
        },
        "socialPreview": {
            "source": str(ECOSYSTEM_BACKGROUND_SOURCE.relative_to(ROOT)),
            "canonicalLogos": [
                str(PROGRAMMABLE_MARK.relative_to(ROOT)),
                str(GITHUB_MARK.relative_to(ROOT)),
            ],
            "still": str(SOCIAL_PREVIEW.relative_to(ROOT)),
            "dimensions": list(SOCIAL_PREVIEW_SIZE),
            "maxBytes": 1000000,
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
