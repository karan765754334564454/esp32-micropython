import ubinascii
import hashlib
#import enum
import struct
import network
import socket
import select
from time import sleep
from machine import Pin, PWM

"""
pin_led_r = Pin(21, Pin.OUT)
pin_led_g = Pin(19, Pin.OUT)
pin_led_b = Pin(18, Pin.OUT)
pwm_led_r = PWM(pin_led_r)
pwm_led_g = PWM(pin_led_g)
pwm_led_b = PWM(pin_led_b)

obstacle_sensor = Pin(34, Pin.IN)
line_tracking_left = Pin(35, Pin.IN)
line_tracking_right = Pin(32, Pin.IN)

pin_motor_A = Pin(25, Pin.OUT)
pin_motor_B = Pin(26, Pin.OUT)
"""

"""
essid = 'Telstra38726F'
password = 'bgxavcfa84'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

sta_if.connect(essid, password)

while sta_if.isconnected() == False:
  sleep(1)
  
print('Connected to WiFi')
print(sta_if.ifconfig())
"""

ws_addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
ws = socket.socket()
ws.bind(ws_addr)
ws.listen(1)
print('Listening on', ws_addr)

ws_cl, ws_addr = ws.accept()
print('HTTP client connected from', ws_addr)


ws_cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
webpage_file = open('joy3.html')
response = webpage_file.read()
webpage_file.close()
ws_cl.send(response)

ws_cl.close()

"""
class Actions(enum.Enum):
    Motor = 1
"""

class WebsocketActions:
    Motor = 1

class Motor:
    def stop(self):
        self.pinA.value(0)
        self.pinB.value(0)
        self.pinEnable.duty(0)
        
    def __init__(self, pinA, pinB, pinEnable):
        self.pinA = pinA
        self.pinB = pinB
        self.pinEnable = pinEnable
        self.stop()
        
    def forward(self, duty):
        self.pinA.value(1)
        self.pinB.value(0)
        self.pinEnable.duty(duty)
        
    def backward(self, duty):
        self.pinA.value(0)
        self.pinB.value(1)
        self.pinEnable.duty(duty)

motor_left = Motor(Pin(22, Pin.OUT), Pin(23, Pin.OUT), PWM(Pin(18, Pin.OUT)))
motor_right = Motor(Pin(21, Pin.OUT), Pin(19, Pin.OUT), PWM(Pin(5, Pin.OUT)))
motor_dict = dict()
motor_dict[1] = motor_left
motor_dict[0] = motor_right    

class Speaker:
    def on(self):
        self.pin.value(1)
    
    def off(self):
        self.pin.value(0)
        
    def __init__(self, pin):
        self.pin = pin
        #self.off()
        pass

speaker = Speaker(Pin(33, Pin.OUT))

class RGBLed:
    def off(self):
        self.pinR.duty(0)
        self.pinG.duty(0)
        self.pinB.duty(0)
        
    def __init__(self, pinR, pinG, pinB):
        self.pinR = pinR
        self.pinG = pinG
        self.pinB = pinB
        self.off()
        
    def setColor(self, R, G, B):
        self.pinR.duty(R)
        self.pinG.duty(G)
        self.pinB.duty(B)
        
    def setR(self):
        self.pinR.duty(1023)
        self.pinG.duty(0)
        self.pinB.duty(0)
        
    def setG(self):
        self.pinR.duty(0)
        self.pinG.duty(1023)
        self.pinB.duty(0)
        
    def setB():
        self.pinR.duty(0)
        self.pinG.duty(0)
        self.pinB.duty(1023)


rgb_led_1 = RGBLed(PWM(Pin(25, Pin.OUT)), PWM(Pin(12, Pin.OUT)), PWM(Pin(14, Pin.OUT)))

class DigitalSensor:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        return self.pin.value()

class LineTracker(DigitalSensor):
    def __init__(self, pin):
        self.pin = pin
        super().__init__(pin)
        
linetracker_left = LineTracker(Pin(35, Pin.IN))
linetracker_right = LineTracker(Pin(34, Pin.IN))
obstacle_avoidance = DigitalSensor(Pin(32, Pin.IN))

def checkSensors():
    if obstacle_avoidance.read() == 0:
        speaker.on()
        rgb_led_1.setR()
    else:
        speaker.off()
        rgb_led_1.setG()
    pass

    

#obstacle_avoidance.read()

"""
class Packet:
    #data = None
    def __init__(self, action=None, data=None):
        self.size = 0
        self.data = data
        self.action = action
        pass#self.action = action
        
    def read(self, socket, size=0):
        print('size =', self.size)
        pass
     
    def apply(self):
        pass
"""

class MotorPacket(Packet):
    #class MotorPacketParams(enum.Enum):
    class MotorPacketParams:
       motor = (0, 1) #Index, size
       duty = (1,1)
       
    def __init__(self, action=None, data=None):
        super().__init__(action, data)
        
        self.action = WebsocketActions.Motor
        
        self.motor = None
        self.duty = None
        self.forward = False
        
        self.size = 2
        

    def read(self, socket):
        super().read(socket)
        self.motor = self.data[self.MotorPacketParams.motor[0]]
        self.duty = struct.unpack('@b', bytes([self.data[self.MotorPacketParams.duty[0]]]))[0]
        if self.duty > 0:
            self.forward = True
            
        if abs(self.duty) > 100:
            self.duty = 100
            
        self.duty = int(abs(self.duty)*1023/100.0)
        
    def apply(self):
        super().apply()
        #return
        motor = motor_dict[self.motor]
        if self.duty == 0:
            motor.stop()
        elif self.forward:
            if obstacle_avoidance.read() == 0:
                motor.stop()
                pass
            else:
                motor.forward(self.duty)
        elif not self.forward:
            motor.backward(self.duty)
        
class GPIOPacket(Packet):
    
    class GPIOPacketParams:
       motor = (0, 1) #Index, size
       duty = (1,1)
       
    def __init__(self, action=None, data=None):
        super().__init__(action, data)
        
        self.action = WebsocketActions.Motor
        
        self.motor = None
        self.duty = None
        self.forward = False
        
        self.size = 2
        

    def read(self, socket):
        super().read(socket)
        self.motor = self.data[self.MotorPacketParams.motor[0]]
        self.duty = struct.unpack('@b', bytes([self.data[self.MotorPacketParams.duty[0]]]))[0]
        if self.duty > 0:
            self.forward = True
            
        if abs(self.duty) > 100:
            self.duty = 100
            
        self.duty = int(abs(self.duty)*1023/100.0)
        
    def apply(self):
        super().apply()


class WebSocket:
    def __init__(self, address, port):
        self.port = port
        self.address = address
        s = socket.socket()
        self.socket = s
        self.conn = None
        self.data = None
        self.connected = False
        pass
    
    def send(self, data):
        data_frame_bytes = bytearray()
        data_frame_bytes.append(129)
        send_bytes = bytearray()
        send_bytes.extend(data)
        data_frame_bytes.append(len(send_bytes))
        data_frame_bytes.extend(send_bytes)
        self.conn.sendall(data_frame_bytes)
    
    def bindAndAccept(self):
        addr = socket.getaddrinfo(self.address, self.port)[0][-1]
        self.socket.bind(addr)
        self.socket.listen(1)
        self.conn = self.socket.accept()[0]
        cl_file = self.conn.makefile('rwb', 0)
        
        websocket_key = None
        while True:
          line = cl_file.readline()
          if 'Sec-WebSocket-Key' in line.decode():
            websocket_key = line.decode().split(':')[-1].strip()
          if not line or line == b'\r\n':
              break
        print('Websocket key =', websocket_key)

        websocket_key_concat = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        websocket_key_response = ubinascii.b2a_base64(hashlib.sha1(websocket_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").digest()).decode('utf-8').strip()
        #websocket_key_response = base64.b64encode(hashlib.sha1((websocket_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode('utf-8')).digest()).decode('utf-8').strip()
        websocket_handshake_response = """HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: """
        websocket_handshake_response = websocket_handshake_response + websocket_key_response + '\r\n\r\n'
        print('Websocket handshake response = ', repr(websocket_handshake_response))
        self.conn.sendall(websocket_handshake_response.encode())
        self.connected = True
        
    def parseRecievedData(self, action, data):
        print('Action =', action, ', Data =', data)
        packet = Packet(action, data)
        if action == WebsocketActions.Motor:
            packet = MotorPacket(action, data)
            packet.read(self.socket)
            print('Motor =', packet.motor, 'Duty =', packet.duty, 'Forward =', packet.forward)
            self.send('Ayyy'.encode())
        packet.apply()
        pass
    
    def recieve(self, data=None):
        if not self.connected:
            return
        
        self.data = None
        websocket_frame_data = b''
        try:
            websocket_frame_data = self.conn.recv(2)
        except:
            self.connected = False
            return
            
        if (websocket_frame_data == b''):
            print('Websocket closed')
            return
        
        while len(websocket_frame_data) < 2:
          websocket_frame_data_2 = self.conn.recv(1)
          websocket_frame_data += websocket_frame_data_2
           
        websocket_frame_data_FIN = websocket_frame_data[0] & 128
        websocket_frame_data_OPCODE = websocket_frame_data[0] & 15
        websocket_frame_data_MASK = websocket_frame_data[1] & 128
        websocket_frame_data_PAYLOADLENGTH = websocket_frame_data[1] & 127

        websocket_payload_length = 0
        websocket_payload_offset = 0
        
        if websocket_frame_data_PAYLOADLENGTH <= 125:
          websocket_payload_offset = 0
          websocket_payload_length = websocket_frame_data_PAYLOADLENGTH
          
        elif websocket_frame_data_PAYLOADLENGTH == 126:
          websocket_payload_offset = 2 
          while len(websocket_frame_data) < 2 + websocket_payload_offset:
            websocket_frame_data_2 = self.conn.recv(2 + websocket_payload_offset - len(websocket_frame_data))
            websocket_frame_data += websocket_frame_data_2
          websocket_payload_length = struct.unpack('>H', bytes(websocket_frame_data[2:2+websocket_payload_offset]))[0]
          
        elif websocket_frame_data_PAYLOADLENGTH == 127:
          exit()
          websocket_payload_offset = 4
          while len(websocket_frame_data) < 2 + websocket_payload_offset:
            websocket_frame_data_2 = self.conn.recv(2 + websocket_payload_offset - len(websocket_frame_data))
            websocket_frame_data += websocket_frame_data_2
          websocket_payload_length = struct.unpack('>Q', bytes(websocket_frame_data[2:2+websocket_payload_offset]))[0]
         
        while len(websocket_frame_data) < 2 + websocket_payload_offset + 4 + websocket_payload_length:
          websocket_frame_data_2 = self.conn.recv(2 + websocket_payload_offset + 4 + websocket_payload_length - len(websocket_frame_data))
          websocket_frame_data += websocket_frame_data_2

        websocket_frame_data_MASK =  websocket_frame_data[2 + websocket_payload_offset:2 + websocket_payload_offset +4]
        websocket_data_bytes = []

        for i in range(0, websocket_payload_length):
          websocket_data_bytes.append(websocket_frame_data[2 + websocket_payload_offset + 4 + i] ^ websocket_frame_data_MASK[i % 4])
        print('Payload length=', websocket_payload_length, 'Payload offset=', websocket_payload_offset, 'FIN=', websocket_frame_data_FIN, 'OPCODE=', websocket_frame_data_OPCODE, 'MASK=', websocket_frame_data_MASK, '\nPayload data=', websocket_data_bytes)
        
        self.data = websocket_data_bytes
        
        if websocket_frame_data_OPCODE == 0x2:
            websocket_data_bytes = bytes(websocket_data_bytes)
            action = struct.unpack('@B', bytes([websocket_data_bytes[0]]))[0]
            data = websocket_data_bytes[1:]
            self.parseRecievedData(action, data)
    
    
    
    def sendString(self):
        pass
        
    def sendBytes(self):
        pass
        
#print('A')
w = WebSocket('0.0.0.0', 8081)
w.bindAndAccept()

#print('B')
ws_socket_list = [w.conn]
while True:
    checkSensors()
    #print('C')
    ws_readable_sockets, _, _ = select.select(ws_socket_list, [], [] , 0)
    if (len(ws_readable_sockets) != 0):
        w.recieve()
    
    readable_sockets, _, _ = select.select(socket_list, [], [] , 0)
    if (len(readable_sockets) != 0):
        actionData = socketRecieve(cl, 1)
      
        if actionData == None:
            print('Connection ended.')
            break
        
        action = struct.unpack('@B', actionData)[0]
        if action == Actions.FileForceEnd:
            break
    
    #print('D')
    
  
print('Finished')
while True:
  sleep(1)

