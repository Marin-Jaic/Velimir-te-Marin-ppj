import ulaz
import json

lekser = open('analizator/analizator.py', 'a')

poc_stanje, stanja, akcije = ulaz.ulaz()

lekser.write("pocetno_stanje = {}\n".format(json.dumps(poc_stanje)))
lekser.write("stanja = {}\n".format(json.dumps(stanja)))
for akcija in akcije:
    lekser.write("akcije += [Akcija({})]\n".format(akcija))

lekser.close()