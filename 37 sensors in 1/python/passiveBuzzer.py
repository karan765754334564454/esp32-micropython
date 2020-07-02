import time
from machine import Pin, ADC, PWM

#Keep buzzer duty constant (for constant volume)
#Change its PWM frequency when rotary encoder rotates
pin_PassiveBuzzer = Pin(22, Pin.OUT)
pwm_PassiveBuzzer = PWM(pin_PassiveBuzzer)

while True:
  #Set the buzzers frequency
  pwm_PassiveBuzzer.duty(int(1023/2))
  freq_PassiveBuzzer = 6000
  pwm_PassiveBuzzer.freq(freq_PassiveBuzzer)
  time.sleep(0.01)


