# Validation results

- Input inspected: all ten supplied files readable; five valid RGBA PNGs (lion 160×180; icons 48×48); SVG is a 400×450 vector with an editable path and no embedded bitmap. Existing HTML had no SVG or data URI, but included decorative page wrappers and a single social row.
- Lossless optimization: lion 41,882 bytes; LinkedIn 939; GitHub 1,659; Scholar 1,086; Website 1,914. Decoded pixels match the supplied images exactly. Original SVG retained unchanged.
- Static checks passed: full 3,258 bytes/characters; reply 2,877 bytes/characters. Each has three balanced presentation tables, five HTTPS images, and four exact social URLs. No local paths, inline SVG, data URIs, scripts, Grid, or flexbox in either fragment.
- Playwright with Microsoft Edge passed at viewport widths 900 and 320: no horizontal overflow, all images visible, lion beside identity. Four signature screenshots inspected visually.
- Real browser clipboard write/read verified HTML and plain text, with no page controls or scripts copied. Denied clipboard access selects the reply signature and reports failure. Explicit manual full selection passed.
- Blocked-image rendering preserves identity and link labels; additional screenshot saved.
- Layout tests use intercepted image requests backed by the exact publishable PNG bytes. These tests do not establish public hosting. Postdeployment network evidence belongs in `public-validation.json`.
- Gmail authenticated paste, save/reopen, send/receive, image proxy, and dark mode tests pending manual installation. No claim of Gmail account installation.

Screenshots: `screenshots/full-900.png`, `reply-900.png`, `full-320.png`, `reply-320.png`, `full-images-blocked.png`.

## Production release

PR #1: https://github.com/jacksonpradolima/jacksonpradolima.github.io/pull/1 (merged).
Implementation commit: `c82bfb181829d5ad57c2072021a241f163f46c37`.
Production merge: `849cbfd3fa803845b8c36891ba9d8e59965242e0`.
GitHub-generated `pages build and deployment` run `44854779139`: completed successfully.

Postdeployment unauthenticated HTTPS validation passed for all five exact PNG URLs, including HTTP 200, `image/png`, PNG signature, and byte-for-byte comparison. Evidence and SHA-256 hashes: `public-validation.json`. GitHub, Google Scholar, and the website returned HTTP 200. LinkedIn returned anti-bot HTTP 999; its supplied URL is preserved and requires a manual browser check.

Installation URL: https://jacksonpradolima.github.io/executive-email-signature/INSTALL.html
