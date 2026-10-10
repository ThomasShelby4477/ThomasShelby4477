#!/usr/bin/env python3
"""Build native GitHub Markdown with accessible, responsive SVG artwork."""
import html
import json
from pathlib import Path
from visuals import build_static

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'profile.json').read_text())
ASSETS = ROOT / 'assets'


def picture(stem, alt):
    return f'''<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/{stem}-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="assets/{stem}-light-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/{stem}-dark.svg">
  <img src="assets/{stem}-light.svg" width="100%" alt="{html.escape(alt, quote=True)}">
</picture>'''


def contacts():
    links = {c['label']: c['url'] for c in CONFIG['contacts']}
    destinations = [('linkedin', 'LinkedIn', links['LinkedIn']), ('gmail', 'Email Vaibhav', links['Email']),
                    ('github', 'GitHub repositories', f'https://github.com/{CONFIG["username"]}?tab=repositories'),
                    ('maskr', 'Maskr on the Chrome Web Store', CONFIG['projects'][0]['url'])]
    return '<p>\n' + '\n'.join(f'  <a href="{html.escape(url,quote=True)}"><img src="assets/connect-{icon}.svg" height="38" alt="{label}"></a>' for icon,label,url in destinations) + '\n</p>\n'


def build_readme():
    base = f'https://github.com/{CONFIG["username"]}'
    snapshot = json.loads((ASSETS/'stats.json').read_text())
    out = ['<!-- Generated from profile.json. Edit the source and rebuild. -->',
           picture('hero', f'{CONFIG["display_name"]} — Cybersecurity, data, and software engineering.'),
           '\n<p align="center">\n  <a href="#selected-work">Selected work</a> &nbsp; · &nbsp; <a href="#experience">Experience</a> &nbsp; · &nbsp; <a href="#toolkit">Toolkit</a> &nbsp; · &nbsp; <a href="#education">Education</a> &nbsp; · &nbsp; <a href="#github-activity">Activity</a> &nbsp; · &nbsp; <a href="#connect">Connect</a>\n</p>',
           f'\n### {CONFIG["headline"]}\n\n{CONFIG["intro"]}\n', contacts(),
           '\n'+picture('overview', f'{snapshot["contributions"]} public profile contributions in the rolling year · {snapshot["repositories"]} public owned repositories · {snapshot["stars"]} stars earned · on GitHub since {snapshot["joined"]}.'),
           '\n## Currently\n\n| Focus | What I’m working on |\n| :--- | :--- |\n'
           '| **At Delhivery** | Risk analytics, shipment anomalies, and operational insights |\n'
           '| **Building** | On-device privacy tools, structural context for AI assistants, and full-stack products |\n'
           '| **Studying** | M.Tech in Computer Science Engineering, specialising in Cyber Security |',
           '\n## Selected work\n\nFour projects across privacy, developer infrastructure, and everyday workflows.']
    for i,p in enumerate(CONFIG['projects'],1):
        url = p.get('url') or f'{base}/{p["repo"]}'
        out.append(f'\n<a href="{html.escape(url,quote=True)}">\n'+picture(f'project-{i}',p['name']+' — '+p['description'])+'\n</a>')
        links = [f'[{p.get("primary_label","Repository")} ↗]({url})']
        if p.get('extra_url'):
            links.append(f'[{p["extra_label"]} ↗]({p["extra_url"]})')
        out.append(f'\n**[{p["name"]}]({url})** — {p["description"]}\n\n'+' &nbsp; · &nbsp; '.join(links)+'\n')
    out.append('\n<details>\n<summary><strong>More projects & experiments</strong></summary>\n\n'
               f'- [Satellite Telemetry]({base}/Satellite-Malware-Detection) — Isolation Forest anomaly detection, Flask, and Streamlit monitoring.\n'
               f'- [SecureVault]({base}/securevault) — Flask file management, encryption, and audit logging.\n'
               f'- [Chess Analyser Pro]({base}/Chess_Analyser_Pro) — Computer vision for chess-piece classification and board reconstruction.\n'
               f'- [Auditorium Booking Portal]({base}/Real-time-Auditorium-Booking-Portal) — Availability checks, booking requests, and admin approval.\n'
               f'- [Phone Detection]({base}/Phone_Detection) / [Presence-controlled Lighting]({base}/Turn_on_light) — Computer vision and Arduino experiments.\n\n</details>')
    out.append('\n## Experience')
    for e in CONFIG['experience']:
        out.append(f'\n### {e["role"]} · {e["organisation"]}\n\n<sub>{e["period"]}</sub>\n\n'+'\n'.join('- '+b for b in e['highlights']))
    e = CONFIG.get('leadership')
    if e:
        out.append(f'\n**{e["role"]} · {e["organisation"]}** <sub> / {e["period"]}</sub>\n\n{e["description"]}')
    out.append('\n## Toolkit\n\n'+picture('toolkit','Python, TypeScript, JavaScript, React, Next.js, PostgreSQL, Supabase, and GitHub')+'\n\n'
               '| Area | Skills & technologies |\n| :--- | :--- |\n'
               '| **Security operations** | Elastic SIEM · EQL/KQL · Threat intelligence · Incident response · MITRE ATT&CK |\n'
               '| **Application security** | API security · Burp Suite · OWASP ZAP · Nuclei · Nmap · Cryptography |\n'
               '| **Languages** | Python · TypeScript · JavaScript · SQL |\n'
               '| **Web & APIs** | React · Next.js · Node.js · Express · Flask |\n'
               '| **Data & storage** | PostgreSQL · Supabase · SQLite · LanceDB |\n'
               '| **AI & ML** | MCP · Tree-sitter · Local embeddings · scikit-learn · PyTorch |\n'
               '| **Interfaces & tools** | Streamlit · Tailwind CSS · Git · Docker · Linux · Vercel |')
    e = CONFIG.get('education')
    if e:
        out.append(f'\n## Education\n\n**{e["institution"]}**\n\n'+picture('education','B.Tech in Computer Science Engineering completed. M.Tech in Computer Science Engineering in progress; expected August 2027. Cyber Security specialisation.')+
                   '\n\n**B.Tech completed · M.Tech in progress** — Computer Science Engineering, Cyber Security specialisation.\n\n'
                   '<sub>Working toward Certified Ethical Hacker (EC-Council).</sub>')
    out.append('\n## GitHub activity\n\n'+picture('activity',f'Public calendar: {snapshot["contributions"]} contributions, {snapshot["active_days"]} active days, longest streak {snapshot["longest_streak"]} days. Updated {snapshot["updated"]}.')+
               '\n\n<sub>Public profile snapshot. Contributions follow GitHub’s rolling year; monthly bars cover the displayed calendar, with partial first and last months. Repository metrics cover public, owned, non-fork repos. Streaks count consecutive active calendar days.</sub>\n\n'+
               f'[Contribution calendar ↗]({base}?tab=overview) &nbsp; · &nbsp; [All repositories ↗]({base}?tab=repositories)')
    out.append('\n## Connect\n\nLet’s connect about cybersecurity, privacy engineering, AI developer tools, or useful software.\n\n'+contacts()+
               f'\n[vaibhavya08@gmail.com](mailto:vaibhavya08@gmail.com) &nbsp; · &nbsp; [LinkedIn](https://www.linkedin.com/in/vaibhav082004/)\n\n---\n\n<sub>Thoughtful engineering, from data to interface.</sub>\n')
    (ROOT/'README.md').write_text('\n'.join(out))


if __name__ == '__main__':
    ASSETS.mkdir(exist_ok=True)
    build_static(CONFIG)
    build_readme()
    print('Built README, branded links, and responsive artwork.')
