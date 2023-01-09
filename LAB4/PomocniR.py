class Varijabla:
    def __init__(self, tip, naziv, inicijalna_vrijednost, djelokrug, jePointer = False):  
        self.naziv = naziv
        self.vrijednost = inicijalna_vrijednost
        self.jePointer = jePointer
        if isinstance(self.vrijednost, str):
            if tip == "char":
                self.vrijednost = ord(self.vrijednost.strip("\'"))
            else:
                self.vrijednost = int(self.vrijednost)

        self.adr = ""
        for krug in djelokrug:
            self.adr += krug.upper()
        self.adr += naziv.upper()


    def __repr__(self):
        return self.naziv + " = " + str(self.vrijednost) + "("+str(self.jePointer)+")"

    def kod(self):
        return self.adr + "\t\tDW %D " + str(self.vrijednost) + "\n"

class Funkcija:
    def __init__(self, ime, args, adr):
        self.ime = ime
        self.args = args
        self.adr = adr

    def __repr__(self):
        return self.ime + "(" + str(self.args) + " -> pov)"