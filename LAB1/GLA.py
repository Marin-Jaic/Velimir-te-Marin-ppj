import ulaz
import json

lekser = open('analizator/LA.py', 'a')
#lekser = open('analizator/analizator_v2.py', 'a')

poc_stanje, stanja, akcije = ulaz.ulaz()

lekser.write("\npocetno_stanje = {}\n".format(json.dumps(poc_stanje)))
lekser.write("stanja = {}\n".format(json.dumps(stanja)))
lekser.write("akcije = []\n")
for akcija in akcije:
    lekser.write("akcije += [Akcija({})]\n".format(akcija))

lekser.write("\nanaliza(pocetno_stanje, stanja, akcije)")

lekser.close()