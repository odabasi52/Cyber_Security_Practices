import scapy.all as scp
from sys import argv
from random import randint

class Server:
    def __init__(self, lport):
        self.lport = lport

    def establish_connection(self):
        scp.sniff(filter=f"tcp and port {self.lport}", prn=self.handle_client)        

    def handle_client(self, pkt):
        if scp.TCP in pkt and pkt[scp.TCP].flags == "S":
            print("SYN received from", pkt[scp.IP].src)
            seq_num = pkt[scp.TCP].seq
            ip = scp.IP(src=pkt[scp.IP].dst, dst=pkt[scp.IP].src)
            tcp = scp.TCP(sport=pkt[scp.TCP].dport, dport=pkt[scp.TCP].sport, flags="SA", seq=randint(1000,100000), ack=seq_num + 1)
            syn_ack = ip / tcp
            scp.send(syn_ack)
            print("SYN-ACK sent to", pkt[scp.IP].src)
        elif scp.TCP in pkt and pkt[scp.TCP].flags == "A":
            print("ACK received from", pkt[scp.IP].src)
            print("TCP connection established")
            seq_num = pkt[scp.TCP].seq
            ack_num = pkt[scp.TCP].ack
            i = 0
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
                    ip = scp.IP(src=pkt[scp.IP].dst, dst=pkt[scp.IP].src)
                    tcp = scp.TCP(sport=pkt[scp.TCP].dport, dport=pkt[scp.TCP].sport, flags="FA", seq=ack_num , ack=seq_num)
                    fyn_ack = ip / tcp
                    scp.send(fyn_ack)
                    print("FYN/ACK packet is sent to client. Session terminated")
                    exit()
            
    
if __name__ == "__main__":
    if(len(argv) == 2):
        server = Server(argv[1])
        server.establish_connection()
    else:
        print("Incorrect arguments")