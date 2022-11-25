import ulaz
from json import dumps

class Enka:
    def __init__(self, nezavrsni_znakovi, zavrsni_znakovi, produkcije, pocetno_stanje, t_skup):
        self.nezavrsni_znakovi = nezavrsni_znakovi
        self.zavrsni_znakovi = zavrsni_znakovi
        self.produkcije = produkcije
        self.t_skup = t_skup

        self.stanja = {0: Stanje(1, ["<S'>"], ["$"]), 1: Stanje(1, [".", pocetno_stanje], ["$"])}

        self.prijelazi = {0: {"$": [1]}}

        self.broj_stanja = 2 #pazi ovo, bilo je 2

        self.generiraj(self.stanja[1])
    
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
            #PRVO ODRADUJEMO EPSILON PRIJELAZE
            t_crtano = set()

            if index + 2 == len(stanje.stavka):
                t_crtano.add("$")
            elif stanje.stavka[index + 2] in zavrsni_znakovi:
                t_crtano.add(trenutni_znak)
            else:
                t_crtano.update(self.t_skup[stanje.stavka[index + 2]][:])

                for produkcija in self.produkcije[trenutni_znak]:
                    if "$" in produkcija.ds:
                        t_crtano.update(stanje.t)
                        break
            
            t_crtano = list(t_crtano)
            t_crtano.sort()
            
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

nezavrsni_znakovi, zavrsni_znakovi, syn_znakovi, produkcije = ulaz.ulaz()
gramatika = ulaz.Gramatika(nezavrsni_znakovi, zavrsni_znakovi, produkcije)
enka = Enka(nezavrsni_znakovi, zavrsni_znakovi, produkcije, nezavrsni_znakovi[0], gramatika.t_skup)
print(gramatika)
print(enka)
