import seabreeze
# seabreeze.use('pyseabreeze')
seabreeze.use('cseabreeze')
from seabreeze.spectrometers import list_devices, Spectrometer
# spec = seabreeze.spectrometers.from_first_available()
devices = list_devices()
devices
spec = Spectrometer.from_first_available()
spec.intensities()
spec.integration_time_micros(20000)
spec.wavelengths()
