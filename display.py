import socket
import hashlib

PORT = 9090
HASHLEN = 64
INITIAL_HEADER = 9
HEADER = 6
#SERVER = "10.4.0.238"
FORMAT = "utf-8"
DISCONNECT_MSG = "DISCONNECT"

#globals
display = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
curchatindex = 0

def handle_server():
   global curchatindex
   while True:
      initial = display.recv(INITIAL_HEADER)
      initial = initial.decode(FORMAT)
      if(initial != "!NEW_CHAT"):
            print(f"ERROR - UNKNOWN INITIAL MESSAGE ({initial})")
            break
      outchatindex = str(curchatindex).encode(FORMAT)
      outchatindex += b' ' * (HEADER - len(outchatindex))
      display.send(outchatindex)
      msg_len = display.recv(HEADER)
      msg_len = int((msg_len.decode()).strip(' '))
      unformatted = display.recv(msg_len)
# -> b'[8, 5, 12, 5, 2]23:49:08red91192.168.0.1555279hi'

      decoded = unformatted.decode(FORMAT)
# -> '[8, 5, 12, 5, 2]23:49:08red91192.168.0.1555279hi'

      # loop should start here
      while decoded != '':
         if(decoded[0] != '['):
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("FIRST CHARACTER OF DISPLAY DATA IS NOT '['")
            print(decoded)
            print("EXITING....")
            print("!!!!!!!!!!!!!!!!!!!!!!!!")
            return

         bracketclosepos = "NOPE"
         for i in range(len(decoded)):
            if(decoded[i] == ']' and bracketclosepos == "NOPE"):
               bracketclosepos = i

         if(bracketclosepos == "NOPE"):
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("']' CHARACTER NOT FOUND IN DISPLAY DATA'")
            print(decoded)
            print("EXITING....")
            print("!!!!!!!!!!!!!!!!!!!!!!!!")
            return

         removedbrackets = decoded[1:bracketclosepos]
   # -> '8, 5, 12, 5, 2'

         lengthar = removedbrackets.split(',')
   # -> ['8', '5', '12', '5', '2']

         lengthar = [int(i) for i in lengthar]
   # -> [8, 5, 12, 5, 2]
         timestart = bracketclosepos
         time = decoded[timestart+1:timestart+lengthar[0]+1]
         #'23:49:08'

         usernamestart = timestart + lengthar[0]
         username = decoded[usernamestart + 1:usernamestart + lengthar[1]+1]
         #'red91'

         ipstart = usernamestart + lengthar[1]
         ip = decoded[ipstart + 1: ipstart + lengthar[2]+1]
         #'192.168.0.15'

         portstart = ipstart + lengthar[2]
         port = decoded[portstart +1: portstart + lengthar[3]+1]
         #'55279'

         msgstart = portstart + lengthar[3]
         msg = decoded[msgstart + 1: msgstart + lengthar[4]+1]
         # "[len(time),len(username),len(ip),len(port),len(msg)]timeusernameipportmsg"

         print(f"{time} | {username} {(ip,port)} - {msg}")
         decoded = decoded[msgstart + lengthar[4] + 1:]
         #print(decoded)
         curchatindex+=1



while True:
   SERVER = input("ENTER IP ADDRESS OF SERVER (ex:10.0.0.1)\n")
   print(f"CONNECTING TO SERVER AT {SERVER}")
   ADDR = (SERVER,PORT)
   try:
       display.connect(ADDR)
   except Exception as e:
       print(e)
       print("INCORRECT SERVER ADDRESS / SERVER IS UNREACHABLE")
       raise Exception(e)
   print(f"CONNECTED TO SERVER AT {ADDR[0]}")
   handle_server()
