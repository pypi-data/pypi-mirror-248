import sys, time, os
# Append path to the library
cwd = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cwd)
import paramiko
import adi
import numpy as np
import warnings
warnings.filterwarnings("ignore",category=UserWarning)  
import logging
        
def get_newlog():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter( '%(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    log_filename = (cwd+"/console.log")
    fh = logging.FileHandler(log_filename,mode="w")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger, ch, fh

def get_log():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter( '%(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    log_filename = (cwd+"/console.log")
    fh = logging.FileHandler(log_filename,mode="a")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger, ch, fh

M = int(1e6) 
reference = []

def init_fmc(ip, port, username, password):
    # Connect to tuner through ssh.
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username, password)
    # Initialize tuner with default value.
    try:
        stdin, stdout, stderr = client.exec_command('cd ~/Public ; ./fmc5030.sh rst')
        result = stdout.readlines()
        err = stderr.readlines()
        if result:
            logging.info(result)
        else:
            logging.info(err)
    except Exception:
        logging.info('Cannot connect to the device!')
        raise
    return client, result, err

def ctrl_fmc(cmd=""):
    # Remotely control tuner.
    # Execute ctrl_fmc() to show help for the commands.
    inp = "./fmc5030.sh "
    if cmd:
        inp += cmd
    client = reference[0]
    stdin, stdout, stderr = client.exec_command('cd ~/Public ; '+inp)
    result = stdout.readlines()
    err = stderr.readlines()
    if result:
        logging.info(result)
        return result
    else:
        logging.info(err)
        return err

def init_sdr(ip):
    # Connect to AD9364.
    sdr = adi.ad9364(uri="ip:"+ip)
    time.sleep(1)
    sdr.gain_control_mode_chan0 = "manual"
    sdr.rx_hardwaregain_chan0 = 0
    return sdr

def connect(ip):
    # Connect to FMC5030, return connection information (client).
    username = "analog"
    password = "analog"
    hostname = ip
    port = 22
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, password)
    return client
    
def send_cmd(sshob,cmd,t):
    # Send cmd when remote control with interactive shell.
    sshob.send(cmd)
    time.sleep(t)
    if sshob is not None and sshob.recv_ready():
        data = sshob.recv(9999).decode("utf8")
        while sshob.recv_ready():
            data += sshob.recv(9999).decode("utf8")
    print(data)
    return data

def amtFmcRfRef(ip="169.254.92.202",refClk="int",clkFreq=[]):
    """Set internal or external reference clock and frequency.

    Args:
        ip (str): ZedBoard’s IP. Defualt: 169.254.92.202
        refClk (str): Select internal or external reference clock. “int” to use internal reference clock and “ext” to use external reference clock. Default: int.
        clkFreq (float, optional): External reference clock frequency. Range: 10 to 100 MHz. Ignored if internal reference clock is used.
    """
    # Change reference clock.
    # Internal reference clock is 80 MHz.
    if (clkFreq!=80) & (refClk=="int"):
        if clkFreq==[]:
            clkFreq = 80
        else:
            print("Use internal refClk = "+str(clkFreq)+" MHz (y/n)?")
            yn = input()
            if yn=="y":
                ans="y\n"
                pass
            else:
                ans="n\n"
                clkFreq = 80
    # Use interactive shell.
    client = connect(ip)
    sshob = client.invoke_shell()
    # Execute with root.
    if send_cmd(sshob,"su\n",2).endswith(u"Password: "):
        send_cmd(sshob,'analog\n',2)
    send_cmd(sshob,'cd /home/analog/Public\n',2)
    inp = './amtFmcRfRef.sh '+refClk+" "+str(clkFreq)+'\r'
    if send_cmd(sshob,inp,5).endswith('\n'):
        send_cmd(sshob,ans,10)
    else:
        send_cmd(sshob,inp,10)

def amtFmcRfReset(ip="169.254.92.202", port=22, username="analog", password="analog"):
    """Reset and initialize FMC5030. Return a reference, which denotes the connection between host and device.
    The default settings are: Frequency: 9000 MHz, RxA att: 0 dB

    Args:
        ip (str): ZedBoard’s IP. Defualt: 169.254.92.202
        port (int): Zedboard’s port for SSH. Defualt: 22
        username (str): Zedboard’s username. Defualt: analog 
        password (str): Zedboard’s password to the user. Defualt: analog

    Returns:
        list: The connection objects between host and device.
    """
    global reference
    logger, ch ,fh = get_newlog()
    # Initialize and reset FMC5030 to default values.
    # Connect to tuner.
    client, result, err = init_fmc(ip, port, username, password)
    # Conncect to AD9364.
    sdr = init_sdr(ip=ip)
    # Collect the connection to the device.
    reference = [client, sdr, ip, result, err]
    logger.removeHandler(ch)
    logger.removeHandler(fh)
    return reference

def amtFmcTxConfig(rfPort="A", frequency=2400, rate=30.72, bw=18, txAtt=0, cyclic=True):
    """Config Tx parameters for transmission.

    Args:
        rfPort (str, optional): Select transmission port, A or B. TxA’s frequency range is 70 MHz to 18 GHz, TxB is 70 MHz to 6 GHz. Default: A.
        frequency (int, optional): Frequency in MHz. Default: 2400 MHz.
        rate (float, optional): IQ rate in MSPS Default: 30.72 MSPS.
        bw (int, optional): Set AD9364’s internal analog filter bandwith in MHz. Default: 18 MHz.
        txAtt (int, optional): AD9364’s Tx attenuation in dB. Range: 0 to -89 dB. Default: 0 dB.
        cyclic (bool, optional): True or false. If true, the data in buffer will be transmitted repeatedly. If false, the data in buffer will be transmitted only once. Default: True.
    """
    logger, ch, fh = get_log()
    # Config Tx properties for transmission.
    # Connect to device.
    sdr = reference[1]
    # Set value to "1" to use FDD mode.
    sdr._ctrl.debug_attrs['adi,frequency-division-duplex-mode-enable'].value = '1'
    sdr.tx_enabled_channels = [0]
    # Set frequency deviation and scale.
    sdr.dds_frequencies = "0" # interger, frequency of DDS in Hz.
    sdr.dds_scales = [1] # float, scale of DDS ranges 0 to 1.
    # Set transmit chain.
    # Set rfPort: Select transmission port, A or B.
    # Port A supports frequency from 70 MHz to 18 GHz, Port B supports frquency from 70 MHz to 6 GHz.
    if rfPort=="A" or (frequency > 6000*M):
        sdr._ctrl.find_channel("voltage0",True).attrs['rf_port_select'].value = "A"
    else:
        sdr._ctrl.find_channel("voltage0",True).attrs['rf_port_select'].value = "A"
    # Set frequency: Frequency in MHz.
    cmd = "freq T "+str(frequency)
    ctrl_fmc(cmd)
    # Set rate: IQ rate in MSPS for both Tx and Rx.
    sdr.sample_rate = rate*M
    # Set bw: AD9364’s internal analog filter bandwith in MHz.
    sdr.tx_rf_bandwidth = bw*M
    # Use cyclic buffer to repeatedly transmit data.
    sdr.tx_cyclic_buffer = cyclic
    # Set gain control mode: fast_attack/slow_attack/manual.
    sdr.gain_control_mode_chan0 = "manual"
    # Set AD9364’s Tx attenuation in dB, range:0 to -89 dB.
    sdr.tx_hardwaregain_chan0 = int(txAtt)
    logging.info("Set AD9364 Tx, rfPort="+rfPort+", rate="+str(rate)+" MSPS, bw="+str(bw)+" MHz, txAtt="+str(txAtt)+" dB, cyclic="+str(cyclic))
    logger.removeHandler(ch)
    logger.removeHandler(fh)

def amtFmcRfTxStart(data=[]):
    """Start transmitting data.

    Args:
        data (list): Transmitted data.
    """
    logger, ch, fh = get_log()
    # Start transmitting data.
    sdr = reference[1]
    # Convert data type if not complex
    if not all(isinstance(x, complex) for x in data):
        txdata = []
        for ii in data:
            txdata.append(complex(ii))
        data = txdata
    # Transmit data.
    sdr.tx(data)
    logging.info("Data transmitting... Please input \"stop\" to stop.")
    logger.removeHandler(ch)
    logger.removeHandler(fh)
        
def amtFmcRfTxStop():
    """Stop transmitting.

    Returns:
        bool: Stop signal for communication. 
    """
    logger, ch, fh = get_log()
    # Stop transmitting.
    sdr = reference[1]
    sdr.tx_destroy_buffer()
    stop_transmit = True
    logging.info("Transmission has stopped.")
    logger.removeHandler(ch)
    logger.removeHandler(fh)
    return stop_transmit
        
def amtFmcRxConfig(rfPort="A", frequency=2400, rate=30.72, bw=18, numOfSamples=16384, rxAAtt=0, rxGain=0):
    """Config Rx parameters for receiving.
    Currently FMC5030 Rx doesn’t support cyclic buffer. There are data gaps between each section of receiving data.

    Args:
        rfPort (str, optional): Select receiving port, A or B. RxA’s frequency range is 70 MHz to 18 GHz, RxB is 70 MHz to 6 GHz. Default: A.
        frequency (int, optional): Frequency in MHz. Default:2400 MHz.
        rate (float, optional): IQ rate in MSPS. Default value: 30.72 MSPS. AD9364’s Tx and Rx share the same IQ rate. This value sets Tx rate simultaneously. Default: 30.72 MSPS.
        bw (int, optional): Set AD9364’s internal analog filter bandwith in MHz. Default: 18 MHz.
        numOfSamples (int, optional):Number of IQ samples. Default: 16384.
        rxAAtt (int, optional): RxA attenuation value in dB. Range: 0 to -31 dB. Default: 0 dB.
        rxGain (int, optional): AD9364’s Rx gain in dB. Range: 0 to 70 dB. Default: 0 dB.
    """
    logger, ch, fh = get_log()
    # Config Rx properties for receiving.
    # Connect to device.
    sdr = reference[1]
    # Set value to "1" to use FDD mode.
    sdr._ctrl.debug_attrs['adi,frequency-division-duplex-mode-enable'].value = '1'
    sdr.rx_enabled_channels = [0]
    # Set receive chain.
    # Set rfPort: Select transmission port, A or B.
    # Port A supports frequency from 70 MHz to 18 GHz, Port B supports frquency from 70 MHz to 6 GHz.
    if rfPort=="A" or (frequency > 6000*M):
        sdr._ctrl.find_channel("voltage0",False).attrs['rf_port_select'].value = "A_BALANCED"
    else:
        sdr._ctrl.find_channel("voltage0",False).attrs['rf_port_select'].value = "B_BALANCED"
    # Set frequency: Frequency in MHz.
    cmd = "freq R "+str(frequency)
    # Set rate: IQ rate in MSPS for both Tx and Rx.
    sdr.sample_rate = rate*M
    # Set bw: AD9364’s internal analog filter bandwith in MHz.
    sdr.tx_rf_bandwidth = bw*M
    # Set numOfSamples: Number of IQ sample.
    sdr.rx_buffer_size = int(numOfSamples)
    # Set gain control mode: fast_attack/slow_attack/manual.
    sdr.gain_control_mode_chan0 = "manual"
    # set rxAAtt: RxA attenuation value in dB. Range: 0 to -31 dB.
    cmd += " att "+str(abs(int(rxAAtt)))
    ctrl_fmc(cmd)
    # rxAtt: AD9364’s Rx gain in dB, applicable when gain control mode is "manual". Range: 0 to 70 dB. 
    sdr.rx_hardwaregain_chan0 = int(rxGain)
    logging.info("Set AD9364 Rx, rfPort="+rfPort+", rate="+str(rate)+" MSPS, bw="+str(bw)+" MHz, numOfSamples="+str(numOfSamples)+", rxGain="+str(rxGain)+" dB")
    logger.removeHandler(ch)
    logger.removeHandler(fh)

def amtFmcRfRxRead():
    """Config Rx parameters for receiving.
    Currently FMC5030 Rx doesn’t support cyclic buffer. There are data gaps between each section of receiving data.
    
    Returns:
        list: Received data. Row 0 stores the real part, and row 1 stores the imaginary part with floating-point numbers.
    """
    # Receive one section of data.
    # Connect to device.
    sdr = reference[1]
    # Disable Rx quadrature tracking.
    phy = sdr.ctx.find_device("ad9361-phy")
    phy.reg_write(0x169,0xCC)
    # Received data.
    rxdata = sdr.rx()
    rx = [[0 for x in range(0)] for y in range(2)]
    for ii in range(len(rxdata)):
        rx[0].append(rxdata[ii].real)
        rx[1].append(rxdata[ii].imag)
    sdr.rx_destroy_buffer()
    return rx

def amtFmcRfFv():
    """Display FMC5030 firmware version.
    """
    logger, ch, fh = get_log()
    # Display FMC5030 firmware version.
    cmd = "fv"
    result = ctrl_fmc(cmd=cmd)
    