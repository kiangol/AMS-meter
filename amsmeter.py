#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Sett strømpriser
nettleie = float(0.4795)
wHpris = float(0.5158)
prisPerkWh = float(nettleie + wHpris)
prisPerWh = float(prisPerkWh / 1000)
fastledd = int(129) #100 kr fastledd nettleie + 29 kr fastledd strøm
print prisPerkWh # Skriv ut den totale strømprisen per kWh

# Hvilken GPIO pin som skal være koblet til LDR
pin_to_circuit = 7

def rc_time(pin_to_circuit):
    count = 0

    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(pin_to_circuit, GPIO.IN)

    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
    return count

antall_malinger = 0
sumpris = 0
snittpris = 0
period = 20000 # Måleintervall i ms, 20000 (20s) er standard.
try:
    while True:
        start_time = int(round(time.time() * 1000))
        tim = start_time
        count = 0
        while start_time + period >= tim:
            if rc_time(pin_to_circuit) < 5000:
                count += 1
            tim = time.time() * 1000

        blink_i_timen = count*3*60
        pris_i_timen = blink_i_timen * prisPerWh
        manedspris = (pris_i_timen*24*30+fastledd)
	for i in range(25):
    	       print ' '
        antall_malinger += 1
	print 'MEASURE_COUNT:',antall_malinger
	print 'PULSE_COUNT:',count
        print time.strftime("%H:%M:%S")
	print ' '
	print 'Forbruk (~20s):',blink_i_timen,'Wh'
        print 'Realtime Timepris:',pris_i_timen,'kr'
        print 'Realtime Dagspris:',((fastledd/30)+pris_i_timen*24),'kr'
	print 'Realtime Manedspris:',(manedspris),'kr'
	sumpris += manedspris
	snittpris = sumpris/antall_malinger
	print 'Forelopig beregnet manedspris:',snittpris

except KeyboardInterrupt:
	for i in range(50):
		print ' '
	print 'Antall malinger:',antall_malinger
	print ' '
	print 'Beregnet forbruk per mnd:'
	print snittpris,'kr'
    print '(Beregnet ut ifra siste )',(antall_malinger/3),' minuttene)'
	GPIO.cleanup()
