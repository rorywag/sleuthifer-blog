---
description: >-
  A quick and frank article on what should happen if you are unfortunate to be
  involved in a cyber security incident.
---

# You've been hit, popped or breached?

It's only a matter of time before you are involved with a cybersecurity incident. That's not fear-mongering, that's the truth. Businesses and organisations that respect this will be at the forefront of planning to prevent it, but even the most prepared are fallible and adversaries are evolving on a day-to-day basis.

> &#x20;**Just As Water Retains No Constant Shape, In Warfare There Are No Constant Conditions - Sun Tzu**

This isn't meant to be an in-depth guide to incident response but a guide of what to expect nonetheless.

## Prepare

At this point hopefully, there's some process in place with how to deal with a cyber incident. Whether that be communicating with an IT Service provider, IT Security provider or someone that can assist the business to get the ball rolling.

If there doesn't happen to be anything in place, there's time to start and best to do so as soon as possible.&#x20;

I won't be going into depth regarding this phase as the purpose of this post is what to do once you have an active incident on your hands.

## Identify

Anyone open to the public-facing internet is a target for adversaries but this doesn't necessarily mean you're vulnerable at the time. Scans of the internet are happening with every word typed and that is just how it is. There are events, alerts, and incidents. Daniel Miessler has a brief but informative article [_**here**_](https://danielmiessler.com/study/event-alert-incident/), which I recommend reading to understand the difference.

A good example of an incident is a ransomware attack, so we will use that as we go forward. What is Ransomware?&#x20;

> Ransomware - a type of malicious software designed to block access to a computer system and/or files until a sum of money is paid

Once an incident has been identified, it is highly recommended that an IT Security provider with Digital Forensics and Incident Response expertise is employed. They will know how to guide you through the process, provide calm to the situation and use their expertise to start actioning items to be done and see you out of the incident.

## Contain

I would step on the side of caution regardless of if it's a ransomware incident, a phishing incident, or anything in between.&#x20;

The first step is to contain, contain and contain. Adversaries using Ransomware will be looking to encrypt as many devices in the network as possible and we need to **stop that bleeding** quickly. This means "network containing" the hosts you know have a ransomware infection on by severing the connections to those hosts and further into your network to kick the threat actors out.

A full domain password reset and the implementation of multi-factor authentication (MFA) for services that can use it, is recommended if not already in place.

Another key step is the preservation of systems involved in the incident and it can't be stressed enough as it is key to the next step. This involves the person or business (IT Security provider) with specialisation in Digital Forensics and Incident Response to ensure systems are preserved correctly and quickly. It should be noted that any sort of logging information external to the preserved systems is also preserved.  This can include firewall logging, security appliances, VPNs etc.

## Investigate

This is where digital forensic artifacts containing evidence are pulled out to start forming the story of where it went wrong, what occurred during the incident, and what recommendations can be made after the investigation.

The systems, logs, and data that were preserved earlier are ready to be processed and analysed by a specialist Digital Forensics and Incident Response team part of the IT Security provider engaged in the detection step. This stage can take a while, it is labour-intensive and can be expensive depending on the complexity and spread of the incident.  However, it is well worth it. It allows for positioning yourself to be stronger in the future, reducing the risk caused by the exfiltration of data, and understanding what, how, and why the incident occurred.

An in-depth report should be provided regarding the details of the tactics, techniques and procedures the adversary used to gain access to your environment, actions taken while inside the network, and what they took or damaged.

## Eradication

This step should be done in parallel with the investigation once preservation is secured. The incident has occurred but time is money and we need to get back to business as usual as quickly as possible.

The IT Service provider or Tech Support are going to be key here. This will probably involve tearing down infected infrastructure and clean systems being built to replace it.&#x20;

In some cases, if there are backups, they are going to help to get you up and running in a shorter timeframe than without them.

Note this for lessons learned and future preparations if there aren't backups.

An interesting article regarding not doing the Eradication step can be found [_**here**_](https://www.zdnet.com/article/ransomware-this-is-the-first-thing-you-should-think-about-if-you-fall-victim-to-an-attack/)_._

## Recovery

As touched on in the Eradication section you will want to have the support of both the IT Service provider and the IT Security provider in assisting with getting your environment back to operational status.

The IT Service provider can remove and rebuild the infected systems in your network while the IT Security provider will supply recommendations most likely outlined in the report from the Investigation step.

Such advice may be as follows:

* Systems patched to a safe version.
* Monitoring of the environment for early detection and guard against reinfection with an Endpoint Detection and Response (EDR) solution.
* Implementing the [_**principle of least privilege**_](https://www.cert.govt.nz/it-specialists/critical-controls/principle-of-least-privilege/)_._

There are many pieces of advice and these will be provided on a case by case basis by your IT Security provider regarding the specific circumstances and how the environment was set up before the incident.

## Lessons Learned

No one can change the past but this is prime time to take an introspective look at how the incident could have been prevented and make any changes accordingly for the future. The process of looking at what could have been done better can be difficult but it will produce outcomes that will harden defences already in place and add others.

It is also a good time to look towards information security consulting to begin or continue your journey towards a stronger information security standing.&#x20;

Furthermore, a cyber insurance policy can help with the costs and expertise involved. It doesn't cost much in the scheme of things and is another step in being prepared for the worst.

**One final point that I think is important.**&#x20;

It is easy to look to the side and blame someone else for what went wrong but it is never the failure of a single person but the failure of policies, procedures, and planning. Look to do better, you're a team together :)

