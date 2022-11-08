# Import GPIO Library
import RPi.GPIO as GPIO
# Library documentation
# https://sourceforge.net/p/raspberry-gpio-python/wiki/

# Singleton for stepper driver
# Can change the direction, speed of motors

class Stepper:
    '''

    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Stepper, cls).__new__(cls)
        return cls._instance
    '''

    @staticmethod
    def setup():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(DIR, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(PUL, GPIO.OUT)
        pwm = GPIO.PWM(PUL,1000)

        pwm.start(0)

    def __init__(self, DIR, PUL, start_pin, end_pin):
        # DIR is pin that controls the direction of the steppers
        # PUL (pulse) controls the stepper speed
        self.DIR = DIR
        self.PUL = PUL
        self.start_pin = start_pin
        self.end_pin = end_pin
        

    def __del__(self):
        # Destructor
        GPIO.cleanup()

    def backward():
        # Return to the starting position
        GPIO.wait_for_edge(start_pin, GPIO.RISING)
        GPIO.output(DIR, GPIO.HIGH)

    def forward():
        # Return to the ending position
        GPIO.wait_for_edge(end_pin, GPIO.RISING)

    def stop():
        # Stops when the endstop is hit