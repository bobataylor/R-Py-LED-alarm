import g_socket
import alarm
import leds
from colors import colors
import RPi.GPIO as GPIO


def main():
    HOUR, MIN, TZ = 6, 50, 5
    R, G, B = 17, 27, 22
    PORT = 7777

    try:
        GPIO.setmode(GPIO.BCM)
        led_strip = leds.leds(R, G, B, 300)
        
        #TODO put the socket in a thread
        socket = g_socket.create(PORT)
        socket.listen(1)

        while True:
            print('test')
            if alarm.check_time(HOUR, MIN, TZ):
                led_strip.fade_in(colors.orange)
            conn, addr = socket.accept()
            if conn != None:
                color = g_socket.get_color(conn)
                #TODO get rid of terrible swtich
                if 'red' in color:
                    color = 'RED' 
                elif 'orange' in color:
                    color = 'ORANGE' 
                elif 'yellow' in color:
                    color = 'YELLOW' 
                elif 'green' in color:
                    color = 'GREEN' 
                elif 'blue' in color:
                    color = 'BLUE' 
                elif 'purple' in color:
                    color = 'PURPLE'
                else:
                    color = 'WHITE'
                led_strip.set_color(colors.color)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
