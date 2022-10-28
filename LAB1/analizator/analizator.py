from turtle import update
from automat_akcija import *
import sys

def analiza(pocetno_stanje, stanja, akcije):
    trenutno_stanje = pocetno_stanje
    novi_izraz = True

    #retci = sys.stdin.read().splitlines()
    akcije_tracker = []
    updated_akcije_tracker = []

    current_max = 0 #vjerojatno bespotreban
    finalna_akcija = None
    redak_counter = 0

    #Velimir dodatak da bi bilo pokretno

    #retci = sys.stdin.read().split("\n")

    file_object = open('test/input2.txt', 'r')
    retci = file_object.read().split("\n")
    file_object.close()

    for redak in retci:
        redak_counter += 1
        novi_redak = False
        pocetni_index = 0
        i = 0

        while(i < len(redak)):

            if(novi_izraz): #PRIPREMA ZA OBRADU NOVOG NIZA
                akcije_tracker = [] #resettamo tracker
                current_max = 0
                pocetni_index = i
                finalna_akcija = None

                for akcija in akcije:
                    if akcija.stanje == trenutno_stanje:
                        akcija.automat.reset()
                        akcija.automat.epsilon_prijelaz()
                        akcije_tracker += [[akcija, 0]]

                novi_izraz = False

            index = 0
            max_updated = False
            

            for tracker in akcije_tracker:  #Parsiranje niza kroz sve moguće automate

                if tracker[0].automat.prijelaz(redak[i]):   #postoji li prijelaz za akciju s trenutnim znakom
                    tracker[1] += 1 
                    updated_akcije_tracker.append(tracker)

                    # if current_max < tracker[1]:
                    #     current_max = tracker[1]
                    #     updated_akcije_tracker.append(tracker)
                    #     max_updated = True
                    # elif max_updated and current_max == tracker[1]:
                    #     updated_akcije_tracker.append(tracker)

                #iz elif u if
                if tracker[0].automat.izraz_prihvacen and current_max < tracker[1] or tracker[0].automat.izraz_prihvacen and current_max == tracker[1] and int(finalna_akcija.id) > int(tracker[0].id): 
                    finalna_akcija = tracker[0] #ne postoji, provjeravamo je li niz prihvacen na zadnjem znaku i je li njegova duljina duza od najvece zabiljezene
                    current_max = tracker[1]
            
            if not len(updated_akcije_tracker) and current_max != i - pocetni_index:
                #nema prijelaza i ne postoji definirana finalna akcija -> greske
                print(redak[pocetni_index], file = sys.stderr)
                i = pocetni_index + 1
                novi_izraz = True

            
            elif not len(updated_akcije_tracker) and finalna_akcija is not None: #Nema vise mogucih prijelaza, nece biti daljnje finalne akcije, drugi uvjet je testan
                if int(finalna_akcija.vrati_se):
                    i = pocetni_index + int(finalna_akcija.vrati_se)
                
                if finalna_akcija.udji_u_stanje is not None:
                    trenutno_stanje = finalna_akcija.udji_u_stanje

                if finalna_akcija.lex != "":
                    gas = 0
                    #OBRADA LEKSICKE JEDINKE I ZAPIS MOZDA IDFK MORAM JOS RAZRADIT
                    print(finalna_akcija.lex + " " + str(redak_counter) + " " + redak[pocetni_index:i])

                if finalna_akcija.novi_redak:
                    novi_redak = True
                
                novi_izraz = True

            else:   #ima prijelaza u akcijama spremljenima u updated_ackije_tracker, prenosimo ih u akcije_tracker
                i += 1
                #print(updated_akcije_tracker, finalna_akcija)
                akcije_tracker = updated_akcije_tracker[:]
                updated_akcije_tracker = []
        
        if novi_redak:
            continue




pocetno_stanje = "S_pocetno"
stanja = ["S_pocetno", "S_komentar", "S_unarni"]
akcije = []

akcije += [Akcija("S_pocetno", "#\\|", "", False, "S_komentar", 0, Automat({2: {"#": [3]}, 0: {"$": [2]}, 4: {"|": [5]}, 3: {"$": [4]}, 5: {"$": [1]}}), 0, 1)]


analiza(pocetno_stanje, stanja, akcije)