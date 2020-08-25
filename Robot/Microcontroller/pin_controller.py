import ubinascii
import hashlib

import struct
import network
import socket
import select
from time import sleep
from machine import Pin, PWM

#print('A')

cl_file = cl.makefile('rwb', 0)
cl.sendall(bytes([Actions.PinController]))

#print('B')

pwmMapping = dict()
pinMapping = dict()

while True:
  length = 1
  #print('C')
  recv = cl.recv(length)
  
  action = struct.unpack('@B', recv)[0]
  #print('Action =', action)
  
  if recv == b'':
      print('Socket closed.')
      break
  
  if action == Actions.FileForceEnd:
      print('Force ending execution.')
      break
  #print('1 : ', recv)
  while len(recv) < length:
    recv += cl.recv(length - len(recv))
  payload_length = struct.unpack('@B', recv)[0]
  #print('D')
  print('Payload length:', payload_length)
  #print('2 : ', recv)
  recv = cl.recv(payload_length)
  while len(recv) < payload_length:
    recv += cl.recv(payload_length - len(recv))
  
  #print('3 : ', recv)
  print('Recived from client:', recv)
  
  if recv[0] == 0xfe:
    #print('A')
    pinnum = recv[1]
    if recv[2] == 2:
      #print('B')
      #if 'pin' not in locals():
      if pinnum not in pinMapping:
        pinMapping[pinnum] = Pin(pinnum, Pin.OUT)
      #pin = Pin(pinnum, Pin.OUT)
      pin = pinMapping[pinnum]
      
      if recv[3] == 1:
        #print('C')
        pin.value(recv[4])
        print('Setting', pinnum, 'to', recv[4])
      elif recv[3] == 2:
        #print('D')
        #if 'pinpwm' not in locals():
        if pinnum not in pwmMapping:
          pwmMapping[pinnum] = PWM(pin)
          
        pinpwm = pwmMapping[pinnum]
        pinpwm.duty(int(recv[4] * (1023/100.0)))
  elif recv[0] == Actions.FileExecEnd:
      break  
  
  sleep(10/1000.0)
  continue
  
  length = len('Recieved from server:'.encode()) + len('test'.encode())
  length = 3
  recv = cl.recv(length)
  while len(recv) < length:
    recv += cl.recv(length - len(recv))
    

  recvUTF = recv.decode('UTF-8')
  print('Recived from client:', recvUTF, recv, 'END')
  """
  line = cl_file.readline()
  lineUTF = line.decode('UTF-8')
  print('Recived from client:', lineUTF)
  """

  
  if recv[0] == 0xfe:
    #print('A')
    pinnum = recv[1]
    if recv[2] == 2:
      #print('B')
      pin = Pin(pinnum, Pin.OUT)
      if recv[3] == 1:
        #print('C')
        pin.value(recv[4])
        print('Setting', pinnum, 'to', recv[4])
      elif recv[3] == 2:
        #print('D')
        pinpwm = PWM(pin)
        pinpwm.duty(recv[4])
  
  sleep(10/1000.0)