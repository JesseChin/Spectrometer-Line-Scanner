# import libs
import RPi.GPIO as GPIO
from time import sleep

# Constants
DIR = 37 # Board PIN 37
PUL = 35 # Board PIN 35 for PWM

# Init
# GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(DIR, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(PUL, GPIO.OUT)

# The speed of the scanner is controlled through frequency, not duty cycle!
pwm = GPIO.PWM(PUL,1000)

pwm.start(0)
print("Moving Motor")
pwm.ChangeDutyCycle(50)
sleep(5)
print("Moving Motor Backwards")
GPIO.output(DIR, GPIO.LOW)
sleep(5)
print("Done")
GPIO.cleanup()