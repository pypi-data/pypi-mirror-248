import sys, time, getopt
import amtFMC5030 as fmc
# Import FMC5030 python function.
# import amtFMC as fmc
from threading import Thread, Event
import queue
import numpy as np
from numpy.fft import fft, fftfreq, fftshift
from scipy import signal
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore",category=UserWarning)     

# Use threading to transceive data.
    
def transmit(data=[]):
    # Set global variable 'stop_threads' to stop all threads.
    global stop_threads
    # Config Tx properties for transmission.
    fmc.amtFmcTxConfig(rfPort="A", frequency=2400, rate=30.72, bw=18, txAtt=0, cyclic=True)
    # Start transmitting data.
    fmc.amtFmcRfTxStart(data)
    while True:
        time.sleep(1)
        if stop_threads:
            # Stop transmitting if stop_threads=True.
            fmc.amtFmcRfTxStop()
            break
    
    
def receive(q, cont):
    # Set global variable 'stop_threads' to stop threads.
    global stop_threads
    # Config Rx properties for receiving.
    fmc.amtFmcRxConfig(rfPort="A", frequency=2400, rate=30.72, bw=18, numOfSamples=16384, rxAAtt=0, rxGain=10)
    # Receive one section of data.
    # Currently FMC5030 Rx doesn’t support cyclic buffer. There are data gaps between each section of receiving data.
    rx = fmc.amtFmcRfRxRead()
    # Convert data type to complex
    data = []
    for ii in range (len(rx[0])):
        data.append(rx[0][ii]+1j*rx[1][ii])
    # Put collected data in queue.
    q.put(data)
    # Receive data one time if cont==False.
    while cont:
        if stop_threads:
            # Stop the threads if stop_threads=True
            q.task_done()
            break
        x = fmc.amtFmcRfRxRead()
        # Convert data type to complex
        data = []
        for ii in range (len(x[0])):
            data.append(x[0][ii]+1j*x[1][ii])
        q.put(data)
        
    
def plotrx(q):
    # Plot received data.
    global stop_threads
    # Get current IQ rate.
    sdr = reference[1]
    SampleRate = int(sdr.sample_rate)
    while True:
        # Close figure window to stop the threads.
        if stop_threads:
            plt.close()
            t0.stop()
            break
        # Get rxdata from queue.
        rx = q.get()
        # Calculate spectrum with hamming window.
        N = len(rx)
        w = signal.windows.hamming(N)
        P = np.multiply(rx,w)
        P = abs(fft(P))/N
        # Convert amplitude unit to dBFs, 2047 is fullscale of 12-bit ADC.
        spec_db = 20*np.log10(P/2047+1e-19)
        fr = fftfreq(N, 1/SampleRate)
        plt.clf()
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Magnitude [dBFs]")
        plt.plot(fftshift(fr), fftshift(spec_db))
        plt.show(block=False)
        plt.pause(0.01)
        if not plt.fignum_exists(1):
            t0.stop()
            stop_threads = True
            break
    

class DummyThread(Thread):
# Create event to stop Threads.
    def __init__(self, event: Event):
        Thread.__init__(self)
        self.stop_event = event

    def run(self):
        # Monitoring the event in the Main Thread
        while not self.stop_event.is_set():  
            time.sleep(1)
        print("Waiting for background thread to finish")
        
    def stop(self):
        global stop_threads
        # Stop the thread
        stop_threads = True
        self.stop_event.set()
        plt.close()


if __name__ == "__main__": 
    # Main thread
    # Set stop_threads as flag to synchornize the stop of all threads.
    global stop_threads
    stop_threads = False

    # Input Zedboard information.
    ip = "169.254.92.202" # Zedboard's IP
    port = 22 # Zedboard's port for SSH
    username = "analog" # Zedboard's username
    password = "analog" # Zedboard's password to the user
    # Reset and initialize FMC5030.
    # Return a reference, which denotes the connection between PC and device.
    reference = fmc.amtFmcRfReset(ip,port,username,password)

    # Create a sinusoidal waveform.
    fc = 30000 # frequency of waveform
    N = 1024 # number of data points
    ts = 1 / 30000.0 # time difference
    t = np.arange(0, N * ts, ts) # elaspe time, start from t=0
    i = np.cos(2 * np.pi * t * fc) * 2 ** 15 # cos(2*pi*t*fc)*(2^14)
    q = np.sin(2 * np.pi * t * fc) * 2 ** 15 # sin(2*pi*t*fc)*(2^14)
    txdata = i + 1j * q # make i as real part and q as imag part of txdata
    data=[]
    data.append(txdata)
    
    # Create queue for data transferation between threads.
    q = queue.Queue()
    try:
        # Create an event.
        e = Event()
        t0 = DummyThread(e)
        # Create threads for transceiving.
        t1 = Thread(target=receive,args=(q,True), daemon=True)
        t2 = Thread(target=transmit,args=(data), daemon=True)
        # Append threads to a list.
        rf_list=[]
        rf_list.append(t0)
        rf_list.append(t1)
        rf_list.append(t2)
        # Start the threads.
        for t in rf_list:
            t.start()
        # Show received data. Close the window to stop all threads.
        plotrx(q)
        plt.show(block=True)
    except KeyboardInterrupt:
        # Stop all threads if ctrl+c are pressed.
        t0.stop()
    finally:
        # Wait for all threads finish.
        for t in rf_list:
            t.join()           
            while t.is_alive():
                print("Waiting for background thread to finish")
                sleep(1)
        print("Exiting")