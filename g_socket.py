import socket
import sys
import leds


def create(port):
    #create a socket on a specified port
    HOST = ''
    PORT = port
    socket.setdefaulttimeout(10)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    
    print('Created socket on port {}'.format(port))
    return sock


def get_color(conn):
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
    return color


def main():
    if len(sys.argv) > 1:
        get_color(create(sys.argv[1]))
    else:
        print('missing port')


if __name__ == '__main__':
    main()
