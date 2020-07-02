import time
from machine import Pin

pin_ball = Pin(21, Pin.IN)
while True:
  ball_value = pin_ball.value()
  if (ball_value == 1):
    print('The module is tilted.')
  time.sleep(0.01)
