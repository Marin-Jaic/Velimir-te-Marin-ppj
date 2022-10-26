import ulaz
import pretvorba 
import sys

pocetno_stanje, stanja, akcije = ulaz.ulaz()
trenutno_stanje = pocetno_stanje
novi_izraz = True

#retci = sys.stdin.read().splitlines()
akcije_tracker = []
current_max = 0
max_indexes = []
pocetni_index = 0

for redak in retci:
    for i in range(len(redak)):
        if(novi_izraz):
            current_max = 0
            pocetni_index = i

            for akcija in akcije:
                if akcija.stanje == trenutno_stanje:
                    akcija.automat.reset()
                    akcija.automat.epsilon_prijelaz()
                    akcije_tracker += [akcija, 0]

            novi_izraz = False

        index = 0

        for tracker in akcije_tracker:

            if tracker[1] != -1 and tracker[0].automat.prijelaz(redak[i]):
                tracker[1] += 1 

                if current_max < tracker[1]:
                    current_max = tracker[1]
                elif current_max != tracker[1]:
                    tracker[1] = -1

