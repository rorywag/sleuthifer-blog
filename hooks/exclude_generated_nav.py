"""Keep generated literate-nav files (NAV.md) out of the built site and the feeds.

mkdocs-gen-files adds its files after MkDocs has applied exclude_docs, so
exclude_docs can't reach detections/NAV.md. Hooks run after plugins, so by now
the file exists and can be excluded. literate-nav still reads excluded files.
"""

from mkdocs.structure.files import InclusionLevel


def on_files(files, config, **kwargs):
    for file in files:
        if file.src_uri.endswith("NAV.md"):
            file.inclusion = InclusionLevel.EXCLUDED
    return files
