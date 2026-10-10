#!/usr/bin/env python3
"""Generate local SVG statistics from public GitHub sources.

Private repositories are filtered out. No third-party stats service or PAT
is needed. An optional GitHub Actions token raises the API rate limit.
All fetches finish before replacing assets. Errors fail the run instead of
publishing zeros or partial results.
"""
import argparse
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
import html
import json
import os
from pathlib import Path
import re
import urllib.request

from visuals import THEMES, activity, overview

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



class ContributionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}
        self.tooltip = None
        self.tooltip_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'td' and attrs.get('data-date'):
            self.days[attrs['id']] = {'date': attrs['data-date'], 'level': int(attrs['data-level'])}
        if tag == 'tool-tip' and attrs.get('for') in self.days:
            self.tooltip = attrs['for']
            self.tooltip_text = []

    def handle_data(self, data):
        if self.tooltip:
            self.tooltip_text.append(data)

    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.tooltip:
            value = re.search(r'(No|[\d,]+) contributions?', ''.join(self.tooltip_text))
            if value:
                self.days[self.tooltip]['count'] = 0 if value[1] == 'No' else int(value[1].replace(',', ''))
            self.tooltip = None


def calendar_metrics(markup, expected_total):
    parser = ContributionParser()
    parser.feed(markup)
    days = sorted(parser.days.values(), key=lambda d: d['date'])
    if not days or any('count' not in d or d['level'] not in range(5) for d in days):
        raise ValueError('Incomplete public contribution calendar; preserving previous assets.')
    dates = [date.fromisoformat(d['date']) for d in days]
    if dates[0].weekday() != 6 or any(b-a != timedelta(days=1) for a,b in zip(dates,dates[1:])):
        raise ValueError('Contribution dates are not a complete calendar.')
    if sum(d['count'] for d in days) != expected_total:
        raise ValueError('Calendar disagrees with public headline count; preserving previous assets.')
    months = Counter()
    streak = longest = active = 0
    for d in days:
        months[d['date'][:7]] += d['count']
        streak = streak + 1 if d['count'] else 0
        longest = max(longest, streak)
        active += bool(d['count'])
    return {'calendar': days, 'monthly_contributions': dict(sorted(months.items())),
            'active_days': active, 'longest_streak': longest, 'current_streak': streak,
            'most_active_day': max(days, key=lambda d: d['count'])}


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
        'followers': user['followers'],
        'forks': sum(r['forks_count'] for r in repos),
        **calendar_metrics(markup, int(match.group(1).replace(',', ''))),
        'joined': user['created_at'][:4],
        'contributions': int(match.group(1).replace(',', '')),
        'contribution_scope': 'Rolling year, as displayed on the logged-out GitHub profile',
        'repository_scope': 'Public, owned, non-fork repositories',
        'sources': [f'https://api.github.com/users/{username}', f'https://api.github.com/users/{username}/repos', f'https://github.com/users/{username}/contributions'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from-snapshot', action='store_true', help='Render existing data without network access')
    args = parser.parse_args()
    username = json.loads((ROOT / 'profile.json').read_text())['username']
    data = json.loads((ASSETS / 'stats.json').read_text()) if args.from_snapshot else collect(username)
    outputs = {f'{stem}-{theme}{"-mobile" if mobile else ""}.svg': renderer(data, theme, mobile)
               for stem, renderer in [('activity', activity), ('overview', overview)]
               for theme in THEMES for mobile in [False, True]}
    outputs['stats.json'] = json.dumps(data, indent=2) + '\n'
    ASSETS.mkdir(exist_ok=True)
    for filename, value in outputs.items():
        tmp = ASSETS / (filename + '.tmp')
        tmp.write_text(value)
        tmp.replace(ASSETS / filename)
    print(f'Updated public snapshot: {data["repositories"]} repositories, {data["contributions"]} profile contributions.')


if __name__ == '__main__':
    main()
