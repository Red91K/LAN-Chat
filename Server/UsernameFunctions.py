# takes a line of usernames.txt as input
# returns a array with the 1st item being the IP address, the second item being the usernames
# returns False if the line is not a valid entry (And thus has been corrupted)
def splitUsername(line):
   line = line.strip('\n')
   if(line == ''):
      return False
   spacepos = False
   for i in range (len(line)):
      if(line[i] == ' '):
         spacepos = i
         break
   
   # if there are no spaces in the line, 
   if(spacepos == False):
      print()
      print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      print("No space between ip & username in usernames.txt")
      print(f'Line: [{line}]')
      print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      print()
      return False
   
   ip = line[:spacepos]
   username = line[spacepos+1:]

   if(checkIPValidity == False):
      return False

   return [ip,username]

# when given a IP address, returns True if is a valid IP address
# prints (in detail) the reason why IP is not valid
# the optional argument line makes this function compatible with function splitUsername()
def checkIPValidity(ip,line=False):
   # check if each IP address has four entries
   splitip = ip.split('.')
   if(len(splitip) != 4):
      print()
      print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      if(line != False):
         print("Invalid IP address in usernames.txt - make sure that IP address has four octets")
         print("Ex: '192.168.0.1'")
         print(f'IP Entry: [{ip}]')
         print(f'Line: [{line}]')
      else:
         print("IP Address does not contain four octets!")
      print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      print()
      return False
   
   for octet in splitip:
      # check if each current octet is a number
      try:
         a = int(octet)
      except ValueError:
         print()
         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
         print("OCTET in IP address is not a number in usernames.txt!")
         print(f'OCTET: [{octet}]')
         print(f'IP Entry: [{ip}]')
         print(f'Line: [{line}]')
         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
         print()
         return False
      
      # check if each octet is between 0 and 255
      if(int(octet) >= 0 and int(octet) <= 255):
         pass
      else:
         print()
         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
         print("OCTET in IP address is not between 0 and 255")
         print("Check usernames.txt")
         print(f'OCTET: [{octet}]')
         print(f'IP Entry: [{ip}]')
         print(f'Line: [{line}]')
         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
         print()
         return False
   return True

# when given a ip and the corresponding username, writes them to usernames.txt
def writeUsernameandIp(ip,username):
   if(checkIPValidity(ip) == True):
      with open ('usernames.txt', 'r') as f:
         contents = f.readlines()
      with open('usernames.txt','w') as f:
         for line in contents:
            f.write(line)
         f.write('\n' if contents != [] else '')
         f.write(f'{ip} {username}')
   else:
      print("!ERROR - USERNAME NOT RECORDED TO TXT FILE")

# when given a IP address, checks usernames.txt for it's corresponding username
# if the IP address / it's corresponding username is not found, return False
def returnUsernameFromIp(ip):
   with open ('usernames.txt', 'r') as f:
      for line in f.readlines():
         outar = splitUsername(line)
         if(outar != False):
            if(ip == outar[0]):
               return outar[1]
      return False

# when given a username, checks in usernames.txt to see if it exists
# returns True / False
def checkifUsernameExists(username):
   with open ('usernames.txt','r') as f:
      for line in f.readlines():
         outar = splitUsername(line)
         if(outar != False):
            if(username == outar[1]):
               return True
      return False