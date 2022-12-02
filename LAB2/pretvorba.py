import ulaz
from json import dumps
import sys

class Enka:
    def __init__(self, nezavrsni_znakovi, zavrsni_znakovi, produkcije, pocetno_stanje, t_skup):
        self.nezavrsni_znakovi = nezavrsni_znakovi
        self.zavrsni_znakovi = zavrsni_znakovi
        self.produkcije = produkcije
        self.t_skup = t_skup

        # Ako se piše samo stavka onda je 0. stavka .S jer je produkcija S' -> S
        #self.stanja = {0: Stanje(0, ["<S'>"], ["$"]), 1: Stanje(1, [".", pocetno_stanje], ["$"])}

        self.stanja = {0: Stanje(1, [".", pocetno_stanje], ["$"])}

        self.prijelazi = {0: {"$": [1]}}

        self.broj_stanja = 1 #pazi ovo, bilo je 2

        self.generiraj(self.stanja[0]) # pazi i ovo
    
    def dodaj_prijelaz(self, id, znak, nova_stavka, t_crtano):
        sljedece_stanje_id = None
        novo_stanje_stvoreno = True

        for postojece_stanje in self.stanja.values():
            if nova_stavka == postojece_stanje.stavka and t_crtano == postojece_stanje.t:
                sljedece_stanje_id = postojece_stanje.id
                novo_stanje_stvoreno = False
                break

        if sljedece_stanje_id is None:
            #print(self.broj_stanja, nova_stavka, t_crtano)
            sljedece_stanje_id = self.broj_stanja
            sljedece_stanje = Stanje(sljedece_stanje_id, nova_stavka, t_crtano)

            self.stanja[sljedece_stanje_id] = sljedece_stanje

            self.broj_stanja += 1

        self.prijelazi[id][znak] += [sljedece_stanje_id]

        return novo_stanje_stvoreno

    def generiraj(self, stanje):
        index = stanje.stavka.index(".")
        
        #DOSLI SMO DO KRAJA STAVKE, VRACAMO SE
        if index + 1 == len(stanje.stavka):
            return
        
        trenutni_znak = stanje.stavka[index + 1]
        self.prijelazi[stanje.id] = {}
        #ISPRED TOCKE JE NEZAVRSNI ZNAK
        if trenutni_znak in nezavrsni_znakovi:
            #namjestimo t_skup

            t_crtano = set()

            # if index + 2 == len(stanje.stavka):
            #     t_crtano.add("$")
            # elif stanje.stavka[index + 2] in zavrsni_znakovi:
            #     t_crtano.add(trenutni_znak)
            # else:
            #     t_crtano.update(self.t_skup[stanje.stavka[index + 2]][:])

            #     for produkcija in self.produkcije[trenutni_znak]:
            #         if "$" in produkcija.ds:
            #             t_crtano.update(stanje.t)
            #             break

            i = index + 2
            dodaj_sljedeci = True

            while(i < len(stanje.stavka) and dodaj_sljedeci):
                dodaj_sljedeci = False

                if stanje.stavka[i] in zavrsni_znakovi:
                    t_crtano.add(stanje.stavka[i])
                elif i + 1 != len(stanje.stavka):
                    t_crtano.update(self.t_skup[stanje.stavka[i]][:])

                    for produkcija in self.produkcije[stanje.stavka[i]]:
                        if "$" in produkcija.ds:
                            dodaj_sljedeci = True
                            break

                i += 1
            
            if i == len(stanje.stavka) and dodaj_sljedeci:
                    t_crtano.update(stanje.t)

            
            t_crtano = list(t_crtano)
            t_crtano.sort()

            #PRVO ODRADUJEMO EPSILON PRIJELAZE
            self.prijelazi[stanje.id]["$"] = []

            for produkcija in self.produkcije[trenutni_znak]:

                nova_stavka = produkcija.ds[:]
                if "$" in nova_stavka: nova_stavka.remove("$")
                nova_stavka.insert(0, ".")

                if self.dodaj_prijelaz(stanje.id, "$", nova_stavka, t_crtano):
                    self.generiraj(self.stanja[self.broj_stanja - 1])

            #NAKON EPSILON PRIJELAZA ODRADUJEMO OBICNI PRIJELAZ
            nova_stavka = stanje.stavka[:]
            nova_stavka.remove(".")
            nova_stavka.insert(index + 1, ".")
            t_crtano = stanje.t[:]

            self.prijelazi[stanje.id][trenutni_znak] = []

            if self.dodaj_prijelaz(stanje.id, trenutni_znak, nova_stavka, t_crtano):
                self.generiraj(self.stanja[self.broj_stanja - 1])

        else:
            nova_stavka = stanje.stavka[:]
            nova_stavka.remove(".")
            nova_stavka.insert(index + 1, ".")
            t_crtano = stanje.t[:]

            self.prijelazi[stanje.id][trenutni_znak] = []

            if self.dodaj_prijelaz(stanje.id, trenutni_znak, nova_stavka, t_crtano):
                self.generiraj(self.stanja[self.broj_stanja - 1])
    
        return
    
    def __str__(self):
        output = dumps(self.prijelazi)

        for i in reversed(range(self.broj_stanja)):
            output = output.replace(str(i), "".join(self.stanja[i].stavka) + ", T(" + ",".join(self.stanja[i].t) + ")")
            #output = output.replace(str(i), "".join(self.stanja[i].stavka))
        return output
    

#mislim da je uglavnom dobro
class Stanje:
    def __init__(self, id, stavka, t):
        self.id = id
        self.stavka = stavka
        self.t = t


    
class DKAStanje:

    def __init__(self, id, set_starih_stanja, opisi_stanja):
        self.id = id

        self.stavke_skupovi = set()

        for stanje in set_starih_stanja:
            self.stavke_skupovi.add((tuple(opisi_stanja[stanje].stavka), frozenset(opisi_stanja[stanje].t)))

    def __str__(self):
        return "(" + str(self.id) + ") -> " + str(self.stavke_skupovi)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id



class Dka:
    def __init__(self, enka):
        self.broj_stanja = 0
        self.prijelazi = dict()
        self.enka_u_dka(enka)

    def eokolina(self, stanje_ul, prijelazi, bio_e):
        stanje = stanje_ul.copy()
        okolina = stanje
        bio_e += stanje
        for s in stanje:
            if s in prijelazi.keys():
                pr = prijelazi[s]
                if '$' in pr.keys():
                    for z in pr['$']:
                        if z not in bio_e:
                            okolina += self.eokolina([z], pr, bio_e + [z])
                            bio_e += [z]
        return okolina


    def dodaj_bivana_stanja(self, bio, stanje):
        for stanje in stanje:
            bio[stanje] = 1

    def grupiraj_eokoline(self, br_stanja, prijelazi):
        nova_stanja = [self.eokolina([0], prijelazi, [])]
        bio = [0 for i in range(0, br_stanja)]
        self.dodaj_bivana_stanja(bio, nova_stanja[0])

        for stanje in range(0, br_stanja):
            if bio[stanje] == 0:
                novo_stanje = self.eokolina([stanje], prijelazi, [])
                self.dodaj_bivana_stanja(bio, novo_stanje)
                nova_stanja += [novo_stanje]
        
        nova_nova_stanja = []
        for novo_stanje in nova_stanja:
            nova_nova_stanja += [frozenset(novo_stanje)]
        return nova_nova_stanja


    def stanja_koje_sadrzavaju(self, stanja, trazeno):
        ret = []
        for stanje in stanja:
            if any(item in trazeno for item in stanje):
                ret += [stanje]
        if(len(ret) > 1):
            print("ERROR - gruirano stanje ima više slijedecih stanja za ulazni znak (nije DKA nego NKA)", file=sys.stderr)
        return ret[0]


    def ekstrapoliraj_prijelaze(self, stanja, enka_prijelazi):
        prijelazi = dict()

        for grupno_stanje in stanja:
            prijelazi[grupno_stanje] = dict()
            for stanje in grupno_stanje:
                if stanje not in enka_prijelazi.keys():
                    continue
                for znak in enka_prijelazi[stanje].keys():
                    if znak == '$':
                        continue
                    prijelazi[grupno_stanje][znak] = self.stanja_koje_sadrzavaju(stanja, enka_prijelazi[stanje][znak])

        return prijelazi

    def preimenovanje_grupiranih_stanja(self, stanja, prijelazi, enka_stanja):
        pretvorba = dict()
        obrnuta_pretvorba = dict()
        lista_stanja = []
        for i in range(0, len(stanja)):
            pretvorba[stanja[i]] = DKAStanje(i, stanja[i], enka_stanja)
            lista_stanja += [pretvorba[stanja[i]]]
            #obrnuta_pretvorba[i] = stanja[i]

        novi_prijelazi = dict()

        for grupno_stanje in prijelazi.keys():
            novi_prijelazi[pretvorba[grupno_stanje]] = dict()
            for znak in prijelazi[grupno_stanje]:
                novi_prijelazi[pretvorba[grupno_stanje]][znak] = pretvorba[prijelazi[grupno_stanje][znak]]

        return lista_stanja, novi_prijelazi

    def enka_u_dka(self, enka):
        nova_stanja = self.grupiraj_eokoline(enka.broj_stanja, enka.prijelazi)
        novi_prijelazi = self.ekstrapoliraj_prijelaze(nova_stanja, enka.prijelazi)
        print(novi_prijelazi)
        self.stanja, self.prijelazi = self.preimenovanje_grupiranih_stanja(nova_stanja, novi_prijelazi, enka.stanja)

    def __str__(self):
        st = "Stanja:\n"
        for stanje in self.stanja:
            st += stanje.__str__() + "\n"

        st += "Prijelazi:\n"
        for stanje in self.stanja:
            st += str(self.prijelazi[stanje]) + "\n"


        return st
#pr = {0: { '$':[1, 3]}, 1: {'$': [2]}, 2: {'$':[3], 'a':[3]}, 3:{'$':[2], 'a':[4]}, 4:{'$':[1]}}
#print(eokolina([4], pr, []))



nezavrsni_znakovi, zavrsni_znakovi, syn_znakovi, produkcije = ulaz.ulaz()
gramatika = ulaz.Gramatika(nezavrsni_znakovi, zavrsni_znakovi, produkcije)
enka = Enka(nezavrsni_znakovi, zavrsni_znakovi, produkcije, nezavrsni_znakovi[0], gramatika.t_skup)
dka = Dka(enka)
print()
print(enka)
print(gramatika.t_skup)
# print()
# print(dka)

