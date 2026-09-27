---
description: Where to find the PowerShell history file.
---

# PowerShell History

## What is PowerShell?

I'm guessing you already know what it is if you are here but I like to keep these articles as informational as possible for everyone interested to read them.&#x20;

Quickly let's cover off what PowerShell is then. It is a command-line shell provided by Microsoft within the Windows operating system (OS). It is typically used for querying information within the OS, scripting and automating tasks.

## Why is this useful?

In nearly if not all Incident Response engagements I work on, PowerShell is used by adversaries to conduct a whole raft of tactics and techniques to achieve their objectives. From a Digital Forensics perspective, this is gold as it can provide insight into what tactics, techniques and procedures they used. Furthermore, possibly what tools they employed to do so.

## Where is it located?

The name of the file is "ConsoleHost\_history.txt and can be found in the location below.

```powershell
$env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

It is specific to each user profile. For example, if I were wanting to find my specific PowerShell history I would search for the below location and file.

```text
C:\Users\sleuthifer\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

## Timestamps

The ConsoleHost\_history from my understanding is created when a user first interacts with PowerShell and runs commands that can be stored in the history file, although this will need testing to confirm.

The contents of the file do not timestamp specific commands being run so the next best thing to go off is the $standard\_information modified timestamp, which is the timestamp you would see when using file explorer in Windows as shown below.

![ConsoleHost\_history file with created and modified timestamps](<../.gitbook/assets/image (3).png>)

The modified timestamp will tell us at what time the last command in the ConsoleHost\_history.txt file was executed.

## Conclusion

Identifying commands run by adversaries during or after an attack is invaluable to investigating actions taken on a system.

The timestamp tells us when the last command was run and based on other artifacts identified during the forensic investigation will build a picture of the timing of other commands executed in the file.

A downfall of this file is like many others it can be deleted or actions may not be captured because a different method has been utilised. I believe that there are several logs that businesses and organisations don't recognise as being important to capture and this is an instance of just one.

It is possible to enable a logging feature named "Script Block Logging" which captures script/commands that are processed/executed in PowerShell and can be viewed in the Windows event log, preferably these logs would be aggregated along with other logging information somewhere else to avoid them being deleted easily. \
Check out details regarding this feature on the Microsoft Documentation website [_**here**_](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows?view=powershell-7.1#enabling-script-block-logging) or the FireEye website [_**here**_](https://www.fireeye.com/blog/threat-research/2016/02/greater_visibilityt.html).

