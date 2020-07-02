import time
from machine import Pin, ADC, PWM

inputPin = Pin(34, Pin.IN) #GPIO 34 is input only
pwm_LED = PWM(Pin(21, Pin.IN))
pwm_LED_duty = 512

while True:
  inputValue = inputADC.value()
  if inputValue == 1:
    print('Module is tilted.')
    pwm_LED_duty+=1
    pwm_LED.duty(pwm_LED_duty)
  time.sleep(0.01)
