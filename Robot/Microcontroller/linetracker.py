from time import sleep
from machine import Pin, PWM

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

while True:
    #print('Left =', linetracker_left.read(), 'Right =', linetracker_right.read())
    
    left = linetracker_left.read()
    right = linetracker_right.read()

    
    if left == 1 and right == 0:
        print('Turning right')
        motor_left.forward(int(75 * (1023/100.0)))
        #motor_right.stop()
        motor_right.backward(int(75 * (1023/100.0)))
    elif (left == 0 and right == 1):
        print('Turning left')
        motor_right.forward(int(75 * (1023/100.0)))
        #motor_left.stop()
        motor_left.backward(int(75 * (1023/100.0)))
    elif (left == 1 and right == 1):
        print('Going forward')
        motor_right.forward(int(75 * (1023/100.0)))
        motor_left.forward(int(75 * (1023/100.0)))
    elif (left == 0 and right == 0):
        print('Stop')
        motor_right.backward(int(75 * (1023/100.0)))
        motor_left.backward(int(75 * (1023/100.0)))
        #motor_right.stop()
        #motor_left.stop()

    #sleep(1.0/1000)
    