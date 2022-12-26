import ulaz
from Stablo import *

korijen = ulaz.ulaz()

def jebroj(broj):
    if not broj.isdigit():
        return False
    broj = int(broj)
    return (-2147483648 <= broj and broj <= 2147483647)


def jeznak(znak):
    if(len(znak) == 1 and znak[0] != "\\"):
        return True
    elif(len(znak) == 2 and znak[0] == "\\" and znak[1] in ("t", "n", "0", "\'", "\"", "\\")):
        return False
    return False


def jenizznakova(niz):
    it = 0
    while("\\" in niz[it:]):
        it = niz[it:].index("\\")
        if it + 1 == len(niz) or niz[it + 1] not in ("t", "n", "0", "\'", "\"", "\\"):
            return False
        it += 2
    return True



def provjeri(cvor):
    if(cvor.znak == "<primarni_izraz>"):
        djeca = cvor.djeca

        if(djeca[0].znak == "IDN"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].izraz

            #TODO provjera deklariranosti imena identifikatora u višezarinskoj tablici identifikatora 


        elif(djeca[0].znak == "BROJ"):
            cvor.tip = "int"
            cvor.lizraz = False

            if not jebroj(djeca[0].vrijednost):
                print("<primarni_izraz> ::= " + str(djeca[0]))


        elif(djeca[0].znak == "ZNAK"):
            cvor.tip = "char"
            cvor.lizraz = False

            if not jeznak(djeca[0].vrijdnost):
                print("<primarni_izraz> ::= " + str(djeca[0]))


        elif(djeca[0].znak == "NIZ_ZNAKOVA"):
            cvor.tip = "niz(const(char))"
            cvor.lizraz = False

            if not jenizznakova(djeca[0].vrijdnost):
                print("<primarni_izraz> ::= " + str(djeca[0]))

        
        elif(djeca[0].znak == "L_ZAGRADA"):

            cvor.tip = djeca[1].tip
            cvor.lizraz = djeca[1].lizraz

            provjeri(djeca[1])
        
        else:
            print("POGREŠKA U <primarni_izraz>")