"""Mark blog posts as og:type "article" instead of "website".

Material's social plugin writes the Open Graph tags into the built HTML after
the page template renders (on_post_page, priority 50), with og:type fixed to
"website" in its card layout, so a theme override can't change it. This hook
runs after it and switches the tag on blog posts only, using the same guard as
the BlogPosting JSON-LD in overrides/main.html: pages the blog plugin gives
the blog-post.html template. Every other page stays "website".
"""

import logging

log = logging.getLogger("mkdocs.hooks.og_type_article")

WEBSITE = '<meta property="og:type" content="website" />'
ARTICLE = '<meta property="og:type" content="article" />'


def on_post_page(output, page, config, **kwargs):
    if page.meta.get("template") != "blog-post.html":
        return output
    if WEBSITE not in output:
        # Warn (which fails a strict build) if Material changes the tag's markup.
        log.warning("og:type tag not found on blog post %s", page.file.src_uri)
        return output
    return output.replace(WEBSITE, ARTICLE, 1)
