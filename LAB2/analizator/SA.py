#TODO oporavak od pogreške!


from pomocni_razredi import *

class LRparser:
    def __init__(self, akcija, novo_stanje):
        self.stog = Stog(Cvor(0, "DNO_STOGA"))
        self.akcija = akcija
        self.novo_stanje = novo_stanje
        self.vrsni_cvor = UnutarnjiCvor(-1, '<S\'>', [])         # pocetni_znak ili S' nisam siguran ...
    

    def oporavakOdGreske(self, ulazni_niz, iterator, syn_znakovi):
        while(ulazni_niz[iterator] not in syn_znakovi):
            iterator += 1

        while(self.akcija[self.stog.peek(1)[0].stanje][ulazni_niz[iterator]] == None):
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
                    novi_cvor = UnutarnjiCvor(-1, redukcija.novi, ['$'])
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
                #iterator = self.oporavakOdGreske(ulazni_niz, iterator, syn_znakovi)
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
lrparser = LRparser({0: {'$': None, 'OPERAND': Pomak(1), 'OP_MINUS': None, 'UMINUS': Pomak(2), 'LIJEVA_ZAGRADA': Pomak(3), 'DESNA_ZAGRADA': None}, 1: {'$': Redukcija(1, ['OPERAND'], "<atom>"), 'OPERAND': None, 'OP_MINUS': Redukcija(1, ['OPERAND'], "<atom>"), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': None}, 2: {'$': None, 'OPERAND': Pomak(1), 'OP_MINUS': None, 'UMINUS': Pomak(2), 'LIJEVA_ZAGRADA': Pomak(3), 'DESNA_ZAGRADA': None}, 3: {'$': None, 'OPERAND': Pomak(7), 'OP_MINUS': None, 'UMINUS': Pomak(8), 'LIJEVA_ZAGRADA': Pomak(9), 'DESNA_ZAGRADA': None}, 4: {'$': Prihvat(), 'OPERAND': None, 'OP_MINUS': Pomak(12), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': None}, 5: {'$': Redukcija(4, ['<atom>'], "<expr>"), 'OPERAND': None, 'OP_MINUS': Redukcija(4, ['<atom>'], "<expr>"), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': None}, 6: {'$': Redukcija(2, ['UMINUS', '<atom>'], "<atom>"), 'OPERAND': None, 'OP_MINUS': Redukcija(2, ['UMINUS', '<atom>'], "<atom>"), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': None}, 7: {'$': None, 'OPERAND': None, 'OP_MINUS': Redukcija(1, ['OPERAND'], "<atom>"), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': Redukcija(1, ['OPERAND'], "<atom>")}, 8: {'$': None, 'OPERAND': Pomak(7), 'OP_MINUS': None, 'UMINUS': Pomak(8), 'LIJEVA_ZAGRADA': Pomak(9), 'DESNA_ZAGRADA': None}, 9: {'$': None, 'OPERAND': Pomak(7), 'OP_MINUS': None, 'UMINUS': Pomak(8), 'LIJEVA_ZAGRADA': Pomak(9), 'DESNA_ZAGRADA': None}, 10: {'$': None, 'OPERAND': None, 'OP_MINUS': Pomak(15), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': Pomak(16)}, 11: {'$': None, 'OPERAND': None, 'OP_MINUS': Redukcija(4, ['<atom>'], "<expr>"), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': Redukcija(4, ['<atom>'], "<expr>")}, 12: {'$': None, 'OPERAND': Pomak(1), 'OP_MINUS': None, 'UMINUS': Pomak(2), 'LIJEVA_ZAGRADA': Pomak(3), 'DESNA_ZAGRADA': None}, 13: {'$': None, 'OPERAND': None, 'OP_MINUS': Redukcija(2, ['UMINUS', '<atom>'], "<atom>"), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': Redukcija(2, ['UMINUS', '<atom>'], "<atom>")}, 14: {'$': None, 'OPERAND': None, 'OP_MINUS': Pomak(15), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': Pomak(18)}, 15: {'$': None, 'OPERAND': Pomak(7), 'OP_MINUS': None, 'UMINUS': Pomak(8), 'LIJEVA_ZAGRADA': Pomak(9), 'DESNA_ZAGRADA': None}, 16: {'$': Redukcija(3, ['LIJEVA_ZAGRADA', '<expr>', 'DESNA_ZAGRADA'], "<atom>"), 'OPERAND': None, 'OP_MINUS': Redukcija(3, ['LIJEVA_ZAGRADA', '<expr>', 'DESNA_ZAGRADA'], "<atom>"), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': None}, 17: {'$': Redukcija(5, ['<expr>', 'OP_MINUS', '<atom>'], "<expr>"), 'OPERAND': None, 'OP_MINUS': Redukcija(5, ['<expr>', 'OP_MINUS', '<atom>'], "<expr>"), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': None}, 18: {'$': None, 'OPERAND': None, 'OP_MINUS': Redukcija(3, ['LIJEVA_ZAGRADA', '<expr>', 'DESNA_ZAGRADA'], "<atom>"), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': Redukcija(3, ['LIJEVA_ZAGRADA', '<expr>', 'DESNA_ZAGRADA'], "<atom>")}, 19: {'$': None, 'OPERAND': None, 'OP_MINUS': Redukcija(5, ['<expr>', 'OP_MINUS', '<atom>'], "<expr>"), 'UMINUS': None, 'LIJEVA_ZAGRADA': None, 'DESNA_ZAGRADA': Redukcija(5, ['<expr>', 'OP_MINUS', '<atom>'], "<expr>")}}, {0: {'<expr>': 4, '<atom>': 5}, 1: {'<expr>': None, '<atom>': None}, 2: {'<expr>': None, '<atom>': 6}, 3: {'<expr>': 10, '<atom>': 11}, 4: {'<expr>': None, '<atom>': None}, 5: {'<expr>': None, '<atom>': None}, 6: {'<expr>': None, '<atom>': None}, 7: {'<expr>': None, '<atom>': None}, 8: {'<expr>': None, '<atom>': 13}, 9: {'<expr>': 14, '<atom>': 11}, 10: {'<expr>': None, '<atom>': None}, 11: {'<expr>': None, '<atom>': None}, 12: {'<expr>': None, '<atom>': 17}, 13: {'<expr>': None, '<atom>': None}, 14: {'<expr>': None, '<atom>': None}, 15: {'<expr>': None, '<atom>': 19}, 16: {'<expr>': None, '<atom>': None}, 17: {'<expr>': None, '<atom>': None}, 18: {'<expr>': None, '<atom>': None}, 19: {'<expr>': None, '<atom>': None}})
lrparser.parsiraj(ulazni_niz, ['OPERAND', 'UMINUS', 'LIJEVA_ZAGRADA'])
lrparser.ispis_gen_stabla()