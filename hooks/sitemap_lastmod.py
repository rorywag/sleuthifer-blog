"""Give each sitemap entry the page's last commit date instead of the build date.

MkDocs sets page.update_date to the build date, and its sitemap template writes
that as <lastmod>, so every URL carried the same date. git-revision-date-localized
works out each page's last commit time but only stores it in its own page.meta
keys. This hook copies the date part of that value into page.update_date.

It runs in on_page_markdown, not on_page_context: MkDocs renders sitemap.xml
after populating pages (when on_page_markdown runs) but before rendering them
(when on_page_context runs), so a later event would miss the sitemap. Hooks run
after plugins at the same priority, so the git plugin has already set its keys.
Pages the plugin excludes (detections/* and README.md) have no such key and keep
the build date. The raw value is "YYYY-MM-DD HH:MM:SS", the same key that
hooks/blogposting_dates.py reads.
"""


def on_page_markdown(markdown, page, config, **kwargs):
    modified = page.meta.get("git_revision_date_localized_raw_iso_datetime")
    if modified:
        page.update_date = modified.split(" ", 1)[0]
    return markdown
