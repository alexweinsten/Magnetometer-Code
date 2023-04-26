import serial
import numpy as np
import time
import socket 
import pandas as pd
from datetime import datetime, timezone

x_val = []
y_val = []
z_val = []


# connect to magnetometer
#connect ethernet to serial via ip

# using the ip address to create the port connection as a socket and setting the parameters after)
mag = serial.serial_for_url("socket://192.168.1.2:1222")
mag.baudrate = 19200
mag.timeout = 1      
mag.parity = serial.PARITY_NONE
mag.xonxoff = True 

print(mag)


if mag.isOpen():
    mag.close()
mag.open()
mag.isOpen()


write_enable = bytearray('*99WE\r', 'ascii')
make_binary = bytearray('*99B\r', 'ascii')
bcmdtest = bytearray('*99C\r', 'ascii') #Sending stream command to mag
set_samplerate = bytearray('*99R = 154\r', 'ascii') #setting sample rate     

mag.write(write_enable)
time.sleep(1)
mag.write(make_binary)
time.sleep(1)
mag.write(set_samplerate)
time.sleep(1)
mag.write(bcmdtest)

header = "0d"
splitline = [4,8,12]
sentence_length = 14

def s16(value): 
    """Converts hex into signed decimal from 2's complement
    :param value: integer """
   
    return -(value & 0x8000) | (value & 0x7fff) 

total_time = 5
t_end = time.time() + total_time
while time.time() < t_end:
    buf = ''
    sentence = ''
    
    reading_sentence = False
    sentence_complete = False

    while not sentence_complete: 
        
        if len(sentence) == sentence_length - len(header): #Check if expected sentence length is reached (minus header length)
            sentence_complete = True 
           
            #Splitting the readout "sentence" based on character position (splitline)
            split_result = [sentence[i:j] for i, j in zip([0] + splitline, splitline + [None])]          
            x_raw = split_result[0]
            y_raw = split_result[1]
            z_raw = split_result[2]


        else:
            onebyte = mag.read().hex() #Reading bytes from serial port 
           
            if reading_sentence: # if start bytes found on last pass...    
                # start acculumlating the data 
                sentence += onebyte
         
            if header in onebyte: 
                
                reading_sentence = True
    
    x_mag = round(s16(int(x_raw,16))*4/60000, 7) #Changing HEX to signed decimal from 2's complement..,,
    y_mag = round(s16(int(y_raw,16))*4/60000, 7) #Then multiplying by scaling factor, and rounding.
    z_mag = round(s16(int(z_raw,16))*4/60000,7) #XYZ values are outputted from range of -30000 to 30000, must convert to -2 to 2 gauss


    x_val.append(x_mag)
    y_val.append(y_mag)
    z_val.append(z_mag)

print("done")


data = {'x': x_val, 'y': y_val, 'z': z_val}

# Create DataFrame
df = pd.DataFrame(data)

#date time to string c
current_time = datetime.now(timezone.utc).strftime('%Y_%m_%d.%H_%M_%S')

df.to_csv(current_time + "mag_file.csv", index = False)




