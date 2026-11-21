"""HTML, artwork, external URL and browser checks. Run from any directory."""
import argparse
import hashlib
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build import HOST, LINKS, signature

class Fragment(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.images = []; self.links = []; self.tables = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        assert tag not in ['script', 'svg', 'style', 'html', 'body'], tag
        if tag in ['table', 'tr', 'td', 'div', 'span', 'a']:
            if tag == 'tr': assert self.stack[-1] == 'table'
            if tag == 'td': assert self.stack[-1] == 'tr'
            self.stack.append(tag)
        if tag == 'table':
            self.tables += 1
            assert a.get('role') == 'presentation' and a.get('cellpadding') == a.get('cellspacing') == '0'
        if tag == 'img':
            assert a['src'].startswith(HOST) and a['alt'] and int(a['width']) and int(a['height'])
            self.images.append(a['src'])
        if tag == 'a': self.links.append(a['href'])
    def handle_endtag(self, tag):
        assert self.stack.pop() == tag, tag

def static():
    result = {}
    for name, reply in [('FULL_GMAIL.html', False), ('REPLY_GMAIL.html', True)]:
        text = (ROOT/name).read_text(encoding='utf-8')
        assert text == signature(reply) + '\n', 'Run build.py to regenerate'
        for forbidden in ['file:', 'data:', '<svg', '<script', 'C:\\', 'D:\\', 'display:flex', 'display:grid', 'COLEMAN']:
            assert forbidden not in text
        assert len(text) < 8000
        p = Fragment(); p.feed(text); assert not p.stack
        assert len(p.images) == 5 and set(p.links) == {url for _, _, url in LINKS}
        for word in ['Jackson Antonio do Prado Lima, PhD', 'Chief of Technology', 'LinkedIn', 'GitHub', 'Scholar', 'Website']:
            assert word in text
        assert text.count('PhD') == 1
        if not reply:
            for word in ['BRICK ABODE', 'Technology Strategy', 'Applied &amp; Agentic AI', 'Software Engineering', 'Best regards,']: assert word in text
        result[name] = {'bytes': len(text.encode()), 'characters': len(text), 'images': len(p.images), 'tables': p.tables}
    for file in (ROOT/'assets').glob('*.png'):
        assert file.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
        assert file.read_bytes() == (ROOT.parent/'email-signature'/file.name).read_bytes()
    print(json.dumps(result, indent=2)); return result

def network():
    results = []
    for name in ['lion', 'linkedin', 'github', 'scholar', 'website']:
        url = HOST + name + '.png'
        with urlopen(Request(url, headers={'User-Agent': 'SignatureValidation/1.0'}), timeout=30) as response:
            content = response.read()
            assert response.status == 200 and response.url.startswith('https://')
            assert response.headers.get_content_type() == 'image/png'
            assert content.startswith(b'\x89PNG\r\n\x1a\n')
            assert content == (ROOT/'assets'/(name+'.png')).read_bytes()
            results.append({'url': url, 'status': response.status, 'content_type': 'image/png', 'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()})
    for _, label, url in LINKS:
        try:
            with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30) as response:
                results.append({'link': label, 'url': url, 'status': response.status, 'final_url': response.url})
        except HTTPError as error:
            results.append({'link': label, 'url': url, 'status': error.code, 'note': 'External server rejected automated client; manual link test required'})
        except URLError as error:
            results.append({'link': label, 'url': url, 'error': str(error.reason), 'note': 'Manual link test required'})
    (ROOT/'tests'/'public-validation.json').write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(results, indent=2))

def browser():
    from playwright.sync_api import sync_playwright
    import threading
    from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
    from functools import partial
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT.parent)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    shots = ROOT/'tests'/'screenshots'; shots.mkdir(exist_ok=True)
    try:
      with sync_playwright() as pw:
        b = pw.chromium.launch(channel='msedge', headless=True)
        context = b.new_context(permissions=['clipboard-read', 'clipboard-write'])
        page = context.new_page()
        # Deterministic layout checks use identical bundled bytes before deployment.
        page.route(HOST+'*', lambda route: route.fulfill(path=str(ROOT/'assets'/route.request.url.split('/')[-1]), content_type='image/png'))
        for width in [900, 320]:
          page.set_viewport_size({'width': width, 'height': 700})
          for name in ['FULL', 'REPLY']:
            page.goto(origin+'/executive-email-signature/'+name+'_GMAIL.html')
            page.wait_for_function('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Horizontal overflow'
            table = page.locator('body > table')
            assert page.locator('img').count() == 5
            lion = page.locator('img').first.bounding_box()
            text = page.get_by_text('Jackson Antonio do Prado Lima, PhD', exact=True).bounding_box()
            assert lion['x'] + lion['width'] < text['x'], 'Lion must be beside text'
            table.screenshot(path=str(shots/f'{name.lower()}-{width}.png'))
        page.goto(origin+'/executive-email-signature/INSTALL.html')
        page.get_by_role('button', name='Copy Full Signature', exact=True).click()
        page.wait_for_function("document.getElementById('full-status').textContent.includes('copied')")
        payload = page.evaluate('''async () => {const items=await navigator.clipboard.read(); const item=items[0]; return {types:item.types,html:await (await item.getType('text/html')).text(),text:await (await item.getType('text/plain')).text()};}''')
        assert 'text/html' in payload['types'] and 'text/plain' in payload['types']
        assert '<script' not in payload['html'] and 'Copy Full' not in payload['html'] and HOST in payload['html']
        assert 'Chief of Technology' in payload['text']
        page.evaluate("Object.defineProperty(navigator, 'clipboard', {value:{write:async()=>{throw new Error('denied')}},configurable:true})")
        page.get_by_role('button', name='Copy Reply Signature', exact=True).click()
        page.wait_for_function("document.getElementById('reply-status').textContent.includes('failed')")
        assert 'Chief of Technology' in page.evaluate('getSelection().toString()')
        page.get_by_role('button', name='Select Full Signature Manually', exact=True).click()
        assert 'Technology Strategy' in page.evaluate('getSelection().toString()')
        # Blocked-image fallback keeps every label and the identity readable.
        page.route(HOST+'*', lambda route: route.abort())
        page.goto(origin+'/executive-email-signature/FULL_GMAIL.html')
        assert page.get_by_text('LinkedIn', exact=True).is_visible()
        page.screenshot(path=str(shots/'full-images-blocked.png'))
        b.close()
    finally: server.shutdown()
    print('Browser: desktop/narrow layout, rich clipboard, denial fallback, manual selection and blocked images passed.')

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--public', action='store_true'); p.add_argument('--browser', action='store_true'); args = p.parse_args()
    static()
    if args.public: network()
    if args.browser: browser()
