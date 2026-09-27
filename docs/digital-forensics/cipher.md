---
description: Gone with out a trace (a garbled one at least)
---

# Cipher (Anti-forensics)

Something I came across recently in an incident response engagement was the potential use of "Cipher.exe". Let's take a look at how it works. The testing site is on an exFAT USB but in-depth analysis regarding the exFAT process of deleting files etc will not be discussed today but more so focussed on what Cipher.exe does to the file instead.

## What is Cipher.exe

According to Microsoft:

> "_Displays or alters the encryption of directories and files on NTFS volumes. If used without parameters, cipher displays the encryption state of the current directory and any files it contains._"&#x20;

**It also has a function to be able to overwrite deleted data.**

As you may know when you delete something from your Windows system it isn't fully "deleted". Instead, it isn't accessible from the file explorer and the file essentially waves a flag to the filesystem saying "I'm not needed anymore but will hang around. Overwrite me if you need".

This is useful to Digital Forensic examiners and Incident Responders as they can in cases carve deleted data that hasn't yet been overwritten by new data.

## Testing it out

I will use FTKimager to showcase the process.&#x20;

Having created a folder with a file named "Cipher\_Test.txt" on a USB (exFAT filesystem) we can see how the folder's contents look before anything has occurred. Below we can see the file entry in question beginning at offset 0x0c0.

![Cipher\_Test.txt file before deletion](<../.gitbook/assets/Cipher folder + contents.PNG>)

The contents of the file are shown below so we can confirm it is a reasonably normal text file with some content within it.

![Contents of Cipher\_Test.txt](<../.gitbook/assets/Cipher test file.PNG>)

Now let's delete the file from the USB and see what it looks like. FTKimager makes it easy to determine it is deleted based on the icon to the left of the file name in the File Listing area with the cross through it. Further, there are identifiers in the hex that signify that the file is "not in use".

![Cipher\_Test.txt deleted](<../.gitbook/assets/Cipher test file deleted.PNG>)

Although "deleted" we can still view the contents. Take my word and I'll save some space as I would be posting the same photo you saw above earlier.

Alright, so we had a file and now it's deleted but we can still view it using FTKimager or other forensic tools. Let's point Cipher.exe at the location and start the overwriting process.

The command I will use is below. It's very simple in that it executes the Cipher.exe utility with the argument "/w:" telling it to overwrite deleted data and in this case points it F:\Cipher folder I made to contain the text file on my USB. The next step is to sit back and wait as it does its stuff.

```bat
cipher.exe/w:f:\Cipher
```

The first step for Cipher.exe is to write zeros over the deleted (0x00), it then moves to write 255's (0xFF) over the deleted files and finally random letters. Essentially a three-pass wipe of anything that has been deleted rendering it unreadable and of no use.

![Cipher.exe command line output](<../.gitbook/assets/Cipher cmdline.PNG>)

Once completed I checked back on the file that was originally on the USB, deleted and then Cipher.exe used. As you can see below the deleted file has been completely changed to something that doesn't resemble what it once does.

![Deleted file after Cipher.exe use](<../.gitbook/assets/Cipher file output.PNG>)

## Conclusion

Cipher.exe is a tool that can be utilised by actors as part of the "[_**Defense Evasion**_](https://attack.mitre.org/tactics/TA0005/)" tactic. It can also be a handy tool if you wanted to wipe a disk and confirm no deleted files are available to be carved as a result of the Cipher.exe process.

There appear to be no artifacts produced by the execution of this program by default on Windows systems but you can enable "Command line process auditing". I would suggest enabling "PowerShell Script Block Loggin&#x67;**",** as well as both of these, are commonly used by actors which is an identified behaviour called "[_**living off the land**_](https://logrhythm.com/blog/what-are-living-off-the-land-attacks/)".

> Harlan's Corollary to the First Law of Computer Forensics "Once you understand what actions or conditions create or modify an artifact, then the absence of that artifact is itself an artifact."

## Notes

When running Cipher.exe but only pointing at the drive letter instead of the specific folder that held the file contents, it didn't appear to overwrite the deleted file space.

The process can take a long time to complete depending on the amount of deleted data it is required to overwrite.

## _References_

<https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/cipher>

<https://docs.microsoft.com/en-us/troubleshoot/windows-server/windows-security/use-cipher-to-overwrite-deleted-data>

<https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/manage/component-updates/command-line-process-auditing>
