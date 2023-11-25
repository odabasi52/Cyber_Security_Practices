import subprocess
import optparse
import re

def main():
    #create option parser
    parser = optparse.OptionParser()
    print("manual_mac_changer started")

    #add options and store them as variables <dest>
    parser.add_option("-i","--interface", help="Interface that you use (wlan0, eth0...)",dest="interface")
    parser.add_option("-m","--mac", help="New MAC address (like 00:11:22:33:44:55)",dest="mac")
    args = parser.parse_args()[0]

    #Call subprocesses to change MAC address
    subprocess.call(["sudo","ifconfig",args.interface, "down"])
    subprocess.call(["sudo","ifconfig",args.interface, "hw","ether",args.mac])
    subprocess.call(["sudo","ifconfig",args.interface, "up"])

    #check and store process of ifconfig <interface>
    ifconfig = subprocess.check_output(["ifconfig", args.interface])
    
    mac_address = re.search(r"[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}", str(ifconfig))
    if mac_address.group(0).upper() == args.mac.upper():
        print(f"SUCCESSFULL, new MAC address of {args.interface} is {mac_address.group(0).upper()}")

    else:
        print("manual_mac_changer did not finish properly")


if __name__ == "__main__":
    try:
        main()
    except:
        print("\nUsage: python manual_mac_changer.py -i <interface> -m <new_mac>\nNote: MAC address should start with even value\nNote: MAC adress can only contain HEXADECIMAL values (123456789abcdef)")
