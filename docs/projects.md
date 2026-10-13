---
description: >-
  Projects by Rory Wagner: the Narcos digital forensics scenario published on
  Digital Corpora, and Hayabusa Bulk Runner for triaging KAPE collections.
# Single-page tab: the left sidebar would only repeat this page's title.
hide:
  - navigation
---

# Projects

Work I've built outside the day job.

## Narcos, a digital forensics scenario

A drug-trafficking investigation scenario I built with my WelTec team, the DFIR
Sleuths. It's published on Digital Corpora as the
[2019 Narcos scenario](https://digitalcorpora.org/corpora/scenarios/2019-narcos/),
and the project site is [DFIR Sleuths](https://dfirsleuths.github.io/).

## Hayabusa Bulk Runner

A PowerShell wrapper that runs [Hayabusa](https://github.com/Yamato-Security/hayabusa)
across a folder of KAPE collections, one run per host. It extracts the ZIPs and
mounts the disk images, then gives each host its own HTML alert report, CSV
timeline and log, plus a dashboard showing which hosts are worst and which rules
fired where. It's in pre-release, and the code is on GitHub at
[rorywag/Hayabusa-Bulk-Runner](https://github.com/rorywag/Hayabusa-Bulk-Runner).
