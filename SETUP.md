# Profile package

This directory contains the profile draft for `ThomasShelby4477`. No remote profile repository existed at review time. The draft has not been published.

## Edit and rebuild

The header includes a self-contained typing animation in its SVG assets. The name types once and the tagline cycles slowly; reduced-motion preferences select static text. All animation timing is generated in `scripts/visuals.py`.

`profile.json` contains the name, introduction, public contact links, projects, experience, leadership, and education. Edit it, then run:

```sh
python3 scripts/update_stats.py
python3 scripts/build_profile.py
```

`show_experience` is currently `false`, so the entire Experience section and its navigation item are omitted from the generated README.

For an offline rebuild from the last successful public snapshot:

```sh
python3 scripts/update_stats.py --from-snapshot
python3 scripts/build_profile.py
```

The API accepts an optional `GH_TOKEN` to raise its rate limit. The hosted workflow uses its own ephemeral GitHub token. Private repos are explicitly excluded, and the public contribution HTML is fetched without authentication.

## Preview

With GitHub CLI authenticated:

```sh
python3 scripts/build_preview.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/preview/dark.html` or the light variant. Preview files and source research downloads are ignored by Git. The preview uses GitHub's Markdown renderer; its surrounding page is a local approximation.

## Publication

Publish only after reviewing the draft. GitHub requires a **public repository named `ThomasShelby4477`** owned by `ThomasShelby4477`, with a nonempty root `README.md`, to show this content on the profile.

The intended published files are `README.md`, `profile.json`, `assets/`, `scripts/`, `.github/workflows/profile.yml`, `.gitignore`, `SETUP.md`, and `research/PROFILE_AUDIT.md`. The résumé itself and local preview screenshots are not part of the profile repository.

After publication, run the **Refresh profile** workflow manually once and verify its output. It is also scheduled daily at 02:23 UTC. The last committed cards remain available if a later refresh fails. Repository settings or branch protection may require an adjustment before the bot can push its updates.

Update sidebar name, bio, social links, and pins using the reviewed suggestions in `research/PROFILE_AUDIT.md`. They are separate GitHub profile settings; adding a README does not change them.
