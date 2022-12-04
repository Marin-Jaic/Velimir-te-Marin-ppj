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
        print(syn_znakovi)
        while(ulazni_niz[iterator].znak not in syn_znakovi):
            print(ulazni_niz[iterator], iterator)
            iterator += 1

        while(self.akcija[self.stog.peek(1)[0].stanje][ulazni_niz[iterator].znak] == None):
            print(self.stog.pop(1), file = sys.stderr)
            
        
        return iterator

    def parsiraj(self, ulaz, syn_znakovi):
        iterator = 0
        while(iterator < len(ulaz)):
            ulazniZnak = ulaz[iterator]
            stanje = self.stog.peek(1)[0].stanje

            print(ulazniZnak, self.stog.ostatak())
            
            if(isinstance(self.akcija[stanje][ulazniZnak.znak], Pomak)):
                print("pom")
                novo_stanje = self.akcija[stanje][ulazniZnak.znak].u
                self.stog.push(List(novo_stanje, ulazniZnak))
                iterator += 1

            elif(isinstance(self.akcija[stanje][ulazniZnak.znak], Redukcija)):
                print("red")
                redukcija = self.akcija[stanje][ulazniZnak.znak]
                sadrzaj_stoga = self.stog.peek(len(redukcija.uzorak))
                uzorak_stoga = [i.znak for i in sadrzaj_stoga]
                if(uzorak_stoga == redukcija.uzorak):
                    novi_cvor = UnutarnjiCvor(-1, redukcija.novi, sadrzaj_stoga)
                    self.stog.pop(len(redukcija.uzorak))
                    novi_cvor.stanje = self.novo_stanje[self.stog.peek(1)[0].stanje][redukcija.novi]
                    self.stog.push(novi_cvor)
                elif(redukcija.uzorak == ['$']):
                    print("red eps", self.stog.peek(1)[0].stanje, redukcija.novi)
                    novi_cvor = UnutarnjiCvor(-1, redukcija.novi, [ListEps()])
                    novi_cvor.stanje = self.novo_stanje[self.stog.peek(1)[0].stanje][redukcija.novi]
                    self.stog.push(novi_cvor)
                else:
                    print("GREŠKA PRI REDUKCIJI - različiti sadržaj stoga")
                iterator += 0

            elif(isinstance(self.akcija[stanje][ulazniZnak.znak], Prihvat)):
                self.vrsni_cvor.djeca = self.stog.ostatak()
                print("PRIHVACEN NIZ")
                break

            else:
                iterator = self.oporavakOdGreske(ulazni_niz, iterator, syn_znakovi)
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
    ulazna_dat = open('test/analizator/input.txt', 'r')
    retci = ulazna_dat.read().splitlines()

    niz = []
    for redak in retci:
        r = redak.strip().split(" ")
        niz.append(UlazniZnak(r[0], r[1], " ".join(r[2:])))

    niz.append(UlazniZnak("$", "-1", "KRAJ_NIZA"))
    return niz

#------------------SVE ISPOD OVE CRTE JE DODANO OD STRANE GSA:--------------------------


ulazni_niz = dohvati_ulazni_niz()
lrparser = LRparser({0: {'$': None, 'a': Redukcija(5, ['$'], "<A>"), 'b': Redukcija(6, ['$'], "<B>")}, 1: {'$': Prihvat(), 'a': None, 'b': None}, 2: {'$': Redukcija(2, ['<X>'], "<S>"), 'a': Redukcija(5, ['$'], "<A>"), 'b': Redukcija(6, ['$'], "<B>")}, 3: {'$': None, 'a': Pomak(6), 'b': None}, 4: {'$': None, 'a': None, 'b': Pomak(7)}, 5: {'$': Redukcija(1, ['<X>', '<S>'], "<S>"), 'a': None, 'b': None}, 6: {'$': None, 'a': None, 'b': Redukcija(5, ['$'], "<A>")}, 7: {'$': None, 'a': Redukcija(6, ['$'], "<B>"), 'b': None}, 8: {'$': None, 'a': None, 'b': Pomak(10)}, 9: {'$': None, 'a': Pomak(11), 'b': None}, 10: {'$': Redukcija(3, ['<A>', 'a', '<A>', 'b'], "<X>"), 'a': Redukcija(3, ['<A>', 'a', '<A>', 'b'], "<X>"), 'b': Redukcija(3, ['<A>', 'a', '<A>', 'b'], "<X>")}, 11: {'$': Redukcija(4, ['<B>', 'b', '<B>', 'a'], "<X>"), 'a': Redukcija(4, ['<B>', 'b', '<B>', 'a'], "<X>"), 'b': Redukcija(4, ['<B>', 'b', '<B>', 'a'], "<X>")}}, {0: {'<S>': 1, '<X>': 2, '<A>': 3, '<B>': 4}, 1: {'<S>': None, '<X>': None, '<A>': None, '<B>': None}, 2: {'<S>': 5, '<X>': 2, '<A>': 3, '<B>': 4}, 3: {'<S>': None, '<X>': None, '<A>': None, '<B>': None}, 4: {'<S>': None, '<X>': None, '<A>': None, '<B>': None}, 5: {'<S>': None, '<X>': None, '<A>': None, '<B>': None}, 6: {'<S>': None, '<X>': None, '<A>': 8, '<B>': None}, 7: {'<S>': None, '<X>': None, '<A>': None, '<B>': 9}, 8: {'<S>': None, '<X>': None, '<A>': None, '<B>': None}, 9: {'<S>': None, '<X>': None, '<A>': None, '<B>': None}, 10: {'<S>': None, '<X>': None, '<A>': None, '<B>': None}, 11: {'<S>': None, '<X>': None, '<A>': None, '<B>': None}})
lrparser.parsiraj(ulazni_niz, ['a'])
lrparser.ispis_gen_stabla()