"""Logs environmental data from a BME280 sensor into a CSV file."""


import os
import time

import board    # Pip board module
from adafruit_bme280 import basic as adafruit_bme280    # From circuitPython


# Raspberry Pi and BME280 sensor are set up to use I2C communication.
# This can be changed if you wish to use SPI instead. In my case, I2C is
# used to allow simultaneous use of a capacitive soil sensor on one Pi board.
def boardSetup():
    """Enables the reading of sensor data."""
    i2c = board.I2C()
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
    return bme280


# Uses time module instead of datetime module to prevent ambiguities in
# data collection that can occur due to the hour changing. This occurs
# during switches in Daylight Saving Time.
def getTime():
    """Returns current local time."""
    t = time.time()
    currentTime = time.strftime("%Y-%m-%d %H:%M %Z", time.localtime(t))
    return currentTime


def main():
    bme280 = boardSetup()
    temperature = round(bme280.temperature, 2)
    humidity = round(bme280.humidity, 2)
    pressure = round(bme280.pressure, 2)
    
    time = getTime()
    
    with open('enviro_log.csv', 'a') as f:
        if os.stat('enviro_log.csv').st_size == 0:  # Checks if file is empty
            f.write('Time,Temperature,Humidity,Pressure\n')
        f.write(str(time) + ','
        + str(temperature) + ' C,'
        + str(humidity) + ' %,'
        + str(pressure) + ' hPa\n')


if __name__ == "__main__":
    main()