class Cvor:
    def __init__(self, stanje, znak):
        self.stanje = stanje
        self.znak = znak
        self.tip = None
        self.lizraz = None

    def __repr__(self):
        return "Cvor(" + str(self.stanje) + ", " + self.znak + ")"

class List(Cvor):
    def __init__(self, stanje, ulazniZnak):
        self.red = ulazniZnak.red
        self.unif = ulazniZnak.unif
        super().__init__(stanje, ulazniZnak.znak)
    def __str__(self):
        return self.znak + " " + self.red + " " + self.unif
class ListEps(Cvor):
    def __init__(self):
        self.znak = "$"
    def __str__(self):
        return self.znak

class UnutarnjiCvor(Cvor):
    def __init__(self, stanje, znak, djeca):
        self.djeca = djeca
        super().__init__(stanje, znak)

class UlazniZnak:
    def __init__(self, znak, red, unif):
        self.znak = znak
        self.red = red
        self.unif = unif
    def __repr__(self):
        return "UlazniZnak(\'"+ self.znak + "\', " + self.red + ", " + self.unif + ")"
