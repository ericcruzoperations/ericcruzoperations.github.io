# Eric Cruz Operations

Official portfolio of Eric John Cruz | Operations, Administrative & Digital Support.

Website: https://ericcruzoperations.github.io/

This independent static website presents verified experience in operations coordination, administrative support, reporting, SEO and content support. It reuses the completed cream and deep-teal design and actual professional portrait.

## Pages and downloads

- `index.html`: homepage, capabilities, experience and contact options.
- `resume.html`: complete online resume.
- `work.html`: three evidence-based case studies in reporting, coordination and research-to-publication support.
- `downloads/Eric_John_Cruz_Virtual_Assistant_Resume.pdf`: one-page, selectable-text resume.
- `downloads/Eric_John_Cruz_Virtual_Assistant_Resume.docx`: editable, single-column Word resume.
- `samples/`: four anonymized excerpts and explicitly labeled blank templates.

Legacy download filenames are retained for compatibility. Public branding is Eric Cruz Operations. All required assets live here; canonical URLs use the root domain.

## Recovery and separation

Recovered from `Virtual_Assistant_Portfolio_Migration.zip`, prepared on 13 October 2026. The original source is PR 11 in `ericcruzdigital/ericcruzdigital.github.io`, branch `virtual-assistant-portfolio-20261013`, commit `25e757d40f8a2c0688b216d77099fc95175cc068`.

`scripts/recovery-manifest.json` records source fingerprints. The original portrait, favicon and four sample files are preserved by SHA-256. The recovered CSS retains the original design, with a requested bold, upright sans-serif page headlines. Only the dedicated site and supporting files were extracted. The marketing and electrical engineering repositories are not modified by this project or workflow.

## Build and validation

Requires Python 3.12, Node.js 22, Chromium, LibreOffice Writer, Poppler and Carlito fonts. Dependencies are declared in `requirements.txt` and `package.json`.

```sh
python -m pip install -r requirements.txt
npm install --no-audit --no-fund
npx playwright install --with-deps chromium
python scripts/build-va-resume.py
python scripts/build-va-pdf.py
python scripts/qa/render_docx.py downloads/Eric_John_Cruz_Virtual_Assistant_Resume.docx --output_dir qa-va/word --emit_pdf --dpi 120
python scripts/check-va-resume.py --word-render qa-va/word
python scripts/check-va-migration.py
node scripts/check-va-site.cjs
python scripts/package-site.py
```

On Ubuntu install `libreoffice-writer poppler-utils fonts-crosextra-carlito` before rendering Word. Inspect every rendered page after layout changes.

Shared factual content lives in `scripts/va-resume.json`. Both builders consume it. Checks compare facts across Word, rendered Word, PDF and HTML, and reject inherited title borders and page spills.

The recovered browser suite checks three pages at 1440, 768, 390 and 320 pixels, WCAG A/AA rules at desktop and mobile widths, keyboard skip navigation, navigation without JavaScript, sample links and actual PDF/Word download interactions. It also checks external destinations. LinkedIn can restrict automated requests; that limitation is reported separately.

## Deployment

GitHub Pages uses GitHub Actions on `main`. The workflow validates branches and pull requests, renders resumes, uploads review artifacts and packages only public files into `_site`. Deployment runs only on the default branch. A separate job waits for the matching public homepage and verifies actual live HTML, assets and exact download bytes.

Official GitHub-maintained Actions are pinned to immutable commits. Build permissions are read-only. Only deployment requests `pages: write` and `id-token: write`. No personal access token, private backend or form-service credential is needed.

For same-repository pull requests, a separate review job uses `contents: write` only to preserve QA images and reports on a unique `qa/operations-<run>-<attempt>` branch. It does not update the source branch or `main`. This permits visual review when artifact downloads are unavailable. QA branches are excluded from deployment triggers.

## Professional accuracy

Historical titles, dates and tools remain tied to the recovered evidence. The current headline describes transferable capabilities. Samples omit client identifiers, contact records, private figures and internal task boards. Blank templates are explicitly labeled. No testimonials, unsupported qualifications or performance gains are invented.

See `QA_STATUS.md` and the workflow's `va-qa` and `va-live-qa` artifacts for release evidence.
