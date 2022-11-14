class Enka:
    def __init__(self, nezavrsni_znakovi, zavrsni_znakovi, produkcije, pocetno_stanje, t_skup):
        self.nezavrsni_znakovi = nezavrsni_znakovi
        self.zavrsni_znakovi = zavrsni_znakovi
        self.produkcije = produkcije
        self.t_skup = t_skup

        self.stanja = [Stanje(0, [".", pocetno_stanje], "$")]

        self.prijelazi = {0: {"$": [self.stanja[0]]}}

        self.broj_stanja = 1
        

        self.generiraj(self.prijelazi[0])
    
    def generiraj(self, stanje):
        index = stanje.stavka.index(".")

        if index + 1 == len(stanje.stavka):
            return
            # nova_stavka = stanje.stavka[:]
            # nova_stavka.remove(".").insert(index + 1, ".")

            # t_crtano = stanje.t[:]
            # self.broj_stanja += 1

            # return Stanje(self.broj_stanja, nova_stavka, t_crtano.sorted()) 
        
            
        if stanje.stavka[index + 1] in self.nezavrsni_znakovi:
            nezavrsni_znak = stanje.stavka[index + 1]
            prenesi_t = "$" in self.produkcije[nezavrsni_znak].keys()
            t_crtano = stanje.t[:]

            if prenesi_t:
                t_crtano += self.t_skup[stanje.stavka[index + 1]]

            for produkcija in self.produkcije[nezavrsni_znak]:
                nova_stavka = produkcija[:]

                if nova_stavka[0] == "$":
                    nova_stavka.remove("$")

                nova_stavka.insert(0, ".")
                sljedece_stanje = None

                for dosad_stanje in self.stanja:
                    if nova_stavka == dosad_stanje.stavka and t_crtano == dosad_stanje.t:
                        sljedece_stanje = dosad_stanje
                        break

                if sljedece_stanje is None:
                    sljedece_stanje = Stanje(self.broj_stanja, nova_stavka, t_crtano.sorted())
                    self.broj_stanja += 1

                    self.generiraj(sljedece_stanje)

                elif stanje.id in self.prijelazi.keys() and nezavrsni_znak in self.prijelazi[nezavrsni_znak].keys():
                    self.prijelazi[stanje.id]["$"] += sljedece_stanje
                else:
                    self.prijelazi[stanje.id]["$"] = [sljedece_stanje]
                
                
        
        nova_stavka = stanje.stavka[:]
        nova_stavka.remove(".")
        nova_stavka.insert(index + 1, ".")
        t_crtano = stanje.t[:]

        sljedece_stanje = Stanje(self.broj_stanja, nova_stavka, t_crtano.sorted())

        self.prijelazi[stanje.id][stanje.stavka[index - 1]] += sljedece_stanje

        self.generiraj(sljedece_stanje)
            
            



#mislim da je uglavnom dobro, treba testirat i razmislit jos kako optimirat
                
            



                




class Stanje:
    def __init__(self, id, stavka, t):
        self.id = id
        self.stavka = stavka
        self.t = t
    