#processes are ending and taking the main process with them
import time, os, sys 
import RPi.GPIO as GPIO
from multiprocessing import Process

def setup(pins):
    #Perform some GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pins, GPIO.OUT, initial=GPIO.LOW)


def check_time(HOUR, MIN, TZ):
    now = time.localtime()
    hour = now.tm_hour - TZ
    mint = now.tm_min
    wday = now.tm_wday

    return (hour == HOUR and mint == MIN and wday !=5 and wday !=6)


def fade_channel(channel, value, speed):
    frequency = 200
    led = GPIO.PWM(channel, frequency)
    led.start(0)
    #start the duty cycle at 0 and go up to value
    duty = ((float(value) / 256.0) * 100.0) + 1.0
    step = float(value) / (float(speed) * 60.0)
    dutyCycle = 0
    start = time.time()
    while dutyCycle <= duty and dutyCycle <= 100:
        led.ChangeDutyCycle(dutyCycle)
        time.sleep(3)
        dutyCycle += step
    while time.time() - start <= (20*60):
        time.sleep(10)

def fade_in(pins, values, speed):
    processes = []
    for i in range(0,3):
        if values[i] > 0:
            processes.append(Process(target=fade_channel, args=(pins[i], values[i], speed)))
    for p in processes:
        p.daemon = True
        p.start()
    for p in processes:
        p.join()


def main():
    if len(sys.argv) < 4:
        print('Usage: python alarm.py HOUR MINUTE TIMEZONE')
        print('HOUR = The hour you want to set the alarm at: 0 - 23')
        print('MINUTE = The minute you want to set the alarm at: 0 -59')
        print('TIMEZONE = Your local timezone\'s difference from UTC in hours.')
        sys.exit()

    HOUR, MIN, TZ = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    RED, GREEN, BLUE = 17, 27, 22
    pins = [RED, GREEN, BLUE]
    color = [255.0, 8.0, 0.0]
    TEST = True
    count = 0
    
    try:
        setup(pins)
        while True:
            #Get the current time
            if check_time(HOUR, MIN, TZ) or TEST: 
                #run fade in the lights
                start_time = time.time()
                fade_in(pins, color, 10.0)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        sys.exit(0)

if __name__ == "__main__":
    main()
