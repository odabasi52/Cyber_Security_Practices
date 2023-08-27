import scapy.all as scp
from sys import argv
from random import randint

class Server:
    def __init__(self, lport):
        self.lport = lport

    def establish_connection(self):
        scp.sniff(filter=f"tcp and port {self.lport}", prn=self.handle_client)

    def terminate_session(self,pkt,ack_num,seq_num):
        ip = scp.IP(src=pkt[scp.IP].dst, dst=pkt[scp.IP].src)
        tcp = scp.TCP(sport=pkt[scp.TCP].dport, dport=pkt[scp.TCP].sport, flags="FA", seq=ack_num , ack=seq_num)
        fyn_ack = ip / tcp
        scp.send(fyn_ack)
        print("FYN/ACK packet is sent to client. Session terminated")
        exit()

    def user_input_mode(self, pkt, seq_num, ack_num):
        global i
        while True:
            i += 1
            data_pkt = scp.sniff(filter=f"tcp and src {pkt[scp.IP].src} and dst {pkt[scp.IP].dst} and port {pkt[scp.TCP].dport} and port {pkt[scp.TCP].sport}", count=1)[0]
            if scp.TCP in data_pkt and data_pkt[scp.TCP].flags == "PA":
                client_ip = data_pkt[scp.IP].src
                client_data = data_pkt[scp.Raw].load.decode("utf-8")
                print(f"{client_ip} has sent: {client_data}")
                seq_num += (len(client_data))
                if i > 1: 
                    ack_num += 1
                ip = scp.IP(src=pkt[scp.IP].dst, dst=pkt[scp.IP].src)
                tcp = scp.TCP(sport=pkt[scp.TCP].dport, dport=pkt[scp.TCP].sport, flags="A", seq=ack_num , ack=seq_num)
                ack = ip / tcp
                scp.send(ack)
            elif scp.TCP in data_pkt and data_pkt[scp.TCP].flags == "F":
                client_ip = data_pkt[scp.IP].src
                print(f"{client_ip} has sent FIN packet to terminate session")
                seq_num += 1
                if i > 1: 
                    ack_num += 1
                self.terminate_session(data_pkt, ack_num, seq_num)    

    def pcap_write_mode(self, pkt, seq_num, ack_num):
        global i
        packets = []
        while True:
            i += 1
            data_pkt = scp.sniff(filter=f"ether src {pkt[scp.Ether].src} and ether dst {pkt[scp.Ether].dst}", count=1)[0]
            if scp.TCP in data_pkt and data_pkt[scp.TCP].flags == "PA":
                packets.append(data_pkt)
                client_ip = data_pkt[scp.IP].src
                client_data = data_pkt[scp.Raw].load
                print(f"{client_ip} has sent a pcap packet")
                seq_num += (len(client_data))
                if i > 1: 
                    ack_num += 1
                ip = scp.IP(src=pkt[scp.IP].dst, dst=pkt[scp.IP].src)
                tcp = scp.TCP(sport=pkt[scp.TCP].dport, dport=pkt[scp.TCP].sport, flags="A", seq=ack_num , ack=seq_num)
                ack = ip / tcp
                scp.send(ack)
            elif scp.TCP in data_pkt and data_pkt[scp.TCP].flags == "F":
                client_ip = data_pkt[scp.IP].src
                print(f"{client_ip} has sent FIN packet to terminate session")
                scp.wrpcap("received.pcap", packets)
                print("All received packets are saved as received.pcap")
                seq_num += 1
                if i > 1: 
                    ack_num += 1
                self.terminate_session(data_pkt, ack_num, seq_num)

    def handle_client(self, pkt):
        mode = "0"
        if scp.TCP in pkt and pkt[scp.TCP].flags == "S":
            print("SYN received from", pkt[scp.IP].src)
            seq_num = pkt[scp.TCP].seq
            ip = scp.IP(src=pkt[scp.IP].dst, dst=pkt[scp.IP].src)
            tcp = scp.TCP(sport=pkt[scp.TCP].dport, dport=pkt[scp.TCP].sport, flags="SA", seq=randint(1000,100000), ack=seq_num + 1)
            syn_ack = ip / tcp
            scp.send(syn_ack)
            print("SYN-ACK sent to", pkt[scp.IP].src)
        elif scp.TCP in pkt and pkt[scp.TCP].flags == "A":
            global i
            i = 0

            print("ACK received from", pkt[scp.IP].src)
            print("TCP connection established")
            mode = pkt[scp.Raw].load.decode("utf-8")
            seq_num = pkt[scp.TCP].seq
            ack_num = pkt[scp.TCP].ack
            
            if mode == "1":
                self.user_input_mode(pkt, seq_num, ack_num)     
            elif mode == "2":
                self.pcap_write_mode(pkt, seq_num, ack_num)
            
    
if __name__ == "__main__":
    if(len(argv) == 2):
        print(f"server port: {argv[1]}")
        server = Server(argv[1])
        server.establish_connection()
    elif(len(argv) == 1):
        print("server port: 4242 [Default Port]")
        server = Server("4242")
        server.establish_connection()
    else:
        print("Incorrect arguments")
