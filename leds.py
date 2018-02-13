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
        print(duty)
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

        self.color = [0.0, 0.0, 0.0]

    def set_color(self, color):
        '''
        Changes the color of the leds.
        Custom colors can be set by providing color as an array of r b g values.

        Any color is the combination of the R G B channels at varying intensities. The different intensities are achieved by varying the on/off ratio of the lights, also known as the duty cycle. Duty cycles can be between 0 (always ofF) to 100 (always on).

        We determine duty cycle by taking the ratio of the given value for the channel to its max value (value/256) then multiplying by 100.
        '''
        self.color = color
        for i in range(0,3):
            if color[i] > 0:
                duty_cycle = (float(color[i])/255.0) * 100.0
            else:
                duty_cycle = 0
            self.channels[i].set_duty(duty_cycle)


    def fade_in(self, color, speed):
        wait = 0.1
        #Determine the step size by which to change each channels duty cycle.
        #Should work regardless of current values

        #first let's get the current RGB values of the strip

        #now lets find each channels step size 
        num_steps = float(speed) * 60.0 * (1.0/wait)
        print('num_steps = {}'.format(num_steps))
        step = [
                (color[0] - self.color[0])/num_steps,
                (color[1] - self.color[1])/num_steps,
                (color[2] - self.color[2])/num_steps]

        #finally, set the new step color
        for i in range(0, int(num_steps)):
            step_color = [
                    self.color[0] + step[0],
                    self.color[1] + step[1],
                    self.color[2] + step[2]]
            print(step_color)
            self.set_color(step_color)
            if color == self.color:
                break # we have reached the final color, exit this function
            time.sleep(wait)
