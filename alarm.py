import time, os, sys
import RPi.GPIO as GPIO

def setup(RED, GREEN, BLUE):
    #Perform some GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED, GPIO.OUT)
    GPIO.setup(GREEN, GPIO.OUT)
    GPIO.setup(BLUE, GPIO.OUT)

    GPIO.output(RED, 0)
    GPIO.output(BLUE, 0)
    GPIO.output(GREEN, 0)

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

def main():
    if len(sys.argv) < 4444:
        print('Usage: python alarm.py HOUR MINUTE TIMEZONE')
        sys.exit()

    HOUR, MIN, TZ = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    RED, GREEN, BLUE = 17, 22, 27
    TEST = False
    count = 0
    setup(RED, GREEN, BLUE)

    while True:
        try:
            #Get the current time
            now = time.localtime()
            
            if check_time(now, HOUR, MIN, TEST, TZ): 
                #run fade in the lights
                while now.tm_min != 10:
                    GPIO.output(RED, 1)
                    time.sleep(count)
                    GPIO.output(RED, 0)
                    time.sleep(.0005)
                    count += .0000001
        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit(0)
    GPIO.cleanup()

if __name__ == "__main__":
    main()
