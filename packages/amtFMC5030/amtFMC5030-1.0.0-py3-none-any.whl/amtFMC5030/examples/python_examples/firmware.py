# Import FMC5030 python library.
import amtFMC5030 as fmc
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

# Display FMC5030 firmware version.
fmc.amtFmcRfFv()