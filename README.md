<p align="center">
  <a href="https://sleuthifer.nz/"><img src="docs/assets/images/logo.png" alt="Sleuthifer mask logo" width="120"></a>
</p>

<h1 align="center">Sleuthifer</h1>

<p align="center">
  Notes on digital forensics, incident response, memory analysis and KQL detections for Microsoft Sentinel.
</p>

<p align="center">
  <a href="https://sleuthifer.nz/"><img src="https://img.shields.io/badge/site-sleuthifer.nz-3a5e88" alt="Site: sleuthifer.nz"></a>
  <a href="https://github.com/rorywag/sleuthifer-blog/actions/workflows/deploy.yml"><img src="https://github.com/rorywag/sleuthifer-blog/actions/workflows/deploy.yml/badge.svg" alt="Deploy status"></a>
  <a href="https://sleuthifer.nz/subscribe/"><img src="https://img.shields.io/badge/RSS-subscribe-b12f40" alt="Subscribe via RSS"></a>
</p>

## What's on the site

| Section | What it covers |
|---|---|
| [Blog](https://sleuthifer.nz/blog/) | Walkthroughs and notes, grouped into Digital Forensics, Incident Response and Memory Analysis. FTK Imager, Wireshark, file carving, Volatility, threat intelligence and more. |
| [Detections](https://sleuthifer.nz/detections/) | KQL detection queries from [rorywag/KQL-Detections](https://github.com/rorywag/KQL-Detections), browsable by MITRE ATT&CK tactic. |
| [Tools](https://sleuthifer.nz/tools/) | Forensics and incident response tools worth knowing. |
| [Useful Links](https://sleuthifer.nz/useful-links/) | Training, news and reading for DFIR. |
| [Projects](https://sleuthifer.nz/projects/) | Work outside the day job, including the Narcos digital forensics scenario. |
| [Subscribe](https://sleuthifer.nz/subscribe/) | An RSS feed of new blog posts. |

## How it's built

- [MkDocs](https://www.mkdocs.org/) with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), deployed to GitHub Pages by [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) on every push to `main` and nightly.
- The Detections section is generated at build time from the KQL-Detections repo by [`scripts/gen_detections.py`](scripts/gen_detections.py), so new detections appear on the next nightly build.
- Blog posts carry BlogPosting structured data, social cards and RSS entries. Fonts are self-hosted, and page views are counted with cookieless [GoatCounter](https://www.goatcounter.com/).
- Python dependencies are pinned with hashes in `requirements.txt`, and Dependabot keeps them and the GitHub Actions up to date.

## Building locally

Needs Python 3.12 and the Cairo and FreeType libraries for the social cards (on Debian or Ubuntu: `libcairo2-dev libfreetype6-dev libffi-dev libjpeg-dev libpng-dev libz-dev pngquant`).

```sh
python -m venv .venv
source .venv/bin/activate
pip install --require-hashes -r requirements.txt
mkdocs serve
```

The first build clones KQL-Detections into `.cache/kql-detections`. Set `KQL_DETECTIONS_OFFLINE=1` to reuse that clone without pulling.

## Repository layout

```text
docs/        Site content: home page, blog posts, Tools, Useful Links, Projects, Subscribe
overrides/   Theme overrides (header, 404 page, structured data)
hooks/       MkDocs hooks (feed images, Open Graph type, structured data dates, nav)
scripts/     Detections generator
```

## Credits

The mask logo is the [Twemoji](https://github.com/jdecked/twemoji) emoji U+1F479, © Twitter, Inc and other contributors, licensed under [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/).
