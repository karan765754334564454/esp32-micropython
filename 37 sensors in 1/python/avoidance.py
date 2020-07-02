import time
from machine import Pin

pin_avoidance = Pin(21, Pin.IN)
while True: 
  avoidance_value = pin_avoidance.value()
  if (avoidance_value == 0):
    print('Obstacle detected')
  time.sleep(0.01)
