# R-Py-LED-alarm
Waking up in the morning is hard. Especially when it's still dark outside.
This project started as a python alarm clock designed to gently fade in an LED strip, and slowly became an easy way to control RGB LEDs with a Rasberry Pi and the Google Assistant.

# Features
<ul>
  <li>Easy RGB LED controll</li>
  <ul><p>All the complicated bits, like PWM and duty cycles, are abstracted away into the leds and channels classes. An experienced user can modify these to add functionality as they please, but a more basic user can controll color and brightness with a predifend set of colors, or by passing in their own RGB values (0-255).</p></ul>

  <li>Google Assistant integration</li>
  <ul><p>RGB LED strips are cheap and fun, but their controllers and IR remotes are rather, well... bad. Here the controller is replaced by GPIO on a Rasberry Pi and the remote is replaced by integration with the Google Assistant. Custom commands can be added to g_socket.py and itgration is run through <a href="https://ifttt.com/">IFTTT</a>.</p></ul>
  
  <li>Customizable</li>
  <ul>New LED lighting sequences and features can be easily created using the methods provided in the leds class. There is no need to worry about threading, PWM, the various color channels, or any low level control over the leds. For example, a stobe could be implemented as follows.</ul>
</ul>
```
import leds, time, colors
R, G, B, P = 22, 27, 25, 7
led_strip = leds.(R, G, B, P, freq)
led_strip.on()
led_Strip.set_color(colors.white)
while True:
leds.set_brightness(100.0)
time.sleep(wait)
leds.set_brightness(0.0)
time.sleep(wait)
led_strip.off()
```

# Dependencies
- This repository should be used with a driving circuit to deliver power to the LEDs and not to power the LEDs directly from the Raspbery Pi. In it's simplest form the curcuit can be 4 transistors, a power supply, and the Raspberry Pi wired to the bases of the transistors.<!--An example of said curcuit can be found on my blog.-->
- This repository is designed with a common anode RGB LED strip, but the code should work with common cathode RGB LEDs as well. This only stipulation is that the driving circuit will need to be reversed.

# Issues
- Some flickering is seen in the LED strip. It is believed to be a hardware issue, but has yet to be confirmed either way.

# TO-DO
- Thread alarm functionality and Google Assistant integration to run simultainiously
