# Profile artwork

These assets are the self-hosted artwork for Programmable's public GitHub profile.

- `programmable-night-garden.gif` centers the canonical Programmable mark in the landing page's night garden while
  four painted flower heads move in a restrained, stepped loop.
- `programmable-night-garden.jpg` is the reduced-motion fallback.
- `programmable-builder-skill.jpg` balances the canonical Programmable and white GitHub marks in a second moonlit
  garden composition.
- `programmable-profile-ecosystem.jpg` closes the README with a quieter night-garden clearing.
- `programmable-github-social-preview.jpg` is the 1280×640 repository social-preview image. GitHub uses the account
  avatar—not this image—when someone shares the shorter personal-profile URL.
- `open-in-claude-code-night.png` and `copy-for-any-agent-night.png` are the two GitHub-safe action buttons beneath
  the builder artwork.
- `animation-manifest.json` records dimensions, timing and motion constraints.
- `source/` preserves the final background plates and exact canonical marks used by the deterministic asset builder.

The GitHub mark comes from [GitHub's official logo resources](https://github.com/logos) and is used only to identify
the GitHub destination. Instrument Sans is included under the SIL Open Font License in `source/fonts/`.

Run `python3 tools/build_profile_assets.py` from the repository root to reproduce the rendered profile assets.

The Programmable name, mark and artwork are reserved brand assets. Their presence in this public repository does not
place them under an open-source software license.
