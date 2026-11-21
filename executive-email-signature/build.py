"""Rebuild standalone fragments and previews using only the Python standard library."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent
HOST = 'https://jacksonpradolima.github.io/email-signature/'
LINKS = [('linkedin', 'LinkedIn', 'https://www.linkedin.com/in/pradolima/'), ('github', 'GitHub', 'https://github.com/jacksonpradolima'), ('scholar', 'Scholar', 'https://scholar.google.com/citations?user=Kx0r5jkAAAAJ&hl=en'), ('website', 'Website', 'https://jacksonpradolima.github.io/')]
TABLE = 'role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;"'

def signature(reply=False):
    size, height = (56, 63) if reply else (88, 99)
    social = ''
    for i in (0, 2):
        social += '<tr>'
        for icon, label, url in LINKS[i:i+2]:
            social += f'<td valign="middle" style="padding:3px 12px 3px 0;white-space:nowrap;"><a href="{escape(url)}" style="font:12px Arial,Helvetica,sans-serif;color:#2563EB;text-decoration:none;"><img src="{HOST}{icon}.png" width="14" height="14" alt="{label}" style="border:0;vertical-align:middle;">&nbsp;<span style="text-decoration:underline;">{label}</span></a></td>'
        social += '</tr>'
    details = '<div style="font-size:13px;line-height:19px;color:#475569;">Chief of Technology &middot; Brick Abode</div>' if reply else '<div style="font-size:15px;line-height:21px;font-weight:bold;color:#2563EB;">Chief of Technology</div><div style="font-size:11px;line-height:19px;letter-spacing:1px;font-weight:bold;color:#475569;">BRICK ABODE</div>'
    specialty = '' if reply else '<div style="font-size:12px;line-height:18px;color:#64748B;padding:6px 0;">Technology Strategy &middot; Applied &amp; Agentic AI<br>Software Engineering</div>'
    greeting = '' if reply else '<tr><td colspan="2" style="padding:0 0 14px;font-size:13px;line-height:18px;color:#475569;">Best regards,</td></tr>'
    return f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="480" style="width:100%;max-width:480px;border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;color:#0B1F53;">{greeting}<tr><td width="{size}" valign="middle" style="width:{size}px;padding:0 12px 0 0;vertical-align:middle;"><img src="{HOST}lion.png" width="{size}" height="{height}" alt="Prado Lima lion" style="display:block;border:0;"></td><td valign="middle" style="border-left:2px solid #2563EB;padding:0 0 0 12px;vertical-align:middle;"><div style="font-family:Georgia,Times New Roman,serif;font-size:{16 if reply else 19}px;line-height:{20 if reply else 24}px;font-weight:bold;">Jackson Antonio do Prado Lima, PhD</div>{details}<table {TABLE} width="56"><tr><td height="2" bgcolor="#2563EB" style="height:2px;font-size:0;line-height:2px;">&nbsp;</td></tr></table>{specialty}<table {TABLE}>{social}</table></td></tr></table>'

def page(local=False):
    sections = ''
    for label, key, reply in [('Full signature', 'full', False), ('Reply signature', 'reply', True)]:
        markup = signature(reply)
        if local:
            markup = markup.replace(HOST, 'assets/')
        controls = '<p>Local artwork preview only. Open INSTALL.html to copy the hosted version.</p>' if local else f'<p><button data-copy="{key}">Copy {label.title()}</button> <button data-select="{key}">Select {label.title()} Manually</button></p>'
        sections += f'<section><h2>{label}</h2><div class="preview"><div id="{key}" class="signature">{markup}</div></div>{controls}<p id="{key}-status" role="status" aria-live="polite"></p></section>'
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prado Lima | Gmail signature installation</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f5f9;color:#0B1F53;font:16px/1.6 Arial,Helvetica,sans-serif}main{max-width:900px;margin:auto;padding:24px 12px 64px}h1{font:700 32px Georgia,serif}h2{font-size:21px}section{background:white;border:1px solid #dbe3ef;border-radius:8px;margin:24px 0;padding:16px}.preview{background:#fff;padding:12px 0}.signature{max-width:480px}button{background:#0B1F53;color:white;border:0;border-radius:4px;padding:12px;margin:4px 4px 4px 0;font:14px Arial;cursor:pointer}button:focus-visible,a:focus-visible{outline:3px solid #2563EB;outline-offset:3px}a{color:#2563EB}li{margin:8px 0}code{overflow-wrap:anywhere}#assets li{font-size:14px} .signature div{box-sizing:content-box}</style></head><body><main><h1>Prado Lima | Executive signature</h1><p>Personal executive identity · Brick Abode</p>''' + ('<p><strong>Local preview: do not copy into Gmail.</strong></p>' if local else '<p>Copy a signature below, then paste into Gmail using Ctrl+V. If clipboard access fails, use Select Manually and press Ctrl+C (Command+C on Mac).</p>') + sections + '''<section><h2>Image hosting and links</h2><p id="hosting" role="status">Checking public images…</p><ul id="assets"></ul><p>Social destinations (click to verify; external sites may block automated requests):</p><ul>''' + ''.join(f'<li><a href="{escape(url)}" target="_blank" rel="noopener noreferrer">{label}</a></li>' for _, label, url in LINKS) + '''</ul></section><section><h2>Install in Gmail</h2><ol><li>Wait until all five hosted images pass the check above. Open Gmail → Settings → See all settings → General → Signature.</li><li>Create <strong>Prado Lima | Executive</strong>. Copy the full signature and paste it into the editor using Ctrl+V.</li><li>Create <strong>Prado Lima | Reply</strong>. Copy and paste the reply signature.</li><li>Under Signature defaults, set <strong>For new emails: Prado Lima | Executive</strong> and <strong>For replies/forwards: Prado Lima | Reply</strong>.</li><li>Click Save Changes at the bottom. Reopen settings to confirm the signatures persisted.</li><li>Compose a message and use the Insert signature (pen) menu to switch signatures for that email. Send a test to another account and inspect desktop and mobile.</li></ol><p>Live Gmail insertion, persistence, and received-message rendering require a manual test. Browser previews alone do not verify them.</p><p><a href="https://support.google.com/mail/answer/8395?hl=en">Official Gmail signature instructions</a></p></section></main>''' + ('' if local else '<script src="install.js"></script>') + '</body></html>'

if __name__ == '__main__':
    for name, text in [('FULL_GMAIL.html', signature()), ('REPLY_GMAIL.html', signature(True)), ('INSTALL.html', page()), ('PREVIEW_LOCAL.html', page(True).replace('Checking public images…', 'Local preview uses bundled assets. Open INSTALL.html to check public hosting.'))]:
        (ROOT / name).write_text(text + '\n', encoding='utf-8', newline='\n')
