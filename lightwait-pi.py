#!/usr/bin/env python3

import re
import socket
import time
import threading

from gpiozero import PWMLED

# BCM Pin numbering! "GPIO 14", "GPIO 15" and "GPIO 18" are next to each other!
RED_PORT = 18
GREEN_PORT = 15
BLUE_PORT = 14


def bytes_to_float_colors(colors):
    return [float(color) for color in colors]


def validate_color(colors):
    return all([color >= 0 and color <= 255 for color in colors])


def parse_color_code(color):
    blink = color.startswith(b'b')

    colors = re.findall(b'(?:\|?(\d+):(\d+):(\d+))', color)

    int_colors = [bytes_to_float_colors(byte_colors) for byte_colors in colors]

    if not all([validate_color(byte_color) for byte_color in int_colors]):
        print('not all valid multiple')
        return blink, None

    return blink, [[color / 255 for color in colors] for colors in int_colors]


class LightwaitPi(object):

    red_led = None
    green_led = None
    blue_led = None

    run_blinking = False

    def __init__(self, red_port, green_port, blue_port):
        self.__setup_gpio(red_port, green_port, blue_port)

    def start(self):
        thread = threading.Thread(target=self.__tcp_socket_handler)
        thread.daemon = True
        thread.start()
    
        self.__udp_socket_handler()

    def __setup_gpio(self, red_port, green_port, blue_port):
        self.red_led = PWMLED(red_port)
        self.green_led = PWMLED(green_port)    
        self.blue_led = PWMLED(blue_port)

    def __udp_socket_handler(self):
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.bind(('0.0.0.0', 3030))
        print('udp listening')

        while True:
            data = udp_sock.recv(1024)
            print('udp received')
            self.__process_data(data)

    def __tcp_socket_handler(self):
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.bind(('0.0.0.0', 3030))
        print('tcp listening')
        tcp_sock.listen(5)

        while True:
            conn, _ = tcp_sock.accept()

            data = conn.recv(1024)
            print('tcp received')
            self.__process_data(data)

    def __process_data(self, data):
        '''processes received data from the TCP or UDP connection '''
        blink, parsed_color = parse_color_code(data)

        print(blink, parsed_color)

        if blink:
            if len(parsed_color) == 1:
                parsed_color.append((0, 0, 0))
            self.__set_multi_blink(parsed_color)
            
        else:
            self.run_blinking = False
            red, green, blue = parsed_color[0]
            self.__set_color_on_gpio(red, green, blue)

    def __set_color_on_gpio(self, red, green, blue):
        '''maps range 0-255 to 0-100 '''
        self.red_led.value = red
        self.green_led.value = green
        self.blue_led.value = blue

    def __set_multi_blink(self, colors):
        self.all_colors = colors
        if self.run_blinking:
            return
        
        self.run_blinking = True

        def blinking():
            index = 0

            while self.run_blinking:
                time.sleep(0.5)
                if self.run_blinking:
                    current_color = self.all_colors[index % len(self.all_colors)]
                    self.__set_color_on_gpio(*current_color)
                    index += 1

        thread = threading.Thread(target=blinking)
        thread.start()

def main():
    l_pi = LightwaitPi(RED_PORT, GREEN_PORT, BLUE_PORT)
    l_pi.start()

if __name__ == '__main__':
    main()
