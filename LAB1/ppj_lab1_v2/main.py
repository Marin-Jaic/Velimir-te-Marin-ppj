import ulaz
import pretvorba 
import sys

pocetno_stanje, stanja, akcije = ulaz.ulaz()
trenutno_stanje = pocetno_stanje
novi_izraz = True

#retci = sys.stdin.read().splitlines()
akcije_tracker = []
updated_akcije_tracker = []

current_max = 0 #vjerojatno bespotreban
pocetni_index = 0
finalna_akcija = None

for redak in retci:
    novi_redak = False
    i = 0
    while(i < len(redak)):

        if(novi_izraz): #PRIPREMA ZA OBRADU NOVOG NIZA
            current_max = 0
            pocetni_index = i

            for akcija in akcije:
                if akcija.stanje == trenutno_stanje:
                    akcija.automat.reset()
                    akcija.automat.epsilon_prijelaz()
                    akcije_tracker += [akcija, 0]

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

            elif tracker[0].automat.izraz_prihvacen and current_max < tracker[1]: #ne postoji, provjeravamo je li niz prihvacen na zadnjem znako i je li njegova duljina duza od najvece zabiljezene
                finalna_akcija = tracker[0]
                current_max = tracker[1]
            
        if not len(updated_akcije_tracker): #Nema vise mogucih prijelaza, nece biti daljnje finalne akcije
            if int(finalna_akcija.vrati_se):
                i = pocetni_index + int(finalna_akcija.vrati_se)
            
            if finalna_akcija.udji_u_stanje is not None:
                trenutno_stanje = finalna_akcija.udji_u_stanje

            if finalna_akcija.lex != "":
                gas = 0
                #OBRADA LEKSICKE JEDINKE I ZAPIS MOZDA IDFK MORAM JOS RAZRADIT

            if finalna_akcija.novi_redak:
                novi_redak = True
            
            akcije_tracker = [] #resettamo tracker
            novi_izraz = True

        else:   #ima prijelaza u akcijama spremljenima u updated_ackije_tracker, prenosimo ih u akcije_tracker
            i += 1
            akcije_tracker = updated_akcije_tracker[:]
            updated_akcije_tracker = []
    
    if novi_redak:
        continue

