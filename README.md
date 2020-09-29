# AMS-meter
Python program to measure electricity usage on AMS.

Included ´sensorholder.stl´ fits the sensor and can be mounted on the electricity meter directly. 

Requires: 
1. Raspberry Pi running Raspbian
2. LDR / photoresistor
3. 2.2µ capacitor

You can change the pin to circuit on line 17 in amsmeter.py
Default wiring is as follows:

![Wiring](https://github.com/kiangol/AMS-meter/blob/master/wiring.png?raw=true)


Run with `python amsmeter.py`
