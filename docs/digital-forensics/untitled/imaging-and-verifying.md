---
description: How to create a forensic image with FTK Imager
---

# Imaging & Verifying

Let's start off by defining what is imaging.

Imaging is the process of creating an identical copy of something down to the exacts same bits and bytes that the original contains.

Before we go any deeper let's clear up something which can add confusion and that is the difference between a forensic image and a clone.

Both are a bit for bit copy of the original media but a forensic image is encapsulated in a forensic file format such as E01 (we will discuss this soon) which prevents the data from being altered while a forensic clone is just a bit for bit copy made to another piece of target media the same size or larger and could be altered if there was a need to.

With that out of the way, let's introduce the main FTK Imager interface as shown below.

![FTK Imager Interface](<../../.gitbook/assets/Imager 1.PNG>)

Today I have a 32GB USB that I will image to demonstrate the process and in this case, I am creating a forensic image. The USB is connected to my computer but in a lab environment, we would use an intermediary device called a write blocker to ensure that my computer can't write data to the evidence being imaged but it can read the data on the evidence item to image it of course.

To kick off the process we need to select "Create Disk Image" which can be found under the File tab in the top right of FTK Imager or the icon; both are shown below.

![The options to "Create Disk Image"](<../../.gitbook/assets/Imager 4.PNG>)

Once "Create Disk Image" has been selected a new window will open requesting what is the source i.e what are you imaging? As we mentioned earlier it is a 32GB USB and I want to capture everything on it so a physical image is what we are looking to create. I will talk about the other types of images in another article.

This is what it look likes as shown below.

![Select your source window](<../../.gitbook/assets/Imager 5.PNG>)

Now that we selected Physical Drive we need to select which Physical Drive that is going to be, as I could image my hard drive if I wanted but that's not what we're here to do so as you can see below I will select the drive named "SanDisk Cruzer Snap USB Device \[30GB USB]" which is the USB I plugged into my computer earlier and has been assigned PHYSICALDRIVE3.

![Select your drive window](<../../.gitbook/assets/Imager 6.PNG>)

Our final steps are now to choose the destination we want to image to go to and if we want to verify the image. First let's choose a destination location and name for the image by clicking the add button shown below. Another noted is to check the "Verify images after they are created" this is important and will be discussed after this step.

![](<../../.gitbook/assets/Imager 7.PNG>)

Next, we decide what type of image we are creating and this is what differentiates an image from a clone. In this case, we are selecting the E01 image type and clicking next. The next page is for any information we want to add to our image. You can see both these steps below and what I have chosen.

![Select the image type](<../../.gitbook/assets/Imager 8.PNG>)

![Evidence Item Information](<../../.gitbook/assets/Imager 9.PNG>)

We are on the final straight here and close to creating your first forensic image. We need to decide the name of the image and where its destination is. You can see I have called mine "ForensicImageTutorial" and it will be outputted to.&#x20;

You may notice the "Image Fragment Size (MB)" and "Compression" options. The former allows you to control how the image is broken up which can help with moving large images if you need to in the future and I typically leave this at its default of 1500 MB. The latter is if you want to apply compression to save space but I personally set this to 0.

![Select Image Destination](<../../.gitbook/assets/Imager 10.PNG>)

You made it and now go click Start! 🎉

Sit back and wait for the process to finish. You can see the progress bar and in the background is the destination which is slowly filling up with 1500 MB segments of the image until complete.

![](<../../.gitbook/assets/Imager 11.PNG>)

Now to finish off let's quickly discuss that "Verify images after they are created" tick box we checked earlier. This is extremely important as it checks the integrity of the image by comparing a hash of the original media against a hash of the forensic image. If the hashes match then you have correctly created a bit by bit copy forensic image but if they mismatch then something has gone wrong which will require some troubleshooting so you can either explain the difference or complete the imaging process successfully.

To finish up, below is the computed hashes of the USB and the hashes of the forensic image matching which means we have correctly created the image. This information is also found within a text file in the destination folder of the image and will contain the information we added to the image earlier and the hashes.

![Image Verify Results.](<../../.gitbook/assets/Imager 12.PNG>)
