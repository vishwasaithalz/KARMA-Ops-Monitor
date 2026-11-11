#!/usr/bin/env python3
"""Offline, read-only smoke checks for the public KARMA-Ops-Monitor site."""
import json
from html.parser import HTMLParser
from pathlib import Path

ALLOWED_REPOS = {
    'LogSentry', 'recon-lite', 'AI-Automation-Lab', 'CyberPlayground',
    'YYYH', 'flagship-api', 'nextjs-boilerplate', 'vishwasaithalz',
}
ALLOWED_STATES = {'passed', 'failed', 'running', 'not_verified', 'unavailable'}


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = False
        self.viewport = False
        self.description = False
        self.title = False
        self.in_title = False
        self.title_value = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = bool(attrs.get('lang'))
        elif tag == 'title':
            self.in_title = True
            self.title = True
        elif tag == 'meta':
            name = attrs.get('name', '').lower()
            if name == 'viewport' and attrs.get('content'):
                self.viewport = True
            if name == 'description' and attrs.get('content'):
                self.description = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_value += data


def check(root: Path) -> None:
    page = (root / 'index.html').read_text(encoding='utf-8')
    assert page.lstrip().lower().startswith('<!doctype html'), 'doctype missing'
    doc = Document()
    doc.feed(page)
    assert doc.lang and doc.viewport and doc.description, 'HTML metadata incomplete'
    assert doc.title and doc.title_value.strip(), 'document title empty'

    data = json.loads((root / 'public-status.json').read_text(encoding='utf-8'))
    projects = data.get('projects')
    assert isinstance(projects, list) and len(projects) == len(ALLOWED_REPOS), 'unexpected project count'
    repos = [item.get('repository') for item in projects]
    assert len(repos) == len(set(repos)), 'duplicate repo'
    assert set(repos) == ALLOWED_REPOS, 'non-public/unapproved repo detected'
    for item in projects:
        assert item.get('state') in ALLOWED_STATES, 'unknown status'
        url = item.get('run_url')
        if url:
            assert url.startswith('https://github.com/vishwasaithalz/'), 'unexpected Actions URL'
            assert '/actions/runs/' in url, 'not a workflow-run link'
    print('PASS: public HTML metadata and eight allowlisted GitHub CI signals')


if __name__ == '__main__':
    check(Path(__file__).resolve().parents[1])
