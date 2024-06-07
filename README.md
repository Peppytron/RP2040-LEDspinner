# RP2040-LEDspinner
RPi 2040 LED virtual spinning wheel

This project is based on the Raspberry Pi Pico (RP2040). It controls a NeoPixel LED strip and uses a push button as an input. 

# Environment

The Rapsberry Pi Pico is running Circuit Python (https://circuitpython.org/board/raspberry_pi_pico). Coding and testing is done using the Mu editor (https://codewith.mu). A small LED strip can be powered off the development board, but for larger strips an external 5V supply should be used. 

# Description

The main loop consists of three functions:

- draw the marker LED at the desired position
- decay the intensity of all other LEDs
- restart the spin when the button is pressed

The marker LED is drawn on LED_POSITION. When the timer reaches LED_POSITION_PERIOD, the position of the marker is moved by one. When the position reaches the end. it wraps around back to the very beginning. As the marker is moved it is slowed down by increasing the value of LED_POSITION_PERIOD for the next update. Once the value reaches a certain threshold (LED_STOP_PERIOD) it stops moving and remains stationary. At this point the color changes. 
