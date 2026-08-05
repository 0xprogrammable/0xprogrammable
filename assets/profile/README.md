# Profile artwork

These assets are the self-hosted artwork for Programmable's public GitHub profile.

- `programmable-night-garden.gif` centers the canonical Programmable mark in the landing page's night garden while
  four painted flower heads move in a restrained, stepped loop.
- `programmable-night-garden.jpg` is the reduced-motion fallback.
- `animation-manifest.json` records dimensions, timing and motion constraints.
- `source/` preserves the exact landing artwork and canonical mark used by the deterministic asset builder.

Run `python3 tools/build_profile_assets.py` from the repository root to reproduce the rendered profile assets.

The Programmable name, mark and artwork are reserved brand assets. Their presence in this public repository does not
place them under an open-source software license.
