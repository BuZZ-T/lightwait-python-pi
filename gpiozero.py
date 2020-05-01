''' 
This is a simple local mock of the Raspberry PI python module gpiozero
Make sure to not deploy this on the Raspberry Pi! :)
'''

class Pwmled(object):

    port = None
    value = 0

    def __init__(self, port):
        self.port = port
        print('Pwmled created for port %s' % port)

    def __setattr__(self, name, value):
        if name == 'value':
            print('port: %s, value set: %s' % (self.port, value))

        super().__setattr__(name, value)


def PWMLED(port):
    return Pwmled(port)
