import alarm, leds, socket
from colors import colors
import RPi.GPIO as GPIO
import socket, threading, sys, time


def assistant(led_strip):
    print('created thread for the Google Assistant')
    HOST = ''
    PORT = 7777
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        color = ''
        while True:
            data = conn.recv(1024)
            if not data:    break
            color += data
        conn.close()
        index = color.find("&color=")
        color = color[index+7:].lower()
        print("you said {}".format(color))
        led_strip.on()
        led_strip.set_color(color)


def alarmclock(led_strip, HOUR, MIN, TZ, TEST):
    print('Created alarm clock thread')
    while True:
        if alarm.check_time(HOUR, MIN, TZ) or TEST == '1':
            print('wake up')
            #Protect critical section section
            #Prevent led_strip object from experiencing race conditions
            led_strip.on()
            led_strip.fade_in(colors.dark_orange, fade_time)
            time.sleep(20*60)
            led_strip.off()
        time.sleep(30)


def main():
    HOUR, MIN, TZ = 6, 45, 5
    R, G, B = 17, 27, 22 
    PORT = 7777
    TEST = sys.argv[1]
    fade_time = 10.0
    if TEST == '1':
        fade_time = .1

    try:
        #TODO thread the alarm and the socket with the shared led_strip object
        GPIO.setmode(GPIO.BCM)
        led_strip = leds.leds(R, G, B, 300)
        
        tid1 = threading.Thread(target=assistant, args=[led_strip])
        tid2 = threading.Thread(target=alarmclock, args=[led_strip, HOUR, MIN, TZ, TEST])
        tid1.daemon = True
        tid2.daemon = True
        tid1.start()
        tid2.start()
        #tid1.join()
        #tid2.join()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
