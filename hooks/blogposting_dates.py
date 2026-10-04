"""Full ISO 8601 dates, with a timezone, for the BlogPosting JSON-LD.

Google's Rich Results Test wants datePublished and dateModified as datetimes
with a timezone offset. The JSON-LD in overrides/main.html reads the two
values this hook sets on each blog post's page.meta:

- jsonld_date_published: the post's front-matter date at midnight in
  Pacific/Auckland, e.g. 2021-05-25T00:00:00+12:00. zoneinfo picks the
  offset for that date, so NZ daylight saving (+13:00) is applied when it
  was in effect.
- jsonld_date_modified: the last commit time from git-revision-date-localized,
  in Pacific/Auckland. The plugin's raw iso_datetime is in its own configured
  timezone (UTC by default) without an offset, so it's read in that timezone
  first.
"""

from datetime import datetime, time
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Pacific/Auckland")


def on_page_context(context, page, config, **kwargs):
    if page.meta.get("template") != "blog-post.html":
        return context

    created = getattr(getattr(page, "config", None), "date", None)
    if created is not None:
        day = created.created.date()
        page.meta["jsonld_date_published"] = datetime.combine(day, time(), TZ).isoformat()

    modified = page.meta.get("git_revision_date_localized_raw_iso_datetime")
    if modified:
        plugin = config.plugins.get("git-revision-date-localized")
        source_tz = ZoneInfo((plugin.config.get("timezone") if plugin else None) or "UTC")
        stamp = datetime.strptime(modified, "%Y-%m-%d %H:%M:%S").replace(tzinfo=source_tz)
        page.meta["jsonld_date_modified"] = stamp.astimezone(TZ).isoformat()

    return context
