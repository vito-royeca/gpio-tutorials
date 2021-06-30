from ADCDevice import *
from gpiozero import PWMLED
from time import sleep

adc = ADCDevice() # Define an ADCDevice class object
led = PWMLED(21)

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
    
    led.value = currentValue # Mapping to PWM duty Cycle
    print("ADC Value: %d, Voltage: %.2f" % (currentValue, currentVoltage))
            
    while True:
        value = adc.analogRead(0) # Read the ADC value of channel 0
        voltage = value / 255.0 * 3.3 # Calculate the voltage value
        if (currentValue != value or currentVoltage != voltage):
            currentValue = value
            currentVoltage = voltage
            ledValue = ((currentValue*100)/255)/100 # Mapping to PWM duty Cycle
            led.value = ledValue
            print("ADC Value: %d, LED Value: %.2f, Voltage: %.2f" % (currentValue, ledValue, currentVoltage))
            
            sleep(0.03)
        
def destroy():
    adc.close()
    
if __name__ == "__main__": # Program entrance    
    print("Program is starting...")
    try:
        setup()
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()