import RPi.GPIO as GPIO
import time

class channel:
    def __init__(self, pin, freq, duty):
        self.pin = pin
        self.frequency = freq
        self.duty_cycle = duty
        self.pwm = None

    def set_duty(self, duty):
        self.pwm.ChangeDutyCycle(duty)
        self.duty_cycle = duty

    def on(self):
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(0)
    
    def off(self):
        self.pwm.stop()

'''
This class is a container for each of the 3 leds colors.
Each color is created as its own channel object.

The single container approach is to simplify outside access to the leds by abstracting away the various color channels and making the leds appread as one object.
'''
class leds:
    def __init__(self, R, G ,B, P, freq):
        self.red   = channel(R, freq, 0.0)
        self.green = channel(G, freq, 0.0)
        self.blue  = channel(B, freq, 0.0)
        self.power = channel(P, freq, 0.0)
        self.channels = [self.red, self.green, self.blue, self.power]

        self.color = [0.0, 0.0, 0.0]
        self.brightness = 0.0

    def on(self):
        self.red.on()
        self.green.on()
        self.blue.on()
        self.power.on()

    def off(self):
        self.red.off()
        self.blue.off()
        self.green.off()
        self.power.off()

    def set_color(self, color):
        '''
        Changes the color of the leds.
        Custom colors can be set by providing color as an array of r b g values.

        Any color is the combination of the R G B channels at varying intensities. The different intensities are achieved by varying the on/off ratio of the lights, also known as the duty cycle. Duty cycles can be between 0 (always ofF) to 100 (always on).

        We determine duty cycle by taking the ratio of the given value for the channel to its max value (value/256) then multiplying by 100.
        '''
        self.color = color
        for i in range(0,3):
            if color[i] < 0.0:
                color[i] = 0.0
            elif color[i] > 100.0:
                color[i] = 100.0
            duty_cycle = (float(color[i])/255.0) * 100.0
            self.channels[i].set_duty(duty_cycle)

    def set_brightness(self, brightness):
        if brightness > 100.0:
            brightness = 100.0
        elif brightness < 0.0:
            brightness = 0.0
        self.power.set_duty(brightness)
        self.brightness = brightness

    def fade_in(self, color, brightness, speed):
        wait = 0.1
        #Determine the step size by which to change each channels duty cycle.
        #Should work regardless of current values

        #first let's get the current RGB values of the strip
        #Then lets find each channels step size 
        num_steps = (speed * 60.0 * (1.0/wait))
        step = [
                (color[0] - self.color[0])/num_steps,
                (color[1] - self.color[1])/num_steps,
                (color[2] - self.color[2])/num_steps,
                (brightness - self.brightness)/num_steps]

        #finally, set the new step color
        for i in range(0, int(num_steps)):
            step_color = [
                    self.color[0] + step[0],
                    self.color[1] + step[1],
                    self.color[2] + step[2]]
            step_brightness = self.brightness + step[3]
            self.set_color(step_color)
            self.set_brightness(step_brightness)
            #not needed if our math is good
            if color == self.color:
                break # we have reached the final color, exit this function
            time.sleep(wait)
