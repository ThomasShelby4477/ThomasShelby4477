#!/usr/bin/env python3
"""Render a local review using GitHub's Markdown API and GitHub-like CSS.

Preview files are excluded from the profile repository. This is a local visual
approximation; only publication can confirm the complete live GitHub profile.
"""
import json
from pathlib import Path
import re
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / 'preview'
PREVIEW.mkdir(exist_ok=True)
payload = json.dumps({'text': (ROOT / 'README.md').read_text(), 'mode': 'gfm'})
result = subprocess.run(['gh', 'api', 'markdown', '--input', '-'], input=payload, text=True, capture_output=True, check=True)
markup = result.stdout
(PREVIEW / 'rendered.html').write_text(markup)

# GitHub's Markdown API omits heading anchors, which the live page supplies.
def anchor(match):
    level, body = match.groups()
    plain = re.sub('<[^>]+>', '', body)
    slug = re.sub(r'[^\w\s-]', '', plain).strip().lower().replace(' ', '-')
    return f'<h{level} id="{slug}">{body}</h{level}>'

markup = re.sub(r'<h([1-6])>(.*?)</h\1>', anchor, markup)
css_url = 'https://raw.githubusercontent.com/sindresorhus/github-markdown-css/main/github-markdown.css'
if not (PREVIEW / 'github-markdown.css').exists():
    with urllib.request.urlopen(css_url, timeout=30) as response:
        (PREVIEW / 'github-markdown.css').write_bytes(response.read())

for theme in ['light', 'dark']:
    dark = theme == 'dark'
    css = (PREVIEW / 'github-markdown.css').read_text()
    css = css.replace('@media (prefers-color-scheme: dark)', '@media all' if dark else '@media not all').replace('@media (prefers-color-scheme: light)', '@media not all' if dark else '@media all')
    (PREVIEW / f'{theme}.css').write_text(css)
    content = markup.replace('media="(prefers-color-scheme: dark) and (max-width: 600px)"', f'media="{"(max-width: 600px)" if dark else "not all"}"').replace('media="(prefers-color-scheme: dark)"', f'media="{"all" if dark else "not all"}"')
    content = content.replace('href="#', f'href="/preview/{theme}.html#')
    bg, fg, border, muted = ('#0d1117', '#f0f6fc', '#3d444d', '#9198a1') if dark else ('#ffffff', '#1f2328', '#d1d9e0', '#59636e')
    doc = f'''<!doctype html><html lang="en" data-theme="{theme}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="/"><title>Vaibhav Yadav | GitHub profile preview</title><link rel="stylesheet" href="preview/{theme}.css"><style>
*{{box-sizing:border-box}}html{{color-scheme:{theme}}}body{{margin:0;background:{bg};color:{fg};font:14px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.review-bar{{border-bottom:1px solid {border};padding:16px 24px;display:flex;justify-content:space-between;align-items:center;gap:12px;color:{muted}}}.review-bar a{{color:{fg};text-decoration:none;border:1px solid {border};border-radius:6px;padding:6px 12px}}.review-bar nav{{display:flex;gap:8px}}main{{max-width:930px;margin:32px auto;border:1px solid {border};border-radius:6px;padding:32px}}.filename{{font-size:12px;margin:0 0 24px;color:{muted}}}.markdown-body{{background:transparent!important;font-size:16px;line-height:1.5}}.markdown-body img{{background:transparent}}.markdown-body picture{{display:block}}.markdown-body picture img{{display:block;width:100%;height:auto}}.markdown-body sub{{color:{muted}}}
@media(max-width:600px){{main{{margin:16px 8px;padding:16px}}.review-bar{{padding:12px;align-items:flex-start;font-size:12px}}.review-bar nav{{flex-shrink:0}}.markdown-body{{font-size:15px}}}}
</style></head><body><header class="review-bar"><span>LOCAL DRAFT · GitHub-rendered Markdown</span><nav><a href="preview/light.html">Light</a><a href="preview/dark.html">Dark</a></nav></header><main><p class="filename">ThomasShelby4477 / README.md</p><article class="markdown-body" data-theme="{theme}">{content}</article></main></body></html>'''
    (PREVIEW / f'{theme}.html').write_text(doc)
print('Built light and dark previews from GitHub-rendered Markdown.')
