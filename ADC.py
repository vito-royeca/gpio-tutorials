from ADCDevice import *
from time import sleep

adc = ADCDevice() # Define an ADCDevice class object

def setup():
    global adc
    
    if (adc.detectI2C(0x48)): #Detect the pcf8591
        adc = PCF8591()
    elif (adc.detectI2C(0x4b)): #Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command ' i2cdetect -y 1 to check the I2C address!\n"
        "Program Exit\n")
        exit(-1)
        
def loop():
    currentValue = 0
    currentVoltage = 0.0
            
    while True:
        value = adc.analogRead(0) # Read the ADC value of channel 0
        voltage = value / 255.0 * 3.3 # Calculate the voltage value
        if (currentValue != value or currentVoltage != voltage):
            print("ADC Value: %d, Voltage: %.2f" % (value, voltage))
            currentValue = value
            currentVoltage = voltage
            sleep(0.1)
        
def destroy():
    adc.close()
    
if __name__ == "__main__": # Program entrance    
    print("Program is starting...")
    try:
        setup()
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()