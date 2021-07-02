from ADCDevice import *
from gpiozero import RGBLED
from time import sleep

adc = ADCDevice()

def setup():
    global adc, led

    if (adc.detectI2C(0x48)): #Detect the pcf8591
        adc = PCF8591()
    elif (adc.detectI2C(0x4b)): #Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command ' i2cdetect -y 1 to check the I2C address!\n"
        "Program Exit\n")
        exit(-1)
        
    led   = RGBLED(16, 20, 21)  # Define an RGBLED class object
        
def loop():
    currentRedValue     = 0
    currentGreenValue   = 0
    currentBlueValue    = 0
    
    print("Start")
    setLEDValues(currentRedValue, currentGreenValue, currentBlueValue)
    
    while True:
        redValue   = adc.analogRead(0) # Read the ADC value of channel 0
        greenValue = adc.analogRead(1) # Read the ADC value of channel 1
        blueValue  = adc.analogRead(2) # Read the ADC value of channel 2
        
        if (currentRedValue != redValue or currentGreenValue != greenValue or currentBlueValue != blueValue):
            currentRedValue     = redValue
            currentGreenValue   = greenValue
            currentBlueValue    = blueValue
            setLEDValues(currentRedValue, currentGreenValue, currentBlueValue)             
        sleep(0.1)

def setLEDValues(red, green, blue):
    # Calculate the voltage values
    redVoltage   = red / 255.0 * 3.3 
    greenVoltage = green / 255.0 * 3.3
    blueVoltage  = blue / 255.0 * 3.3

    # Mapping to PWM duty Cycle
    redLEDValue   = 1-red/255.0
    greenLEDValue = 1-green/255.0
    blueLEDValue  = 1-blue/255.0                             #((blue*100)/255)/100
    
    print("R ADC: %d, Value: %.2f, Voltage: %.2f" % (red, redLEDValue, redVoltage))
    print("G ADC: %d, Value: %.2f, Voltage: %.2f" % (green, greenLEDValue, greenVoltage))
    print("B ADC: %d, Value: %.2f, Voltage: %.2f" % (blue, blueLEDValue, blueVoltage))
    print("#%02x%02x%02x" % (red, green, blue))
    print("")
    
    led.color = (redLEDValue, greenLEDValue, blueLEDValue)
    
def destroy():
    adc.close()
    led.close()
    
if __name__ == "__main__": # Program entrance    
    print("Program is starting...")
    try:
        setup()
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()