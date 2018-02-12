#processes are ending and taking the main process with them
import time, os, sys 
import RPi.GPIO as GPIO
from leds import leds


#RGB color values
#TODO change values
COLORS = {
    'RED'    : [255.0, 0.0,   0.0], 
    'ORANGE' : [255.0, 10.0, 0.0],
    'YELLOW' : [100.0, 100.0, 0.0],
    'GREEN'  : [0.0,   255.0, 0.0],
    'BLUE'   : [0.0,   0.0,   255.0],
    'PURPLE' : [255.0, 0.0,   255.0]
}


def check_time(HOUR, MIN, TZ):
    now = time.localtime()
    hour = now.tm_hour - TZ
    mint = now.tm_min
    wday = now.tm_wday

    return (hour == HOUR and mint == MIN and wday !=5 and wday !=6)


def main():
    if len(sys.argv) < 4:
        print('Usage: python alarm.py HOUR MINUTE TIMEZONE')
        print('HOUR = The hour you want to set the alarm at: 0 - 23')
        print('MINUTE = The minute you want to set the alarm at: 0 -59')
        print('TIMEZONE = Your local timezone\'s difference from UTC in hours.')
        sys.exit()

    HOUR, MIN, TZ = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    RED, GREEN, BLUE = 17, 27, 22
    TEST = True
    
    try:
        GPIO.setmode(GPIO.BCM)
        light = leds(RED, GREEN, BLUE, 300)
        while True:
            #Get the current time
            if check_time(HOUR, MIN, TZ) or TEST: 
                #run fade in the lights
                start_time = time.time()
                light.fade_in(COLORS['ORANGE'], 10.0)
    except KeyboardInterrupt:
        pass
    #finally:
    #    GPIO.cleanup()
    #    sys.exit(0)

if __name__ == "__main__":
    main()
