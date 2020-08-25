# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import socket
import select
import struct
import os
import network
from time import sleep

def socketRecieve(socket, size):
    try:
        data = socket.recv(size)
        if data == b'':
            return None
        while len(data) < size:
            data2 = socket.recv(size-len(data))
            if data2 == b'':
                return None
            data += data2
        #print('Read data:', data)
        return data
    except:
        return None
class Actions:
    Motor = 1
    File = 10
    FileExec = 11
    Files = 12
    Login = 13
    LoginVerified = 14
    LoginFailed = 15
    FileExecEnd = 16
    PinController = 17
    FileForceEnd = 18
class Packet:
    #data = None
    def __init__(self, action=None, data=None, socket=None):
        self.size = 0
        self.data = data
        self.action = action
        self.socket = socket
        pass#self.action = action
        
    def read(self, socket, size=0):
        print('size =', self.size)
        pass
     
    def get(self, socket):
        pass
        
    def apply(self):
        pass
        
class FilePacket(Packet):
    class FilePacketParams:
       name_size = (0, 4) #Index, size
       name = (4,4+name_size[1])
       file_size = (4+name_size[1], 4+name_size[1]+4)
       file = (4+name_size[1]+4, 4+name_size[1]+4+file_size[1])
    
    def get(self, socket):
        file_name_size_buffer = socketRecieve(self.socket, 4)
        self.file_name_size = struct.unpack('>I', file_name_size_buffer)[0]
        
        self.file_name = socketRecieve(self.socket, self.file_name_size).decode('utf-8')
        
        file_size_buffer = socketRecieve(self.socket, 4)
        self.file_size = struct.unpack('>I', file_size_buffer)[0]
        
        self.file = socketRecieve(self.socket, self.file_size)
        pass
        
    def __init__(self, action=None, data=None, socket=None):
        super().__init__(action, data, socket)
        self.action = Actions.File
        
        self.file_name_size = None
        self.file_name = None
        self.file_size = None
        self.file = None
        
        self.socket = socket
        
        self.get(socket)
        
        
    def apply(self):
        super().apply()
        f = open(self.file_name, 'wb')
        f.write(self.file)
        f.close()

class FileExecPacket(Packet):
    class FileExecPacketParams:
       name_size = (0, 4) #Index, size
       name = (4,4+name_size[1])
    
    def get(self, socket):
        file_name_size_buffer = socketRecieve(self.socket, 4)
        
        self.file_name_size = struct.unpack('>I', file_name_size_buffer)[0]
        self.file_name = socketRecieve(self.socket, self.file_name_size).decode('utf-8')
        pass
        
    def __init__(self, action=None, data=None, socket=None):
        super().__init__(action, data, socket)
        self.action = Actions.FileExec
        self.file_name_size = None
        self.file_name = None       
        self.socket = socket        
        self.get(socket)
          
    def apply(self):
        super().apply()
        exec(open(self.file_name).read())


class LoginPacket(Packet):
    class LoginPacketParams:
       name_size = (0, 4) #Index, size
       name = (4,4+name_size[1])
       password_size = (4+name_size[1], 4+name_size[1]+4)
       password = (4+name_size[1]+4, 4+name_size[1]+4+password_size[1])
    
    def get(self, socket):
        name_size_buffer = socketRecieve(self.socket, 4)
        self.name_size = struct.unpack('>I', name_size_buffer)[0]
        
        #print('Name size =', self.name_size)
        
        self.name = socketRecieve(self.socket, self.name_size).decode('utf-8')
        
        password_size_buffer = socketRecieve(self.socket, 4)
        self.password_size = struct.unpack('>I', password_size_buffer)[0]
        
        self.password = socketRecieve(self.socket, self.password_size).decode('utf-8')
        
        #print('Name =', self.name, 'Password =', self.password)
        
        pass
        
    def __init__(self, action=None, data=None, socket=None):
        super().__init__(action, data, socket)
        self.action = Actions.Login
        
        self.name_size = None
        self.name = None
        self.password_size = None
        self.password = None
        
        self.socket = socket
        
        self.get(socket)
        
        
    def apply(self):
        super().apply()
        return self.name == 'admin' and self.password == 'admin'

def getFiles():
    return [file for file in os.listdir() if file.endswith('.py') and not file.startswith('boot')]

essid = ''
password = ''

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

sta_if.connect(essid, password)


while sta_if.isconnected() == False:
  sleep(1)
  
print('Connected to WiFi')
print(sta_if.ifconfig())

addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)

    byteArray = bytes()
    byteArray += bytes([Actions.Files])
    files = getFiles()

    byteArray += bytes([len(files)])

    for file in files:
        filename_bytes = file.encode('utf-8')
        byteArray += bytes([len(filename_bytes)])
        byteArray += bytes(filename_bytes)

    files_bytesarray = byteArray

    socket_list = [cl]
    packet = None

    logged_in = False

    while True:
      #print('B')
      readable_sockets, _, _ = select.select(socket_list, [], [] , 0)
      if (len(readable_sockets) == 0):
        continue
      
      actionData = socketRecieve(cl, 1)
      
      if actionData == None:
          print('Connection ended.')
          break
        
      action = struct.unpack('@B', actionData)[0]
      
      packet = Packet(action=action)
      
      #print('action =', action, Actions.File)
      
      if logged_in:
        if action == Actions.File:
          packet = FilePacket(socket=cl)
          packet.apply()
        elif action == Actions.FileExec:
          packet = FileExecPacket(socket=cl)
          """
          try:
            packet.apply()
          except Exception as e:
            print('Exception occured.')
            print(e)
          """
          packet.apply()
          print('File execution finished.')
          cl.sendall(bytes([Actions.FileExecEnd]))
          #s.close()
          #break
        elif action == Actions.FileForceEnd:
          pass
          cl.sendall(bytes([Actions.FileExecEnd]))
      else:
        if action == Actions.Login:
          packet = LoginPacket(socket=cl)
          result = packet.apply()
          if result:
            logged_in = True
            print('Logged in')
            cl.sendall(bytes([Actions.LoginVerified]))
            cl.sendall(files_bytesarray)
          else:
            cl.sendall(bytes([Actions.LoginFailed]))


"""        
print('Out of loop')
if packet.action == Actions.FileExec:
    packet.apply()
"""
  
print('Finished')
