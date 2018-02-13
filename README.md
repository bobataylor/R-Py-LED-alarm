# R-Py-LED-alarm
Waking up in the morning is hard. Especially when it's still dark outside.
This project started as a python alarm clock designed to gently fade in an LED strip, and slowly became an easy way to control RGB LEDs with a Rasberry Pi and the Google Assistant.

# Features
- Easy RGB LED controll
<p>All the complicated bits, like PWM and duty cycles, are abstracted away into the leds and channels classes. An experienced user can modify these to add functionality as they please, but a more basic user can controll color and brightness with a predifend set of colors, or by passing in their own RGB values (0-255).</p>

- Google Assistant integration
<p>RGB LED strips are cheap and fun, but their controllers and IR remotes are rather, well... bad. Here the controller is replaced by GPIO on a Rasberry Pi and the remote is replaced by integration with the Google Assistant. Custom commands can be added to g_socket.py and itgration is run through <a href="https://ifttt.com/">IFTTT</a>.</p>

# Issues
- Some flickering is seen in the LED strip. It is believed to be a hardware issue, but has yet to be confirmed either way.

# TO-DO
- Thread alarm functionality and Google Assistant integration to run simultainiously
