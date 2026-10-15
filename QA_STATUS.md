# Release validation

Target: https://ericcruzoperations.github.io/

This release continues the recovered standalone project. The source PR remains open and unmerged; source branches and QA materials remain available.

## Recovery checks

- Primary input: the 13 October 2026 migration archive containing 30 project files.
- Original source head rechecked as `25e757d40f8a2c0688b216d77099fc95175cc068` on 15 October 2026.
- The contrast correction, explicit mobile headline spacing and inherited Word-border removal are retained.
- Original portrait, favicon and four public CSV samples remain byte-for-byte unchanged. The page headlines now use bold, upright sans-serif typography at the owner's request; the remaining recovered styling is retained.
- Public branding, metadata, contact subject and all required URLs were adapted for Eric Cruz Operations at the domain root.
- Historical roles, dates, capabilities and case-study evidence remain unchanged.

## Release gates

The workflow produces reports and rendered pages in QA artifacts. Release acceptance requires:

1. Shared resume facts in online, PDF, Word and freshly rendered Word formats; both documents remain one page.
2. A clean visual review of generated Word and PDF pages.
3. Three pages tested at desktop, tablet and mobile widths; no overflow or broken assets.
4. Zero WCAG A/AA violations in desktop and mobile scans, plus keyboard and no-JavaScript navigation checks.
5. Exact download bytes, internal anchors, sample labels and public contact destinations verified.
6. A successful Pages deployment followed by actual public-content verification.

Earlier source QA is recovery evidence, not a substitute for these release checks. Use this repository's Actions run and pull request for the current outcome.

## Scope

The case studies distinguish documented responsibilities, anonymized public excerpts and blank templates. LinkedIn can refuse automated requests; such a response is recorded rather than misrepresented as a verified page load.

Only this repository is changed. Marketing and engineering portfolios are separately maintained and excluded from all mutation and deployment steps.
