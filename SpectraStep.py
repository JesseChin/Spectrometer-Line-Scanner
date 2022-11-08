import RPi.GPIO as GPIO
from time import sleep
import matplotlib.pyplot as plt
import numpy as np

# Spectrometer Setup
import seabreeze
seabreeze.use('cseabreeze')
from seabreeze.spectrometers import list_devices, Spectrometer