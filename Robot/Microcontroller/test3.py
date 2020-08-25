print('test3.py. This file loops infinitely until told to exit.')

while True:
  readable_sockets, _, _ = select.select(socket_list, [], [] , 0)
  if (len(readable_sockets) == 0):
    continue

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