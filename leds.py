import RPi.GPIO as GPIO
import time

class channel:
    def __init__(self, pin, freq, duty):
        self.pin = pin
        self.frequency = freq
        self.duty_cycle = duty

        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        self.pwm = GPIO.PWM(pin, freq)
        self.pwm.start(0)

    def set_duty(self, duty):
        self.pwm.ChangeDutyCycle(duty)
        self.duty_cycle = duty


'''
This class is a container for each of the 3 leds colors.
Each color is created as its own channel object.

The single container approach is to simplify outside access to the leds by abstracting away the various color channels and making the leds appread as one object.
'''
class leds:
    def __init__(self, R, G ,B, freq):
        self.red   = channel(R, freq, 0.0)
        self.green = channel(G, freq, 0.0)
        self.blue  = channel(B, freq, 0.0)

        self.channels = [self.red, self.green, self.blue]


    def set_color(self, color):
        '''
        Changes the color of the leds.
        Custom colors can be set by providing color as an array of r b g values.

        Any color is the combination of the R G B channels at varying intensities. The different intensities are achieved by varying the on/off ratio of the lights, also known as the duty cycle. Duty cycles can be between 0 (always ofF) to 100 (always on).

        We determine duty cycle by taking the ratio of the given value for the channel to its max value (value/256) then multiplying by 100.
        '''
        for i in range(0,3):
            if color[i] > 0:
                duty_cycle = (float(value[i])/256.0) * 100.0
            else:
                duty_cycle = 0
            self.channels[i].set_duty(duty_cycle)


    def fade_in(self, color, speed):
        #TODO change math for steps to account for wiat properly
        wait = 0.1
        #Determine the step size by which to change each channels duty cycle.
        #Should work regardless of current values

        #get the change in value (these are delta duty cycles)
        steps = []
        for i in range(0, 3):
            delta = (color[i] / 256.0 - self.channels[i].duty_cycle)
            steps.append(delta / (speed * 60.0 * wait))
        
        done = False
        while not done:
            for i in range(0, 3):
                self.channels[i].set_duty(self.channels[i].duty_cycle + steps[i])
                if self.channels[i].duty_cycle <= color[i] / 256.0:
                    done = False
            time.sleep(wait)
