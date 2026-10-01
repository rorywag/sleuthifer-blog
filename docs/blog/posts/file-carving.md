---
date: 2020-10-19
categories:
  - Digital Forensics
slug: file-carving
description: >-
  File carving concepts (sectors, clusters, file size and fragmentation), then
  manually carving a deleted file from a FAT32 file system with FTK Imager.
---

# File Carving

File carving refers to a process used in Digital Forensics to recover data from a file system which has typically been deleted. File carving can be automated using software or done so manually. The sign of a good Digital Forensics practitioner is the ability to do this manually or at the minimum understand how this process is carried out when using forensic programs that can do it for you.

<!-- more -->

Through learning about file carving we will learn about the most common file systems you will encounter and the different components that make them up. I will explain concepts used within the specific file systems to some detail but recommend referring to the "Useful Links" page to find more information if it isn't written about in-depth here or using Google.

The three file systems I will be writing about are FAT32, exFAT and NTFS.

* FAT32 = File Allocation Table 32 bit version
* exFAT = extensible File Allocation Table
* NTFS = New Technology File System

In the next section we will begin with FAT32 as this is a great starting point from a learning point of view as well as being less complex as say NTFS, but don't worry it isn't impossible.

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

## FAT32 File Carving

Let's begin the process of manually carving a deleted file from a FAT32 filesystem but as always find resources outside of this article to help you further your understanding and remember Google is your friend.

It is recommended having a read of the File Carving section found [**here** ](#carving)to have a baseline understanding of concepts.

### Sector and Cluster Size

#### The VBR (Volume Boot Record)

The VBR (Volume Boot Record) is found in logical sector 0 of the partition/volume. The VBR contains information about the volume/partition. We are interested in the two pieces of information: Bytes per Sector, and Sectors per Cluster.

The table below shows us the location of these two values.&#x20;

| Offset (Hex) | Size (Bytes) | Description         |
| ------------ | ------------ | ------------------- |
| 0x0B         | 2            | Bytes per Sector    |
| 0x0D         | 1            | Sectors per Cluster |

I have highlighted the two values we are looking at in the picture below.

![The VBR of FAT32 filesystem on a USB](<../../.gitbook/assets/FTKimager 0 edited (1).png>)

The Bytes per Sector shows the value 0x0002 which read as little-endian (the bytes are read right to left) is 0x200 and this in decimal is 512 bytes in each sector.

The Sectors per Cluster shows the value 0x02 which as it is only one byte can be read as it appears, and in decimal is 2. We now know that 2 sectors make up a cluster and our sectors are 512 bytes in size meaning a cluster is 512 x 2 which in turn is 1,024 bytes in size.&#x20;

### Root Directory

We can see on the left-hand side the evidence tree and in particular partition 1 with sub-folder ‘root’ which is open, this is the root directory where our files reside on the filesystem. The file list shows us what files are within the root folder.

Notice there is a file named ‘Secret Deal.docx’ with an icon showing a cross; this is how FTKimager shows a deleted file is present, but we can’t open it as a result of it being deleted.

![Root directory of FAT32 filesystem on the USB](<../../.gitbook/assets/FTKimager 1 (1).PNG>)

### Short and Long Filename

If we turn our attention to the hexadecimal in the bottom pane, we can see how the root directory is set out in 16-byte rows. You can see in the pictures below the short and long file name of the deleted ‘Secret Deal.docx” file.&#x20;

The long filename is the first 64 bytes in this case but can vary in the number of bytes used taking up more than 1 directory entry, followed by the short filename which is always 32 bytes in length. Other than the icon in the File List view, we know that this file has been deleted because of the status byte 0xE5 at the start of each 32 bytes.

![Long & Short Filename Directory Entry](<../../.gitbook/assets/FTKimager 2.PNG>)

The Long Filename Directory Entry is for storing filenames longer than 8 bytes.

![Long Filename Directory Entry](<../../.gitbook/assets/FTKimager 3.PNG>)

The Short Filename Directory Entry is where we find our other important file information such as Location and File Size etc.

![Short Filename Directory Entry](<../../.gitbook/assets/FTKimager 4.PNG>)

We are mainly interested in the short file name as this is where the filesystem stores the information we require to carve and successfully recover the file. The short file name only stores the first 8 ASCII characters and 3 extension characters; therefore, the long filename is used to store filenames with characters over that limit.

The table below shows how a short filename directory entry is made up.

| Offset (Hex) | Size (Bytes) | Description                                                    |
| ------------ | ------------ | -------------------------------------------------------------- |
| 0x00         | 8            | Filename (the first byte is the status byte)                   |
| 0x08         | 3            | File Extension                                                 |
| 0x0B         | 1            | File Attribute Byte                                            |
| 0x0C         | 1            | Lower Case Flags                                               |
| 0x0D         | 1            | File Creation Time in Milliseconds                             |
| 0x0E         | 2            | File Creation Time                                             |
| 0x10         | 2            | File Creation Date                                             |
| 0x12         | 2            | Last Accessed Date                                             |
| 0x14         | 2            | High Word Starting Cluster (if zero only the Low Word is used) |
| 0x16         | 2            | Time of Last Write to File                                     |
| 0x18         | 2            | Date of Last Write to File                                     |
| 0x1A         | 2            | Low Word Starting Cluster                                      |
| 0x1C         | 4            | File Size                                                      |

### Location

The high word is 0x0000 meaning we only need the low word value at offset 0x1A to find the starting cluster. The value at offset 0x1A is 0x4300 and this read as little-endian is 0x43 which when converted to decimal is telling us the file starts at cluster 67.

### File Size

The value at offset 0x1C = 44 62 01 00. This is read as little-endian which is 0x16244 and using the programmer calculator within Windows (which has a hex to dec function) is 90,692 byte&#x73;**,** which is the logical size. Refer to the File Carving Intro [**here** ](#physical-vs-logical-file-size)for what the difference between logical and physical size.

We can now divide the file size by cluster size to identify the number of clusters the file uses 90,692/1,024 = 88.57 clusters which we round up to 89 clusters.

![](<../../.gitbook/assets/FTKimager 5 (1).png>)

![Hex to Dec file size value](<../../.gitbook/assets/FTKimager 6.PNG>)

### FAT

The FAT (File Allocation Table) tells us what clusters are in use within the FAT32 filesystem and in the picture below we can see the FAT. The FAT works by showing if a cluster is allocated to a file and how to identify the next cluster it allocates. A FAT32 entry is 4 bytes in length.

For example, the first cluster allocated in the filesystem is cluster 5 at offset 0x14 and it is showing us the next cluster used is cluster 6. This goes on until you reach the hexadecimal value of 0xFFFFFF0F signifying the file ends in this cluster which can be seen at offset 0x108 which is cluster 42 in hexadecimal and cluster 66 in decimal.

![The FAT (File Allocation Table)](<../../.gitbook/assets/FTKimager 7.PNG>)

Earlier we identified cluster 67 as our starting cluster which is 0x43 in hexadecimal.

#### Contiguous or fragmented?

We will need to check if the file we are going to carve is contiguous (in sequence) or fragmented meaning we need to locate clusters in different locations.

In the sections File Size and Location, we determined that our file's physical size was 89 clusters and that the starting cluster was 67. I have highlighted cluster 67 within the FAT and the other clusters that make up the file, and as a result, we can say that the file is contiguous.

You may wonder why aren't the highlighted clusters pointing to the next cluster as the example from the initial FAT intro had done so? This is because when a file is deleted the cluster chain is deleted as we can see below.&#x20;

![Deleted file entry in FAT](<../../.gitbook/assets/FTKimager 8.PNG>)

### Carving the data & Recovering the file

We have essentially done the heavy lifting now and can finish off with the data carving.&#x20;

Let's use the "Go to sector/cluster" tool by right-clicking in the hexadecimal of the SLEUTH USB \[FAT32] section as shown below. This allows us to navigate to the cluster in question being 67.

![Go to sector/cluster tool in FTKimager](<../../.gitbook/assets/FTKimager 9.PNG>)

![Selecting cluster 67 to navigate to](<../../.gitbook/assets/FTKimager 10.PNG>)

Now at cluster 67 which starts at the offset 0x10400, we can use another tool within FTKimager by right-clicking the hexadecimal and selecting "Set Selection Length" as shown below and in this case, we know our logical file size is 90,692 bytes so we will use that.

![Selecting 90,692 bytes from start of the file starting cluster](<../../.gitbook/assets/FTKimager 11.PNG>)

Once the selection from the starting cluster and the correct size is highlighted then we can right-click once more and use "Save selection..." which allows us to save the raw data as a file and provide an extension so the appropriate program can open it.&#x20;

### File Signature

In some cases, we can use the extension found in the Short Filename Directory Entry but someone could have given the file in question a different extension for one reason or another. It is best to identify the file signature, also known as a file header, to ensure the correct extension for use with the file.

![File Signature identified at start of files starting cluster](<../../.gitbook/assets/FTKimager 12.PNG>)

In this case, I can see 'PK' is visible which already provides me with the clue that it is a compound file and with some comparison work using [Gary Kesslers File Signatures](https://www.garykessler.net/library/file_sigs.html) website, determined it to be a Microsoft Office file.

### Conclusion

We have successfully carved data from a FAT32 filesystem and below we can view the recovered file using Microsoft Word.

I hope you take something away from this article and if you want to follow along to carve the data and recover the file yourself you can download a zip of the image I used at my Github page by clicking [**here**](https://github.com/rorywag/File-Carving).

![The recovered deleted file](<../../.gitbook/assets/FTKimager 13.PNG>)
