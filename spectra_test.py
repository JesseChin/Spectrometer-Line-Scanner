import RPi.GPIO as GPIO
from time import sleep
import matplotlib.pyplot as plt
import numpy as np

# Spectrometer Setup
import seabreeze
seabreeze.use('cseabreeze')
from seabreeze.spectrometers import list_devices, Spectrometer
spec = Spectrometer.from_first_available()
spec.integration_time_micros(20000)

# Constants
DIR = 37 # Board PIN 37
PUL = 35 # Board PIN 35 for PWM
SPEED = 2000 # freq of PWM to control the speed of the motor
# empirically tested range 20-10,000Hz

# Init
# GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(DIR, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(PUL, GPIO.OUT)

# The speed of the scanner is controlled through frequency, not duty cycle!
# ~20Hz is slowest speed, 10,000Hz is fastest speed (starts slipping after)
pwm = GPIO.PWM(PUL,SPEED) 
pwm.start(0)

intensities_arr = [] # to store in numpy
halted = False

def start():
    print("Moving motor to beginning")
    # Move motor backwards
    GPIO.output(DIR, GPIO.LOW)
    # GPIO.PWM(PUL,SPEED)
    pwm.ChangeDutyCycle(50)

def end():
    print("Moving motor to end")
    # Move motor forwards
    GPIO.output(DIR, GPIO.HIGH)
    # GPIO.PWM(PUL,SPEED)
    pwm.ChangeDutyCycle(50)

def halt():
    # Stop motor moving forward
    pwm.ChangeDutyCycle(0)
    halted = True

def exit_program():
    GPIO.cleanup()
    # break

def integration_process():
    ''' 
    This function doesn't exit properly until it is
    modified to work with asynchronously with asyncio.
    In current implementation, consider exiting when it hits
    the end with ctrl-c
    '''
    # i = 0
    mult_intensities = np.empty((3648,1), np.float64)
    for i in range(30):
        halt()
        integrate(i)
        # move motor forward
        # pwm.ChangeDutyCycle(50)
        end()
        sleep(1)
        # i += 1
        
def integrate_inplace():
    i = 0
    # mult_intensities = []
    mult_intensities = np.empty((3648,1), np.float64)
    for i in range(15):
        intensities, _= np.asarray(integrate(i))
        sleep(.5)
        # np.append(mult_intensities, intensities, axis=0)
        # mult_intensities.append(intensities, axis=1)
        # mult_intensities = np.vstack((mult_intensities, intensities))
        mult_intensities = np.column_stack((mult_intensities, intensities))
    mult_intensities = mult_intensities[:,1:]
    print(mult_intensities.shape)
    np.save('mult_intensities_ref', mult_intensities)

def integrate(i):
    spec.integration_time_micros(20000)
    intensities = spec.intensities()
    wavelengths = spec.wavelengths()

    fig = plt.figure();
    ax = plt.axes()
    buf = "Lettuce Spectrum 2022-11-07 Sample #%d" % i
    ax.set_title(('Spectra #%d',i))
    ax.set_xlabel('wavelength (nm)')
    ax.set_ylabel('intensities')
    ax.plot(wavelengths, intensities) 
    buf = "data/spectra%d.png" % i
    fig.savefig(buf)
    return intensities, wavelengths

print('Valid inputs: start, end, halt, integrate')
print('Because we do not have endstops yet, we need to ')
print('feed in the inputs \'start\', wait for it to reach ')
print('the origin, \'halt\' to stop it from hitting the ')
print('edge, and \'integrate\' to begin integrations. At ')
print('the end of the sequence.')
ended = False
while ended == False:
    command = input('Input: ')

    if (command == 'start'):
        print('Going to start')
        start()
    elif (command == 'end'):
        print('Going to end')
        end()
    elif (command == 'halt'):
        print('Ending')
        halt()
    elif (command == 'integrate'):
        print('Starting integration process')
        integration_process()
    elif (command == 'inplace'):
        print('Integrating without moving')
        integrate_inplace()
    elif (command == 'exit'):
        print('Exiting program')
        exit_program()
        ended = True
        # break
