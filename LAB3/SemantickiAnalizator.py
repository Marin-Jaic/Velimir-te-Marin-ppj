import ulaz
from Stablo import *
import copy

korijen = ulaz.ulaz()

#provjeri(korijen, dict())


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

def jeNizX(str):
    return str[0:4] == "niz(" and str[len(str)-1] == ")" and jeX(str[4:(len(str)-1)])

def jeNizT(str):
    return str[0:4] == "niz(" and str[len(str)-1] == ")" and jeT(str[4:(len(str)-1)])

def jeNizConstX(str):
    return str[0:4] == "niz(" and str[len(str)-1] == ")" and jeConstX(str[4:(len(str)-1)])

def jeNizConstT(str):
    return str[0:4] == "niz(" and str[len(str)-1] == ")" and jeConstT(str[4:(len(str)-1)])

# Ovo je suvisno
def jeConstX(str):
    return str[0:6] == "const(" and str[len(str)-1] == ")" and jeX(str[6:(len(str)-1)])
#---------------

def jeConstT(str):
    return str[0:6] == "const(" and str[len(str)-1] == ")" and jeT(str[6:(len(str)-1)])

def jeX(str):
    return str == "const(int)" or str == "const(char)" or str == "int" or str == "char" 

def jeT(str):
    return str == "int" or str == "char"

def ImplicitnoXToY(x, y): # Gleda vrijedi li x ~ y, nisam sto posto ako je tranzitivno okruzenje potpuno, cini mi se da je, ali mi špurijus govori da nije
    #return x == y or jeT(x) and jeConstT(y) and x != "char" and y != int or jeConstT(x) and jeT(y) and x != "char" and y != int  or x == "char" and y == "int" or jeNizT(x) and jeNizConstT(y) and x != "char" and y != int
    return (x == y or jeT(x) and jeConstT(y) or jeConstT(x) and jeT(y) or jeNizT(x) and jeNizConstT(y)) and x != "char" and y != int or x == "char" and y == "int"

def EksplicitnoXToY(x, y):
    return jeX(x) and jeT(y)




def provjeri(cvor, tablica_IDN):
    djeca = cvor.djeca

    if(cvor.znak == "<primarni_izraz>"):

        if(djeca[0].znak == "IDN"):

            if tablica_IDN[djeca[0].vrijednost] == None:
                print("<primarni_izraz> ::= " + str(djeca[0]))
                return False
            
            tip = tablica_IDN[djeca[0].vrijednost]
            # tip će biti ili string "int", "char" i tako
            # ili tuple oblika (params, pov) ("void", "void"), (["int", "int"], "char") i tako

            cvor.tip = tip
            cvor.lizraz = not isinstance(tip, Funkcija) and jeT(tip) 


        elif(djeca[0].znak == "BROJ"):

            if not jebroj(djeca[0].vrijednost):
                print("<primarni_izraz> ::= " + str(djeca[0]))
                return False

            cvor.tip = "int"
            cvor.lizraz = False


        elif(djeca[0].znak == "ZNAK"):
            if not jeznak(djeca[0].vrijdnost):
                print("<primarni_izraz> ::= " + str(djeca[0]))
                return False

            cvor.tip = "char"
            cvor.lizraz = False



        elif(djeca[0].znak == "NIZ_ZNAKOVA"):
            if not jenizznakova(djeca[0].vrijdnost):
                print("<primarni_izraz> ::= " + str(djeca[0]))
                return False

            cvor.tip = "niz(const(char))"
            cvor.lizraz = False



        elif(djeca[0].znak == "L_ZAGRADA"):
            if not provjeri(djeca[1]):
                return False

            cvor.tip = djeca[1].tip
            cvor.lizraz = djeca[1].lizraz

        
        else:
            print("POGREŠKA U <primarni_izraz>")
            return False


    elif(cvor.znak == "<postfiks_izraz>"):
        if(djeca[0].znak == "<primarni_izraz>"):
            if not provjeri(djeca[0]):
                return False

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

        
        elif(djeca[2].znak == "<izraz>"):
            if not provjeri(djeca[0]):
                return False

            if not jeNizX(djeca[0].tip): #Nije implicitno kastabilan u int (nisam siguran je li to isto kao X, tj. je li char implicitno castabilan u int u ovom)
                print("<postfiks_izraz> ::= <postfiks_izraz> " + str(djeca[1]) + " <izraz> " + str(djeca[3]))
                return False

            if not provjeri(djeca[2]):
                return False

            if not jeX(djeca[2].tip):
                print("<postfiks_izraz> ::= <postfiks_izraz> " + str(djeca[1]) + " <izraz> " + str(djeca[3]))
                return False
                
            cvor.tip = djeca[1].tip[4:(len(str)-1)]
            cvor.lizraz = not jeConstT(cvor.tip)


        elif(djeca[2].znak == "D_ZAGRADA"):
            if not provjeri(djeca[0]):
                return False

            if not (isinstance(djeca[0].tip, Funkcija) and djeca[0].tip.params == "void"):
                print("<postfiks_izraz> ::= <postfiks_izraz> " + str(djeca[1]) + " " + str(djeca[2]))
                return False

            cvor.tip = djeca[0].tip.pov
            cvor.lizraz = False


        elif(djeca[2].znak == "<lista_argumenata>"):
            if not provjeri(djeca[0]):
                return False
            
            if not provjeri(djeca[2]):
                return False
            
            if not (isinstance(djeca[0].tip, Funkcija) and isinstance(djeca[0].tip.params, list) and len(djeca[0].tip.params) == len(djeca[2].tipovi)):
                print("<postfiks_izraz> ::= <postfiks_izraz> " + str(djeca[1]) + " <lista_argumenata> " + str(djeca[3]))
                return False

            for i in range(len(djeca[2].tipovi)):
                if not ImplicitnoXToY(djeca[0].tip.params[i], djeca[2].tipovi[i]):
                    print("<postfiks_izraz> ::= <postfiks_izraz> " + str(djeca[1]) + " <lista_argumenata> " + str(djeca[3]))
                    return False

            cvor.tip = djeca[0].tip.pov
            cvor.lizraz = False


        elif(djeca[1].znak == "OP_INC" or djeca[1].znak == "OP_DEC"):
            cvor.tip = "int"
            cvor.lizraz = False

            if not provjeri(djeca[0]):
                return False

            if not djeca[0].lizraz or not jeX(djeca[0].tip): #Ponovno pretpostavka da je X jednako kao implicitno castabilan u int
                print("<postfiks_izraz> ::= <postfiks_izraz> " + str(djeca[1]))
                return False

        else:
            print("POGREŠKA U <postfiks_izraz>")
            return False

        
    elif(cvor.znak == "<lista_argumenata>"):
        if(djeca[0].znak == "<izraz_pridruzivanja>"):
            if not provjeri(djeca[0]):
                return False

            cvor.tipovi = [ djeca[0].tip ]
            

        elif(djeca[0].znak == "<lista_argumenata>"):
            if not provjeri(djeca[0]):
                return False
            
            if not provjeri(djeca[2]):
                return False
            
            cvor.tipovi = djeca[0].tipovi + [ djeca[2].tip ] 

        
        else:
            print("POGREŠKA U <lista_argumenata>")
            return False
        


    elif(cvor.znak == "<unarni_izraz>"):
        if(djeca[0].znak == "<postfiks_izraz>"):
            if not provjeri(djeca[0]):
                return False

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

        elif(djeca[1].znak == "<unarni_izraz>"):
            if not provjeri(djeca[1]):
                return False
            
            if not (djeca[1].lizraz and jeX(djeca[1].tip)):
                print("<unarni_izraz> ::= " + str(djeca[0]) + " <unarni_izraz>")
                return False

            cvor.tip = "int"
            cvor.lizraz = False


        elif(djeca[0].znak == "<unarni_operator>"):
            if not provjeri(djeca[1]):
                return False
            
            if not jeX(djeca[1].tip):
                print("<unarni_izraz> ::= <unarni_operator> <cast_izraz>")
                return False    

            cvor.tip = "int"
            cvor.lizraz = False

        else: 
            print("POGREŠKA U <unarni_izraz>")
            return False


    elif(cvor.znak == "<cast_izraz>"):
        if(djeca[0].znak == "<unarni_izraz>"):
            if not provjeri(djeca[0]):
                return False

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

        
        elif(djeca[0].znak == "L_ZAGRADA"):
            if not provjeri(djeca[1]):
                return False
            if not provjeri(djeca[3]):
                return False
            
            if not EksplicitnoXToY(djeca[3].tip, djeca[1].tip):
                print("<cast_izraz> ::= "+str(djeca[0])+" <ime_tipa> "+str(djeca[2])+" <cast_izraz>")
                return False

            cvor.tip = djeca[1].tip
            cvor.lizraz = False

        else: 
            print("POGREŠKA U <cast_izraz>")
            return False



    elif(cvor.znak == "<ime_tipa>"):
        if(djeca[0].znak == "<specifikator_tipa>"):            
            if not provjeri(djeca[0]):
                return False

            cvor.tip = djeca[0].tip

        
        elif(djeca[0].znak == "KR_CONST"):
            if not provjeri(djeca[1]):
                return False

            if (djeca[0].tip == "void"):
                print("<ime_tipa> ::= " + str(djeca[0]) + " <specifikator_tipa>")
                return False
            
            cvor.tip = "const(" + djeca[1].tip + ")"

        else:
            print("POGREŠKA U <ime_tipa>")
            return False



    elif(cvor.znak == "<specifikator_tipa>"):
        if(djeca[0].znak == "KR_VOID"):
            cvor.tip = "void"
        
        elif(djeca[0].znak == "KR_CHAR"):
            cvor.tip = "char"
        
        elif(djeca[0].znak == "KR_INT"):
            cvor.tip = "int"

        else:
            print("POGREŠKA U <specifikator_tipa>")
            return False
        


    elif(cvor.znak == "<multiplikativni izraz>"):
        if(djeca[0].znak == "<cast_izraz>"):
            if not provjeri(djeca[0]):
                return False

            cvor.tip = "void"
            cvor.lizraz = djeca[0].lizraz

        
        elif(djeca[0].znak == "<multiplikativni_izraz>"):
            if not provjeri(djeca[0]):
                return False
            if not jeX(djeca[0].tip):
                print("<multiplikativni_izraz> ::= <multiplikativni_izraz> " + str(djeca[1]) + " <cast_izraz>")
                return False
            if not provjeri(djeca[2]):
                return False
            if not jeX(djeca[2].tip):
                print("<multiplikativni_izraz> ::= <multiplikativni_izraz> " + str(djeca[1]) + " <cast_izraz>")
                return False
            
            cvor.tip = "int"
            cvor.lizraz = False


        else:
            print("POGREŠKA U <multiplikativni_izraz>")
            return False
    


    elif(cvor.znak == "<aditivni izraz>"):
        if(djeca[0].znak == "<multiplikativni_izraz>"):
            if not provjeri(djeca[0]):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

        
        elif(djeca[0].znak == "<aditivni_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = False

            if not provjeri(djeca[0]):
                return False
            if not jeX(djeca[0].tip):
                print("<aditivni_izraz> ::= <aditivni_izraz> " + str(djeca[1]) + " <multiplikativni_izraz>")
                return False
            if not provjeri(djeca[2]):
                return False
            if not jeX(djeca[2].tip):
                print("<aditivni_izraz> ::= <aditivni_izraz> " + str(djeca[1]) + " <multiplikativni_izraz>")
                return False        
        else:
            print("POGREŠKA U <aditivni_izraz>")
            return False
        

    elif(cvor.znak == "<odnosni_izraz>"):
        if(djeca[0].znak == "<aditivni_izraz>"):
            if not provjeri(djeca[0]):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
        

        elif(djeca[0].znak == "<odnosni_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = False

            if not provjeri(djeca[0]):
                return False
            if not jeX(djeca[0].tip):
                print("<odnosni_izraz> ::= <odnosni_izraz> " + str(djeca[1]) + " <aditivni_izraz>")
                return False
            if not provjeri(djeca[2]):
                return False
            if not jeX(djeca[2].tip):
                print("<odnosni_izraz> ::= <odnosni_izraz> " + str(djeca[1]) + " <aditivni_izraz>")
                return False
        
        else:
            print("POGREŠKA U <odnosni_izraz>")
            return False



    elif(cvor.znak == "<jednakosni_izraz>"):
        if(djeca[0].znak == "<odnosni_izraz>"):        
            if not provjeri(djeca[0]):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
                
        
        elif(djeca[0].znak == "<jednakosni_izraz>"):   
            if not provjeri(djeca[0]):
                return False
            if not jeX(djeca[0].tip):
                print("<jednakosni_izraz> ::= <jednakosni_izraz> " + str(djeca[1]) + " <odnosni_izraz>")
                return False
            if not provjeri(djeca[2]):
                return False
            if not jeX(djeca[2].tip):
                print("<jednakosni_izraz> ::= <jednakosni_izraz> " + str(djeca[1]) + " <odnosni_izraz>")
                return False   

            cvor.tip = "int"
            cvor.lizraz = False

        else:
            print("POGREŠKA U <jednakosni_izraz>")
            return False
    

    
    elif(cvor.znak == "<bin_i_izraz>"):
        if(djeca[0].znak == "<jednakosni_izraz>"):       
            if not provjeri(djeca[0]):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

        
        elif(djeca[0].znak == "<bin_i_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = False
        
            if not provjeri(djeca[0]):
                return False
            if not jeX(djeca[0].tip):
                print("<bin_i_izraz> ::= <bin_i_izraz> " + str(djeca[1]) + " <jednakosni_izraz>")
                return False
            if not provjeri(djeca[2]):
                return False
            if not jeX(djeca[2].tip):
                print("<bin_i_izraz> ::= <bin_i_izraz> " + str(djeca[1]) + " <jednakosni_izraz>")
                return False
        
        else:
            print("POGREŠKA U <bin_i_izraz>")
            return False

    
    elif(cvor.znak == "<bin_xili_izraz>"):
        if(djeca[0].znak == "<bin_i_izraz>"):       
            if not provjeri(djeca[0]):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
        
        elif(djeca[0].znak == "<bin_xili_izraz>"):
            if not provjeri(djeca[0]):
                return False
            if not jeX(djeca[0].tip):
                print("<bin_xili_izraz> ::= <bin_xili_izraz> "+str(djeca[1])+ " <bin_i_izraz>")
                return False
            if not provjeri(djeca[2]):
                return False
            if not jeX(djeca[2].tip):
                print("<bin_xili_izraz> ::= <bin_xili_izraz> "+str(djeca[1])+ " <bin_i_izraz>")
                return False
            cvor.tip = "int"
            cvor.lizraz = False

        
        else:
            print("POGREŠKA U <bin_xili_izraz>")
            return False
    
    elif(cvor.znak == "<bin_ili_izraz>"):
        if(djeca[0].znak == "<bin_xili_izraz>"):        
            if not provjeri(djeca[0]):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
        
        elif(djeca[0].znak == "<bin_ili_izraz>"):
            if not provjeri(djeca[0]):
                return False
            if not jeX(djeca[0].tip):
                print("<bin_ili_izraz> ::= <bin_ili_izraz> "+str(djeca[1])+" <bin_xili_izraz>")
                return False

            if not provjeri(djeca[2]):
                return False
            if not jeX(djeca[2].tip):
                print("<bin_ili_izraz> ::= <bin_ili_izraz> "+str(djeca[1])+" <bin_xili_izraz>")
                return False        
            cvor.tip = "int"
            cvor.lizraz = False
        
        else:
            print("POGREŠKA U <bin_ili_izraz>")
            return False
    
    elif(cvor.znak == "<log_i_izraz>"):
        if(djeca[0].znak == "<bin_ili_izraz>"):       
            if not provjeri(djeca[0]):
                return False

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
        

        elif(djeca[0].znak == "<log_i_izraz>"):
            if not provjeri(djeca[0]):
                return False
            if not jeX(djeca[0].tip):
                print("<log_i_izraz> ::= <log_i_izraz> "+str(djeca[1])+" <bin_ili_izraz>")
                return False
            if not provjeri(djeca[2]):
                return False
            if not jeX(djeca[2].tip):
                print("<log_i_izraz> ::= <log_i_izraz> "+str(djeca[1])+" <bin_ili_izraz>")
                return False

            cvor.tip = "int"
            cvor.lizraz = False

        else:
            print("POGREŠKA U <log_i_izraz>")
            return False
    

    elif(cvor.znak == "<log_ili_izraz>"):
        if(djeca[0].znak == "<log_i_izraz>"):       
            if not provjeri(djeca[0]):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

        
        elif(djeca[0].znak == "<log_ili_izraz>"):
            if not provjeri(djeca[0]):
                return False
            if not jeX(djeca[0].tip):
                print("<log_ili_izraz> ::= <log_ili_izraz> "+str(djeca[1])+" <log_i_izraz>")
                return False
            if not provjeri(djeca[2]):
                return False
            if not jeX(djeca[2].tip):
                print("<log_ili_izraz> ::= <log_ili_izraz> "+str(djeca[1])+" <log_i_izraz>")
                return False
            
            cvor.tip = "int"
            cvor.lizraz = False

        else:
            print("POGREŠKA U <log_ili_izraz>")
            return False

    elif(cvor.znak == "<izraz_pridruzivanja>"):
        if(djeca[0].znak == "<log_ili_izraz>"):        
            if not provjeri(djeca[0]):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz


        elif(djeca[0].znak == "<postfiks_izraz>"):
            if not provjeri(djeca[0]):
                return False
            if not djeca[0].lizraz:
                print("<izraz_pridruzivanja> ::= <postfiks_izraz> "+str(djeca[1])+" <izraz_pridruzivanja>")
                return False
            if not provjeri(djeca[2]):
                return False
            if not ImplicitnoXToY(djeca[2].tip, djeca[0].tip):
                print("<izraz_pridruzivanja> ::= <postfiks_izraz> "+str(djeca[1])+" <izraz_pridruzivanja>")
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = False

        else:
            print("POGREŠKA U <izraz_pridruzivanja>")
            return False
    
    elif(cvor.znak == "<izraz>"):
        if(djeca[0].znak == "<izraz_pridruzivanja>"):        
            if not provjeri(djeca[0]):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

        
        elif(djeca[0].znak == "<izraz>"):
            if not provjeri(djeca[0]):
                return False
            if not provjeri(djeca[2]):
                return False

            cvor.tip = djeca[0].tip
            cvor.lizraz = False

        else:
            print("POGREŠKA U <izraz>")
            return False
    
    #4.4.5 Naredbena struktura programa
    elif(cvor.znak == "<slozena_naredba>"):
        if(djeca[1].znak == "<lista_naredbi>"):
            if not provjeri(djeca[1]):
                return False
        
        elif(djeca[1].znak == "<lista_deklaracija>"):
            if not provjeri(djeca[1]):
                return False
            if not provjeri(djeca[2]):
                return False

        else:
            print("POGREŠKA U <slozena_naredba>")
            return False
    
    elif(cvor.znak == "<lista_naredbi>"):
        if(djeca[0].znak == "<naredba>"):
            if not provjeri(djeca[0]):
                return False

        elif(djeca[1].znak == "<naredba>"):
            if not provjeri(djeca[0]):
                return False
            if not provjeri(djeca[1]):
                return False

        else:
            print("POGREŠKA U <lista_naredbi>")
            return False

    #nesto <naredba> potencijalno zajebaje, str 63

    elif(cvor.znak == "<izraz_naredba>"):
        if(djeca[0].znak == "TOCKAZAREZ"):
            cvor.tip = "int"

        elif(djeca[0].znak == "<izraz>"):
            cvor.tip = djeca[0].tip

            if not provjeri(djeca[0]):
                return False

        else:
            print("POGREŠKA U <izraz_naredba>")
            return False
    
    elif(cvor.znak == "<naredba_grananja>"):
        if(len(djeca) == 5):
            if not provjeri(djeca[2]):
                return False

            if not jeX(djeca[2].tip):
                print("<naredba_grananja> ::= "+str(djeca[0])+" "+str(djeca[1])+" <izraz> "+str(djeca[3])+" <naredba>")
                return False

            if not provjeri(djeca[4]):
                return False
        

        elif(len(djeca) == 7):
            if not provjeri(djeca[2]):
                return False

            if not jeX(djeca[2].tip):
                print("<naredba_grananja> ::= " + str(djeca[0]) + " <izraz> "+str(djeca[2])+" <naredba> " +str(djeca[4])+ " <naredba>")
                return False

            if not provjeri(djeca[4]):
                return False
            if not provjeri(djeca[6]):
                return False
        
        else:
            print("POGREŠKA U <naredba_grananja>")
            return False
        
    elif(cvor.znak == "<naredba_petlje>"):
        if(djeca[0].znak == "KR_WHILE"):
            if not provjeri(djeca[2]):
                return False
            if not jeX(djeca[2].tip):
                print("<naredba_petlje> ::= "+str(djeca[0])+" "+str(djeca[1])+" <izraz> "+str(djeca[3])+" <naredba>")
                return False
            if not provjeri(djeca[4]):
                return False
        
        elif(djeca[4] == "D_ZAGRADA"):
            if not provjeri(djeca[2]):
                return False
            if not provjeri(djeca[3]):
                return False
            if not jeX(djeca[3].tip):
                print("<naredba_petlje> ::= "+str(djeca[0])+" "+str(djeca[1])+" <izraz_naredba> <izraz_naredba> "+str(djeca[4])+" <naredba>")
                return False
            if not provjeri(djeca[5]):
                return False

        elif(djeca[4] == "<izraz>"):
            if not provjeri(djeca[2]):
                return False
            if not provjeri(djeca[3]):
                return False
            if not jeX(djeca[3].tip):
                print("<naredba_petlje> ::= "+str(djeca[0])+" "+str(djeca[1])+" <izraz_naredba> <izraz_naredba> <izraz> "+str(djeca[5])+" <naredba>")
                return False
            if not provjeri(djeca[4]):
                return False
            if not provjeri(djeca[6]):
                return False

        else:
            print("POGREŠKA U <naredba_petlje>")
            return False
    
    elif(cvor.znak == "<naredba_skoka>"):
        if(djeca[0].znak == "KR_CONTINUE" or djeca[0].znak == "KR_BREAK"):
            #TODO naredba se nalazi unutar petlje ili unutar bloka koji je ugnijeˇzden u petlji
            pass

        elif(djeca[1].znak == "TOCKAZAREZ"):
            #TODO 1. naredba se nalazi unutar funkcije tipa funkcija(params → void)
            pass

        elif(djeca[1].znak == "<izraz>"):
            if not provjeri(djeca[1]):
                return False
            #TODO naredba se nalazi unutar funkcije tipa funkcija(params → pov) i vrijedi <izraz>.tip ∼ pov
        
        else:
            print("POGREŠKA U <naredba_skoka>")
            return False
    
    elif(cvor.znak == "<prijevodna_jedinica>"):
        if(djeca[0].znak == "<vanjska_deklaracija>"):
            if not provjeri(djeca[0]):
                return False
        
        elif(djeca[0].znak == "<prijevodna_jedinica>"):
            if not provjeri(djeca[0]):
                return False
            if not provjeri(djeca[1]):
                return False
        
        else:
            print("POGREŠKA U <prijevodna_jedinica>")
            return False

    #TODO 4.4.6 Deklaracije i definicije
    elif(cvor.znak == "<definicija_funkcije>"):
        if(djeca[3].znak == "KR_VOID"):
            if not provjeri(djeca[0]):
                return False
            if not jeConstT(djeca[0].tip):
                print("<definicija_funkcije> ::= <ime_tipa> "+djeca[1]+" "+djeca[2]+" "+djeca[3]+" "+djeca[4]+" <slozena_naredba>")
                return False
            if (tablica_IDN[djeca[1].vrijednost] != None and isinstance(tablica_IDN[djeca[1].vrijednost], Funkcija) and tablica_IDN[djeca[1].vrijednost].definirana):
                print("<definicija_funkcije> ::= <ime_tipa> "+djeca[1]+" "+djeca[2]+" "+djeca[3]+" "+djeca[4]+" <slozena_naredba>")
                return False  
            if not (tablica_IDN[djeca[1].vrijednost] != None and isinstance(tablica_IDN[djeca[1].vrijednost], Funkcija) and tablica_IDN[djeca[1].vrijednost].params == "void" and tablica_IDN[djeca[1].vrijednost].pov == djeca[0].tip):
                print("<definicija_funkcije> ::= <ime_tipa> "+djeca[1]+" "+djeca[2]+" "+djeca[3]+" "+djeca[4]+" <slozena_naredba>")
                return False  
            
            if tablica_IDN[djeca[1].vrijednost] == None:
                tablica_IDN[djeca[1].vrijednost] = Funkcija("void", djeca[0].tip, True)
            else:
                tablica_IDN[djeca[1].vrijednost].definirana = True
            
            if not provjeri(djeca[5]):
                return False
        
        elif(djeca[3].znak == "<lista_parametara>"):
            if not provjeri(djeca[0]):
                return False
            if not jeConstT(djeca[0].tip):
                print("<definicija_funkcije> ::= <ime_tipa> "+str(djeca[1])+" "+str(djeca[2])+" <lista_parametara> "+str(djeca[4])+" <slozena_naredba>")
                return False
            if (tablica_IDN[djeca[1].vrijednost] != None and isinstance(tablica_IDN[djeca[1].vrijednost], Funkcija) and tablica_IDN[djeca[1].vrijednost].definirana):
                print("<definicija_funkcije> ::= <ime_tipa> "+djeca[1]+" "+djeca[2]+" "+djeca[3]+" "+djeca[4]+" <slozena_naredba>")
                return False  
            if not provjeri(djeca[2]):
                return False
            if not (tablica_IDN[djeca[1].vrijednost] != None and isinstance(tablica_IDN[djeca[1].vrijednost], Funkcija) and tablica_IDN[djeca[1].vrijednost].params == djeca[3].tipovi and tablica_IDN[djeca[1].vrijednost].pov == djeca[0].tip):
                print("<definicija_funkcije> ::= <ime_tipa> "+djeca[1]+" "+djeca[2]+" "+djeca[3]+" "+djeca[4]+" <slozena_naredba>")
                return False  
            
            if tablica_IDN[djeca[1].vrijednost] == None:
                tablica_IDN[djeca[1].vrijednost] = Funkcija("void", djeca[0].tip, True)
            else:
                tablica_IDN[djeca[1].vrijednost].definirana = True
            
            nova_tablica = copy.deepcopy(tablica_IDN)
            for i in range(len(djeca[3].tipovi)):
                nova_tablica[djeca[3].imena[i]] = djeca[3].tipovi[i]

            if not provjeri(djeca[5], nova_tablica):
                return False
            

        else:
            print("POGREŠKA U <prijevodna_jedinica>")
            return False
        
    elif(cvor.znak == "<lista_parametara>"):
        if(djeca[0].znak  == "<deklaracija_parametra>"):
            if not provjeri(djeca[0]):
                return False
            cvor.tipovi = [ djeca[0].tip ]
            cvor.tipovi = [ djeca[0].ime ]
        
        elif(djeca[0].znak == "<lista_parametara>"):
            if not provjeri(djeca[0]):
                return False
            if not provjeri(djeca[2]):
                return False
            if djeca[2].ime in djeca[0].imena:
                print("<lista_parametara> ::= <lista_parametara> "+str(djeca[1])+" <deklaracija_parametra>")
                return False

            cvor.tipovi = djeca[0].tipovi + [ djeca[2].tip ]
            cvor.imena = djeca[0].imena + [ djeca[2].ime ]

        else:
            print("POGREŠKA U <lista_parametara>")
            return False
    
    elif(cvor.znak == "<deklaracija_parametra>"):
        if(len(djeca) == 2):
            if not provjeri(djeca[0]):
                return False
            if djeca[0].tip == "void":
                print("<deklaracija_parametra> ::= <ime_tipa> " +str(djeca[1]))
                return False
            
            cvor.tip = djeca[0].tip
            cvor.ime = djeca[1].vrijednost
        
        elif(len(djeca) == 4):
            if not provjeri(djeca[0]):
                return False
            if djeca[0].tip == "void":
                print("<deklaracija_parametra> ::= <ime_tipa> "+str(djeca[1])+" "+str(djeca[2])+" "+str(djeca[3]))
                return False
            
            cvor.tip = "niz(" + djeca[0].tip + ")"
            cvor.ime = djeca[1].vrijednost
        
        else:
            print("POGREŠKA U <deklaracija_parametra>")
            return False
    
    elif(cvor.znak == "<lista_deklaracija>"):
        if(djeca[0].znak == "<deklaracija>"):
            if not provjeri(djeca[0]): 
                return False
        
        elif(djeca[1].znak == "<deklaracija>"):
            if not provjeri(djeca[0]):
                return False
            if not provjeri(djeca[1]):
                return False

        else:
            print("POGREŠKA U <lista_deklaracija>")
            return False

    elif(cvor.znak == "<deklaracija>"):
        if(djeca[0].znak == "<ime_tipa>"):
            if not provjeri(djeca[0]): 
                return False      
            #TODO provjeri(<lista_init_deklaratora>) uz nasljedno svojstvo <lista_init_deklaratora>.ntip ← <ime_tipa>.tip

            # Specifiˇcnost toˇcke 2 je nasljedno svojstvo ntip nezavrˇsnog znaka <lista_init_deklaratora>.
            # Svojstvo ntip sluˇzi za prijenos jednog dijela informacije o tipu u sve deklaratore. Za varijable brojevnog 
            # tipa ntip ´ce biti cijeli tip, za nizove ´ce biti tip elementa niza, a za funkcije ´ce biti povratni tip.
        
        else:
            print("POGREŠKA U <deklaracija>")
            return False

    elif(cvor.znak == "<lista_init_deklaratora>"):
        if(djeca[0].znak == "<init_deklarator>"):
            #TODO provjeri(<init_deklarator>) uz nasljedno svojstvo <<init_deklarator>>.ntip ← <lista_init_deklaratora>.tip
            gas = 0

        elif(djeca[0].znak == "<init_deklarator>"): #cudno je numerirano nesto u ovoj produkciji str 68 pa samo ostavljam natuknicu
            #TODO provjeri(<lista_init_deklaratora>2) uz nasljedno svojstvo <lista_init_deklaratora>2.ntip ← <lista_init_deklaratora>1.ntip
            #TODO provjeri(<init_deklarator>) uz nasljedno svojstvo <init_deklarator>.ntip ← <lista_init_deklaratora>1.ntip
            gas = 0
        
        else:
            print("POGREŠKA U <lista_init_deklaratora>")
            return False
    
    elif(cvor.znak == "<init_deklarator>"):
        if(len(djeca) == 1):
            #TODO provjeri(<izravni_deklarator>) uz nasljedno svojstvo <izravni_deklarator>.ntip ← <init_deklarator>.ntip
            if jeConstT(djeca[0].tip) or jeNizConstT(djeca[0].tip):
                return False
    
        elif(len(djeca) == 3):
            #TODO provjeri(<izravni_deklarator>) uz nasljedno svojstvo <izravni_deklarator>.ntip ← <init_deklarator>.ntip
            if not provjeri(djeca[2]):
                return False

            if jeT(djeca[0].tip) or jeConstT(djeca[0].tip):
                #TODO <inicijalizator>.tip ∼ T
                gas = 0
            elif jeNizT(djeca[0].tip) or jeNizConstT(djeca[0].tip):
                #TODO <inicijalizator>.br-elem ≤ <izravni_deklarator>.br-elem za svaki U iz <inicijalizator>.tipovi vrijedi U ∼ T
                gas = 0
            else:
                return False 
        
        else:
            print("POGREŠKA U <init_deklarator>")
            return False
    
    elif(cvor.znak == "<izravni_deklarator>"):
        if(len(djeca) == 1):
            #TODO ntip != void
            #TODO IDN.ime nije deklarirano u lokalnom djelokrugu
            #TODO zabiljeˇzi deklaraciju IDN.ime s odgovaraju´cim tipom

            #TODO tip ← ntip
            gas = 0

        elif(djeca[2].znak == "BROJ"):
            #TODO ntip != void
            #TODO IDN.ime nije deklarirano u lokalnom djelokrugu
            #TODO zabiljeˇzi deklaraciju IDN.ime s odgovaraju´cim tipom

            #TODO tip ← ntip
            #TODO br-elem ← BROJ.vrijednost
            gas = 0

        elif(djeca[2].znak == "KR_VOID"):
            #TODO ako je IDN.ime deklarirano u lokalnom djelokrugu, tip prethodne deklaracije je jednak funkcija(void → ntip)
            #TODO zabiljeˇzi deklaraciju IDN.ime s odgovaraju´cim tipom ako ista funkcija ve´c nije deklarirana u lokalnom djelokrugu

            #TODO tip ← funkcija(void → ntip)
            gas = 0
        
        elif(djeca[2].znak == "<lista_parametara>"):
            if not provjeri(djeca[3]):
                return False
            #TODO ako je IDN.ime deklarirano u lokalnom djelokrugu, tip prethodne deklaracije je jednak funkcija(<lista_parametara>.tipovi → ntip)
            #TODO zabiljeˇzi deklaraciju IDN.ime s odgovaraju´cim tipom ako ista funkcija ve´c nije deklarirana u lokalnom djelokrugu

            #TODO tip ← funkcija(<lista_parametara>.tipovi → ntip)

        else:
            print("POGREŠKA U <izravni_deklarator>")
            return False
    
    elif(cvor.znak == "<izravni_deklarator>"):
        if not provjeri(djeca[0]):
            return False

        #TODO ako je <izraz_pridruzivanja> ∗⇒ NIZ_ZNAKOVA:
            # br-elem ← duljina niza znakova + 1
            # tipovi ← lista duljine br-elem, svi elementi su char
        else:
            cvor.tip = djeca[0].tip

    return True
    
    

