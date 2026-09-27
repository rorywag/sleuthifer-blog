# Follow TCP Stream and SMTP

In this section we will be analysing SMTP traffic from a packet capture and using some other Wireshark features such as Follow TCP Stream.

This is carrying on from Chapter 4 of of the book "Tracking Hackers through Cyberspace" by Sherri Davidoff and Jonathan Ham.

## Lets begin

Quickly lets talk about what SMTP is first. The guys over at GeekforGeeks put it simply below as:

> SMTP is a push protocol and is used to send the mail whereas POP (post office protocol) or IMAP (internet message access protocol) are used to retrieve those mails at the receiver’s side. - [**GeekforGeeks**](https://www.geeksforgeeks.org/simple-mail-transfer-protocol-smtp/)

First lets find the first SMTP packet using the Display Filter section with the filter below.

```text
smtp
```

Here is our output as seen from the Packet List Pane with the Display Filter section shown in green above it.

![Packet List Pane using SMTP filter ](<../../.gitbook/assets/image (1).png>)

Wireshark has a great feature that allows us as to follow protocol streams such as a TCP stream between two addresses allowing us to see to see the contents of packets how it would be seen at layer 7 (Presentation Layer) of the OSI model in a easily readable format.&#x20;

We will use this feature to view the TCP Stream between the IP address 192.168.30.108 we determined was assigned to the device with the name "ann-laptop" in the previous post and a new IP identified below as 64.12.168.40.&#x20;

Just right click on the packet you want to view and select Follow > TCP Stream as shown below.

![How to follow a TCP stream](<../../.gitbook/assets/Wireshark 7.PNG>)

We can now see the flow of traffic between the two addresses which appears to be a Mail User Agent (MUA) and a Mail Submission Agent (MSA). Click [**here** ](https://afreshcloud.com/sysadmin/mail-terminology-mta-mua-msa-mda-smtp-dkim-spf-dmarc)to learn more about mail terminology, which is outside the scope of this article.

![TCP Stream](<../../.gitbook/assets/Wireshark 9.PNG>)

To end lets take a quick look at what's in the TCP Stream we've captured. Looking down the flow of text we can see a point where Ann's laptop is looking to authenticate with the MSA using plain text. This means the authentication process isn't encrypted and in this case is using base64 encoding which are the strings at lines 6 to 9.

```text
250-AUTH=XAOL-UAS-MB LOGIN PLAIN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250 DSN
AUTH LOGIN
334 VXNlcm5hbWU6
c25lYWt5ZzMza3k=
334 UGFzc3dvcmQ6
czAwcGVyczNrcjF0
235 2.7.0 Authentication successful
```

We can decode the gibberish below to identify Ann's username and password a couple of ways.

The first "technical" way you could do this is using the command line in Linux with the following command. I have left the last one blank for you to try if you like

```
echo "VXNlcm5hbWU6" | base64 -d
Username:

echo "c25lYWt5ZzMza3k=" | base64 -d
sneakyg33ky

echo "UGFzc3dvcmQ6" | base64 -d
Password:

echo "czAwcGVyczNrcjF0" | base64 -d
...
```

The second "easier and possibly quicker" way you could do it is using a website such as [**base64decode**](https://www.base64decode.org/)  to decode the base64 into readable ASCII.
