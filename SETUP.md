# Profile package

This directory contains the published profile for [`ThomasShelby4477`](https://github.com/ThomasShelby4477), hosted by the public [`ThomasShelby4477/ThomasShelby4477`](https://github.com/ThomasShelby4477/ThomasShelby4477) repository. Publication was authorised and completed on 10 October 2026.

## Edit and rebuild

The header includes a self-contained typing animation in its SVG assets. The name types once and the tagline cycles slowly; reduced-motion preferences select static text. All animation timing is generated in `scripts/visuals.py`.

`profile.json` contains the name, introduction, public contact links, projects, experience, leadership, and education. Edit it, then run:

```sh
python3 scripts/update_stats.py
python3 scripts/build_profile.py
```

`show_experience` is currently `false`, so the entire Experience section and its navigation item are omitted from the generated README.

`intro_headline` controls the centred professional introduction. `show_past_work` is `true`; roles marked `past_role` and the leadership record appear in a compact disclosure below Current focus.

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

Preview image URLs include content fingerprints so rebuilds display current artwork rather than cached SVGs.

## Publication

The reviewed profile is published. GitHub displays it because the public repository matches the username and contains a nonempty root `README.md`.

The intended published files are `README.md`, `profile.json`, `assets/`, `scripts/`, `.github/workflows/profile.yml`, `.gitignore`, `SETUP.md`, and `research/PROFILE_AUDIT.md`. The résumé itself and local preview screenshots are not part of the profile repository.

The first hosted **Refresh profile** workflow completed successfully and committed updated public statistics. It is scheduled daily at 07:53 IST (02:23 UTC). The last committed cards remain available if a later refresh fails. Repository settings or branch protection may require an adjustment before the bot can push its updates.

Update sidebar name, bio, social links, and pins using the reviewed suggestions in `research/PROFILE_AUDIT.md`. They are separate GitHub profile settings; adding a README does not change them.

## Contact privacy

The public profile uses email, LinkedIn, GitHub, and the Maskr store listing. Do not add Vaibhav's personal mobile number or upload the résumé PDF. This restriction was explicitly requested on 10 October 2026.
