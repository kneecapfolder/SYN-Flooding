import customtkinter as tk
from tkinter import messagebox
import ipaddress
import client

class FloodApplication:
    def __init__(self, dest_ip, dest_port):
        # Set theme
        tk.set_appearance_mode("Dark")
        tk.set_default_color_theme('themes/red.json')
        self.my_font = lambda size: tk.CTkFont(size=size, weight='bold', family='Ariel')
        
        # Configure app window
        self.root = tk.CTk()
        self.root.geometry('320x200')
        self.root.title('DOS Attack')
        self.root.resizable(False, False)

        # Title
        self.title_label = tk.CTkLabel(self.root, text='SYN Flood Attack', text_color='tomato', font=self.my_font(25))
        self.title_label.pack(pady=10)
        
        # IP input fields
        self.target_ip_input = tk.CTkEntry(self.root, placeholder_text='target ip', width=230, height=40)
        self.target_port_input = tk.CTkEntry(self.root, placeholder_text='target port', width=230, height=40)

        self.target_ip_input.pack()
        self.target_port_input.pack(pady=5)
        
        # Start attack button
        self.attack_button = tk.CTkButton(self.root, command=self.start_attack, text='FLOOD!', font=self.my_font(20), width=230, height=40)
        self.attack_button.pack(pady=8)

        # Run app
        self.root.mainloop()

    
    def start_attack(self):
        dest_ip = self.target_ip_input.get()
        dest_port = int(self.target_port_input.get())

        # Check ip input
        if not self.is_valid_ip(dest_ip):
            messagebox.showinfo('faulty value given', "please enter a valid target ip")
            return
        
        # Check port input
        if dest_port not in range(65536):
            messagebox.showinfo('faulty value given', "please enter a valid target port")
            return

        self.flooder = client.Flooder(dest_ip, dest_port)
        self.flooder.start()

        self.toggle_attack_button_off()


    def stop_attack(self):
        self.flooder.stop()
        self.toggle_attack_button_on()


    def toggle_attack_button_on(self):
        self.attack_button.destroy()
        self.attack_button = tk.CTkButton(self.root, command=self.start_attack, text='FLOOD!', font=self.my_font(20), width=230, height=40)
        self.attack_button.pack(pady=8)

    
    def toggle_attack_button_off(self):
        self.attack_button.configure(command=self.stop_attack, text='STOP', fg_color='gray24', hover_color='gray22')


    def is_valid_ip(self, ip):
            try:
                ipaddress.ip_address(ip)
                return True
            except ValueError:
                return False
        
    
if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 80

    app = FloodApplication(HOST, PORT)