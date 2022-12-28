
                    novi_cvor = UnutarnjiCvor(-1, redukcija.novi, sadrzaj_stoga)
                    self.stog.pop(len(redukcija.uzorak))
                    novi_cvor.stanje = self.novo_stanje[self.stog.peek(1)[0].stanje][redukcija.novi]
                    self.stog.push(novi_cvor)
                elif(redukcija.uzorak == ['$']):
                    #print("red eps", self.stog.peek(1)[0].stanje, redukcija.novi)
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
        self.ispis_razine(self.vrsni_cvor.djeca, 0)        #