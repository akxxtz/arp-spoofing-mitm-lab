# ARP Spoofing & MITM Attack — Lab Demonstration

## Overview
The lab demonstrates a Man-in-The-Middle attack where the threat actor intercepts packets before they are able to reach their destination.

An attack like this shows how our info can be easily intercepted without our knowledge since on the surface nothing seems out of place.

The main attributing factor is how ARP operates - **It lacks any authentication** whether the reply is legitimate or **whether the reply was actually even solicited in the first place**

ARP accepts replies even without sending a request first, This is what makes unsolicited ARP replies possible and the attack so effective.

## Environment & Tools
Kathará - Docker-based network emulation tool that doesnt require image files, thus lightweight compared to other such as CML or GNS3

Scapy - Python library for crafting, sending, and capturing network packets at a low level (ethernet frames / ARP headers / raw packet bytes)

Docker — Containerisation Platform that allows us to host multiple interconnected devices

## Network Topology
![Network Topology](screenshots/network-topology.png)

## How It Works
The threat actor would have to act as a router to effectively become the Man-in-The-Middle so that packets that are from the victim(h1) meant for server(h2) goes through him first before reaching the desired destination.

### ARP Poisoning
The ARP table before any malicious activity would point to the correct MAC address associated with that IP address. What ARP Poisoning does is the threat actor gives a false ARP reply to its desired target, claiming to be the MAC address associated with the legitimate IP address. This successfully makes the device think that it is sending packets to the right host, although it would be far from the truth.

### Traffic Redirection
The threat actor poisons the ARP tables of **both** sides (victim and server), making the victim think it is sending directly to the server and vice versa. When the packet arrives at the attacker machine, IP forwarding automatically reroutes it to its actual destination — maintaining the illusion of direct communication.

### Credential Capture
Credential capture occurs in the brief moment the packet passes through the attacker before being forwarded. The packet sniffer script decodes the packet to extract valuable information. In this instance, it looks for the HTTP POST method and strings containing `user=` or `pass=` — tailored specifically to the target server.

## Key Results
### Attacker MAC Address
![attacker mac](screenshots/attacker-mac-addr.png)

### Before ARP Poisoning
![before](screenshots/server-h2-arp-table-before-spoofing.png)

### After ARP Poisoning
![after](screenshots/server-h2-arp-table-after-spoofing.png)

### Captured Credentials
![captured](screenshots/intercepted-login-details.png)

## Defensive Countermeasures
### DAI (Dynamic ARP Inspection) 
Core Idea : DAI intercepts every ARP reply on untrusted ports and validates it against a trusted database before allowing it through

The database it uses : **DHCP Snooping Binding Table**

When DHCP Snooping is enabled, the switch records every legit IP-to-MAC assignment it sees, so when an attacker tries to send a malicious ARP reply, the packet gets dropped after the switch checks that it is not the legitimate MAC address associated with the IP it is trying to spoof as.

### HTTPS/TLS 
The problem with HTTP is that it sends everything in plaintext, therefore anyone intercepting traffic can read it. 

**TLS (Transport Layer Security)** solves this by introducing encryption to the data. Even if the traffic is read during transit, the data is scrambled, rendering the attack useless

## References / What I Learned
I learned using Scapy to create and capture packets. That you can even craft the packets in several layers, like manipulating the ARP headers and Ethernet frames. 

I also learned how to use Kathara as a network simulation tool; setting up the topology, connecting each device to the same collision domain to simulate the devices being in the same network

What really surprised me was how easy the attack was, just two short python scripts and I was able to obtain the login credentials of an unsuspecting user. It is clear to me now why most websites nowadays use HTTPS instead of HTTP to block this sort of thing from happening.



