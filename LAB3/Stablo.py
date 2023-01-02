class Cvor:
    def __init__(self, znak):
        self.znak = znak
        self.tip = None
        self.lizraz = None
        self.tipovi = None
        self.ime = None #Marin dodavanje
        self.imena = None #Marin dodavanje
        self.ntip = None
        self.brelem = None

    def __repr__(self):
        return "Cvor(" + self.znak + ")"

class List(Cvor):
    def __init__(self, znak, red, vrijednost):
        self.red = red
        self.vrijednost = vrijednost
        super().__init__(znak)

    def __str__(self):
        return self.znak + "(" + self.red + ", " + self.vrijednost + ")"
    def __repr__(self):
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



class Funkcija:
    def __init__(self, params, pov, definirana=False):
        self.params = params
        self.pov = pov
        self.definirana = definirana

class tablicaPodatak:
    def __init__(self, tip, djelokrug):
        self.tip = tip
        self.djelokrug = djelokrug

class djelokrugPodatak:
    def __init__(self, vrsta, dubina):
        self.vrsta = vrsta
        self.dubina = dubina
    
    def __eq__(self, other):
        return self.vrsta == other.vrsta and self.dubina == other.dubina