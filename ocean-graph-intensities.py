import matplotlib.pyplot as plt
import seabreeze
seabreeze.use('cseabreeze')
from seabreeze.spectrometers import list_devices, Spectrometer
import numpy as np
# spec = seabreeze.spectrometers.from_first_available()
# devices = list_devices()
# devices
spec = Spectrometer.from_first_available()
spec.integration_time_micros(20000)
intensities = spec.intensities()
wavelengths = spec.wavelengths()

fig = plt.figure();
ax = plt.axes()
ax.plot(wavelengths, intensities) 
ax.set_title('Lettuce Spectrum 2022-11-07 Img 1')
ax.set_xlabel('wavelength (nm)')
ax.set_ylabel('intensities')
fig.savefig('spectra')

intensities_np = np.asarray(intensities)
wavelengths_np = np.asarray(wavelengths)

np.save('intensities', intensities)
np.save('wavelengths', wavelengths)