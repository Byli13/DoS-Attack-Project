import re
import logging
import socket
from typing import Tuple, Optional
from datetime import datetime

class InputValidator:
    """Class for validating input data such as IP addresses, ports, and URLs."""
    @staticmethod
    def validate_ip(ip: str) -> bool:
        """Validate IP address format"""
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    @staticmethod
    def validate_port(port: int) -> bool:
        """Validate port number"""
        return 1 <= port <= 65535

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None

class Logger:
    def __init__(self, filename: str = "dos_attack.log"):
        """Initialize logger with specified filename"""
        self.logger = logging.getLogger('DOSLogger')
        self.logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_attack_start(self, target: Tuple[str, int], method: str) -> None:
        """Log attack start"""
        self.logger.info(f"Attack started - Target: {target[0]}:{target[1]} - Method: {method}")

    def log_attack_stop(self, target: Tuple[str, int], duration: float, packets: int) -> None:
        """Log attack stop"""
        self.logger.info(
            f"Attack stopped - Target: {target[0]}:{target[1]} - "
            f"Duration: {duration:.2f}s - Packets sent: {packets}"
        )

    def log_attack_details(self, target: Tuple[str, int], method: str, packet_type: str, result: str) -> None:
        """Log attack details"""
        self.logger.info(
            f"Attack details - Target: {target[0]}:{target[1]} - Method: {method} - "
            f"Packet Type: {packet_type} - Result: {result}"
        )

    def log_error(self, error_msg: str) -> None:
        """Log error message"""
        self.logger.error(f"Error occurred: {error_msg}")

class Statistics:
    def __init__(self):
        self.start_time = datetime.now()
        self.packets_sent = 0
        self.successful_connections = 0
        self.failed_connections = 0

    def update_stats(self, success: bool = True) -> None:
        """Update attack statistics"""
        self.packets_sent += 1
        if success:
            self.successful_connections += 1
        else:
            self.failed_connections += 1

    def get_stats(self) -> dict:
        """Get current statistics"""
        duration = (datetime.now() - self.start_time).total_seconds()
        return {
            'duration': duration,
            'packets_sent': self.packets_sent,
            'successful_connections': self.successful_connections,
            'failed_connections': self.failed_connections,
            'success_rate': (self.successful_connections / self.packets_sent * 100) if self.packets_sent > 0 else 0,
            'packets_per_second': self.packets_sent / duration if duration > 0 else 0
        }

    def reset_stats(self) -> None:
        """Reset all statistics"""
        self.start_time = datetime.now()
        self.packets_sent = 0
        self.successful_connections = 0
        self.failed_connections = 0
