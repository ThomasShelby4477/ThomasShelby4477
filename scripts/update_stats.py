#!/usr/bin/env python3
"""Generate local SVG statistics from public GitHub sources.

Private repositories are filtered out. No third-party stats service or PAT
is needed. An optional GitHub Actions token raises the API rate limit.
All fetches finish before replacing assets. Errors fail the run instead of
publishing zeros or partial results.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import re
import urllib.request

from build_profile import THEMES, svg, text

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'


def fetch(url):
    api = url.startswith('https://api.github.com/')
    headers = {'User-Agent': 'github-profile-public-snapshot', 'Accept': 'application/vnd.github+json' if api else 'text/html'}
    token = os.environ.get('GH_TOKEN')
    if api and token:
        headers['Authorization'] = 'Bearer ' + token
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode()


def collect(username):
    user = json.loads(fetch(f'https://api.github.com/users/{username}'))
    repos = []
    page = 1
    while True:
        batch = json.loads(fetch(f'https://api.github.com/users/{username}/repos?type=owner&per_page=100&page={page}'))
        repos.extend(r for r in batch if not r['private'] and not r['fork'] and r['owner']['login'].casefold() == username.casefold())
        if len(batch) < 100:
            break
        page += 1
    languages = Counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        for values in pool.map(lambda r: json.loads(fetch(r['languages_url'])), repos):
            languages.update(values)
    language_total = sum(languages.values())
    percentages = {name: 100 * size / language_total for name, size in languages.most_common(4)} if language_total else {}
    if len(languages) > 4:
        percentages['Other'] = 100 - sum(percentages.values())
    # Fetch exactly what logged-out profile visitors can already see.
    markup = fetch(f'https://github.com/users/{username}/contributions')
    plain = re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', markup)))
    match = re.search(r'([\d,]+) contributions? in the last year', plain)
    if not match:
        raise ValueError('Public contribution count unavailable; preserving previous cards.')
    return {
        'username': username,
        'updated': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'repositories': len(repos),
        'stars': sum(r['stargazers_count'] for r in repos),
        'joined': user['created_at'][:4],
        'contributions': int(match.group(1).replace(',', '')),
        'contribution_scope': 'Rolling year, as displayed on the logged-out GitHub profile',
        'repository_scope': 'Public, owned, non-fork repositories',
        'language_percentages': percentages,
        'language_bytes': dict(languages.most_common()),
        'sources': [f'https://api.github.com/users/{username}', f'https://api.github.com/users/{username}/repos', f'https://github.com/users/{username}/contributions'],
    }


def card(data, theme, mobile):
    c = THEMES[theme]
    w, h = (420, 474) if mobile else (960, 304)
    x = 28 if mobile else 44
    out = text(x, 42, 'GITHUB / ACTIVITY & CODE', 12, c['accent'], 600, 'letter-spacing="1.4"')
    metrics = [(data['contributions'], 'Contributions', 'Last 12 months'), (data['repositories'], 'Repositories', 'Public · owned'), (data['stars'], 'Stars earned', 'Public repositories')]
    for i, (value, label, detail) in enumerate(metrics):
        mx = x + i * (125 if mobile else 161)
        out += text(mx, 107 if mobile else 140, f'{value:,}', 39 if mobile else 49, c['fg'], 600, 'letter-spacing="-1"')
        out += text(mx, 133 if mobile else 173, label, 12 if mobile else 14, c['fg'], 600)
        out += text(mx, 153 if mobile else 197, detail, 10 if mobile else 11, c['muted'])
    if mobile:
        out += f'<path d="M28 183h364" stroke="{c["line"]}"/>'
        lx, ly, barw = 28, 220, 250
    else:
        out += f'<path d="M543 75v157" stroke="{c["line"]}"/>'
        lx, ly, barw = 581, 88, 216
    out += text(lx, ly, 'REPOSITORY LANGUAGES', 11, c['muted'], 600, 'letter-spacing="1"')
    colors = [c['accent'], c['warm'], '#64a2b4', '#b8a2cb', c['muted']]
    for i, (language, percentage) in enumerate(data['language_percentages'].items()):
        y = ly + 28 + i * 30
        out += text(lx, y, language, 12, c['fg'])
        bx = lx + 98
        bw = barw - 98
        out += f'<rect x="{bx}" y="{y-8}" width="{bw}" height="6" rx="3" fill="{c["line"]}"/>'
        out += f'<rect x="{bx}" y="{y-8}" width="{bw*percentage/100:.2f}" height="6" rx="3" fill="{colors[i]}"/>'
        out += text(lx + barw + 12, y, f'{percentage:.1f}%', 11, c['muted'])
    out += text(x, h - 43, f'On GitHub since {data["joined"]}', 11, c['muted'])
    out += text(x, h - 23, f'Public snapshot · updated {data["updated"]} UTC', 10 if mobile else 11, c['muted'])
    desc = f'{data["contributions"]} contributions displayed on the public GitHub profile in the last year, {data["repositories"]} public owned repositories, and {data["stars"]} stars. Repository languages are measured by code bytes.'
    return svg(w, h, out, 'GitHub activity and repository languages', desc, theme)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from-snapshot', action='store_true', help='Render existing data without network access')
    args = parser.parse_args()
    username = json.loads((ROOT / 'profile.json').read_text())['username']
    data = json.loads((ASSETS / 'stats.json').read_text()) if args.from_snapshot else collect(username)
    outputs = {f'activity-{theme}{"-mobile" if mobile else ""}.svg': card(data, theme, mobile) for theme in THEMES for mobile in [False, True]}
    outputs['stats.json'] = json.dumps(data, indent=2) + '\n'
    ASSETS.mkdir(exist_ok=True)
    for filename, value in outputs.items():
        tmp = ASSETS / (filename + '.tmp')
        tmp.write_text(value)
        tmp.replace(ASSETS / filename)
    print(f'Updated public snapshot: {data["repositories"]} repositories, {data["contributions"]} profile contributions.')


if __name__ == '__main__':
    main()
