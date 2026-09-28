"""Point RSS feed images at the social card Material actually builds for a page.

mkdocs-rss-plugin guesses a page's social card from its source path, so
docs/blog/posts/wireshark.md becomes .../blog/posts/wireshark.png. Material's
social plugin names cards after the built page instead (.../blog/wireshark.png
for a post), so those feed images 404. Setting page.meta["illustration"] (read
by the RSS plugin, ignored by Material) gives it the correct URL.
"""


def on_page_markdown(markdown, page, config, **kwargs):
    if "illustration" not in page.meta:
        # Same rule as Material's social plugin: blog/wireshark/index.html becomes
        # blog/wireshark.png, and an index page's index.html becomes index.png.
        suffix = "/index.html" if config.use_directory_urls and not page.is_index else ".html"
        card = page.file.dest_uri.replace(suffix, ".png")
        page.meta["illustration"] = f"{config.site_url}assets/images/social/{card}"
    return markdown
