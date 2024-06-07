import board
import neopixel
import time
import digitalio
import random

PURPLE = (255,0,255)
WHITE  = (255,255,255)
BLACK  = (0,0,0)

LED_STOP_COLOR            = WHITE
LED_MOVE_COLOR            = PURPLE
LED_NUM_PIXELS            = 30
LED_COLOR                 = LED_MOVE_COLOR
LED_DECAY                 = 0.6
LED_SLEEP                 = 0.01
#LED_SLOW_DOWN             = 1.02
LED_POSITION              = 0
LED_POSITION_PERIOD_RESET = 2
LED_POSITION_PERIOD       = LED_POSITION_PERIOD_RESET
LED_BRIGHTNESS            = 1
LED_STOP_PERIOD           = 15
LED_DECELERATION          = 1.02

SPINNING                  = 1

TIMER_REDRAW              = 0
TIMER_POS                 = 0

pixels = neopixel.NeoPixel(board.GP0, LED_NUM_PIXELS)
pixels.brightness = LED_BRIGHTNESS

button = digitalio.DigitalInOut(board.GP13)
button.switch_to_input(pull=digitalio.Pull.DOWN)

# INITIALIZE LED MEMORY
old_pixels = []
for i in range(LED_NUM_PIXELS):
    old_pixels.append(BLACK)

# REDRAW ENTIRE LED STRIP (EXCEPT LED_POSITION) WITH BRIGHTNESS DECAY
def redraw_strip(DECAY,old_pixels) :
    for i in range(LED_NUM_PIXELS) :
        # ONLY DECAY LEDs NOT IN CURRENT LED_POSITION
        if ( i != LED_POSITION ) :
            pixels[i] = (LED_DECAY*old_pixels[i][0],LED_DECAY*old_pixels[i][1],LED_DECAY*old_pixels[i][2])

# BRIGHT LED AT LED_POSITION WITH COLOR LED_COLOR
def draw_marker(POSITION) :
    pixels[POSITION] = LED_COLOR

while True:

    ###########################################################################
    # BUTTON PRESS EVENT
    ###########################################################################

    # IF BOTTON IS PRESSED, RESTART SPIN AND CHANGE LED COLOR TO LED_MOVE_COLOR
    if button.value :
        LED_POSITION_PERIOD = LED_POSITION_PERIOD_RESET * (0.9 + 0.2*random.random()) # RANDOMIZE STARTING PERIOD
        SPINNING = 1
        LED_COLOR = LED_MOVE_COLOR # CHANGE LED COLOR

    ###########################################################################
    # LED STRIP DRAWING
    ###########################################################################

    # LED STRIP DECAY EVERY TICK
    if (TIMER_REDRAW > 0 ) :
        redraw_strip(LED_DECAY,old_pixels)
        TIMER_REDRAW = 0
    else :
        TIMER_REDRAW += 1

    # LED POSITION INCREMENT EVERT LED_POSITION_PERIOD
    if (TIMER_POS > LED_POSITION_PERIOD ) :
        # INCREMENT LED_POSITION UNTIL IT IS TOO SLOW
        if (LED_POSITION_PERIOD < LED_STOP_PERIOD ) :
            # CHECK CURRENT POSITION AND EITHER INCREMENT OR RESET TO ZERO (WRAP AROUND)
            if LED_POSITION < (LED_NUM_PIXELS-1 ):
                LED_POSITION += 1 # ADVANCE POSITION BY ONE
            else:
                LED_POSITION  = 0 # WRAP AROUND BY RESETTING POSITION TO ZERO

            LED_POSITION_PERIOD = LED_POSITION_PERIOD * LED_DECELERATION # ADD FRICTION / SLOW DOWN

        else :
            # LED STOPPED
            LED_POSITION = LED_POSITION # HOLD POSITION
            SPINNING = 0                # UPDATE SPINNING FLAG
            LED_COLOR = LED_STOP_COLOR  # CHANGE LED COLOR TO LED_STOP_COLOR

        TIMER_POS  = 0 # RESET TIMER

    else :

        TIMER_POS += 1 # INCREMENT TIMER

    draw_marker(LED_POSITION)

    # STORE STRIP STATUS IN PIXEL MEMORY
    for i in range(LED_NUM_PIXELS) :
        old_pixels[i] = pixels[i]

