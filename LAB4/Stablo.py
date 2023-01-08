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
        self.jePozivFunkcije = False

    def __repr__(self):
        return self.znak + " ( tip= " + str(self.tip) + ", tipovi= " + str(self.tipovi) + ", ime=" + str(self.ime) + ", imena=" + str(self.imena) + ", brelem=" + str(self.brelem) + ", jePoziF=" + str(self.jePozivFunkcije) +  " )" 

class List(Cvor):
    def __init__(self, znak, red, vrijednost):
        self.red = red
        self.vrijednost = vrijednost
        super().__init__(znak)

    def __repr__(self):
        return self.znak + " ( tip= " + str(self.tip) + ", vrijednost=" + str(self.vrijednost) + ", tipovi= " + str(self.tipovi) + ", ime=" + str(self.ime) + ", imena=" + str(self.imena) + ", brelem=" + str(self.brelem) + " )" 

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
    def __repr__(self):
        return "funkcija: " + str(self.params) + " -> " + self.pov

    def __eq__(self, other):
        if not isinstance(other, Funkcija):
            return False
        return self.params == other.params and self.pov == other.pov

class tablicaPodatak:
    def __init__(self, tip, djelokrug):
        self.tip = tip
        self.djelokrug = djelokrug
    def __repr__(self):
        return "tip: " + str(self.tip) + " djelokrug: " + str(self.djelokrug)
class djelokrugPodatak:
    def __init__(self, vrsta, dubina):
        self.vrsta = vrsta
        self.dubina = dubina
    
    def __eq__(self, other):
        return self.vrsta == other.vrsta and self.dubina == other.dubina
    
    def __repr__(self):
        return "(vrsta: " +str(self.vrsta) + " dub: " + str(self.dubina) + ")"
    def __str__(self):
        return "(vrsta: " +str(self.vrsta) + " dub: " + str(self.dubina) + ")"