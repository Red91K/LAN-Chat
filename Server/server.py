import threading
import socket
import hashlib

from datetime import datetime
from UsernameFunctions import *

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('255.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

def returnSHA256HASH(string):
    return hashlib.sha256(string).hexdigest()

def checkifusername(username):
    with open ('usernames.txt', 'r') as f:
        pass

INITIAL_HEADER = 9
HEADER = 6
PORT = 5050
DISPLAY_PORT = 9090
HASHLEN = 64
SERVER = extract_ip()
ADDR = (SERVER, PORT)
DISPLAY_ADDR = (SERVER,DISPLAY_PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

display_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
display_server.bind(DISPLAY_ADDR)

# globals
clientcnt = 0
displayconnections = []
# chatlog format [time - (%H,%M,%S),username,ip,port,msg]
chatlog = []

def handle_client(conn,addr):
    global clientcnt
    global chatlog
    global displayconnections

    clientcnt+=1
    print(f"[NEW CLIENT] - {addr} connected")

    #! if the connected client does not have a username
    if(returnUsernameFromIp(addr[0]) == False):
        # keep looping until unique username is received
        while True:
            # ask for username
            conn.send("!USERNAME".encode(FORMAT))

            # get username reply
            # 1st message is length of username
            msg_len = conn.recv(HEADER).decode(FORMAT)
            msg_len = int(msg_len)

            # 2nd is username
            username = conn.recv(msg_len).decode(FORMAT)
            if(checkifUsernameExists(username) == False):
                # save username to usernames.txt
                writeUsernameandIp(addr[0],username)
                break
            else:
                print(f'Username from {addr} - "{username}" already exists')

        CTSMSG = "CTS".encode(FORMAT) + b' ' * (INITIAL_HEADER - 3)
        conn.send(CTSMSG)
    else:
        CTSMSG = "CTS".encode(FORMAT) + b' ' * (INITIAL_HEADER - 3)
        conn.send(CTSMSG)


    connected = True
    while connected:
        #first message should always be 64 bites long, and contain the length of the next message
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            try:
                msg_len = int(msg_len)
                msg = conn.recv(msg_len)
                message = msg.decode(FORMAT)
                #print(f'Hash: [{msg}] {returnSHA256HASH(msg)}')

                #we send the SHA256 hash of the entire recieved message
                conn.send(returnSHA256HASH(msg).encode())

                # get current time
                now = datetime.now()

                username = returnUsernameFromIp(addr[0])
                if(username == False):
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("ERROR - CLIENT HAS NO USERNAME")
                    print("CLOSING CONNECTION....")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    conn.close()
                # add chat to chatlog
                chatlog.append([now.strftime('%H:%M:%S'),username,addr[0],addr[1],message])

                try:
                    # send chatlog to displays
                    # chatlog send format

                    # "[len(time),len(username),len(ip),len(port),len(msg)]timeusernameipportmsg"
                    displayar = []
                    # [time - (%H,%M,%S),username,ip,port,msg]
                    for chat in chatlog:
                        displaystr = b""
                        datePart = chat[0].encode(FORMAT)
                        usernamePart = chat[1].encode(FORMAT)
                        IPPart = chat[2].encode(FORMAT)
                        PortPart = str(chat[3]).encode(FORMAT)
                        msgPart = chat[4].encode(FORMAT)

                        displaystr += str([len(datePart),len(usernamePart),len(IPPart),len(PortPart),len(msgPart)]).encode(FORMAT)
                        displaystr += datePart + usernamePart + IPPart + PortPart + msgPart
                        displayar.append(displaystr)

                    for display in displayconnections:
                        try:
                            display[0].send("!NEW_CHAT".encode(FORMAT))

                            # chatlogindex - number of chats the display has received
                            chatlogindex = display[0].recv(HEADER)
                            try:
                                chatlogindex = chatlogindex.decode(FORMAT)
                                chatlogindex = int(chatlogindex.strip(' '))
                            except Exception as err:
                                print(err)
                                print("ERROR! - CHATLOGINDEX IS NOT A INTEGER")

                            outstr = b''
                            for i in range(chatlogindex,len(displayar)):
                                outstr += displayar[i]
                            msg_len = len(outstr)
                            msg_len = str(msg_len).encode(FORMAT)
                            msg_len += b' ' * (HEADER - len(msg_len))
                            print(msg_len)
                            #print(displaystr)
                            display[0].send(msg_len)
                            display[0].send(outstr)
                        except Exception as err:
                            print(err)
                            print(f"DISPLAY AT {display[1]} DISCONNECTED")
                            print(f'CLOSING CONNECTION...')
                            display[0].close()
                            displayconnections.remove(display)
                            print("CONNECTION CLOSED")

                except Exception as err:
                    print("tis")
                    print(err)

                print(f"{now.strftime('%H:%M:%S')} | {username} {addr} - {message}")
                #print(chatlog)
            except Exception as err:
                print("ERROR - TRANSMISSION FAILED")
                print(err)
            if(message == DISCONNECT_MSG):
                print(f"[DISCONNECTING] from {addr}")
                connected = False

    clientcnt -= 1
    conn.close()

def handle_display(conn,addr):
    print("hiu")
    conn.send("hello".encode(FORMAT))
    conn.close()


def serverAccept():
    global clientcnt
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr),daemon=True)
        thread.start();
        print(f"[ACTIVE CONNECTIONS] {clientcnt}")

def displayAccept():
    global displayconnections
    while True:
        display_conn,display_addr = display_server.accept()
        displayconnections.append([display_conn,display_addr])
        print(f"[NEW DISPLAY] - {display_addr} connected")

        # entire code from here is sending chatlog once a display has connected
        displayar = []
        for chat in chatlog:
            displaystr = b""
            datePart = chat[0].encode(FORMAT)
            usernamePart = chat[1].encode(FORMAT)
            IPPart = chat[2].encode(FORMAT)
            PortPart = str(chat[3]).encode(FORMAT)
            msgPart = chat[4].encode(FORMAT)

            displaystr += str([len(datePart),len(usernamePart),len(IPPart),len(PortPart),len(msgPart)]).encode(FORMAT)
            displaystr += datePart + usernamePart + IPPart + PortPart + msgPart
            displayar.append(displaystr)

        display_conn.send("!NEW_CHAT".encode(FORMAT))
        # chatlogindex - number of chats the display has received
        chatlogindex = display_conn.recv(HEADER)
        try:
            chatlogindex = chatlogindex.decode(FORMAT)
            chatlogindex = int(chatlogindex.strip(' '))
        except Exception as err:
            print(err)
            print("ERROR! - CHATLOGINDEX IS NOT A INTEGER")

        outstr = b''
        for i in range(chatlogindex,len(displayar)):
            outstr += displayar[i]
        msg_len = len(outstr)
        msg_len = str(msg_len).encode(FORMAT)
        msg_len += b' ' * (HEADER - len(msg_len))
        print(msg_len)

        display_conn.send(msg_len)
        display_conn.send(outstr)



def start():
   server.listen()
   display_server.listen()
   print(f"[LISTENING ON] {SERVER}")

   serverthread = threading.Thread(target=serverAccept,daemon=True)
   displaythread = threading.Thread(target=displayAccept,daemon=True)
   serverthread.start()
   displaythread.start()
   serverthread.join()


print("Server is Starting...")
start()
