#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

nettleie = float(0.4795)
wHpris = float(0.5158)
prisPerkWh = float(nettleie + wHpris)
prisPerWh = float(prisPerkWh / 1000)
fastledd = int(129)  # 100 kr fastledd nettleie + 29 kr fastledd strom
print(prisPerkWh)  # Skriv ut den totale stromprisen per kWh

print("Folgende priser er registrert: ")
print("Nettleie:", nettleie * 100, "ore")
print("kWh-pris:", wHpris * 100, "ore")
print("Fastledd:", fastledd, "kr")

valg = raw_input("Onsker du aa gjore endringer? (ja/enter for nei): ")
if(valg):
    ny_nettleie = input(
        "Nettleie er satt til 47,95 ore, skriv inn ny verdi (i ore) eller trykk enter for aa beholde: ")
    if(ny_nettleie != ""):
        nettleie = float(ny_nettleie/100)
        print("Nettleie er satt til", ny_nettleie, "ore!")
    else:
        print("Nettleie er", nettleie * 100, "ore")
    ny_kWh = input(
        "Pris per kWh er satt til 51,58 ore, skriv inn ny verdi (i ore) eller trykk enter for aa beholde: ")
    if(ny_kWh != ""):
        wHpris = float(ny_kWh/100)
        print("Ny kWh-pris er", wHpris*100, "ore!")
    else:
        print("Pris per kWh er ", wHpris * 100, " ore")
    print("Nye priser er satt! ")
    print("Nettleie: ", nettleie * 100, " ore")
    print("kWh-pris: ", wHpris * 100, " ore")
    print("Fastledd: ", fastledd, " kr")

else:
    print("Priser er ikke endret! ")
print("Maaling startet ", time.strftime("%H:%M:%S"))
# Hvilken GPIO pin som skal vaere koblet til LDR
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
# Maaleintervall i ms, 20s (20000 ms) er standard. Hoyere intervall gir hoyere presisjon.
intervall = 20000
try:
    while True:
        start_time = int(round(time.time() * 1000))
        tim = start_time
        count = 0
        while start_time + intervall >= tim:
            if rc_time(pin_to_circuit) < 5000:
                count += 1
            tim = time.time() * 1000

        blink_i_timen = count*3*60
        pris_i_timen = blink_i_timen * prisPerWh
        manedspris = (pris_i_timen*24*30+fastledd)
        for i in range(25):
            print ' '
        antall_malinger += 1
        print 'MEASURE_COUNT:', antall_malinger
        print 'PULSE_COUNT:', count
        print time.strftime("%H:%M:%S")
        print ' '
        print 'Forbruk (~20s):', blink_i_timen, 'Wh'
        print 'Realtime Timepris:', pris_i_timen, 'kr'
        print 'Realtime Dagspris:', ((fastledd/30)+pris_i_timen*24), 'kr'
        print 'Realtime Manedspris:', (manedspris), 'kr'
        sumpris += manedspris
        snittpris = sumpris/antall_malinger
        print 'Forelopig beregnet manedspris:', snittpris

except KeyboardInterrupt:
    print ' '
    print 'Antall malinger:', antall_malinger
    print ' '
    print 'Beregnet forbruk per mnd:'
    print snittpris, 'kr'
    print '(Beregnet ut ifra siste )', (antall_malinger/3), ' minuttene)'
    GPIO.cleanup()
