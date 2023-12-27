import sys, time, os
# Append path to the library
cwd = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cwd)
import paramiko
import adi
import numpy as np
import warnings
warnings.filterwarnings("ignore",category=UserWarning)  
M=1e6
class zed():
    """Zedboard information.
    Default:
        ip: 169.254.92.202
        port: 22
        username: analog
        password: analog
    """
    def __init__(self):
        self.ip="169.254.92.202"
        self.port=22
        self.username="analog"
        self.password="analog"
    def zed_inf(self):
        print(self.ip)
        print(self.port)
        print(self.username)
        print(self.password)
    def setzed_ip(self,ipname):
        self.ip = str(ipname)
    def setzed_port(self,value):
        self.port = value
    def setzed_username(self,name):
        self.username = str(name)
    def setzed_password(self,password):
        self.password = str(password)
inf = zed()

# control terminal
def ctrl_fmc(cmd=""):
    """Remotely control device through SSH.

    Args:
        cmd (str): Commands to the device.

    Returns:
        str: Output from the remote device.
    """
    # remotely control tuner
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(inf.ip, inf.port, inf.username, inf.password)
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.readlines()
    err = stderr.readlines()
    if result:
        print(result)
        return result
    else:
        print(err)
        return err
 
def radi_reg(reg=[],ip=""):
    """Read AD9364's register.

    Args:
        reg (int): aD9364's register address.
        ip (str, optional): Zedboard's IP. Default: 169.254.92.202.
        
    Returns:
        int: Register value in decimal form.
    """
    if ip:
        global inf
        inf.setzed_ip(ip)
    sdr = adi.ad9364(uri="ip:"+inf.ip)
    phy = sdr.ctx.find_device("ad9361-phy")
    val = phy.reg_read(reg)
    return val

def read_attr(ip=""):
    """Read attribute.

    Args:
        ip (str, optional): Zedboard's IP. Default: 169.254.92.202.
    """
    cmd = "cd /home/analog/Public ; ./fmc5030.sh inf"
    if ip:
        global inf
        inf.setzed_ip(ip)
    ctrl_fmc(cmd)
    
def debug_attr(ip=""):
    """Read debug attribute.

    Args:
        ip (str, optional): Zedboard's IP. Default: 169.254.92.202.
    """
    if ip:
        global inf
        inf.setzed_ip(ip)
    cmd = "iio_attr -u ip:"+ip+" ad9361-phy -D"
    ctrl_fmc(cmd)
    
def adi_freq(tr="TR",freq=[],ip=""):
    """Set Tx or Rx LO frequency on bypass path.

    Args:
        tr (str, optional): TR: Set both Tx and Rx. T: Set Tx, ignore Rx. R: Set Rx, ignore Tx. Default: TR.
        freq (float): Frequency in MHz. Range: 70 to 6000 MHz.
        ip (str, optional): Zedboard's IP. Default: 169.254.92.202.
    """
    if ip:
        global inf
        inf.setzed_ip(ip)
    sdr = adi.ad9364(uri="ip:"+inf.ip)
    sdr.tx_enabled_channels = [0]
    sdr.rx_enabled_channels = [0]
    if tr=="t" or tr=="T":
        sdr.tx_lo = int(freq*M)
    elif tr=="r" or tr=="R":
        sdr.rx_lo = int(freq*M)
    elif tr=="tr" or tr=="TR":
        sdr.tx_lo = int(freq*M)
        sdr.rx_lo = int(freq*M)
       
def set_dds(freq=[],scale=[],ip=""):
    """Set DDS frequency and scale.

    Args:
        freq (int): Frequencies of DDS in Hz.
        scale (float): Scale of DDS signal generators. Ranges: 0 to 1.
        ip (str, optional): Zedboard's IP. Default: 169.254.92.202.
    """
    if ip:
        global inf
        inf.setzed_ip(ip)
    sdr = adi.ad9364(uri="ip:"+inf.ip)
    sdr.dds_single_tone(freq, scale, channel=0)
    
def set_port(tr="TR",port="",ip=""):
    """Set to use port A or B.

    Args:
        tr (str, optional): TR: Set both TxA and RxA. T: Set TxA, ignore RxA. R: Set RxA, ignore TxA. Default: TR.
        port (str): Select port, A or B. TxA and RxA’s frequency range is 70 MHz to 18 GHz, TxB and RxB's is 70 MHz to 6 GHz.
        ip (str, optional): Zedboard's IP. Default: 169.254.92.202.
    """
    if ip:
        global inf
        inf.setzed_ip(ip)
    sdr = adi.ad9364(uri="ip:"+inf.ip)
    if port=="A":
        rxport="A_BALANCED"
    elif port=="B":
        rxport="B_BALANCED"
    if tr=="t" or tr=="T":
        sdr._ctrl.find_channel("voltage0",True).attrs['rf_port_select'].value = port
    elif tr=="r" or tr=="R":
        sdr._ctrl.find_channel("voltage0",False).attrs['rf_port_select'].value = rxport
    elif tr=="tr" or tr=="TR":
        sdr._ctrl.find_channel("voltage0",True).attrs['rf_port_select'].value = port
        sdr._ctrl.find_channel("voltage0",False).attrs['rf_port_select'].value = rxport
      
def adi_txAtt(val=[],ip=""):
    """Set Tx attenuation on bypass path.

    Args:
        val (int): AD9364’s Tx attenuation in dB. Range: 0 to -89 dB.
        ip (str, optional): Zedboard's IP. Default: 169.254.92.202.
    """
    if ip:
        global inf
        inf.setzed_ip(ip)
    sdr = adi.ad9364(uri="ip:"+inf.ip)
    val = -abs(val)
    sdr.gain_control_mode_chan0 = "manual"
    sdr.tx_hardwaregain_chan0 = int(val)
  
def adi_rxGain(val=[],ip=""):
    """Set Rx gain.

    Args:
        val (int): AD9364’s Rx gain in dB. Range: 0 to 70 dB.
        ip (str, optional): Zedboard's IP. Default: 169.254.92.202.
    """
    if ip:
        global inf
        inf.setzed_ip(ip)
    sdr = adi.ad9364(uri="ip:"+ip)
    sdr.gain_control_mode_chan0 = "manual"
    sdr.rx_hardwaregain_chan0 = int(abs(val))

def tuner_freq(tr="TR",freq=[],ip=""):
    """Set TxA or RxA LO frequency on convert path.

    Args:
        tr (str, optional): TR: Set both TxA and RxA. T: Set TxA, ignore RxA. R: Set RxA, ignore TxA. Default: TR.
        freq (float): Frequency in MHz. Range: 6 to 18 GHz.
        ip (str, optional): Zedboard's IP. Default: 169.254.92.202.
    """
    cmd = "cd /home/analog/Public ; ./fmc5030.sh freq "+str(tr)+" "+str(freq)
    if ip:
        global inf
        inf.setzed_ip(ip)
    ctrl_fmc(cmd)
   
def tuner_rxAtt(val=[],ip=""):
    """Set RxA attenuation on convert path.

    Args:
        val (int): RxA attenuation value in dB. Range: 0 to -31 dB.
        ip (str, optional): Zedboard's IP. Default: 169.254.92.202.
    """
    cmd = "cd /home/analog/Public ; ./fmc5030.sh att "+str(val)
    if ip:
        global inf
        inf.setzed_ip(ip)
    ctrl_fmc(cmd)
       
def path(tr="TR",path="",ip=""):
    """Set TxA or RxA to convert or bypass path.

    Args:
        tr (str, optional): TR: Set both TxA and RxA. T: Set TxA, ignore RxA. R: Set RxA, ignore TxA. Default: TR.
        path (str): con: Use convert path. pass: Use bypass path.
        ip (str, optional): Zedboard's IP. Default: 169.254.92.202.
    """
    cmd = "cd /home/analog/Public ; ./fmc5030.sh path "+str(tr)+" "+str(path)
    if ip:
        global inf
        inf.setzed_ip(ip)
    ctrl_fmc(cmd)

def sel_ref(sel="",ip=""):
    """Set internal or external reference clock.

    Args:
        sel (str): Select internal or external reference clock. “int” to use internal reference clock and “ext” to use external reference clock.
        ip (str, optional): Zedboard's IP. Default: 169.254.92.202.
    """
    if (sel == "int" or sel == "ext"):
        if sel=="int":
            val = 0
        elif sel=="ext":
            val = 1
        cmd = "cd /home/analog/Public ; ./FMCmain -r "+str(val)
        if ip:
            global inf
            inf.setzed_ip(ip)
        ctrl_fmc(cmd)