# Protocol Summary and DHCP

I am going to be following chapter 4 of the book "Tracking Hackers through Cyberspace" by Sherri Davidoff and Jonathan Ham. There may be acronyms or subjects beyond the scope of this article that you may not be familiar with but just flick them into Google and you'll be up to speed in no time.

I really enjoyed this book and it's has a plethora of interesting information. If you are interested you can buy the book here: [https://www.amazon.com/Network-Forensics-Tracking-Hackers-Cyberspace/dp/0132564718](https://www.amazon.com/Network-Forensics-Tracking-Hackers-Cyberspace/dp/0132564718).&#x20;

In the scenario below I have been provided with a pcap capture and will use Wireshark to analyse it.

## Lets begin

To start we will look at the Wireshark interface and start to explore different features it provides to the analyst when analysing a pcap file. In the picture below is the layout of Wireshark.

![Wireshark main interface](<../../.gitbook/assets/Wireshark 1.PNG>)

### Protocol Hierarchy

The first feature we will look at is called the Protocol Hierarchy. This provides us with a high level view of what protocols build up the captured packets within the pcap file. In the picture below we can identify some trends such as:

Data Link Layer

* 100 percent of frames are ethernet

Network Layer

* 100 percent of packets are IPv4

Transport Layer

* 19.3 percent of packets use UDP
* 80.4 percent of packets use TCP

Application Layer

* 0.4 percent of packets are Dynamic Host Configuration Protocol (DHCP)
* 13.2 percent of packets are Domain Name Service (DNS)
* 10.8 percent of packets are Simple Mail Transfer Protocol (SMTP)
* 11.7 percent of packets are Internet Message Access Protocol (IMAP)
* 4.5 percent of packets are Hypertext Markup Protocol (HTTP)

I haven't listed everything here but just to give an idea of what is portrayed.

![Protocol Hierarchy view](<../../.gitbook/assets/Wireshark 2.PNG>)

### Dynamic Host Configuration Protocol (DHCP)

Lets quickly cover what DHCP is in brief. DHCP as you can see what it stands for above is a protocol used by devices to request IP addresses from a DHCP server thus not requiring a static IP address (this is the simple version).

In this situation know what the MAC address of the computer of interest is, which is: 00:21:70:4D:4F:AE. With this knowledge we can use a filter within Wireshark to drill down into the packets.&#x20;

This is the filter we will use:

```
eth.addr == 00:21:70:4d:4f:ae and dhcp
```

All this means is we are looking for packets that have a MAC address of 00:21:70:4d:4f:ae and use DHCP.

... and voila we have identified 4 packets which we can see in the "Packet List Pane" based on our filter.

![Packet List Pane](<../../.gitbook/assets/Wireshark 3.PNG>)

The first packet is a DHCP request and is a broadcast packet, we know this as the destination IP is 255.255.255.255 (this goes to every device on the network) and the source is 0.0.0.0 because at this point the device doesn't have an IP address assigned to it. The two subsequent are the same too.

Lets take a closer look at the first packet we have filtered. We will now move into the "Packet Details Pane" which i have added a red rectangle to show.

Two things we can notice is the device is requesting the IP address 192.168.30.108 and that the requesting device has a host name of "ann-laptop"

![](<../../.gitbook/assets/Wireshark 4.PNG>)

Finally the fourth packet a DHCP ACK (Acknowledgment) packet from the Packet List Pane shows the source address 192.168.30.10 to the destination address of 192.168.30.108 which was the address the DHCP request packet was requesting and seems to have been provided by the DHCP server.&#x20;

We can confirm that the IP address 192.168.30.108 has been provided to the device with the MAC address 00:21:70:4d:4f:ae as it is the DHCP ACK packet as highlighted in the picture below.

![](<../../.gitbook/assets/Wireshark 5.PNG>)
