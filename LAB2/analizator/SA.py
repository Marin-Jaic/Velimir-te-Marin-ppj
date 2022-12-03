#TODO oporavak od pogreške!


from pomocni_razredi import *

class LRparser:
    def __init__(self, akcija, novo_stanje):
        self.stog = Stog(Cvor(0, "DNO_STOGA"))
        self.akcija = akcija
        self.novo_stanje = novo_stanje
        self.vrsni_cvor = UnutarnjiCvor(-1, '<S\'>', [])         # pocetni_znak ili S' nisam siguran ...
        

    def parsiraj(self, ulaz):
        iterator = 0
        while(iterator < len(ulaz)):
            ulazniZnak = ulaz[iterator]
            stanje = self.stog.peek(1)[0].stanje

            print(ulazniZnak, self.stog.ostatak())
            
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
                else:
                    print("GREŠKA PRI REDUKCIJI - različiti sadržaj stoga")
                iterator += 0

            elif(isinstance(self.akcija[stanje][ulazniZnak.znak], Prihvat)):
                self.vrsni_cvor.djeca = self.stog.ostatak()
                print("PRIHVACEN NIZ")
                break

            else:
                print("GREŠKA - Odbacivanje ulaznog niza po tablici Akcija")
                break
    def ispis_razine(self, cvorovi, n):
        for cvor in cvorovi:
            for i in range(n):
                print(" ", end="")
            if(isinstance(cvor, List)):
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
lrparser = LRparser({0: {'$': None, 'b': Pomak(1), 'a': None, '(': None, ')': None, 'L': None}, 1: {'$': None, 'b': None, 'a': None, '(': Pomak(2), ')': None, 'L': Pomak(11)}, 2: {'$': None, 'b': Pomak(3), 'a': None, '(': None, ')': None, 'L': None}, 3: {'$': None, 'b': None, 'a': None, '(': Pomak(4), ')': None, 'L': Pomak(6)}, 4: {'$': None, 'b': Pomak(5), 'a': None, '(': None, ')': None, 'L': None}, 5: {'$': None, 'b': None, 'a': None, '(': Pomak(4), ')': None, 'L': Pomak(6)}, 6: {'$': None, 'b': None, 'a': None, '(': None, ')': Redukcija(3, ['L'], "<A>"), 'L': None}, 7: {'$': None, 'b': None, 'a': None, '(': None, ')': Pomak(8), 'L': None}, 8: {'$': None, 'b': None, 'a': None, '(': None, ')': Redukcija(2, ['(', 'b', '<A>', ')'], "<A>"), 'L': None}, 9: {'$': None, 'b': None, 'a': None, '(': None, ')': Pomak(10), 'L': None}, 10: {'$': None, 'b': None, 'a': Redukcija(2, ['(', 'b', '<A>', ')'], "<A>"), '(': None, ')': None, 'L': None}, 11: {'$': None, 'b': None, 'a': Redukcija(3, ['L'], "<A>"), '(': None, ')': None, 'L': None}, 12: {'$': None, 'b': None, 'a': Pomak(13), '(': None, ')': None, 'L': None}, 13: {'$': Redukcija(1, ['b', '<A>', 'a'], "<S>"), 'b': None, 'a': None, '(': None, ')': None, 'L': None}, 14: {'$': Prihvat(), 'b': None, 'a': None, '(': None, ')': None, 'L': None}}, {0: {'<S>': 14, '<A>': None}, 1: {'<S>': None, '<A>': 12}, 2: {'<S>': None, '<A>': None}, 3: {'<S>': None, '<A>': 9}, 4: {'<S>': None, '<A>': None}, 5: {'<S>': None, '<A>': 7}, 6: {'<S>': None, '<A>': None}, 7: {'<S>': None, '<A>': None}, 8: {'<S>': None, '<A>': None}, 9: {'<S>': None, '<A>': None}, 10: {'<S>': None, '<A>': None}, 11: {'<S>': None, '<A>': None}, 12: {'<S>': None, '<A>': None}, 13: {'<S>': None, '<A>': None}, 14: {'<S>': None, '<A>': None}})
lrparser.parsiraj(ulazni_niz)
lrparser.ispis_gen_stabla()