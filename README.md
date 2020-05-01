# lightwait-python-pi

This is a [Presenter](https://github.com/BuZZ-T/lightwait#presenter) in the [lightwait-stack](https://github.com/BuZZ-T/lightwait) using a [Raspberry Pi](https://www.raspberrypi.org/).

## Features

* Written in a few lines of python (&lt; 100)
* Listening to both UDP and TCP Port 3030 for color updates using the [lightwait-tp](https://github.com/BuZZ-T/lightwait#transmitter---presenter) communication protocol.
* Using `gpiozero` to display the received color code
* All GPIO Pins are available on every version of the Raspberry Pi, so it should be compatible with every Pi you have

## Usage

* Copy this script on a Raspberry Pi (TODO)
* Setup the script to be loaded on every start of the Pi (TODO)
* Use a [lightwait-transmitter](https://github.com/BuZZ-T/lightwait#transmitter) which is able to communicate via UDP or TCP.

Currently these lightwait-transmitters are able to do so:

* [ligthwait-python-tcp-udp](https://github.com/BuZZ-T/lightwait-python-tcp-udp)

For testing purposes, you can also use these commands when using bash:

```bash
# for udp
echo -n "0:255:0" > /dev/udp/localhost/3030 
echo -n "b255:255:0" > /dev/udp/localhost/3030
echo -n "b255:255:0|255:0:0" > /dev/udp/localhost/3030

#for tcp
echo -n "0:255:0" > /dev/tcp/localhost/3030 
echo -n "b255:255:0" > /dev/tcp/localhost/3030
echo -n "b255:255:0|255:0:0" > /dev/tcp/localhost/3030
```
## Pinout

| RGB Color | GPIO
|-|-
Red | TODO
Green | TODO
Blue | TODO

## Tested on

| Hardware | OS | python | Result
|-|-|-|-
Raspberry Pi 4 | raspbian | 3.5.x | ?

TODO