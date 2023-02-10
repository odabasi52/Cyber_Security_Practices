import scapy.all as scp
import optparse
import subprocess
import re

#If you want to get info about scapy class
#    scp.ls(scp.class())

def get_interface_ip_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])

    #Get IP and MAC address of interface
    mac_address = re.search(r"[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}", str(ifconfig))
    ip_address = re.search(r"([0-9]{1,3}\.){3}[0-9]{1,3}", str(ifconfig))
    
    return (mac_address.group(0), ip_address.group(0))

def arp_request_broadcast(interface, ip_range):

    mac, ip = get_interface_ip_mac(interface)

    #SET destination ip range, source mac and source ip of arp_request
    arp_request = scp.ARP(pdst=ip_range, hwsrc=mac, psrc=ip)

    #SET source MAC and destination MAC (which is brodcast MAC)
    broadcast = scp.Ether(dst="ff:ff:ff:ff:ff:ff", src=mac)
    
    #return combined broadcast-arp_request package
    return broadcast/arp_request

def response_output():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface", help="Interface that you use such as (wlan0, eth0)",dest="interface", default="wlan0")
    parser.add_option("-r","--ip-range",help="IP range such as (192.168.1.1/24 or 192.168.1.32)", dest="ip_range")
    parser.add_option("-t","--timeout",help="Level of timeout (1-1000). Bigger timeout makes it more precise to detect network", dest="timeout", default="10")
    args = parser.parse_args()[0]

    if args.ip_range == None:
        print("Enter IP range")
    else:
        combined_pack = arp_request_broadcast(args.interface, args.ip_range)

        results = scp.srp(combined_pack, timeout=int(args.timeout), verbose=False)[0]
        
        #summarize detected IPs and MACs
        for i in results:
            mac = i[1].hwsrc
            ip = i[0].pdst
            print(f"IPv4 is {ip} - MAC is {mac}")

if __name__ == "__main__":
    response_output()