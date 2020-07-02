import time
from machine import Pin, ADC

pin_JoystickX = Pin(32, Pin.IN)
pin_JoystickY = Pin(33, Pin.IN)

ADC_JoyStickX = ADC(pin_JoystickX)
ADC_JoyStickY = ADC(pin_JoystickY)
ADC_JoyStickX.atten(ADC.ATTN_11DB)
ADC_JoyStickY.atten(ADC.ATTN_11DB)
ADC_JoyStickX.width(ADC.WIDTH_12BIT)
ADC_JoyStickY.width(ADC.WIDTH_12BIT)

pin_JoystickSwitch = Pin(22, Pin.IN)
prev_JoystickSwitch_value = pin_JoystickSwitch.value()

joystickX_deadvalue = 1810
joystickY_deadvalue = 1840

joystickX_deadzone = 100
joystickY_deadzone = 100

while True:
  clk_value = pin_CLK.value()
  ddt_value = pin_DDT.value()
  
  if prev_clk_value != clk_value:
    print('Rotation occured.')
    if clk_value != ddt_value:
      print('Clockwise rotation')
    else:
      print('Anticlockwise rotation')
      
  joystickX_value = ADC_JoyStickX.read()
  joystickY_value = ADC_JoyStickY.read()
  
  if abs(joystickX_value - joystickX_deadvalue) > joystickX_deadzone:
    if joystickX_value > joystickX_deadvalue:
      print('X moved left')
    else:
      print('X moved right')
    
  if abs(joystickY_value - joystickY_deadvalue) > joystickY_deadzone:
    if joystickY_value > joystickY_deadvalue:
      print('Y moved up')
    else:
      print('Y moved down')
      
  joystick_value = pin_JoystickSwitch.value()
  if joystick_value != prev_JoystickSwitch_value:
    print('Joystick value changed. Previous =', prev_JoystickSwitch_value, ', Current =', joystick_value)
  
  prev_JoystickSwitch_value = joystick_value
  time.sleep(0.01)

