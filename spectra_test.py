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
DIR = 37 # Board Pin 37 for Direction control
PUL = 35 # Board Pin 35 for PWM
ENA = 33 # Board Pin 33 for Enable pin - used to turn motor on and off
END1 = 31 # Board Pin 31 for button 1
SPEED = 2000 # freq of PWM to control the speed of the motor
# empirically tested range 20-10,000Hz

# Init
# GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(DIR, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(END1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# The speed of the scanner is controlled through frequency, not duty cycle!
# ~20Hz is slowest speed, 10,000Hz is fastest speed (starts slipping after)
pwm = GPIO.PWM(PUL,SPEED) 
pwm.start(0)

intensities_arr = [] # to store in numpy
halted = False

start_reached = False
end_reached = False

def backward():
    print("Moving motor to beginning")
    # Move motor backwards
    enable()
    GPIO.output(DIR, GPIO.LOW)
    pwm.start(50)

def forward():
    print("Moving motor to forward")
    # Move motor forwards
    enable()
    GPIO.output(DIR, GPIO.HIGH)
    pwm.start(50)

def enable():
    GPIO.output(ENA, GPIO.LOW)
    
def disable():
    GPIO.output(ENA, GPIO.HIGH)

def endstop1_callback(END1):
    print("Endstop 1 reached")
    halt()
    start_reached = True

def halt():
    print("Halted")
    # Stop motor moving forward
    disable()
    pwm.ChangeDutyCycle(0)
    halted = True
    pwm.stop()

def exit_program():
    pwm.stop()
    GPIO.cleanup()

def integration_process(wait_time=1):
    ''' 
    This function doesn't exit properly until it is modified to work with asynchronously with asyncio. 
    In current implementation, consider exiting when it hits the end with ctrl-c
    '''
    mult_intensities = np.empty((3648,1), np.float64)
    for i in range(30):
        halt()
        intensities, _ = np.asarray(integrate(i))
        forward()
        sleep(wait_time)
        mult_intensities = np.column_stack((mult_intensities, intensities))
    mult_intensities = mult_intensities[:,1:]
    print(mult_intensities.shape)
    # np.save('mult_intensities_ref', mult_intensities)
        
def integrate_inplace():
    i = 0
    mult_intensities = np.empty((3648,1), np.float64)
    for i in range(15):
        intensities, _= np.asarray(integrate(i))
        sleep(.5)
        mult_intensities = np.column_stack((mult_intensities, intensities))
    mult_intensities = mult_intensities[:,1:]
    print(mult_intensities.shape)
    # np.save('mult_intensities_ref2', mult_intensities)

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

def graph_spectrum(fname, intensities, wavelengths):
    fig = plt.figure();
    ax = plt.axes()
    buf = "Lettuce Spectrum 2022-11-07 Sample #%d" % i
    ax.set_title(('Spectra #%d',i))
    ax.set_xlabel('wavelength (nm)')
    ax.set_ylabel('intensities')
    ax.plot(wavelengths, intensities) 
    buf = "data/spectra%d.png" % i
    fig.savefig(buf)

def change_speed(speed=2000):
    print('Changing speed to', speed)
    pwm.ChangeFrequency(speed)

print(''' Valid inputs: backward, forward, halt, integrate, enable, disable 
Because we do not have endstops yet, we need to feed in the inputs \'backward\', wait 
for it to reach the origin, \'halt\' to stop it from hitting the edge, and \'integrate\' 
to begin integrations. At the end of the sequence.
''') 
print('Make sure you run enable before running the program')


GPIO.add_event_detect(END1, GPIO.RISING, callback=endstop1_callback, bouncetime=100)

ended = False
while ended == False:
    command = input('Input: ')

    if (command == 'backward'):
        print('Going to backward')
        backward()
    elif (command == 'forward'):
        print('Going to forward')
        forward()
    elif (command == 'halt'):
        print('Ending')
        halt()
    elif (command == 'integrate'):
        print('Starting integration process')
        integration_process()
    elif (command == 'inplace'):
        print('Integrating without moving')
        integrate_inplace()
    elif (command == 'speed'):
        new_speed = int(input('New desired speed: '))
        change_speed(new_speed)
    elif (command == 'exit'):
        print('Exiting program')
        exit_program()
        ended = True