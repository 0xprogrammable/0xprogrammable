#!/usr/bin/env python3
"""Build the animated, self-hosted artwork used by the GitHub profile README."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "profile"
SOURCE_DIR = ASSET_DIR / "source"
QA_DIR = ROOT / ".artifacts" / "profile"

HERO_SOURCE = SOURCE_DIR / "programmable-profile-ecosystem-source.png"
BUILDER_SOURCE = SOURCE_DIR / "programmable-builder-source.png"

HERO_GIF = ASSET_DIR / "programmable-profile-ecosystem.gif"
HERO_STILL = ASSET_DIR / "programmable-profile-ecosystem.jpg"
BUILDER_GIF = ASSET_DIR / "programmable-builder-skill.gif"
BUILDER_STILL = ASSET_DIR / "programmable-builder-skill.jpg"
MANIFEST = ASSET_DIR / "animation-manifest.json"

WIDTH = 1400
HERO_FRAMES = 28
FRAME_DURATION_MS = 190

PINK = (232, 118, 171)
PALE_PINK = (245, 181, 207)
BLUE = (114, 150, 193)
GOLD = (231, 199, 129)
IVORY = (250, 242, 222)


def fit_width(image: Image.Image, width: int = WIDTH) -> Image.Image:
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def bezier(points: list[tuple[float, float]], t: float) -> tuple[float, float]:
    """Evaluate a Bezier curve of arbitrary degree using De Casteljau."""
    work = list(points)
    while len(work) > 1:
        work = [
            (
                work[i][0] * (1 - t) + work[i + 1][0] * t,
                work[i][1] * (1 - t) + work[i + 1][1] * t,
            )
            for i in range(len(work) - 1)
        ]
    return work[0]


def stepped_wave(frame: int, period: int, phase: int = 0) -> float:
    step = ((frame + phase) % period) / period
    raw = 0.5 + 0.5 * math.sin(step * math.tau)
    return round(raw * 4) / 4


def draw_cross(draw: ImageDraw.ImageDraw, x: float, y: float, radius: int, color: tuple[int, ...]) -> None:
    draw.line((x - radius, y, x + radius, y), fill=color, width=1)
    draw.line((x, y - radius, x, y + radius), fill=color, width=1)
    draw.ellipse((x - 1, y - 1, x + 1, y + 1), fill=color)


def add_hero_motion(base: Image.Image, frame: int) -> Image.Image:
    width, height = base.size
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    crisp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    draw = ImageDraw.Draw(crisp)

    # The source art stays completely still. Only separately composed paper-light
    # details move, preserving the hand-built collage instead of warping it.
    seed = (0.105 * width, 0.545 * height)
    pulse = stepped_wave(frame, 16)
    for ring, alpha in ((35, 58), (50, 38), (66, 22)):
        r = ring + round(6 * pulse)
        glow_draw.ellipse(
            (seed[0] - r, seed[1] - r, seed[0] + r, seed[1] + r),
            outline=GOLD + (round(alpha * (0.55 + 0.45 * pulse)),),
            width=2,
        )

    routes = [
        [(0.13, 0.54), (0.34, 0.40), (0.55, 0.43), (0.78, 0.20)],
        [(0.13, 0.54), (0.35, 0.45), (0.57, 0.55), (0.82, 0.51)],
        [(0.13, 0.54), (0.34, 0.50), (0.51, 0.70), (0.73, 0.77)],
    ]
    for route_index, route in enumerate(routes):
        route_px = [(x * width, y * height) for x, y in route]
        for mote in range(3):
            t = ((frame + route_index * 4 + mote * 9) % HERO_FRAMES) / (HERO_FRAMES - 1)
            x, y = bezier(route_px, t)
            intensity = 0.45 + 0.55 * stepped_wave(frame, 12, route_index * 3 + mote * 2)
            radius = 3 if intensity < 0.75 else 5
            glow_draw.ellipse(
                (x - 13, y - 13, x + 13, y + 13),
                fill=GOLD + (round(58 * intensity),),
            )
            draw_cross(draw, x, y, radius, IVORY + (round(205 + 50 * intensity),))
            for trail_step in range(1, 4):
                trail_t = max(0, t - trail_step * 0.012)
                trail_x, trail_y = bezier(route_px, trail_t)
                trail_radius = max(1, 4 - trail_step)
                draw.ellipse(
                    (
                        trail_x - trail_radius,
                        trail_y - trail_radius,
                        trail_x + trail_radius,
                        trail_y + trail_radius,
                    ),
                    fill=GOLD + (125 - trail_step * 25,),
                )

    # Pool rings illuminate in independent stepped phases, making the three
    # destinations read as distinct models rather than one synchronized effect.
    pools = [
        (0.765, 0.205, 0),
        (0.825, 0.515, 6),
        (0.735, 0.775, 11),
    ]
    for px, py, phase in pools:
        wave = stepped_wave(frame, 19, phase)
        cx, cy = px * width, py * height
        for offset, color in ((0, BLUE), (9, PALE_PINK), (18, GOLD)):
            radius_x = 28 + offset + round(wave * 11)
            radius_y = round(radius_x * 0.39)
            draw.arc(
                (cx - radius_x, cy - radius_y, cx + radius_x, cy + radius_y),
                198,
                342,
                fill=color + (round(105 + 125 * wave),),
                width=2,
            )
        draw.ellipse(
            (cx - 3, cy - 3, cx + 3, cy + 3),
            fill=IVORY + (round(120 + 120 * wave),),
        )

    stars = [
        (0.075, 0.105, 0),
        (0.245, 0.080, 4),
        (0.365, 0.145, 9),
        (0.478, 0.075, 14),
        (0.600, 0.120, 2),
        (0.305, 0.760, 7),
        (0.482, 0.870, 12),
        (0.565, 0.660, 16),
    ]
    for sx, sy, phase in stars:
        intensity = stepped_wave(frame, 17, phase)
        if intensity >= 0.5:
            draw_cross(
                draw,
                sx * width,
                sy * height,
                3 + round(3 * intensity),
                GOLD + (round(75 + 150 * intensity),),
            )

    # Six small paper petals follow unique, intentionally stepped arcs.
    petal_specs = [
        (0.225, 0.235, 8, 0, PALE_PINK),
        (0.310, 0.310, 11, 5, IVORY),
        (0.420, 0.180, 7, 10, PINK),
        (0.535, 0.335, 10, 14, GOLD),
        (0.620, 0.260, 6, 19, PALE_PINK),
        (0.685, 0.600, 9, 23, BLUE),
    ]
    for index, (px, py, travel, phase, color) in enumerate(petal_specs):
        state = ((frame + phase) % HERO_FRAMES) // 3
        dx = (state % 5) - 2
        dy = -((state * (index % 3 + 1)) % travel)
        x = px * width + dx * 1.4
        y = py * height + dy
        angle = ((state + index) % 6) * math.pi / 6
        rx, ry = 7, 3
        points = []
        for sign_x, sign_y in ((-rx, 0), (0, -ry), (rx, 0), (0, ry)):
            pxr = sign_x * math.cos(angle) - sign_y * math.sin(angle)
            pyr = sign_x * math.sin(angle) + sign_y * math.cos(angle)
            points.append((x + pxr, y + pyr))
        draw.polygon(points, fill=color + (180,))

    glow = glow.filter(ImageFilter.GaussianBlur(radius=5))
    return Image.alpha_composite(Image.alpha_composite(base.convert("RGBA"), glow), crisp).convert("RGB")


def add_builder_motion(base: Image.Image, frame: int) -> Image.Image:
    width, height = base.size
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    crisp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    draw = ImageDraw.Draw(crisp)

    # The monitor, paper background and both marks are immutable. Motion is
    # authored only as independent pollen, petal and light-cutout layers.
    pollen_routes = [
        [(0.37, 0.80), (0.30, 0.66), (0.23, 0.56), (0.16, 0.48)],
        [(0.46, 0.74), (0.42, 0.57), (0.39, 0.43), (0.36, 0.31)],
        [(0.60, 0.76), (0.64, 0.60), (0.68, 0.45), (0.72, 0.29)],
        [(0.72, 0.70), (0.77, 0.58), (0.82, 0.46), (0.87, 0.34)],
    ]
    for route_index, route in enumerate(pollen_routes):
        route_px = [(x * width, y * height) for x, y in route]
        for mote in range(3):
            t = ((frame + route_index * 5 + mote * 9) % HERO_FRAMES) / (HERO_FRAMES - 1)
            x, y = bezier(route_px, t)
            intensity = stepped_wave(frame, 15, route_index * 3 + mote * 4)
            glow_draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill=GOLD + (round(26 + 38 * intensity),))
            draw_cross(draw, x, y, 3 + round(2 * intensity), IVORY + (round(155 + 90 * intensity),))

    twinkles = [
        (0.13, 0.23, 1),
        (0.22, 0.38, 7),
        (0.30, 0.64, 13),
        (0.44, 0.25, 18),
        (0.57, 0.18, 4),
        (0.66, 0.34, 10),
        (0.78, 0.22, 15),
        (0.86, 0.47, 21),
        (0.73, 0.67, 25),
    ]
    for tx, ty, phase in twinkles:
        intensity = stepped_wave(frame, 18, phase)
        if intensity >= 0.5:
            draw_cross(
                draw,
                tx * width,
                ty * height,
                3 + round(3 * intensity),
                GOLD + (round(95 + 150 * intensity),),
            )

    petals = [
        (0.32, 0.52, 0, PINK),
        (0.41, 0.34, 5, PALE_PINK),
        (0.55, 0.26, 10, IVORY),
        (0.64, 0.39, 15, GOLD),
        (0.74, 0.30, 20, PALE_PINK),
        (0.82, 0.57, 24, BLUE),
    ]
    for index, (px, py, phase, color) in enumerate(petals):
        state = ((frame + phase) % HERO_FRAMES) // 3
        x = px * width + ((state + index) % 5 - 2) * 2
        y = py * height - ((state * (index % 3 + 2)) % 18)
        angle = ((state + index) % 8) * math.pi / 8
        points = []
        for sign_x, sign_y in ((-7, 0), (0, -3), (7, 0), (0, 3)):
            pxr = sign_x * math.cos(angle) - sign_y * math.sin(angle)
            pyr = sign_x * math.sin(angle) + sign_y * math.cos(angle)
            points.append((x + pxr, y + pyr))
        draw.polygon(points, fill=color + (190,))

    glow = glow.filter(ImageFilter.GaussianBlur(radius=5))
    return Image.alpha_composite(Image.alpha_composite(base.convert("RGBA"), glow), crisp).convert("RGB")


def global_palette(frames: list[Image.Image], colors: int) -> Image.Image:
    sample_width = 240
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


def quantize_frames(frames: list[Image.Image], colors: int = 112) -> list[Image.Image]:
    palette = global_palette(frames, colors)
    return [
        frame.quantize(palette=palette, dither=Image.Dither.NONE)
        for frame in frames
    ]


def save_gif(frames: list[Image.Image], path: Path, duration_ms: int, colors: int = 112) -> None:
    quantized = quantize_frames(frames, colors)
    quantized[0].save(
        path,
        save_all=True,
        append_images=quantized[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
        disposal=1,
    )


def build_hero() -> list[Image.Image]:
    source = Image.open(HERO_SOURCE).convert("RGB")
    base = fit_width(source)
    frames = [add_hero_motion(base, frame) for frame in range(HERO_FRAMES)]
    save_gif(frames, HERO_GIF, FRAME_DURATION_MS, colors=192)
    base.save(HERO_STILL, quality=91, optimize=True, progressive=True)
    return frames


def build_builder() -> list[Image.Image]:
    source = Image.open(BUILDER_SOURCE)
    source.seek(0)
    base = source.convert("RGB")
    target_height = round(base.width / 2.20)
    base = base.crop((0, 0, base.width, min(base.height, target_height)))
    base = fit_width(base)
    output_frames = [add_builder_motion(base, frame) for frame in range(HERO_FRAMES)]
    save_gif(output_frames, BUILDER_GIF, FRAME_DURATION_MS, colors=176)
    output_frames[0].save(BUILDER_STILL, quality=90, optimize=True, progressive=True)
    return output_frames


def save_contact_sheet(frames: list[Image.Image], path: Path) -> None:
    picks = [0, len(frames) // 5, 2 * len(frames) // 5, 3 * len(frames) // 5, 4 * len(frames) // 5]
    thumb_width = 420
    thumb_height = round(frames[0].height * thumb_width / frames[0].width)
    sheet = Image.new("RGB", (thumb_width * len(picks), thumb_height), (245, 242, 236))
    for index, frame_index in enumerate(picks):
        sheet.paste(
            frames[frame_index].resize((thumb_width, thumb_height), Image.Resampling.LANCZOS),
            (index * thumb_width, 0),
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)


def decode_gif(path: Path) -> list[Image.Image]:
    encoded = Image.open(path)
    decoded: list[Image.Image] = []
    for frame_index in range(encoded.n_frames):
        encoded.seek(frame_index)
        decoded.append(encoded.convert("RGB"))
    return decoded


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    hero_frames = build_hero()
    builder_frames = build_builder()
    encoded_hero_frames = decode_gif(HERO_GIF)
    encoded_builder_frames = decode_gif(BUILDER_GIF)
    save_contact_sheet(encoded_hero_frames, QA_DIR / "hero-contact-sheet.png")
    save_contact_sheet(encoded_builder_frames, QA_DIR / "builder-contact-sheet.png")

    manifest = {
        "hero": {
            "source": str(HERO_SOURCE.relative_to(ROOT)),
            "gif": str(HERO_GIF.relative_to(ROOT)),
            "still": str(HERO_STILL.relative_to(ROOT)),
            "dimensions": list(hero_frames[0].size),
            "frames": len(hero_frames),
            "frameDurationMs": FRAME_DURATION_MS,
            "motion": [
                "Independent stepped light moving from one idea into three model branches",
                "Three separately phased pool ripple systems",
                "Independent paper petals and restrained star twinkles",
                "No camera movement, source deformation, morphing, or embedded text",
            ],
        },
        "builder": {
            "source": str(BUILDER_SOURCE.relative_to(ROOT)),
            "gif": str(BUILDER_GIF.relative_to(ROOT)),
            "still": str(BUILDER_STILL.relative_to(ROOT)),
            "dimensions": list(encoded_builder_frames[0].size),
            "frames": len(encoded_builder_frames),
            "frameDurationMs": FRAME_DURATION_MS,
            "motion": [
                "Independent pollen and paper-petal movement",
                "No camera movement, scene deformation, or logo morphing",
            ],
        },
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
