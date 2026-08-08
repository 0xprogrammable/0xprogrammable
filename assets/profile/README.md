# Profile artwork

These assets are the self-hosted artwork for Programmable's public GitHub profile.

- `programmable-night-garden.gif` centers the Warm-Ivory Programmable mark in the landing page's deep-black night
  garden while two painted plant groups sway independently and round microstars twinkle in staggered phases.
- `programmable-night-garden.jpg` is the reduced-motion fallback.
- `programmable-builder-skill.jpg` balances the canonical Warm-Ivory Programmable mark and GitHub's official
  silhouette, rendered in the same Warm-Ivory palette, in a moonlit garden composition.
- `programmable-profile-ecosystem.jpg` closes the README with a connected root garden. Separate plants share one
  visible underground network without repeating the hero logo composition.
- `programmable-github-social-preview.jpg` is the 1280×640 repository social-preview image. GitHub uses the account
  avatar—not this image—when someone shares the shorter personal-profile URL.
- `programmable-github-avatar-warm-ivory-4096.png` is the pure-black 4096×4096 profile master with the Warm-Ivory
  mark sized for GitHub's circular crop.
- `animation-manifest.json` records dimensions, timing and motion constraints.
- `source/` preserves the exact Warm-Ivory mark, both website botanical cutouts, the official GitHub source mark and
  the connected root-garden master. Backgrounds are generated in `#010103`; the brand mark is locked to `#F8F0E9`.

The GitHub mark comes from [GitHub's official logo resources](https://github.com/logos) and is used only to identify
the GitHub destination.

Run `python3 tools/build_profile_assets.py` from the repository root to reproduce the rendered profile assets.

The Programmable name, mark and artwork are reserved brand assets. Their presence in this public repository does not
place them under an open-source software license.
