# Prado Lima executive email signature

## Files

- `FULL_GMAIL.html` and `REPLY_GMAIL.html`: standalone Gmail-safe fragments, without preview chrome or scripts.
- `INSTALL.html` and `install.js`: hosted previews, rich clipboard copying, manual selection, public image checks, and installation instructions.
- `PREVIEW_LOCAL.html`: offline artwork preview using `assets/`. Do not copy this version into Gmail.
- `assets/`: optimized PNGs and the original, unchanged `lion-editable.svg` for editing.
- `build.py`: deterministic generator for both fragments and preview pages; edit this file before rebuilding.
- `tests/validate.py`: HTML, asset, public URL, browser layout, clipboard and fallback checks.
- `tests/screenshots/`: full and reply at 900px and 320px, plus blocked-image fallback.
- `tests/public-validation.json`: latest external image/link check, generated after publication.
- `../email-signature/`: identical PNG copies at the required public paths.

## Hosting and deployment

GitHub Pages API inspection confirmed legacy Jekyll publication from `master:/`, HTTPS enforced, no custom domain, no custom Actions workflows. `_config.yml` sets the expected origin and an empty `baseurl`. These new static directories are copied by Jekyll; the HTML files have no front matter and bypass theme layouts. Existing site files and configuration are unchanged.

Public image URLs:

- https://jacksonpradolima.github.io/email-signature/lion.png
- https://jacksonpradolima.github.io/email-signature/linkedin.png
- https://jacksonpradolima.github.io/email-signature/github.png
- https://jacksonpradolima.github.io/email-signature/scholar.png
- https://jacksonpradolima.github.io/email-signature/website.png

Installation page: https://jacksonpradolima.github.io/executive-email-signature/INSTALL.html

Published through merged PR #1. The Pages deployment succeeded and all five image URLs passed unauthenticated HTTPS validation (HTTP 200, `image/png`, exact PNG bytes). See `tests/RESULTS.md` and `tests/public-validation.json`. Future changes require merging into `master` and a successful Pages build; a pushed feature branch alone does not publish them.

## Gmail installation

1. Open the installation page. Confirm that all five public images load.
2. Click **Copy Full Signature**. It writes only the signature as `text/html` plus readable `text/plain`. If copying is denied or unsupported, the signature is selected automatically: press Ctrl+C, then Ctrl+V in Gmail. You can always use **Select Full Signature Manually**. On Mac use Command instead of Ctrl. Do not paste as plain text.
3. In **Gmail → Settings → See all settings → General → Signature**, create **Prado Lima | Executive**, then paste the full signature.
4. Click **Copy Reply Signature** (or its manual selection button). Create **Prado Lima | Reply** in Gmail and paste it.
5. Set these exact Signature defaults:
   - **For new emails: Prado Lima | Executive**
   - **For replies/forwards: Prado Lima | Reply**
6. Click **Save Changes** at the bottom. Reopen settings and confirm the images and formatting persisted.
7. In an individual compose window, use **Insert signature** (pen icon) to choose another signature. Keep rich formatting enabled.
8. Send a test message to another account; check the received full and reply signatures on desktop and mobile, including images blocked, links, and dark mode.

See [Google's official instructions](https://support.google.com/mail/answer/8395?hl=en). Google documents a 10,000-character signature limit; the fragments are approximately 3.3KB and 2.9KB before Gmail serialization. Gmail may rewrite pasted markup, so persistence and final size must still be checked in Gmail.

## Compatibility and updating

Critical alignment uses presentation tables with inline styles, explicit image dimensions, vertical alignment, and a fixed lion cell. The overall table is fluid up to 480px. Two rows of labeled social links avoid a long icon strip. The lion is the supplied 160×180 PNG displayed smaller; the social icons are supplied 48×48 PNGs displayed at 14px. Lossless PNG compression preserves pixels. Name, affiliation, specialization and link labels remain text when images are blocked.

PNG files over public HTTPS avoid clipboard dependencies on inline SVG, Base64 or local paths. The editable SVG stays separate from the email markup. This is an email-compatible implementation; browser tests do not establish live Gmail compatibility.

To change artwork, edit the preserved SVG in a vector editor and export a transparent PNG with the same aspect ratio. Replace the PNG in both `assets/` and `../email-signature/`; keep dimensions at least as large as their display dimensions. Update `build.py` if dimensions or links change, then rebuild. Retain the public paths because existing emails reference them. Gmail image proxy caching can delay updates; use a versioned filename and update the generator if immediate cache invalidation is necessary.

From the repository root on Windows:

```powershell
rtk proxy python executive-email-signature/build.py
rtk proxy python executive-email-signature/tests/validate.py
rtk proxy uv run --isolated --with playwright python executive-email-signature/tests/validate.py --browser
rtk proxy python executive-email-signature/tests/validate.py --public
```

Browser checks use installed Microsoft Edge through Playwright. They intercept image requests with identical bundled bytes for repeatable predeployment layout tests, and exercise actual HTML/plain-text clipboard writing, rejected clipboard access, and manual selection. The separate public check downloads all five unauthenticated HTTPS images, verifies MIME type, PNG magic bytes, and exact content, then checks social destinations. External LinkedIn/Scholar anti-bot responses are recorded as manual verification required, not described as broken links or successful checks.

## Verification limits

Authenticated Gmail paste, save/reopen persistence, sent-message rendering, Gmail image proxy behavior, and dark mode remain manual checks. No Gmail settings have been changed by this implementation. No local Ruby/Jekyll runtime is installed; the production Pages build and postdeployment homepage check provide deployment verification.
