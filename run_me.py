import alarm, leds, g_socket
from colors import colors
import RPi.GPIO as GPIO
import socket, threading

def main():
    HOUR, MIN, TZ = 6, 50, 5
    R, G, B = 17, 27, 22
    PORT = 7777

    try:
        #TODO thread the alarm and the socket with the shared led_strip object
        GPIO.setmode(GPIO.BCM)
        led_strip = leds.leds(R, G, B, 300)
        
        while True:
            if alarm.check_time(HOUR, MIN, TZ):
                led_strip.fade_in(colors.orange, 10)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
