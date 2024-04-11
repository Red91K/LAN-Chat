import socket
import hashlib

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

def returnSHA256HASH(string):
    return hashlib.sha256(string).hexdigest()

INITIAL_HEADER = 9
HEADER = 6
PORT = 5050
HASHLEN = 64
#SERVER = "10.4.0.238"
FORMAT = "utf-8"
DISCONNECT_MSG = "DISCONNECT"

print("1/5 - CREATING SOCKET...")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER = input("ENTER IP ADDRESS OF SERVER (ex:10.0.0.1)\n")
ADDR = (SERVER,PORT)

print(f"2/5 - CONNECTING TO SERVER AT {ADDR}")
try:
    client.connect(ADDR)
except Exception as e:
    print(e)
    print("INCORRECT SERVER ADDRESS / SERVER IS UNREACHABLE")
    raise Exception(e)
print("3/5 - CONNECTED!")

def send(msg):
   message = msg.encode(FORMAT)
   msg_len = len(message)
   send_len = str(msg_len).encode(FORMAT)
   send_len += b' ' * (HEADER - len(send_len))
   client.send(send_len)
   client.send(message)

   # we get the hash of the message that we sent and then recieve the hash that the server gives us
   # if they match, this means that the server has correctly recieved our message
   # SHA256 hash of the final message that we sent
   senthash = returnSHA256HASH(message)
   # hash that the server sends us
   receivedhash = client.recv(HASHLEN).decode()
   #print(f'Received [{receivedhash}]')
   #print(f'Sent [{message}]   [{senthash}]')
   if(senthash != receivedhash):
    print("SENDING FAILED")

while True:
    print("4/5 - WAITING FOR CLEAR TO SEND")
    INITIAL_MSG = client.recv(INITIAL_HEADER).decode(FORMAT)
    INITIAL_MSG = INITIAL_MSG.strip(' ')

    # If clear to send... break loop
    if(INITIAL_MSG) == "CTS":
        print("5/5 - CLEAR TO SEND!")
        break

    elif(INITIAL_MSG == "!USERNAME"):
        username = str(input("Enter desired username:\t"))
        username = username.encode(FORMAT)

        username_len = len(username)
        username_len = str(username_len).encode(FORMAT)
        username_len += b' ' * (HEADER - len(username_len))

        client.send(username_len)
        client.send(username)


while True:
   curinput = input(":")
   if(curinput == "END"):
      send(DISCONNECT_MSG)
      break
   else:
      send(curinput)
