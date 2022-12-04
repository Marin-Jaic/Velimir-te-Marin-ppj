#TODO oporavak od pogreške!

import sys
from pomocni_razredi import *

class LRparser:
    def __init__(self, akcija, novo_stanje):
        self.stog = Stog(Cvor(0, "DNO_STOGA"))
        self.akcija = akcija
        self.novo_stanje = novo_stanje
        self.vrsni_cvor = UnutarnjiCvor(-1, '<S\'>', [])         # pocetni_znak ili S' nisam siguran ...
    

    def oporavakOdGreske(self, ulazni_niz, iterator, syn_znakovi):
        
        print("Pogreška u retku: ", ulazni_niz[iterator].red, file=sys.stderr)
        print("Znakovi koji mogu slijediti su: ", file=sys.stderr)
        proslo = self.stog.peek(1)[0].stanje
        lista_mogucih = []
        for znak in self.akcija[proslo].keys():
            if self.akcija[proslo][znak] != None:
                lista_mogucih += [znak]
        print(lista_mogucih, file=sys.stderr)
        print("Uniformni znak: ", ulazni_niz[iterator].znak, file=sys.stderr)
        print("Znakovni prikaz: ", ulazni_niz[iterator].unif, file=sys.stderr)
        print("", file=sys.stderr)

        while(ulazni_niz[iterator].znak not in syn_znakovi):
            iterator += 1

        while(self.akcija[self.stog.peek(1)[0].stanje][ulazni_niz[iterator].znak] == None):
            self.stog.pop(1)
            
        
        return iterator

    def parsiraj(self, ulaz, syn_znakovi):
        iterator = 0
        while(iterator < len(ulaz)):
            ulazniZnak = ulaz[iterator]
            stanje = self.stog.peek(1)[0].stanje
            
            if(isinstance(self.akcija[stanje][ulazniZnak.znak], Pomak)):
                novo_stanje = self.akcija[stanje][ulazniZnak.znak].u
                self.stog.push(List(novo_stanje, ulazniZnak))
                iterator += 1

            elif(isinstance(self.akcija[stanje][ulazniZnak.znak], Redukcija)):
                redukcija = self.akcija[stanje][ulazniZnak.znak]
                sadrzaj_stoga = self.stog.peek(len(redukcija.uzorak))
                uzorak_stoga = [i.znak for i in sadrzaj_stoga]
                if(uzorak_stoga == redukcija.uzorak):
                    novi_cvor = UnutarnjiCvor(-1, redukcija.novi, sadrzaj_stoga)
                    self.stog.pop(len(redukcija.uzorak))
                    novi_cvor.stanje = self.novo_stanje[self.stog.peek(1)[0].stanje][redukcija.novi]
                    self.stog.push(novi_cvor)
                elif(redukcija.uzorak == ['$']):
                    novi_cvor = UnutarnjiCvor(-1, redukcija.novi, [ListEps()])
                    novi_cvor.stanje = self.novo_stanje[self.stog.peek(1)[0].stanje][redukcija.novi]
                    self.stog.push(novi_cvor)
                
                iterator += 0

            elif(isinstance(self.akcija[stanje][ulazniZnak.znak], Prihvat)):
                self.vrsni_cvor.djeca = self.stog.ostatak()
                #print("PRIHVACEN NIZ")
                break

            else:
                iterator = self.oporavakOdGreske(ulaz, iterator, syn_znakovi)
                #print("GREŠKA - Odbacivanje ulaznog niza po tablici Akcija")
                
                

    def ispis_razine(self, cvorovi, n):
        for cvor in cvorovi:
            for i in range(n):
                print(" ", end="")
            if(isinstance(cvor, List) or isinstance(cvor, ListEps)):
                print(cvor)
            elif(isinstance(cvor, UnutarnjiCvor)):
                print(cvor.znak)
                self.ispis_razine(cvor.djeca, n + 1)

    def ispis_gen_stabla(self):
        #self.ispis_razine([self.vrsni_cvor], 0)        ispisuje li se dodana S' produkcija isto u gen stablu??
        self.ispis_razine(self.vrsni_cvor.djeca, 0)        # <-- za slucaj da ne

def dohvati_ulazni_niz():
    #ulazna_dat = open('test/analizator/input.txt', 'r')
    #retci = ulazna_dat.read().split("\n")
    retci = sys.stdin.read().split("\n")

    niz = []
    for redak in retci:
        if len(redak) == 0:
            continue
        r = redak.strip().split(" ")
        niz.append(UlazniZnak(r[0], r[1], " ".join(r[2:])))

    niz.append(UlazniZnak("$", "-1", "KRAJ_NIZA"))
    return niz

#------------------SVE ISPOD OVE CRTE JE DODANO OD STRANE GSA:--------------------------

