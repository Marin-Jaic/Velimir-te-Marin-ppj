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
lrparser = LRparser({0: {'$': Redukcija(4, ['$'], "<A>"), 'a': Pomak(1), 'b': Pomak(2)}, 1: {'$': None, 'a': Pomak(1), 'b': Pomak(2)}, 2: {'$': Redukcija(3, ['b'], "<B>"), 'a': Redukcija(3, ['b'], "<B>"), 'b': Redukcija(3, ['b'], "<B>")}, 3: {'$': Redukcija(2, ['a', '<B>'], "<B>"), 'a': Redukcija(2, ['a', '<B>'], "<B>"), 'b': Redukcija(2, ['a', '<B>'], "<B>")}, 4: {'$': Redukcija(4, ['$'], "<A>"), 'a': Pomak(1), 'b': Pomak(2)}, 5: {'$': Redukcija(1, ['<B>', '<A>'], "<A>"), 'a': None, 'b': None}, 6: {'$': Prihvat(), 'a': None, 'b': None}}, {0: {'<A>': 6, '<B>': 4}, 1: {'<A>': None, '<B>': 3}, 2: {'<A>': None, '<B>': None}, 3: {'<A>': None, '<B>': None}, 4: {'<A>': 5, '<B>': 4}, 5: {'<A>': None, '<B>': None}, 6: {'<A>': None, '<B>': None}})
lrparser.parsiraj(ulazni_niz)
lrparser.ispis_gen_stabla()