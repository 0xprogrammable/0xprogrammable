# Profile artwork

These assets are the self-hosted artwork for Programmable's public GitHub profile.

- `programmable-github-profile-night-garden-v4.gif` is the current 1400×700 profile header. The approved MidJourney
  garden and exact white Programmable mark remain still across all 32 frames. Only 102 detected round point stars
  change luminance over the 6.4 second loop.
- `programmable-github-profile-night-garden-v3.png` is the 1600×800 reduced-motion fallback and source master for the
  animated cover.
- `programmable-builder-skill-v4.jpg` uses a dedicated native 5:2 MidJourney chapter illustration with the exact
  Programmable and official GitHub marks composited afterward.
- `programmable-profile-ecosystem-v4.jpg` uses a separate native 5:2 MidJourney garden for public launch data and
  integration content.
- `profile-v4-manifest.json` records source hashes, output hashes, dimensions, animation timing, MidJourney job IDs and
  moodboard identity.
- `MIDJOURNEY-V4.md` preserves the prompts and selected variation IDs.
- `programmable-github-social-preview.jpg` is the 1280×640 static Night Garden repository social-preview image. GitHub
  uses the account avatar—not this image—when someone shares the shorter personal-profile URL.
- `programmable-github-avatar-warm-ivory-4096.png` is the pure-black 4096×4096 profile master with the Warm-Ivory
  mark sized for GitHub's circular crop.
- `source/` preserves the exact brand marks and the selected native MidJourney sources.

The earlier `programmable-night-garden.*`, `programmable-builder-skill.jpg` and
`programmable-profile-ecosystem.jpg` files are retained for provenance but are no longer used in the profile README.

The GitHub mark comes from [GitHub's official logo resources](https://github.com/logos) and is used only to identify
the GitHub destination.

Run `python3 tools/build_profile_v4.py` from the repository root to reproduce the active rendered profile assets.

The Programmable name, mark and artwork are reserved brand assets. Their presence in this public repository does not
place them under an open-source software license.
