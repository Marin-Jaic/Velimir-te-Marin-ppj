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
    djeca = cvor.djeca

    if(cvor.znak == "<primarni_izraz>"):
        #djeca = cvor.djeca MARIN PROMENA

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
    
    elif(cvor.znak == "<postfiks_izraz>"):
        if(djeca[0].znak == "<primarni_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

            provjeri(djeca[0])
        
        elif(djeca[2].znak == "<izraz>"):
            cvor.tip = "X"
            cvor.lizraz = 1 if cvor.tip != "const(T)" else 0

            provjeri(djeca[0])
            djeca[0].tip = "niz(X)"
            provjeri(djeca[2])
            #TODO provjera za <izraz>.tip ∼ int
        
        elif(djeca[2].znak == "D_ZAGRADA"):
            cvor.tip = "pov" #no idea sto je pov, ali mozemo samo ctrl+h kad skuzimo
            cvor.lizraz = 0

            provjeri(djeca[0])
            djeca[0].tip = "funkcija(void->pov)"

        elif(djeca[2].znak == "<lista_argumenata>"):
            cvor.tip = "pov"
            cvor.lizraz = 0

            provjeri(djeca[0])
            provjeri(djeca[2])
            djeca[0].tip = "funckija(params->pov)"
            #TODO params treba promijenit u tipove iz liste argumenata 
        
        elif(djeca[2].znak == "D_ZAGRADA"):
            cvor.tip = "int"
            cvor.lizraz = 0

            provjeri(djeca[0])
            djeca[0].lizraz = 1
            #TODO provjera za <postfiks_izraz>.tip ∼ int
        
        else:
            print("POGREŠKA U <postfiks_izraz>")
    
    elif(cvor.znak == "<lista_argumenata>"):
        if(djeca[0].znak == "<izraz_pridruzivanja>"):
            #TODO  tipovi ← [ <izraz_pridruzivanja>.tip ]

            provjeri("<izraz_pridruzivanja>")

        elif(djeca[0].znak == "<lista_argumenata>"):
            #TODO  tipovi ← [ <izraz_pridruzivanja>.tip ]

            provjeri("<lista_argumenata>")
            provjeri("<izraz_pridruzivanja>")
        
        else:
            print("POGREŠKA U <lista_argumenata>")
        
    elif(cvor.znak == "<unarni_izraz>"):
        if(djeca[0].znak == "<postfiks_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

        elif(djeca[1].znak == "<unarni_znak>"):
            cvor.tip = "int"
            cvor.lizraz = 0

            provjeri(djeca[1])
            djeca[1].lizraz = 1
            #TODO <unarni_izraz>.tip ∼ int
        
        elif(djeca[0].znak == "<unarni_operator>"):
            cvor.tip = "int"
            cvor.lizraz = 0

            provjeri(djeca[1])
            #TODO <cast_izraz>.tip ∼ int

        else: 
            print("POGREŠKA U <unarni_izraz>")
    
    elif(cvor.znak == "<cast_izraz>"):
        if(djeca[0].znak == "<unarni_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

            provjeri(djeca[0])
        
        elif(djeca[0].znak == "L_ZAGRADA"):
            cvor.tip = djeca[1].tip
            cvor.lizraz = 0

            provjeri(djeca[1])
            provjeri(djeca[3])
            #TODO <cast_izraz>.tip se moˇze pretvoriti u <ime_tipa>.tip 

        else: 
            print("POGREŠKA U <cast_izraz>")

    elif(cvor.znak == "<ime_tipa>"):
        if(djeca[0].znak == "<specifikator_tipa>"):
            cvor.tip = djeca[0].tip
            
            provjeri(djeca[0])
        
        elif(djeca[0].znak == "KR_CONST"):
            cvor.tip = "const(" + djeca[1].tip + ")"

            provjeri(djeca[1])

            if (djeca[0].tip == "void"):
                #TODO greska il stovec
                return

        else:
            print("POGREŠKA U <ime_tipa>")

    elif(cvor.znak == "<specifikator_tipa>"):
        if(djeca[0].znak == "KR_VOID"):
            cvor.tip = "void"
        
        elif(djeca[0].znak == "KR_CHAR"):
            cvor.tip = "char"
        
        elif(djeca[0].znak == "KR_INT"):
            cvor.tip = "int"

        else:
            print("POGREŠKA U <specifikator_tipa>")
        
    elif(cvor.znak == "<multiplikativni izraz>"):
        if(djeca[0].znak == "<cast_izraz>"):
            cvor.tip = "void"
            cvor.lizraz = djeca[0].lizraz

            provjeri(djeca[0])
        
        elif(djeca[0].znak == "<multiplikativni_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = 0

            provjeri(djeca[0])
            #TODO <multiplikativni_izraz>.tip ∼ int
            provjeri(djeca[2])
            #TODO  <cast_izraz>.tip ∼ int

        else:
            print("POGREŠKA U <multiplikativni_izraz>")
    
    elif(cvor.znak == "<aditivni izraz>"):
        if(djeca[0].znak == "<multiplikativni_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

            provjeri(djeca[0])
        
        elif(djeca[0].znak == "<aditivni_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = 0

            provjeri(djeca[0])
            #TODO <aditivni_izraz>.tip ∼ int
            provjeri(djeca[2])
            #TODO <multiplikativni_izraz>.tip ∼ int
        
        else:
            print("POGREŠKA U <aditivni_izraz>")
        

    elif(cvor.znak == "<odnosni_izraz>"):
        if(djeca[0].znak == "<aditivni_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

            provjeri(djeca[0])
        
        elif(djeca[0].znak == "<odnosni_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = 0

            provjeri(djeca[0])
            #TODO <odnosni_izraz>.tip ∼ int
            provjeri(djeca[2])
            #TODO <aditivni_izraz>.tip ∼ int

        else:
            print("POGREŠKA U <odnosni_izraz>")

    elif(cvor.znak == "<jednakosni_izraz>"):
        if(djeca[0].znak == "<odnosni_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
        
            provjeri(djeca[0])
        
        elif(djeca[0].znak == "<jednakosni_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = 0
        
            provjeri(djeca[0])
            #TODO <jednakosni_izraz>.tip ∼ int
            provjeri(djeca[2])
            #TODO <odnosni_izraz>.tip ∼ int
        
        else:
            print("POGREŠKA U <jednakosni_izraz>")
    
    elif(cvor.znak == "<bin_i_izraz>"):
        if(djeca[0].znak == "<jednakosni_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
        
            provjeri(djeca[0])
        
        elif(djeca[0].znak == "<bin_i_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = 0
        
            provjeri(djeca[0])
            #TODO <bin_i_izraz>.tip ∼ int
            provjeri(djeca[2])
            #TODO <jednakosni_izraz>.tip ∼ int
        
        else:
            print("POGREŠKA U <bin_i_izraz>")
    
    elif(cvor.znak == "<bin_xili_izraz>"):
        if(djeca[0].znak == "<bin_i_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
        
            provjeri(djeca[0])
        
        elif(djeca[0].znak == "<bin_xili_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = 0

            provjeri(djeca[0])
            #TODO <bin_xili_izraz>.tip ∼ int
            provjeri(djeca[2])
            #TODO <bin_i_izraz>.tip ∼ int
        
        else:
            print("POGREŠKA U <bin_xili_izraz>")
    
    elif(cvor.znak == "<bin_ili_izraz>"):
        if(djeca[0].znak == "<bin_xili_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
        
            provjeri(djeca[0])
        
        elif(djeca[0].znak == "<bin_ili_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = 0

            provjeri(djeca[0])
            #TODO <bin_ili_izraz>.tip ∼ int
            provjeri(djeca[2])
            #TODO <bin_xili_izraz>.tip ∼ int
        
        else:
            print("POGREŠKA U <bin_ili_izraz>")
    
    elif(cvor.znak == "<log_i_izraz>"):
        if(djeca[0].znak == "<bin_ili_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
        
            provjeri(djeca[0])
        
        elif(djeca[0].znak == "<log_i_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = 0

            provjeri(djeca[0])
            #TODO <log_i_izraz>.tip ∼ int
            provjeri(djeca[2])
            #TODO <bin_ili_izraz>.tip ∼ int
        
        else:
            print("POGREŠKA U <log_i_izraz>")
    
    elif(cvor.znak == "<log_ili_izraz>"):
        if(djeca[0].znak == "<log_i_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
        
            provjeri(djeca[0])
        
        elif(djeca[0].znak == "<log_ili_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = 0

            provjeri(djeca[0])
            #TODO <log_ili_izraz>.tip ∼ int
            provjeri(djeca[2])
            #TODO <log_i_izraz>.tip ∼ int
        
        else:
            print("POGREŠKA U <log_ili_izraz>")

    elif(cvor.znak == "<izraz_pridruzivanja>"):
        if(djeca[0].znak == "<log_ili_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
        
            provjeri(djeca[0])
        
        elif(djeca[0].znak == "<postfiks_izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = 0

            provjeri(djeca[0])
            djeca[0].lizraz = 1
            provjeri(djeca[2])
            #TODO  <izraz_pridruzivanja>.tip ∼ <postfiks_izraz>.tip
        
        else:
            print("POGREŠKA U <izraz_pridruzivanja>")
    
    elif(cvor.znak == "<izraz>"):
        if(djeca[0].znak == "<izraz_pridruzivanja>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
        
            provjeri(djeca[0])
        
        elif(djeca[0].znak == "<izraz>"):
            cvor.tip = djeca[0].tip
            cvor.lizraz = 0

            provjeri(djeca[0])
            provjeri(djeca[2])
        
        else:
            print("POGREŠKA U <izraz>")
    
    #4.4.5 Naredbena struktura programa
    elif(cvor.znak == "<slozena_naredba>"):
        if(djeca[1].znak == "<lista_naredbi>"):
            provjeri(djeca[1])
        
        elif(djeca[1].znak == "<lista_deklaracija>"):
            provjeri(djeca[1])
            provjeri(djeca[2])

        else:
            print("POGREŠKA U <slozena_naredba>")
    
    elif(cvor.znak == "<lista_naredbi>"):
        if(djeca[0].znak == "<naredba>"):
            provjeri(djeca[0])

        elif(djeca[1].znak == "<naredba>"):
            provjeri(djeca[0])
            provjeri(djeca[1])

        else:
            print("POGREŠKA U <lista_naredbi>")

    #nesto <naredba> potencijalno zajebaje, str 63

    elif(cvor.znak == "<izraz_naredba>"):
        if(djeca[0].znak == "TOCKAZAREZ"):
            cvor.tip = "int"

        elif(djeca[0].znak == "<izraz>"):
            cvor.tip = djeca[0].tip

            provjeri(djeca[0])

        else:
            print("POGREŠKA U <izraz_naredba>")
    
    elif(cvor.znak == "<naredba_grananja>"):
        if(len(djeca) == 5):
            provjeri(djeca[2])
            #TODO <izraz>.tip ∼ int
            provjeri(djeca[4])
        
        elif(len(djeca) == 7):
            provjeri(djeca[2])
            #TODO <izraz>.tip ∼ int
            provjeri(djeca[4])
            provjeri(djeca[6])
        
        else:
            print("POGREŠKA U <naredba_grananja>")
        
    elif(cvor.znak == "<naredba_petlje>"):
        if(djeca[0].znak == "KR_WHILE"):
            provjeri(djeca[2])
            #TODO <izraz>.tip ∼ int
            provjeri(djeca[4])
        
        elif(djeca[4] == "D_ZAGRADA"):
            provjeri(djeca[2])
            provjeri(djeca[3])
            #TODO <izraz_naredba>2.tip ∼ int
            provjeri(djeca[5])

        elif(djeca[4] == "<izraz>"):
            provjeri(djeca[2])
            provjeri(djeca[3])
            #TODO <izraz_naredba>2.tip ∼ int
            provjeri(djeca[4])
            provjeri(djeca[6])

        else:
            print("POGREŠKA U <naredba_petlje>")
    
    elif(cvor.znak == "<naredba_skoka>"):
        if(djeca[0].znak == "KR_CONTINUE" or djeca[0].znak == "KR_BREAK"):
            #TODO naredba se nalazi unutar petlje ili unutar bloka koji je ugnijeˇzden u petlji
            gas = 0

        elif(djeca[1].znak == "TOCKAZAREZ"):
            #TODO 1. naredba se nalazi unutar funkcije tipa funkcija(params → void)
            gas = 0

        elif(djeca[1].znak == "<izraz>"):
            provjeri(djeca[1])
            #TODO naredba se nalazi unutar funkcije tipa funkcija(params → pov) i vrijedi <izraz>.tip ∼ pov
        
        else:
            print("POGREŠKA U <naredba_skoka>")
    
    elif(cvor.znak == "<prijevodna_jedinica>"):
        if(djeca[0].znak == "<vanjska_deklaracija>"):
            provjeri(djeca[0])
        
        elif(djeca[0].znak == "<prijevodna_jedinica>"):
            provjeri(djeca[0])
            provjeri(djeca[1])
    
    #TODO 4.4.6 Deklaracije i definicije