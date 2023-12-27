import sys, time
# Import FMC5030 python function.
import amtFMC5030 as fmc
import numpy as np
import warnings
warnings.filterwarnings("ignore",category=UserWarning)        


# Input Zedboard information.
ip = "169.254.92.202" # Zedboard's IP
port = 22 # Zedboard's port for SSH
username = "analog" # Zedboard's username
password = "analog" # Zedboard's password to the user


# Reset and initialize FMC5030.
# Return a reference, which denotes the connection between PC and device.
fmc.amtFmcRfReset(ip,port,username,password)

# Config Tx properties for transmission.
# reference: Connection to the device.
# rfPort: Select receiving port, A or B. Port A supports frequency from 70 MHz to 18 GHz, Port B supports frquency from 70 MHz to 6 GHz.
# frequency: Frequency in MHz.
# rate (optional): IQ rate in MSPS for both Tx and Rx. Default value: 30.72 MSPS. AD9364’s Tx and Rx share the same IQ rate. This value sets Rx rate simultaneously.
# bw (optional): Set AD9364’s internal analog filter bandwith in MHz. Default value: 18 MHz.
# txAtt (optional): AD9364’s Tx attenuation in dB. Range: 0 to -89 dB. Default value: 0 dB.
# cyclic (optional): True or false. If true, use cyclic buffer to repeatedly transmit data. If false, the buffer will be transmitted only once.
fmc.amtFmcTxConfig(rfPort="A", frequency=2400, rate=30.72, bw=18, txAtt=-10, cyclic=True)

# Create a sinusoidal waveform as txdata.
fc = 30000 # Frequency of waveform
N = 1024 # Number of data points
ts = 1 / 30000.0 # Time difference
t = np.arange(0, N * ts, ts) # Elaspe time, start from t=0
i = np.cos(2 * np.pi * t * fc) * 2 ** 14 # cos(2*pi*t*fc)*(2^14)
q = np.sin(2 * np.pi * t * fc) * 2 ** 14 # sin(2*pi*t*fc)*(2^14)
txdata = i + 1j * q # Make i as real part and q as imag part of transmitted data

# Start transmitting data.
fmc.amtFmcRfTxStart(data=txdata)

# Input "stop" to break the loop
inp = input()
while inp=="stop":
    break

# Stop transmitting.
fmc.amtFmcRfTxStop()