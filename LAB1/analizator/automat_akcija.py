import json

class Automat:
    def __init__(self, prijelazi):
        self.prijelazi = prijelazi
        self.broj_stanja = len(prijelazi.keys()) + 1

    def __str__(self):
        return json.dumps(self.prijelazi)
    
    def epsilon_prijelaz(self):
        nova_stanja = set()

        for stanje in self.trenutna_stanja:
            if "$" in self.prijelazi[stanje].keys():
                nova_stanja.update(self.prijelazi[stanje]["$"])

        if nova_stanja.issubset(self.trenutna_stanja):
            self.izraz_prihvacen = 1 in self.trenutna_stanja 
            return 

        self.trenutna_stanja.update(nova_stanja)        #Premjesteno od iznad ifa, jer bi inace uvijek bio subset
        self.epsilon_prijelaz()

    def prijelaz(self, znak):
        sljedeca_stanja = set()

        for stanje in self.trenutna_stanja:
            if znak in self.prijelazi[stanje].keys():
                sljedeca_stanja.update(self.prijelazi[stanje][znak])
                
        pronaden_prijelaz = len(sljedeca_stanja) != 0

        if pronaden_prijelaz:
            self.trenutna_stanja = sljedeca_stanja
            self.epsilon_prijelaz()

        return pronaden_prijelaz
    
    def reset(self):
       self.izraz_prihvacen = False
       self.trenutna_stanja = set()

       return  
    


class Akcija:
    def __init__(self, stanje, regex, lex, novi_redak, udji_u_stanje, vrati_se, automat, pocetno, prihvatljivo):
        self.stanje = stanje
        self.regex = regex
        self.lex = lex
        self.novi_redak = novi_redak
        self.udji_u_stanje = udji_u_stanje
        self.vrati_se = vrati_se
        self.automat = automat
        self.pocetno, self.prihvatljivo = pocetno, prihvatljivo


    def __str__(self):
        str = "Stanje: " + self.stanje + "\nRegex: " + self.regex + "\nLex: " + self.lex
        if(self.novi_redak != False):
            str += "\nNovi redak"
        if(self.udji_u_stanje != None):
            str += "\nUdji u stanje: " + self.udji_u_stanje
        if(self.vrati_se != 0):
            str += "\nVrati se: " + self.vrati_se
        str += "\n" + self.automat.__str__()
        return str
