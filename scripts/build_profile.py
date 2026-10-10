#!/usr/bin/env python3
"""Build GitHub-native Markdown and theme-aware artwork. Python standard library only."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "profile.json").read_text())
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

THEMES = {
    "dark": {"bg": "#101b22", "fg": "#edf5f2", "muted": "#a8bfba", "line": "#2c454b", "accent": "#94ddc2", "warm": "#edb99a", "panel": "#182a30"},
    "light": {"bg": "#f2f5ef", "fg": "#183532", "muted": "#536c65", "line": "#c5d6ce", "accent": "#256a56", "warm": "#9b5e3d", "panel": "#e4ece4"},
}


def svg(width, height, content, title, desc, theme):
    c = THEMES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>
<rect width="{width}" height="{height}" rx="16" fill="{c['bg']}"/>
<g font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Arial, sans-serif">{content}</g></svg>'''


def text(x, y, value, size, color, weight=400, extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{html.escape(str(value))}</text>'


def build_hero(theme, mobile):
    c = THEMES[theme]
    w, h = (420, 350) if mobile else (960, 340)
    x = 28 if mobile else 44
    name = CONFIG["display_name"]
    name_size = min(20 if mobile else 23, (w - 2 * x) / max(len(name), 1) / 0.58)
    content = text(x, 48 if mobile else 51, name, name_size, c["accent"], 600)
    content += text(x, 86 if mobile else 94, "CYBERSECURITY / DATA / SOFTWARE", 11 if mobile else 12, c["muted"], extra='letter-spacing="1.6"')
    content += text(x, 149 if mobile else 165, "Secure systems.", 39 if mobile else 57, c["fg"], 650, 'letter-spacing="-1.9"')
    content += text(x, 200 if mobile else 231, "Useful software.", 39 if mobile else 57, c["fg"], 650, 'letter-spacing="-1.5"')
    content += f'<path d="M{x} {233 if mobile else 269}h{42 if mobile else 52}" stroke="{c["accent"]}" stroke-width="3"/>'
    if mobile:
        content += text(x, 274, "Threat detection. Privacy. Applied AI.", 16, c["muted"])
        content += text(x, 301, "Thoughtful engineering, from data to interface.", 14, c["muted"])
    else:
        content += text(x + 70, 276, "Threat detection. Privacy tools. Full-stack products.", 16, c["muted"])
        content += text(866, 307, "01 / BUILD", 10, c["muted"], extra='text-anchor="end" letter-spacing="1"')
        # A small architectural sketch gives the profile its own visual identity.
        content += f'<g fill="none" stroke="{c["line"]}" stroke-width="1.2"><circle cx="797" cy="154" r="92"/><circle cx="797" cy="154" r="61"/><path d="M705 154h184M797 62v184M731 89l132 132M731 221L863 89"/></g>'
        content += f'<path d="M797 93L858 154L797 215L736 154Z" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="1.5"/>'
        content += f'<path d="M777 143l-12 11 12 11m40-22l12 11-12 11m-14-19l-12 38" fill="none" stroke="{c["accent"]}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
        for cx, cy, color in [(797, 62, c["warm"]), (889, 154, c["accent"]), (797, 246, c["warm"]), (705, 154, c["accent"])]:
            content += f'<circle cx="{cx}" cy="{cy}" r="5" fill="{color}"/>'
    desc = f"{name}. Secure systems. Useful software. Cybersecurity, data, and software engineering."
    (ASSETS / f'hero-{theme}{"-mobile" if mobile else ""}.svg').write_text(svg(w, h, content, name, desc, theme))


def picture(stem, alt):
    return f'''<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/{stem}-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="assets/{stem}-light-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/{stem}-dark.svg">
  <img src="assets/{stem}-light.svg" width="100%" alt="{html.escape(alt, quote=True)}">
</picture>'''


def build_readme():
    user = CONFIG["username"]
    base = f"https://github.com/{user}"
    contact_links = [f'[{c["label"]}]({c["url"]})' for c in CONFIG["contacts"]]
    out = ["<!-- Generated from profile.json by scripts/build_profile.py. -->", picture("hero", f'{CONFIG["display_name"]} — Secure systems. Useful software.'),
           '\n<p align="center">\n  <a href="#selected-work">Selected work</a> &nbsp; · &nbsp; <a href="#experience">Experience</a> &nbsp; · &nbsp; <a href="#toolkit">Toolkit</a> &nbsp; · &nbsp; <a href="#github-activity">Activity</a> &nbsp; · &nbsp; <a href="#connect">Connect</a>\n</p>',
           f'\n### {CONFIG["headline"]}\n\n{CONFIG["intro"]}']
    if contact_links:
        out.append("\n" + " &nbsp; / &nbsp; ".join(contact_links))
    out.append('\n## Selected work\n\nPrivacy tools, developer infrastructure, and products built around real workflows.')
    for i, p in enumerate(CONFIG["projects"], 1):
        url = p.get('url') or f'{base}/{p["repo"]}'
        links = [f'[{p.get("primary_label", "Repository")} ↗]({url})']
        if p.get("extra_url"):
            links.append(f'[{p["extra_label"]} ↗]({p["extra_url"]})')
        out.append(f'\n<sub>{i:02d} / {p["category"]}</sub>\n\n### [{p["name"]}]({url})\n\n{p["description"]}\n\n{p["detail"]}\n\n<sub><strong>{p["stack"]}</strong></sub>\n\n' + " &nbsp; · &nbsp; ".join(links))
    out.append('\n<details>\n<summary><strong>More projects & experiments</strong></summary>\n\n'
               f'- [Satellite Telemetry]({base}/Satellite-Malware-Detection) — Anomaly detection with Isolation Forest, Flask, and Streamlit monitoring dashboards.\n'
               f'- [SecureVault]({base}/securevault) — A Flask file-management project with encryption and audit logging.\n'
               f'- [Chess Analyser Pro]({base}/Chess_Analyser_Pro) — A computer-vision project exploring chess-piece classification and board reconstruction.\n'
               f'- [Auditorium Booking Portal]({base}/Real-time-Auditorium-Booking-Portal) — Booking requests, availability checks, and admin approval workflows.\n'
               f'- [Phone Detection]({base}/Phone_Detection) / [Presence-controlled Lighting]({base}/Turn_on_light) — Early computer-vision and Arduino experiments.\n\n</details>')
    out.append('\n## Experience')
    if CONFIG["experience"]:
        for e in CONFIG["experience"]:
            out.append(f'\n### {e["role"]} · {e["organisation"]}\n\n<sub>{e["period"]}</sub>\n\n' + '\n'.join('- ' + b for b in e["highlights"]))
    else:
        out.append('\nMy project work spans three areas:\n\n'
                   f'- **Developer tooling:** AST parsing, semantic indexing, dependency graphs, and MCP integrations in [Codebase Architect]({base}/CodeBase-Architect).\n'
                   f'- **Product engineering:** Authentication, database-backed workflows, real-time interfaces, and maps in [CampusNest]({base}/campusnest) and [KreedaScore]({base}/sports-week-score-app).\n'
                   f'- **Applied machine learning:** Feature processing, anomaly detection, and monitoring dashboards in [Satellite Telemetry]({base}/Satellite-Malware-Detection).')
    if CONFIG.get('leadership'):
        e = CONFIG['leadership']
        out.append(f'\n**{e["role"]} · {e["organisation"]}** <sub> / {e["period"]}</sub>\n\n{e["description"]}')
    out.append('\n## Toolkit\n\n'
               '| Area | Skills & technologies |\n| :--- | :--- |\n'
               '| **Security operations** | Elastic SIEM · EQL/KQL · Threat intelligence · Incident response · MITRE ATT&CK |\n'
               '| **Application security** | API security · Burp Suite · OWASP ZAP · Nuclei · Nmap · Cryptography |\n'
               '| **Languages** | Python · TypeScript · JavaScript · SQL |\n'
               '| **Web & APIs** | React · Next.js · Node.js · Express · Flask |\n'
               '| **Data & storage** | PostgreSQL · Supabase · SQLite · LanceDB |\n'
               '| **AI & ML** | MCP · Tree-sitter · Local embeddings · scikit-learn · PyTorch |\n'
               '| **Interfaces & tools** | Streamlit · Tailwind CSS · Git · Docker · Linux · Vercel |')
    if CONFIG.get('education'):
        e = CONFIG['education']
        out.append(f'\n## Education\n\n**{e["institution"]}**\n\n{e["qualification"]} · Specialisation in {e["specialisation"]}\n\n<sub>{e["period"]} · CGPA: {e["cgpa"]}</sub>\n\n<sub>Currently working toward Certified Ethical Hacker (EC-Council).</sub>')
    snapshot = json.loads((ASSETS / 'stats.json').read_text())
    langs = ', '.join(f'{k} {v:.1f}%' for k, v in snapshot['language_percentages'].items())
    star_label = 'star' if snapshot['stars'] == 1 else 'stars'
    out.append('\n## GitHub activity\n\n' + picture('activity', f'Public GitHub snapshot: {snapshot["contributions"]} profile contributions in the last year, {snapshot["repositories"]} repositories, {snapshot["stars"]} {star_label}. Repository language bytes: {langs}. Updated {snapshot["updated"]}.') +
               '\n\n<sub>Contributions follow the public profile’s rolling year. Repository stats cover public, owned, non-fork repos. Language shares measure code bytes, not proficiency.</sub>\n\n' +
               f'[Contribution calendar ↗]({base}?tab=overview) &nbsp; · &nbsp; [All repositories ↗]({base}?tab=repositories)')
    out.append('\n## Connect\n\nLet’s connect about cybersecurity, privacy engineering, AI developer tools, or useful software.\n\n')
    if contact_links:
        out.append(" &nbsp; / &nbsp; ".join(contact_links))
    else:
        out.append(f'[Ask about Codebase Architect ↗]({base}/CodeBase-Architect/issues/new) &nbsp; · &nbsp; [Explore my work ↗]({base}?tab=repositories)')
    out.append('\n\n---\n\n<sub>Good tools make complex work feel clear.</sub>\n')
    (ROOT / 'README.md').write_text('\n'.join(out))


if __name__ == '__main__':
    for theme in THEMES:
        for mobile in [False, True]:
            build_hero(theme, mobile)
    build_readme()
    print('Built README and four responsive header assets.')
