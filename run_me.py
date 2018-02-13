import alarm, leds, g_socket
from colors import colors
import RPi.GPIO as GPIO
import socket, threading, sys, time

def main():
    HOUR, MIN, TZ = 6, 45, 5
    R, G, B, P = 17, 27, 22, 7 
    PORT = 7777
    TEST = sys.argv[1]
    fade_time = 10.0
    if TEST == '1':
        fade_time = .1

    try:
        #TODO thread the alarm and the socket with the shared led_strip object
        GPIO.setmode(GPIO.BCM)
        led_strip = leds.leds(R, G, B, P, 300)
        
        while True:
            if alarm.check_time(HOUR, MIN, TZ) or TEST == '1':
                led_strip.on()
                led_strip.fade_in(colors.orange, 30.0, fade_time)
                #led_strip.set_color(colors.dark_orange, 30.0)
                time.sleep(10*60)
                les_strip.off()
            time.sleep(30)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
