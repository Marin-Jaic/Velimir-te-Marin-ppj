class Pomak:
    def __init__(self, novo_stanje):
        self.u = novo_stanje

class Redukcija:
    def __init__(self, id, uzorak, novi):
        self.id = id
        self.uzorak = uzorak
        self.novi = novi

class Prihvat:
    def __init__(self):
        self.prihvat = True


class Cvor:
    def __init__(self, stanje, znak):
        self.stanje = stanje
        self.znak = znak

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


class Stog:
    def __init__(self, poc_el):
        self.stog = [poc_el]

    def peek(self, n):
        lista = []
        for i in range(0, n):
            lista.append(self.stog[len(self.stog) - n + i])
        
        return lista
    
    def pop(self, n):
        lista = self.peek(n)
        for i in range(0, n):
            self.stog.pop()
        return lista

    def push(self, element):
        return self.stog.append(element)

    def ostatak(self):
        return self.stog[1:]
