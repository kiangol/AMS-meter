# AMS-meter
Python program to measure electricity usage on AMS.

Included ´sensorholder.stl´ for 3D printing fits the sensor and can be mounted on the electricity meter directly. 

## Requirements
Requires: 
1. Raspberry Pi running Raspbian
2. LDR / photoresistor
3. 2.2µF capacitor

## Setup
Run with `python amsmeter.py`

You can change the pin to circuit on line 17 in amsmeter.py
Default wiring is as follows:

![Wiring](https://github.com/kiangol/AMS-meter/blob/master/images/wiring.png?raw=true)
![Mounted](https://github.com/kiangol/AMS-meter/blob/master/images/holder.jpeg?raw=true)
