import scapy.all as scp
import random as r
import argparse
from pathlib import Path
import netifaces as ni
from getmac import get_mac_address
import ipaddress

class Client:
    def __init__(self, src_ip, dst_ip, dst_port,iface, pcap=None, ):
        self.dstmac = get_mac_address(ip=dst_ip)
        self.iface=iface
        self.pcap = pcap
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.src_port = r.randint(1024, 49151)

    def send_syn_recv_synack(self):
        # Create SYN packet
        syn = scp.IP(src=self.src_ip, dst=self.dst_ip)/scp.TCP(sport=self.src_port, dport=self.dst_port, seq=r.randint(1000,100000), flags="S")
        # Send SYN and receive SYN-ACK
        return scp.sr1(syn)
    
    def establish_tcp_connection(self):
        syn_ack = self.send_syn_recv_synack()
        if scp.TCP in syn_ack and syn_ack[scp.TCP].flags == "SA":
            print("SYN-ACK received from", self.dst_ip)
            seq_num = syn_ack[scp.TCP].seq
            ack_num = syn_ack[scp.TCP].ack
            ack = scp.IP(src=self.src_ip, dst=self.dst_ip) / scp.TCP(sport=self.src_port, dport=self.dst_port, flags="A", seq=ack_num, ack=seq_num + 1)
            if self.pcap == None:
                scp.send(ack/scp.Raw(load="1"), iface=self.iface)
                print("ACK (1) sent to", self.dst_ip)
                self.send_user_input(ack_num, seq_num)
            else:
                scp.send(ack/scp.Raw(load="2"), iface=self.iface)
                print("ACK (2) sent to", self.dst_ip)
                self.send_pcap(ack[scp.TCP].ack, ack[scp.TCP].seq,)
        else:
            print("No SYN-ACK received.")

    def send_pcap(self, ack_num, seq_num,):
        print(f"sending pcap packets to {self.dst_ip}:{self.dst_port}")
        packs = scp.rdpcap(self.pcap)

        new_src_mac = get_mac_address(ip="0.0.0.0")
        new_dst_mac = self.dstmac

        for i, pkt in enumerate(packs):
            if i > 0:
                ack_num += 1
            pkt[scp.Ether].src = new_src_mac
            pkt[scp.Ether].dst = new_dst_mac

            if scp.IP in pkt:
                pkt[scp.IP].src= self.src_ip 
                pkt[scp.IP].dst= self.dst_ip
            if scp.TCP in pkt:
                pkt[scp.TCP].sport = self.src_port
                pkt[scp.TCP].dport = self.dst_port
                pkt[scp.TCP].ack = ack_num
                pkt[scp.TCP].seq = seq_num
            while True:
                scp.sendp(pkt, iface=self.iface)
                ack_pkt = scp.sniff(timeout=10, filter=f"src {self.dst_ip} and dst {self.src_ip} and port {self.dst_port} and port {self.src_port}", count=1)
                if ack_pkt is not None and len(ack_pkt) > 0:
                    if scp.TCP in ack_pkt[0] and ack_pkt[0][scp.TCP].flags == "A":
                        print("ACK received, server has pcap packet.")
                        break
                
            seq = ack_pkt[0][scp.TCP].ack
            ack = ack_pkt[0][scp.TCP].seq + 1

        print("Sent FIN packet to server")
        data_pkt = scp.IP(src=self.src_ip, dst=self.dst_ip)/scp.TCP(sport=self.src_port, dport=self.dst_port, flags="F", seq=seq, ack=ack)
        scp.send(data_pkt, iface=self.iface)
        fin_ack_pkt = scp.sniff(filter=f"tcp and src {self.dst_ip} and dst {self.src_ip} and port {self.dst_port} and port {self.src_port}", count=1)[0]
        if scp.TCP in fin_ack_pkt and fin_ack_pkt[scp.TCP].flags == "FA":
            print("FIN/ACK packet received from server, session terminated")
            exit()

    def send_user_input(self, ack_num, seq_num):
        print("exit or quit to terminate session\n--------------------\n")
        while True:
            try:
                user_input = input("Enter a string: ")
            except KeyboardInterrupt:
                user_input = "exit"
                  
            seq_num += 1
            if user_input == "exit" or user_input == "quit":
                data_pkt = scp.IP(src=self.src_ip, dst=self.dst_ip)/scp.TCP(sport=self.src_port, dport=self.dst_port, flags="F", seq=ack_num, ack=seq_num)
                print("Sent FIN packet to server")
            
            else:
                data_pkt = scp.IP(src=self.src_ip, dst=self.dst_ip)/scp.TCP(sport=self.src_port, dport=self.dst_port, flags="PA", seq=ack_num, ack=seq_num) / scp.Raw(load=user_input)
                ack_num += len(user_input)
            scp.send(data_pkt, iface=self.iface)

            

            ack_pkt = scp.sniff(filter=f"tcp and src {self.dst_ip} and dst {self.src_ip} and port {self.dst_port} and port {self.src_port}", count=1)[0]
            if scp.TCP in ack_pkt and ack_pkt[scp.TCP].flags == "A":
                print("ACK received from server")
            elif scp.TCP in ack_pkt and ack_pkt[scp.TCP].flags == "FA":
                print("FIN/ACK received. Session is terminated")
                exit()

def arguments():
    parser = argparse.ArgumentParser(description="TCP Connection")
    parser.add_argument('-s', '--src', help="source ip address (can be spoofed ip)",required=True) 
    parser.add_argument('-d', '--dstip', help="destination ip address", required=True)
    parser.add_argument('-i', '--iface', help="interface to send data", required=True)
    parser.add_argument('-p', '--port', help="destination port address",default="4242") 
    parser.add_argument('-c', '--pcap', help="path of .pcap", default=None) 
    return parser.parse_args()

def check_ip(ip) -> bool:
    try:
        ip_object = ipaddress.ip_address(ip)
        print(f"The IP address '{ip_object}' is valid.")
        return True
    except ValueError:
        print(f"The IP address '{ip}' is not valid")
        return False


if __name__ == "__main__":
    try:
        args = arguments()

        if args.iface in ni.interfaces():
            print(f"The interface '{args.iface}' is valid.")
        else:
            print("interface not found.")
            exit()

        if args.port.isdigit():
            print(f"port: {args.port}")
        else:
            print("wrong port number, enter valid value")
            exit()
        
        if not check_ip(args.dstip):
            print("change destination IP")
            exit()
        elif not check_ip(args.src):
            print("change source IP")
            exit()
        
        pcap = None
        if not args.pcap == None:
            pcap = Path(args.pcap)
            if pcap.is_file():
                print("File path is OK, file exists.")
                if pcap.suffix == ".pcap":
                    print("file is pcap, program will be executed on pcap sending mode.")
                else:
                    print("file is not pcap, proram will be executed on user input mode.")
            else:
                print("Given path is wrong. No file found. Program will be executed on user input mode.")
        else:
            print("Pcap option is not used. Program will be executed on user input mode.")

        
        client = Client(args.src,args.dstip, int(args.port), args.iface, args.pcap, )
        client.establish_tcp_connection()
    except Exception as e:
        print(e)
        print("--help/-h to get information about usage")
    
    
    