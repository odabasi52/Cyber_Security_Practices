import scapy.all as scp
import random as r
import argparse

class Client:
    def __init__(self, src_ip, dst_ip, dst_port):
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
            scp.send(ack)
            print("ACK sent to", self.dst_ip)
            self.data_sender_loop(ack_num, seq_num)
        else:
            print("No SYN-ACK received.")

    def data_sender_loop(self, ack_num, seq_num):
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
            scp.send(data_pkt)

            

            ack_pkt = scp.sniff(filter=f"tcp and src {self.dst_ip} and dst {self.src_ip} and port {self.dst_port} and port {self.src_port}", count=1)[0]
            if scp.TCP in ack_pkt and ack_pkt[scp.TCP].flags == "A":
                print("ACK received from server")
            elif scp.TCP in ack_pkt and ack_pkt[scp.TCP].flags == "FA":
                print("FIN/ACK received. Session is terminated")
                exit()

def arguments():
    parser = argparse.ArgumentParser(description="TCP Connection")
    parser.add_argument('-s', '--src', help="source ip address (can be spoofed ip)") 
    parser.add_argument('-d', '--dstip', help="destination ip address") 
    parser.add_argument('-p', '--port', help="destination port address") 
    return parser.parse_args()

if __name__ == "__main__":
    try:
        args = arguments()
        client = Client(args.src,args.dstip, int(args.port))
        client.establish_tcp_connection()
    except:
        print("--help/-h to get information about usage")
    
    
    