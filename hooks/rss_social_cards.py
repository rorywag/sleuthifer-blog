"""Point RSS feed images at the right social card for README.md section pages.

mkdocs-rss-plugin guesses a page's social card from its source file name, so
docs/wireshark/README.md becomes .../wireshark/README.png. Material's social
plugin names cards after the built page instead (.../wireshark/index.png), so
those feed images 404. Setting page.meta["illustration"] (read by the RSS
plugin, ignored by Material) gives it the correct URL.
"""

from pathlib import PurePosixPath


def on_page_markdown(markdown, page, config, **kwargs):
    if PurePosixPath(page.file.src_uri).name == "README.md" and "illustration" not in page.meta:
        card = PurePosixPath(page.file.dest_uri).with_suffix(".png")
        page.meta["illustration"] = f"{config.site_url}assets/images/social/{card}"
    return markdown
