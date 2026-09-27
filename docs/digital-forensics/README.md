---
description: Overview of the digital forensics notes on anti-forensics, PowerShell history, file carving, FTK Imager and Wireshark.
---

# Digital Forensics

Notes on recovering and examining evidence from Windows hosts, disks and network captures. They cover how Cipher.exe wipes deleted data, where PowerShell keeps its command history, carving a deleted file out of a FAT32 volume by hand, imaging and verifying a drive with FTK Imager, and reading a packet capture in Wireshark.

<div class="grid" markdown>

<div class="card" markdown>

[:material-eraser:{ .lg .middle } __Cipher (Anti-forensics)__](cipher.md)

---

How Cipher.exe /w overwrites deleted data, and what that leaves for an examiner.

</div>

<div class="card" markdown>

[:material-powershell:{ .lg .middle } __PowerShell History__](powershell-history.md)

---

Where the per-user ConsoleHost_history.txt file lives and why it matters.

</div>

<div class="card" markdown>

[:material-file-search:{ .lg .middle } __File Carving__](file-carving/README.md)

---

File system concepts for carving, then a manual FAT32 walkthrough.

</div>

<div class="card" markdown>

[:material-harddisk-plus:{ .lg .middle } __FTK Imager__](untitled/README.md)

---

An overview of FTK Imager, then creating and verifying a forensic image.

</div>

<div class="card" markdown>

[:material-lan:{ .lg .middle } __Wireshark__](wireshark/README.md)

---

Protocol hierarchy, DHCP, following TCP streams and decoding an SMTP login.

</div>

</div>
