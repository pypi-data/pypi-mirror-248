import sys, time
# Import FMC5030 python function.
import amtFMC5030 as fmc
import numpy as np
from numpy.fft import fft, fftfreq, fftshift
from scipy import signal
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore",category=UserWarning)     

   
# Input Zedboard information.
ip = "169.254.92.202" # Zedboard's IP
port = 22 # Zedboard's port for SSH
username = "analog" # Zedboard's username
password = "analog" # Zedboard's password to the user


# Reset and initialize FMC5030.
# Return a reference, which denotes the connection between PC and device.
reference = fmc.amtFmcRfReset(ip,port,username,password)
time.sleep(2)
# Config Rx properties for receiving.
# reference: Connection to the device.
# rfPort: Select receiving port, A or B. Port A supports frequency from 70 MHz to 18 GHz, Port B supports frquency from 70 MHz to 6 GHz.
# frequency: Frequency in MHz.
# rate (optional): IQ rate in MSPS. Default value: 30.72 MSPS. AD9364’s Tx and Rx share the same IQ rate. This value sets Tx rate simultaneously.
# bw (optional): Bandwith in MHz. Default value: 18 MHz.
# numOfSamples (optional): Number of IQ samples. Default value: 16384.
# rxAAtt (optional): RxA attenuation value in dB.: Range: 0 to -31 dB. Default value: 0 dB.
# rxAtt (optional): AD9364’s Rx gain in dB. Range: 0 to 70 dB. Default value: 0 dB.
fmc.amtFmcRxConfig(rfPort="A", frequency=2450, rate=30.72, bw=18, numOfSamples=16384, rxAAtt=0, rxGain=20)
time.sleep(2)
# Receive one section of data.
# Currently FMC5030 Rx doesn’t support cyclic buffer. There are data gaps between each section of receiving data.
rx = fmc.amtFmcRfRxRead()

# Convert data type to complex
data = []
for ii in range (len(rx[0])):
    data.append(rx[0][ii]+1j*rx[1][ii])
 
    
# Plot data.
# Get current sample rate.
sdr = reference[1]
SampleRate = sdr.sample_rate
# Calculate spectrum with hamming window.
N = len(data)
w = signal.windows.hamming(N)
P = np.multiply(data,w)
P = abs(fft(P))/N
# Convert amplitude unit to dBFs, 2047 is fullscale of 12-bit ADC.
spec_db = 20*np.log10(P/2047+1e-19)
fr = fftfreq(N, 1/SampleRate)
plt.figure("Received Data trans")
plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude [dBFs]")
plt.plot(fftshift(fr), fftshift(spec_db))
plt.show()
