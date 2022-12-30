class Cvor:
    def __init__(self, znak):
        self.znak = znak
        self.tip = None
        self.lizraz = None
        self.tipovi = None
        self.ime = None #Marin dodavanje
        self.imena = None #Marin dodavanje

    def __repr__(self):
        return "Cvor(" + self.znak + ")"

class List(Cvor):
    def __init__(self, znak, red, vrijednost):
        self.red = red
        self.vrijednost = vrijednost
        super().__init__(znak)

    def __str__(self):
        return self.znak + "(" + self.red + ", " + self.vrijednost + ")"

class ListEps(Cvor):
    def __init__(self):
        self.znak = "$"
        
    def __str__(self):
        return self.znak

class UnutarnjiCvor(Cvor):
    def __init__(self, znak, djeca):
        self.djeca = djeca
        super().__init__(znak)
