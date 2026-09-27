---
description: >-
  How to manually carve files from the most common file systems you will
  encounter.
---

# File Carving

File carving refers to a process used in Digital Forensics to recover data from a file system which has typically been deleted. File carving can be automated using software or done so manually. The sign of a good Digital Forensics practitioner is the ability to do this manually or at the minimum understand how this process is carried out when using forensic programs that can do it for you.

Through learning about file carving we will learn about the most common file systems you will encounter and the different components that make them up. I will explain concepts used within the specific file systems to some detail but recommend referring to the "Useful Links" page to find more information if it isn't written about in-depth here or using Google.

The three file systems I will be writing about are FAT32, exFAT and NTFS.

* FAT32 = File Allocation Table 32 bit version
* exFAT = extensible File Allocation Table
* NTFS = New Technology File System

In the next post we will begin with FAT32 as this is a great starting point from a learning point of view as well as being less complex as say NTFS, but don't worry it isn't impossible.

## Carving

When we are carving there are some items of information we will require to successfully recover the file/data from a disk.

Importantly we will need to know what file system is being used as this will dictate how the file system stores files and how we carve the file from the specific file system.&#x20;

1. Sector and Cluster size
2. Location
3. File size
4. Contiguous or Fragmented
5. File type

### Sector and Cluster size

Disks use sectors and clusters for writing data to them.&#x20;

Sectors are the smallest writable and allocable unit on a disk. This means if you write a file that is only one byte in size, then a whole sector will be allocated to it. Sectors are almost always 512 bytes in size.

Clusters are made up of a number of sectors. For example, the size of a sector maybe 512 bytes and one cluster may be made up of two sectors making a cluster 1,024 bytes in total.

If you were to have a file with a size of 1,200 bytes then two clusters would be allocated to that file to store it, even though it won't completely fill up the second cluster. If the file expands then more clusters are used to allocate that file.

### Location

A file's location lets us know where we need to navigate to within the file system to identify the start of the file we are wanting to recover. The location will be the start of a cluster that we must navigate to in order to find the start of the file.

### File size

A files size is going to let us know from the start of the file how much data we need to be recovering.&#x20;

If we don't get the file size correct then the file will be incomplete. This could mean missing key data or recovering too much which will then create a knock effect when trying to view it once extracted as it won't be complete thus not recognized by the program we open it with.

#### Physical vs Logical file size

These are two important concepts we are required to know to successfully carve a file.

Physical size refers to how much space a file takes up on the disk. This goes back to what I mentioned in the Sector and Cluster size section. For example, if a file requires two clusters then that would be its physical size.

* **Physical size** refers to how much space a file takes up on the disk.
* **Logical size** refers to the actual size of the data a file contains.&#x20;

_**It should be noted that when we carve a file we are only recovering the logical size, not the physical size.**_

Lets tie these two concepts together based on the example from the Sector and Cluster size section.

We had a file of 1,200 bytes which is the **logical size**, but because this doesn't fit in one cluster it was allocated to two 1,024 byte clusters equaling 2,048 bytes, which is the **physical size**.&#x20;

The remaining bytes unused are what we call file slack or slack space. In this case the file slack is (1,024 + 1,024) - 1,200 = 848 bytes of unused allocated space. You can see in the picture below the different sizes.

![](<../../.gitbook/assets/File slack.webp>)

### Contiguous or Fragmented

A file that is contiguous means that the data is in sequence, where as a fragmented file has been broken up.

When a file is contiguous, the file carving process is simpler by which you can recover data from its start to end in one clean swoop.

When a file is fragmented, we are required to work out how many fragments there are and individually carve each fragment based on its size and how the file system tells us where each fragment resides.&#x20;

The picture below helps show the difference between these two terms.

![](<../../.gitbook/assets/Hard Drive Fragmentation.jpg>)

### File Type

The file type (extension) is going to tell you, as well as the operating system, what sort of program/application is able to view the file type. For example .doc or .docx are used by Microsoft Word. This is one of the last pieces of information we require and will be needed after the data/file has been recovered and the file named with the specific extension.

