import RPi.GPIO as GPIO
import time
from colors import colors

class channel:
    def __init__(self, pin, freq, duty):
        self.pin = pin
        self.frequency = freq
        self.duty_cycle = duty
        self.pwm = None

    def set_duty(self, duty):
        print self, duty
        self.pwm.ChangeDutyCycle(int(duty))
        self.duty_cycle = duty

    def on(self):
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(self.duty_cycle)
    
    def off(self):
        self.set_duty(0)

'''
This class is a container for each of the 3 leds colors.
Each color is created as its own channel object.

The single container approach is to simplify outside access to the leds by abstracting away the various color channels and making the leds appear as one object.
'''
class leds:
    def __init__(self, R, G ,B, freq):
        self.red   = channel(R, freq, 0)
        self.green = channel(G, freq, 0)
        self.blue  = channel(B, freq, 0)
        self.channels = [self.red, self.green, self.blue]

        self.color = [0, 0, 0]  

    def on(self):
        self.red.on()
        self.green.on()
        self.blue.on()

    def off(self):
        self.red.off()
        self.blue.off()
        self.green.off()

    def set_color(self, color):
        '''
        Changes the color of the leds.
        Custom colors can be set by providing color as an array of r b g values.

        Any color is the combination of the R G B channels at varying intensities. The different intensities are achieved by varying the on/off ratio of the lights, also known as the duty cycle. Duty cycles can be between 0 (always ofF) to 100 (always on).

        We determine duty cycle by taking the ratio of the given value for the channel to its max value (value/256) then multiplying by 100.
        '''
        if type(color) is not list:
            try:
                color = colors.dict[color]
            except:
                color = colors.white
        print(color)
        self.color = color
        for i in range(0,3):
            if color[i] < 0:
                color[i] = 0
            elif color[i] > 255:
                color[i] = 255
            print "i{} : color{} : corrected{}".format(i, color[i], colors.gamma[color[i]])
            duty_cycle = (float(colors.gamma[color[i]])/255.0) * 100.0
            self.channels[i].set_duty(duty_cycle)


    def fade_in(self, color, speed):
        wait = 0.1
        color = [colors.gamma[color[0]], colors.gamma[color[1]], colors.gamma[colors[2]]]
        #Determine the step size by which to change each channels duty cycle.
        #Should work regardless of current values

        #first let's get the current RGB values of the strip
        #Then lets find each channels step size 
        num_steps = (float(speed) * 60.0 * (1.0/wait))
        step = [
                float(color[0] - self.color[0])/num_steps,
                float(color[1] - self.color[1])/num_steps,
                float(color[2] - self.color[2])/num_steps]

        #finally, set the new step color
        for i in range(0, int(num_steps)):
            step_color = [
                    self.color[0] + step[0],
                    self.color[1] + step[1],
                    self.color[2] + step[2]]
    
            self.set_color(step_color)
           
            time.sleep(wait)
