import json

class Automat:
    def __init__(self, prijelazi):
        self.prijelazi = prijelazi
        self.broj_stanja = len(prijelazi.keys()) + 1

    def __str__(self):
        return json.dumps(self.prijelazi)


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
