import time, os, sys
import RPi.GPIO as GPIO

def setup(RED, GREEN, BLUE):
    #Perform some GPIO setup
    GPIO.setmode(GPIO.BCM)
    pins = [RED, GREEN, BLUE]
    GPIO.setup(pins, GPIO.OUT, initial=GPIO.LOW)

def fade_in(red_value, green_value, blue_value, speed, max_brightness):
    #This method is meant to always start from the off state
    #The speeds at which to change in each channel
    red_speed   = speed / red_value 
    green_speed = speed / blue_value
    blue_speed  = speed / green_value
    
    #Code for changing red channel
    #TODO thread for each channel
    #TODO create PWM objects for each channel
    for x in range(0,red_value):
        RED.ChangeDutyCycle(x)
        time.sleep(red_speed)

def check_time(now, HOUR, MIN, TEST, TZ):
    hour = now.tm_hour - TZ
    mint = now.tm_min
    wday = now.tm_wday

    return (hour == HOUR and mint == MIN and wday !=5 and wday !=6) or TEST

#TODO edit this code to reflect our naming conventions
def color_test(channel, frequency, speed, step):
    p = GPIO.PWM(channel, frequency)
    p.start(0)
    while True:
        for dutyCycle in range(0, 101, step):
            p.ChangeDutyCycle(dutyCycle)
            time.sleep(speed)
            for dutyCycle in range(100, -1, -step):
            p.ChangeDutyCycle(dutyCycle)
            time.sleep(speed)
                                                                              
                                                                                              
def color_test_thread():
    threads = []
    threads.append(threading.Thread(target=color_test, args=(R, 300, 0.02, 5)))
    threads.append(threading.Thread(target=color_test, args=(G, 300, 0.035, 5)))
    threads.append(threading.Thread(target=color_test, args=(B, 300, 0.045, 5)))
    for t in threads:
        t.daemon = True
        t.start()
        for t in threads:
            t.join()


def main():
    if len(sys.argv) < 4:
        print('Usage: python alarm.py HOUR MINUTE TIMEZONE')
        sys.exit()

    HOUR, MIN, TZ = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    RED, GREEN, BLUE = 17, 22, 27
    TEST = False
    count = 0

    try:
        setup(RED, GREEN, BLUE)
        while True:
            #Get the current time
            now = time.localtime()
            
            if check_time(now, HOUR, MIN, TEST, TZ): 
                #run fade in the lights
                #fade_in(color)
                start_time = time.time()
                #Leave the lights on for 20 minutes
                while time.time() - start_time < 20*60:
                    GPIO.output(RED, 1)
                    time.sleep(count)
                    GPIO.output(RED, 0)
                    time.sleep(.0005)
                    count += .0000001
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        sys.exit(0)

if __name__ == "__main__":
    main()
