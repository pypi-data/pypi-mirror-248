import amtFMC5030 as fmc
import warnings
warnings.filterwarnings("ignore",category=UserWarning)


# Zedboard's IP
ip = "169.254.92.202"
# Input “int” to use internal clock and “ext” to use external reference clock.
refClk = "int"
# clkFreq: Reference clock frequency in MHz, range: 10 to 100 MHz.
clkFreq = 0
# Note that 10 MHz reference clock is required to be a sinusoidal wave.
fmc.amtFmcRfRef(ip,refClk,clkFreq)