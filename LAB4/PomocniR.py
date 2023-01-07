class Varijabla:
    def __init__(self, tip, naziv, inicijalna_vrijednost, djelokrug, velicina = 1):  
        self.naziv = naziv
        self.vrijednost = inicijalna_vrijednost

        self.jeniz = (velicina > 1)
        if self.jeniz:
            for i in range(len(self.vrijednost)):
                if isinstance(self.vrijednost[i], str):
                    if tip == "char":
                        self.vrijednost[i] = ord(self.vrijednost[i].strip("\'"))
                    else:
                        self.vrijednost[i] = int(self.vrijednost[i])


            self.vrijednost += [0 for i in range(velicina - len(inicijalna_vrijednost))]
            
            self.adr = ["" for i in range(velicina)]
            for i in range(velicina):
                for krug in djelokrug:
                    self.adr[i] += krug.upper()        
                self.adr[i] += self.naziv.upper() +str(i)

        else:
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
        return self.naziv + " = " + str(self.vrijednost)

    def kod(self):
        if self.jeniz:
            string = ""
            for i in range(len(self.vrijednost)):
                string += self.adr[i] + "\t\tDW %D " + str(self.vrijednost[i]) + "\n"
            return string
        else:
            return self.adr + "\t\tDW %D " + str(self.vrijednost) + "\n"

class Funkcija:
    def __init__(self, ime, args, locals):
        self.ime = ime
        self.args = args
        self.locals = locals

    def __repr__(self):
        return self.ime + "(" + str(self.args) + " -> pov), vars: " + str(self.locals)