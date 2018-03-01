import socket
import sys
import leds
from colors import colors


def create(port):
    #create a socket on a specified port
    HOST = ''
    PORT = port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    
    print('Created socket on port {}'.format(port))
    return sock


def get_color(conn):
    color = "WHITE"
    while True:
        try:
            #read the request and parse the color out
            data = conn.recv(1024)
            if not data: break

            index = data.find('color=')
            if index >= 0:
                color = data[index + 6 : index + 12]
        finally:
            conn.close()
    #TODO get rid of terrible swtich
    if 'red' in color:
        color = colors.red 
    elif 'orange' in color:
        color = colors.orange 
    elif 'yellow' in color:
        color = colors.yellow
    elif 'green' in color:
        color = colors.green
    elif 'blue' in color:
        color = colors.blue
    elif 'purple' in color:
        color = colors.purple
    else:
        color = colors.white

    return color


def g_listen(led_strip):
    sock = create(7777)
    sock.listen(1)

    conn, addr = sock.accept()
    color = get_color(conn)

    led_strip.set_color(color)

def main():
    if len(sys.argv) > 1:
        get_color(create(sys.argv[1]))
    else:
        print('missing port')


if __name__ == '__main__':
    main()
