import alarm, leds, g_socket
from colors import colors
import RPi.GPIO as GPIO
import socket, threading, sys

def main():
    HOUR, MIN, TZ = 6, 50, 5
    R, G, B = 17, 27, 22
    PORT = 7777
    TEST = sys.argv[1]
    fade_time = 10.0
    if TEST: time = .1

    try:
        #TODO thread the alarm and the socket with the shared led_strip object
        GPIO.setmode(GPIO.BCM)
        led_strip = leds.leds(R, G, B, 300)
        
        while True:
            if alarm.check_time(HOUR, MIN, TZ) or TEST:
                led_strip.fade_in(colors.dark_orange, time)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
