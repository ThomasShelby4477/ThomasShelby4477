#!/usr/bin/env python3
"""Build native GitHub Markdown with accessible, responsive SVG artwork."""
import html
import json
from pathlib import Path
from visuals import build_static, project_actions

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'profile.json').read_text())
ASSETS = ROOT / 'assets'


def picture(stem, alt, url=None):
    artwork=f'''<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/{stem}-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="assets/{stem}-light-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/{stem}-dark.svg">
  <img src="assets/{stem}-light.svg" width="100%" alt="{html.escape(alt, quote=True)}">
</picture>'''
    if url:
        artwork=f'<a href="{html.escape(url,quote=True)}">\n{artwork}\n</a>'
    # Native paragraphs give image blocks the same spacing as text on GitHub.
    return f'<p>\n{artwork}\n</p>\n'


def link_badges(items, centered=False):
    align=' align="center"' if centered else ''
    # Ordinary whitespace drops at a line break; nonbreaking spaces indent
    # wrapped rows and misalign mobile actions with the rest of the content.
    return f'<p{align}>\n'+'\n'.join(f'  <a href="{html.escape(url,quote=True)}"><img src="assets/{asset}.svg" height="52" alt="{html.escape(label,quote=True)}"></a>' for asset,label,url in items)+'\n</p>\n'


def navigation():
    sections=[('work','Selected work','selected-work'),('experience','Experience','experience'),('toolkit','Toolkit','toolkit'),('education','Education','education'),('activity','GitHub activity','github-activity'),('connect','Connect','connect')]
    if not CONFIG.get('show_experience', True):
        sections=[section for section in sections if section[0]!='experience']
    return link_badges([(f'nav-{key}',label,f'#{anchor}') for key,label,anchor in sections],True)


def contacts():
    links = {c['label']: c['url'] for c in CONFIG['contacts']}
    destinations = [('linkedin', 'LinkedIn', links['LinkedIn']), ('gmail', 'Email Vaibhav', links['Email']),
                    ('github', 'GitHub repositories', f'https://github.com/{CONFIG["username"]}?tab=repositories'),
                    ('maskr', 'Maskr on the Chrome Web Store', CONFIG['projects'][0]['url'])]
    return link_badges([(f'connect-{icon}',label,url) for icon,label,url in destinations],True)


def introduction():
    parts=CONFIG['intro_headline'].split(' | ')
    headline=' | '.join(html.escape(part) for part in parts[:2])
    if len(parts)>2:
        headline+='\n<br>\n'+' | '.join(html.escape(part) for part in parts[2:])
    first,separator,rest=CONFIG['intro'].partition('. ')
    copy=html.escape(first+'.' if separator else first)
    if separator:
        copy+='\n<br>\n'+html.escape(rest)
    return f'\n<hr>\n\n<h3 align="center">{headline}</h3>\n\n<p align="center">\n{copy}\n</p>\n\n<hr>\n'


def past_work():
    if not CONFIG.get('show_past_work'):
        return ''
    out=['\n<details>\n<summary><strong>Past work & technical leadership</strong></summary>\n']
    for role in CONFIG['experience']:
        if role.get('past_role'):
            out.append(f'\n**{role["role"]} · {role["organisation"]}**\n\n<sub>{role["period"]}</sub>\n\n'+'\n'.join('- '+highlight for highlight in role['highlights']))
    role=CONFIG.get('leadership')
    if role:
        out.append(f'\n**{role["role"]} · {role["organisation"]}**\n\n<sub>{role["period"]}</sub>\n\n{role["description"]}')
    return '\n'.join(out)+'\n\n</details>\n'


def build_readme():
    base = f'https://github.com/{CONFIG["username"]}'
    snapshot = json.loads((ASSETS/'stats.json').read_text())
    out = ['<!-- Generated from profile.json. Edit the source and rebuild. -->',
           picture('hero', f'{CONFIG["display_name"]}: Cybersecurity, data, and software engineering.'),
           navigation(),
           introduction(), contacts(),
           '\n'+picture('overview', f'{snapshot["contributions"]} public profile contributions in the rolling year · {snapshot["repositories"]} public owned repositories · {snapshot["stars"]} stars earned · on GitHub since {snapshot["joined"]}.'),
           '\n## Current focus\n\n| Focus | What I’m working on |\n| :--- | :--- |\n'
           '| **Role** | Data Analyst Intern at Delhivery · Risk analytics and operational insights |\n'
           '| **Specialisation** | Cybersecurity, on-device privacy, and software engineering |\n'
           '| **Building** | On-device privacy tools, structural context for AI assistants, and full-stack products |\n'
           '| **Studying** | M.Tech in Computer Science Engineering, specialising in Cyber Security |',
           past_work(),
           '\n## Selected work\n\nFour projects across privacy, developer infrastructure, and everyday workflows.']
    for i,p in enumerate(CONFIG['projects'],1):
        actions=project_actions(p,CONFIG['username'])
        url=actions[0][2]
        out.append('\n'+picture(f'project-{i}',p['name']+': '+p['description'],url))
        links=[(f'project-{i}-{"primary" if j==0 else "secondary"}',alt,destination) for j,(_,alt,destination,_) in enumerate(actions)]
        out.append(f'\n**{p["name"]}**: {p["description"]}\n\n'+link_badges(links))
        if i<len(CONFIG['projects']):
            out.append('\n<br>\n')
    out.append('\n<details>\n<summary><strong>More projects & experiments</strong></summary>\n\n'
               f'- [Satellite Telemetry]({base}/Satellite-Malware-Detection): Isolation Forest anomaly detection, Flask, and Streamlit monitoring.\n'
               f'- [SecureVault]({base}/securevault): Flask file management, encryption, and audit logging.\n'
               f'- [Chess Analyser Pro]({base}/Chess_Analyser_Pro): Computer vision for chess-piece classification and board reconstruction.\n'
               f'- [Auditorium Booking Portal]({base}/Real-time-Auditorium-Booking-Portal): Availability checks, booking requests, and admin approval.\n'
               f'- [Phone Detection]({base}/Phone_Detection) / [Presence-controlled Lighting]({base}/Turn_on_light): Computer vision and Arduino experiments.\n\n</details>')
    if CONFIG.get('show_experience', True):
        out.append('\n## Experience')
        for e in CONFIG['experience']:
            out.append(f'\n### {e["role"]} · {e["organisation"]}\n\n<sub>{e["period"]}</sub>\n\n'+'\n'.join('- '+b for b in e['highlights']))
        e = CONFIG.get('leadership')
        if e:
            out.append(f'\n**{e["role"]} · {e["organisation"]}** <sub> / {e["period"]}</sub>\n\n{e["description"]}')
    out.append('\n## Toolkit\n\n'+picture('toolkit','Detection and response: Elastic SIEM, EQL/KQL, threat intelligence, incident response. Application security: Burp Suite, OWASP ZAP, Nuclei, Nmap. Programming: Python, TypeScript, JavaScript, SQL. Web and APIs: React, Next.js, Express, Flask. Data and AI: PostgreSQL, Supabase, Tree-sitter, MCP. Tools and interfaces: GitHub, Docker, Linux, Streamlit.')+'\n\n<details>\n<summary><strong>Complete skills & technologies</strong></summary>\n\n'
               '| Area | Skills & technologies |\n| :--- | :--- |\n'
               '| **Security operations** | Elastic SIEM · EQL/KQL · Threat intelligence · Incident response · MITRE ATT&CK |\n'
               '| **Application security** | API security · Burp Suite · OWASP ZAP · Nuclei · Nmap · Cryptography |\n'
               '| **Languages** | Python · TypeScript · JavaScript · SQL |\n'
               '| **Web & APIs** | React · Next.js · Node.js · Express · Flask |\n'
               '| **Data & storage** | PostgreSQL · Supabase · SQLite · LanceDB |\n'
               '| **AI & ML** | MCP · Tree-sitter · Local embeddings · scikit-learn · PyTorch |\n'
               '| **Interfaces & tools** | Streamlit · Tailwind CSS · Git · Docker · Linux · Vercel |\n\n</details>')
    e = CONFIG.get('education')
    if e:
        out.append(f'\n## Education\n\n**{e["institution"]}**\n\n'+picture('education','B.Tech in Computer Science Engineering completed. M.Tech in Computer Science Engineering in progress; expected August 2027. Cyber Security specialisation.')+
                   '\n\n**B.Tech completed · M.Tech in progress**: Computer Science Engineering, Cyber Security specialisation.\n\n'
                   '<sub>Working toward Certified Ethical Hacker (EC-Council).</sub>')
    out.append('\n## GitHub activity\n\n'+picture('activity',f'Public calendar: {snapshot["contributions"]} contributions, {snapshot["active_days"]} active days, longest streak {snapshot["longest_streak"]} days. Updated {snapshot["updated"]}.')+
               '\n\n<sub>Public profile snapshot. Contributions follow GitHub’s rolling year; monthly bars cover the displayed calendar, with partial first and last months. Repository metrics cover public, owned, non-fork repos. Streaks count consecutive active calendar days.</sub>\n\n'+
               link_badges([('activity-calendar','View GitHub contribution calendar',f'{base}?tab=overview'),('activity-repositories','Browse all GitHub repositories',f'{base}?tab=repositories')]))
    out.append('\n## Connect\n\nLet’s connect about cybersecurity, privacy engineering, AI developer tools, or useful software.\n\n'+contacts()+
               f'\n[vaibhavya08@gmail.com](mailto:vaibhavya08@gmail.com) &nbsp; · &nbsp; [LinkedIn](https://www.linkedin.com/in/vaibhav082004/)\n\n---\n\n<sub>Thoughtful engineering, from data to interface.</sub>\n')
    (ROOT/'README.md').write_text('\n'.join(out))


if __name__ == '__main__':
    ASSETS.mkdir(exist_ok=True)
    build_static(CONFIG)
    build_readme()
    print('Built README, branded links, and responsive artwork.')
