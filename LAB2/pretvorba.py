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

        self.stanja = {0: Stanje(0, [".", pocetno_stanje], ["$"])} #pazi na numeraciju, mozda se zezna

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
        if trenutni_znak in self.nezavrsni_znakovi:
            #namjestimo t_skup

            t_crtano = set()

            i = index + 2
            dodaj_sljedeci = True

            while(i < len(stanje.stavka) and dodaj_sljedeci):
                dodaj_sljedeci = False

                if stanje.stavka[i] in self.zavrsni_znakovi:
                    t_crtano.add(stanje.stavka[i])
                else:
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

                if stanje.stavka == [".", "<A>"]:
                    print(nova_stavka)

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

    def __hash__(self):
        return hash(self.id) ^ hash("".join(self.stavka)) ^ hash("".join(self.t))

class StavkaSkup:
    def __init__(self, stavka, skup):
        self.stavka = stavka
        self.skup = skup

    def __hash__(self):
        return hash("".join(self.stavka)) ^ hash(self.skup)
    
    def __repr__(self):
        return str(self.stavka) + " " + str(self.skup)

class DKAStanje:

    def __init__(self, id, set_starih_stanja, opisi_stanja):
        self.id = id

        self.stavke_skupovi = set()

        for stanje in set_starih_stanja:
            ss = tuple()
            self.stavke_skupovi.add(StavkaSkup(opisi_stanja[stanje].stavka, frozenset(opisi_stanja[stanje].t)))

    def __repr__(self):
        return "(" + str(self.id) + ") -> " + str(self.stavke_skupovi)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id



class Dka:
    def __init__(self, enka):
        self.broj_stanja = 0
        self.prijelazi = dict()
        self.stanja, self.prijelazi = self.enka_u_dka(enka)

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
        return self.preimenovanje_grupiranih_stanja(nova_stanja, novi_prijelazi, enka.stanja)

    def __str__(self):
        st = "Stanja:\n"
        for stanje in self.stanja:
            st += stanje.__str__() + "\n"

        st += "Prijelazi:\n"
        for stanje in self.stanja:
            st += self.prijelazi[stanje].__repr__() + "\n"


        return st

    def ispis(self):
        print("Stanja:\n")
        for stanje in self.stanja:
            print(stanje.__str__() + "\n")

        print("Prijelazi:\n")
        for stanje in self.stanja:
            print(str(stanje.id) + " -> " +self.prijelazi[stanje].__repr__() + "\n")

#pr = {0: { '$':[1, 3]}, 1: {'$': [2]}, 2: {'$':[3], 'a':[3]}, 3:{'$':[2], 'a':[4]}, 4:{'$':[1]}}
#print(eokolina([4], pr, []))

class Pomak:
    def __init__(self, novo_stanje):
        self.u = novo_stanje
    
    def __repr__(self):
        return "Pomak(" + str(self.u) + ")"

class Redukcija:
    def __init__(self, produkcija):
        self.id = produkcija.id
        self.uzorak = produkcija.ds
        self.novi = produkcija.ls

    def __repr__(self):
        return "Redukcija(" + str(self.id) + ", " + str(self.uzorak) + ", \"" + str(self.novi) + "\")"

class Prihvat:
    def __init__(self):
        self.prihvat = True
    
    def __repr__(self):
        return "Prihvat()"

class LRparser:
    def __init__(self, dka, gramatika):
        self.akcija = dict()
        self.novo_stanje = dict()

        for stanje in dka.stanja:
            self.akcija[stanje.id] = dict()
            self.novo_stanje[stanje.id] = dict()
            self.akcija[stanje.id]['$'] = None
            for znak in gramatika.zavrsni_znakovi:
                self.akcija[stanje.id][znak] = None
            for znak in gramatika.nezavrsni_znakovi:
                self.novo_stanje[stanje.id][znak] = None
        
        for stanje in dka.stanja:
            if(stanje.id == 33): print(dka.prijelazi[stanje])
            for stavka_skup in stanje.stavke_skupovi:
                stavka = stavka_skup.stavka
                skup = stavka_skup.skup
                
                # Prihvat
                if(stavka == [gramatika.nezavrsni_znakovi[0], "."]):
                    self.akcija[stanje.id]['$'] = Prihvat()

                # Redukcija
                elif(stavka.index(".") == len(stavka) - 1):
                    
                    min_produkcija = None
                    min_id = None
                    stavka_bez_tocke = stavka[:]
                    stavka_bez_tocke.remove('.')
                    if(stavka_bez_tocke == []):
                        stavka_bez_tocke = ['$']
                    for key in gramatika.produkcije.keys():
                        for prod in gramatika.produkcije[key]:
                            if(prod.ds == ["<S\'>"]):
                                continue
                            if prod.ds == stavka_bez_tocke:
                                if min_id == None or prod.id < min_id:
                                    min_id = prod.id
                                    min_produkcija = prod
                    
                    for t_znak in skup:
                        if not isinstance(self.akcija[stanje.id][t_znak], Pomak) and (not isinstance(self.akcija[stanje.id][t_znak], Redukcija) or self.akcija[stanje.id][t_znak].id > min_id):
                            self.akcija[stanje.id][t_znak] = Redukcija(min_produkcija) #pronadi_produkciju_te_stavke
                        
                # Pomak
                elif(stavka[stavka.index(".") + 1] in gramatika.zavrsni_znakovi):
                    tmp = stavka[stavka.index(".") + 1]
                    self.akcija[stanje.id][tmp] = Pomak(dka.prijelazi[stanje][tmp].id)

                # Novo stanje
                elif(stavka[stavka.index(".") + 1] in gramatika.nezavrsni_znakovi):
                    #print(stanje.id, stavka, stavka[stavka.index(".") + 1], dka.prijelazi[stanje][stavka[stavka.index(".") + 1]].id)
                    tmp = stavka[stavka.index(".") + 1]
                    self.novo_stanje[stanje.id][tmp] = dka.prijelazi[stanje][tmp].id

    def __repr__(self):
        return "LRparser(" + str(self.akcija) + ", " + str(self.novo_stanje) + ")"

    def __str__(self):
        return "LRparser(" + str(self.akcija) + ", " + str(self.novo_stanje) + ")"


def generiraj_lr_parser():
    nezavrsni_znakovi, zavrsni_znakovi, syn_znakovi, produkcije = ulaz.ulaz()
    gramatika = ulaz.Gramatika(nezavrsni_znakovi, zavrsni_znakovi, produkcije)
    enka = Enka(nezavrsni_znakovi, zavrsni_znakovi, produkcije, nezavrsni_znakovi[0], gramatika.t_skup)
    #print("Tskup", gramatika.t_skup)
    #print(enka)
    #print(zavrsni_znakovi)
    #print(nezavrsni_znakovi)
    dka = Dka(enka)
    #dka.ispis()

    gramatika.produkcije['<S\'>'] = [ulaz.produkcija(0, ['<S\'>'], [nezavrsni_znakovi[0]])]
    return LRparser(dka, gramatika), syn_znakovi

generiraj_lr_parser()
