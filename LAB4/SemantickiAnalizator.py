import copy
from Stablo import *


allDeclared = True 
whitespaces = 0

def jebroj(broj):
    if not broj.isdigit():
        return False
    broj = int(broj)
    return (-2147483648 <= broj and broj <= 2147483647)

def je1do1024(broj):
    if not broj.isdigit():
        return False
    broj = int(broj)
    return (0 < broj and broj <= 1024)


# Ova funkcija je dosta sussy, idem ja ponovno napisat
# def jeznak(znak):
#     if znak[0] != '\"':
#         return False
#     if znak[len(znak) - 1] != "\"":
#         return False
#     znak = znak[1:(len(znak)-1)]
#     if(len(znak) == 1 and znak[0] != "\\"):
#         return True
#     elif(len(znak) == 2 and znak[0] == "\\" and znak[1] in ("t", "n", "0", "\'", "\"", "\\")):
#         return False
#     return False

def jeznak(znak):
    if znak[0] == '\"': return False
    znak = znak[1:len(znak) - 1]
    return len(znak) == 1 or (len(znak) == 2 and znak[0] == "\\" and znak[1] in ("t", "n", "0", "\'", "\"", "\\"))


def jenizznakova(niz):
    if niz[0] != '\"':
        return False
    if niz[len(niz) - 1] != "\"":
        return False

    it = 0
    while("\\" in niz[it:]):
        it = niz[it:].index("\\")
        if it + 1 == len(niz) or niz[it + 1] not in ("t", "n", "0", "\'", "\"", "\\"):
            return False
        it += 2
    return True

def jeNizX(str):
    return not isinstance(str, Funkcija) and len(str) > 5 and str[0:4] == "niz(" and str[len(str)-1] == ")" and jeX(str[4:(len(str)-1)])

def jeNizT(str):
    return not isinstance(str, Funkcija) and str[0:4] == "niz(" and str[len(str)-1] == ")" and jeT(str[4:(len(str)-1)])

def jeNizConstX(str):
    return not isinstance(str, Funkcija) and str[0:4] == "niz(" and str[len(str)-1] == ")" and jeConstX(str[4:(len(str)-1)])

def jeNizConstT(str):
    return not isinstance(str, Funkcija) and str[0:4] == "niz(" and str[len(str)-1] == ")" and jeConstT(str[4:(len(str)-1)])

# Ovo je suvisno
def jeConstX(str):
    return not isinstance(str, Funkcija) and str[0:6] == "const(" and str[len(str)-1] == ")" and jeX(str[6:(len(str)-1)])
#---------------

def jeConstT(str):
    return not isinstance(str, Funkcija) and str[0:6] == "const(" and str[len(str)-1] == ")" and jeT(str[6:(len(str)-1)])

def jeX(str):
    #return str == "const(int)" or str == "const(char)" or str == "int" or str == "char" or str == "X"
    return jeT(str) or jeConstT(str)

def jeT(str):
    return str == "int" or str == "char" or str == "T"

def ImplicitnoXToY(x, y): # Gleda vrijedi li x ~ y, nisam sto posto ako je tranzitivno okruzenje potpuno, cini mi se da je, ali mi špurijus govori da nije
    #return x == y or jeT(x) and jeConstT(y) and x != "char" and y != int or jeConstT(x) and jeT(y) and x != "char" and y != int  or x == "char" and y == "int" or jeNizT(x) and jeNizConstT(y) and x != "char" and y != int
    #return (x == y or jeT(x) and jeConstT(y) or jeConstT(x) and jeT(y) or jeNizT(x) and jeNizConstT(y)) and x != "int" and y != "char" or x == "char" and y == "int"
    #return (x == y or jeT(x) and (jeConstT(y) or jeT(y)) or jeConstT(x) and (jeT(y) or jeConstT(y)) or jeNizT(x) and (jeNizConstT(y) or jeNizT(y))) and x != "int" and y != "char" or x == "char" and y == "int"
    return (jeT(x) and jeX(y) or jeConstT(x) and jeX(y) or jeNizT(x) and jeNizX(y)) and not (x == "int" and y == "char")

def EksplicitnoXToY(x, y):
    return jeX(x) and jeX(y)
    #return x == "char" and y == "int"
    #return ImplicitnoXToY(x, y) #? ovako radi ig

def checkFunkcije(tablica_IDN, djelokrug):
    global allDeclared
    for value in tablica_IDN.values():
        if isinstance(value.tip, Funkcija) and not value.tip.definirana and djelokrug[-1] == value.djelokrug:
            allDeclared = False
            break

def zavrsnaProvjera(tablica_IDN, djelokrug):
    checkFunkcije(tablica_IDN, djelokrug)
    if not ("main" in tablica_IDN.keys() and isinstance(tablica_IDN["main"].tip, Funkcija) and tablica_IDN["main"].tip.params == "void" and tablica_IDN["main"].tip.pov == "int"):
        print("main")
    elif not allDeclared:
        print("funkcija")
    else:
        print("Uspijeh")




def provjeri(cvor, tablica_IDN, djelokrug):
    djeca = cvor.djeca

    if(cvor.znak == "<primarni_izraz>"):
        if(djeca[0].znak == "IDN"):
            tip = tablica_IDN[djeca[0].vrijednost].tip
            cvor.tip = tip
            cvor.lizraz = not isinstance(tip, Funkcija) and jeT(tip) 

        elif(djeca[0].znak == "BROJ"):
            cvor.tip = "int"
            cvor.lizraz = False


        elif(djeca[0].znak == "ZNAK"):
            cvor.tip = "char"
            cvor.lizraz = False


        elif(djeca[0].znak == "NIZ_ZNAKOVA"):
            cvor.tip = "niz(const(char))"
            cvor.lizraz = False
            cvor.brelem = len(djeca[0].vrijednost) - 2
            

        elif(djeca[0].znak == "L_ZAGRADA"):
            provjeri(djeca[1], tablica_IDN, djelokrug)
            
            cvor.tip = djeca[1].tip
            cvor.lizraz = djeca[1].lizraz



    elif(cvor.znak == "<postfiks_izraz>"):
        if(djeca[0].znak == "<primarni_izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem
        

        elif(djeca[1].znak == "OP_INC" or djeca[1].znak == "OP_DEC"):
            cvor.tip = "int"
            cvor.lizraz = False

            provjeri(djeca[0], tablica_IDN, djelokrug)
       

        elif(djeca[2].znak == "<izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)

            cvor.tip = djeca[0].tip[4:(len(djeca[0].tip)-1)]
            cvor.lizraz = not jeConstT(cvor.tip)


        elif(djeca[2].znak == "D_ZAGRADA"):
            provjeri(djeca[0], tablica_IDN, djelokrug)

            cvor.tip = djeca[0].tip.pov
            cvor.lizraz = False
            cvor.jePozivFunkcije = True

        elif(djeca[2].znak == "<lista_argumenata>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)

            cvor.tip = djeca[0].tip.pov
            cvor.lizraz = False
            cvor.jePozivFunkcije = True


        
    elif(cvor.znak == "<lista_argumenata>"):
        if(djeca[0].znak == "<izraz_pridruzivanja>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)

            cvor.tipovi = [ djeca[0].tip ]
            

        elif(djeca[0].znak == "<lista_argumenata>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)
            
            cvor.tipovi = djeca[0].tipovi + [ djeca[2].tip ] 
        


    elif(cvor.znak == "<unarni_izraz>"):
        if(djeca[0].znak == "<postfiks_izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem


        elif(djeca[1].znak == "<unarni_izraz>"):
            provjeri(djeca[1], tablica_IDN, djelokrug)
            
            cvor.tip = "int"
            cvor.lizraz = False


        elif(djeca[0].znak == "<unarni_operator>"):
            provjeri(djeca[1], tablica_IDN, djelokrug)
            
            cvor.tip = "int"
            cvor.lizraz = False



    elif(cvor.znak == "<cast_izraz>"):
        if(djeca[0].znak == "<unarni_izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem

        
        elif(djeca[0].znak == "L_ZAGRADA"):
            provjeri(djeca[1], tablica_IDN, djelokrug)
            provjeri(djeca[3], tablica_IDN, djelokrug)

            cvor.tip = djeca[1].tip
            cvor.lizraz = False



    elif(cvor.znak == "<ime_tipa>"):
        if(djeca[0].znak == "<specifikator_tipa>"):            
            provjeri(djeca[0], tablica_IDN, djelokrug)

            cvor.tip = djeca[0].tip

        
        elif(djeca[0].znak == "KR_CONST"):
            provjeri(djeca[1], tablica_IDN, djelokrug)

            if (djeca[0].tip == "void"):
                print("<ime_tipa> ::= " + str(djeca[0]) + " <specifikator_tipa>")
                return False
            
            cvor.tip = "const(" + djeca[1].tip + ")"



    elif(cvor.znak == "<specifikator_tipa>"):
        if(djeca[0].znak == "KR_VOID"):
            cvor.tip = "void"
        

        elif(djeca[0].znak == "KR_CHAR"):
            cvor.tip = "char"
        

        elif(djeca[0].znak == "KR_INT"):
            cvor.tip = "int"


    elif(cvor.znak == "<multiplikativni_izraz>"):
        if(djeca[0].znak == "<cast_izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem


        elif(djeca[0].znak == "<multiplikativni_izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)
            
            cvor.tip = "int"
            cvor.lizraz = False



    elif(cvor.znak == "<aditivni_izraz>"):
        if(djeca[0].znak == "<multiplikativni_izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem
        

        elif(djeca[0].znak == "<aditivni_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = False

            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)



    elif(cvor.znak == "<odnosni_izraz>"):
        if(djeca[0].znak == "<aditivni_izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem


        elif(djeca[0].znak == "<odnosni_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = False

            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)



    elif(cvor.znak == "<jednakosni_izraz>"):
        if(djeca[0].znak == "<odnosni_izraz>"):        
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem    
        

        elif(djeca[0].znak == "<jednakosni_izraz>"):   
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)

            cvor.tip = "int"
            cvor.lizraz = False


    
    elif(cvor.znak == "<bin_i_izraz>"):
        if(djeca[0].znak == "<jednakosni_izraz>"):       
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem
        

        elif(djeca[0].znak == "<bin_i_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = False
        
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)



    elif(cvor.znak == "<bin_xili_izraz>"):
        if(djeca[0].znak == "<bin_i_izraz>"):       
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem


        elif(djeca[0].znak == "<bin_xili_izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)

            cvor.tip = "int"
            cvor.lizraz = False

   

    elif(cvor.znak == "<bin_ili_izraz>"):
        if(djeca[0].znak == "<bin_xili_izraz>"):        
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem
        
        elif(djeca[0].znak == "<bin_ili_izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)
            cvor.tip = "int"
            cvor.lizraz = False

    

    elif(cvor.znak == "<log_i_izraz>"):
        if(djeca[0].znak == "<bin_ili_izraz>"):       
            provjeri(djeca[0], tablica_IDN, djelokrug)

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem


        elif(djeca[0].znak == "<log_i_izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)

            cvor.tip = "int"
            cvor.lizraz = False



    elif(cvor.znak == "<log_ili_izraz>"):
        if(djeca[0].znak == "<log_i_izraz>"):       
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem
        

        elif(djeca[0].znak == "<log_ili_izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)
            
            cvor.tip = "int"
            cvor.lizraz = False



    elif(cvor.znak == "<izraz_pridruzivanja>"):
        if(djeca[0].znak == "<log_ili_izraz>"):        
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem 


        elif(djeca[0].znak == "<postfiks_izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = False


    
    elif(cvor.znak == "<izraz>"):
        if(djeca[0].znak == "<izraz_pridruzivanja>"):        
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

        
        elif(djeca[0].znak == "<izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)

            cvor.tip = djeca[0].tip
            cvor.lizraz = False



    #4.4.5 Naredbena struktura programa
    elif(cvor.znak == "<slozena_naredba>"):
        if(djeca[1].znak == "<lista_naredbi>"):
            provjeri(djeca[1], copy.deepcopy(tablica_IDN), djelokrug)
        

        elif(djeca[1].znak == "<lista_deklaracija>"):
            nova_tablica = copy.deepcopy(tablica_IDN)
            provjeri(djeca[1], nova_tablica, djelokrug)
            provjeri(djeca[2], nova_tablica, djelokrug)


    
    elif(cvor.znak == "<lista_naredbi>"):
        if(djeca[0].znak == "<naredba>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)


        elif(djeca[0].znak == "<lista_naredbi>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[1], tablica_IDN, djelokrug)



    elif(cvor.znak == "<naredba>"):
        if djeca[0].znak == "<slozena_naredba>" or djeca[0].znak == "<naredba_petlje>":
            provjeri(djeca[0], copy.deepcopy(tablica_IDN), djelokrug[:] + [djelokrugPodatak("BLOK", len(djelokrug) + 1)])
        else:
            provjeri(djeca[0], tablica_IDN, djelokrug)



    elif(cvor.znak == "<izraz_naredba>"):
        if(djeca[0].znak == "TOCKAZAREZ"):
            cvor.tip = "int"


        elif(djeca[0].znak == "<izraz>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)

            cvor.tip = djeca[0].tip



    elif(cvor.znak == "<naredba_grananja>"):
        if(len(djeca) == 5):
            provjeri(djeca[2], tablica_IDN, djelokrug)
            provjeri(djeca[4], tablica_IDN, djelokrug)
        

        elif(len(djeca) == 7):
            provjeri(djeca[2], tablica_IDN, djelokrug)
            provjeri(djeca[4], tablica_IDN, djelokrug)
            provjeri(djeca[6], tablica_IDN, djelokrug)



    elif(cvor.znak == "<naredba_petlje>"):
        if(djeca[0].znak == "KR_WHILE"):
            provjeri(djeca[2], tablica_IDN, djelokrug)
            provjeri(djeca[4], tablica_IDN, djelokrug[:] + [djelokrugPodatak("PETLJA", len(djelokrug) + 1)])
        

        elif(djeca[4].znak == "D_ZAGRADA"):
            provjeri(djeca[2], tablica_IDN, djelokrug)
            provjeri(djeca[3], tablica_IDN, djelokrug)
            provjeri(djeca[5], tablica_IDN, djelokrug[:] + [djelokrugPodatak("PETLJA", len(djelokrug) + 1)])


        elif(djeca[4].znak == "<izraz>"):
            provjeri(djeca[2], tablica_IDN, djelokrug)
            provjeri(djeca[3], tablica_IDN, djelokrug)
            provjeri(djeca[4], tablica_IDN, djelokrug)
            provjeri(djeca[6], tablica_IDN, djelokrug[:] + [djelokrugPodatak("PETLJA", len(djelokrug) + 1)])



    elif(cvor.znak == "<naredba_skoka>"):
        if(djeca[0].znak == "KR_CONTINUE" or djeca[0].znak == "KR_BREAK"):
            pass


        elif(djeca[1].znak == "TOCKAZAREZ"):
            pass


        elif(djeca[1].znak == "<izraz>"):
            provjeri(djeca[1], tablica_IDN, djelokrug)



    elif(cvor.znak == "<prijevodna_jedinica>"):
        if(djeca[0].znak == "<vanjska_deklaracija>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
        

        elif(djeca[0].znak == "<prijevodna_jedinica>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[1], tablica_IDN, djelokrug)



    elif(cvor.znak == "<vanjska_deklaracija>"):
        provjeri(djeca[0], tablica_IDN, djelokrug)



    #4.4.6 Deklaracije i definicije
    elif(cvor.znak == "<definicija_funkcije>"):
        if(djeca[3].znak == "KR_VOID"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
                  
            if not djeca[1].vrijednost in tablica_IDN.keys():
                tablica_IDN[djeca[1].vrijednost] =tablicaPodatak(Funkcija("void", djeca[0].tip, True), djelokrug[-1])
            else:
                tablica_IDN[djeca[1].vrijednost].tip.definirana = True
            
            provjeri(djeca[5], copy.deepcopy(tablica_IDN), djelokrug[:] + [djelokrugPodatak(Funkcija("void", djeca[0].tip), len(djelokrug)+1)])
        

        elif(djeca[3].znak == "<lista_parametara>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[3], tablica_IDN, djelokrug)
            
            if not djeca[1].vrijednost in tablica_IDN.keys():
                tablica_IDN[djeca[1].vrijednost] = tablicaPodatak(Funkcija(djeca[3].tipovi, djeca[0].tip, True), djelokrug[-1])
            else:
                tablica_IDN[djeca[1].vrijednost].tip.definirana = True
            
            novi_djelokrug = djelokrug[:] + [djelokrugPodatak(Funkcija(djeca[3].tipovi, djeca[0].tip), len(djelokrug)+1)]
            nova_tablica = copy.deepcopy(tablica_IDN) 
            
            for i in range(len(djeca[3].tipovi)):
                nova_tablica[djeca[3].imena[i]] = tablicaPodatak(djeca[3].tipovi[i], novi_djelokrug[-1])

            provjeri(djeca[5], nova_tablica, novi_djelokrug)
            

        
    elif(cvor.znak == "<lista_parametara>"):
        if(djeca[0].znak  == "<deklaracija_parametra>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            cvor.tipovi = [ djeca[0].tip ]
            cvor.imena = [ djeca[0].ime ]
        

        elif(djeca[0].znak == "<lista_parametara>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)

            cvor.tipovi = djeca[0].tipovi + [ djeca[2].tip ]
            cvor.imena = djeca[0].imena + [ djeca[2].ime ]


    
    elif(cvor.znak == "<deklaracija_parametra>"):
        if(len(djeca) == 2):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            cvor.tip = djeca[0].tip
            cvor.ime = djeca[1].vrijednost
        

        elif(len(djeca) == 4):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            cvor.tip = "niz(" + djeca[0].tip + ")"
            cvor.ime = djeca[1].vrijednost
        

    
    elif(cvor.znak == "<lista_deklaracija>"):
        if(djeca[0].znak == "<deklaracija>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
        

        elif(djeca[1].znak == "<deklaracija>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[1], tablica_IDN, djelokrug)



    elif(cvor.znak == "<deklaracija>"):
        if(djeca[0].znak == "<ime_tipa>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            djeca[1].ntip = djeca[0].tip

            provjeri(djeca[1], tablica_IDN, djelokrug)



    elif(cvor.znak == "<lista_init_deklaratora>"):
        if(djeca[0].znak == "<init_deklarator>"):
            djeca[0].ntip = cvor.ntip
            
            provjeri(djeca[0], tablica_IDN, djelokrug)


        elif(djeca[0].znak == "<lista_init_deklaratora>"): #cudno je numerirano nesto u ovoj produkciji str 68 pa samo ostavljam natuknicu
            djeca[0].ntip = cvor.ntip
            
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            djeca[2].ntip = cvor.ntip
            
            provjeri(djeca[2], tablica_IDN, djelokrug)

    

    elif(cvor.znak == "<init_deklarator>"):
        if(len(djeca) == 1):
            djeca[0].ntip = cvor.ntip
            
            provjeri(djeca[0], tablica_IDN, djelokrug)

    
        elif(len(djeca) == 3):
            djeca[0].ntip = cvor.ntip
            
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)



    elif(cvor.znak == "<izravni_deklarator>"):
        if(len(djeca) == 1):
            tablica_IDN[djeca[0].vrijednost] = tablicaPodatak(cvor.ntip, djelokrug[-1])
            cvor.tip = cvor.ntip


        elif(djeca[2].znak == "BROJ"):
            tablica_IDN[djeca[0].vrijednost] = tablicaPodatak("niz("+ cvor.ntip + ")", djelokrug[-1])
            cvor.tip = "niz("+ cvor.ntip + ")"
            cvor.brelem = int(djeca[2].vrijednost)


        elif(djeca[2].znak == "KR_VOID"):
            cvor.tip = Funkcija("void", cvor.ntip)

        
        elif(djeca[2].znak == "<lista_parametara>"):
            provjeri(djeca[2], tablica_IDN, djelokrug)

            if not djeca[0].vrijednost in tablica_IDN.keys() or djelokrug[-1] != tablica_IDN[djeca[0].vrijednost].djelokrug:
                tablica_IDN[djeca[0].vrijednost] = tablicaPodatak(Funkcija(djeca[2].tipovi, cvor.ntip), djelokrug[-1])
            cvor.tip = Funkcija(djeca[2].tipovi, cvor.ntip)



    elif(cvor.znak == "<inicijalizator>"):
        if(djeca[0].znak == "<izraz_pridruzivanja>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)

            if djeca[0].tip == "niz(const(char))":
                cvor.brelem = djeca[0].brelem + 1 
                cvor.tipovi = ["char" for i in range(cvor.brelem)]
            else:
                cvor.tip = djeca[0].tip
        

        elif(djeca[0].znak == "L_VIT_ZAGRADA"):
            provjeri(djeca[1], tablica_IDN, djelokrug)
            
            cvor.brelem = djeca[1].brelem
            cvor.tipovi = djeca[1].tipovi
        


    elif(cvor.znak == "<lista_izraza_pridruzivanja>"):
        if(djeca[0].znak == "<izraz_pridruzivanja>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            
            cvor.tipovi = [djeca[0].tip]
            cvor.brelem = 1
        

        elif(djeca[0].znak == "<lista_izraza_pridruzivanja>"):
            provjeri(djeca[0], tablica_IDN, djelokrug)
            provjeri(djeca[2], tablica_IDN, djelokrug)
            
            cvor.tipovi = djeca[0].tipovi + [djeca[2].tip]
            cvor.brelem = djeca[0].brelem + 1         

    

    if allDeclared:
        checkFunkcije(tablica_IDN, djelokrug)
    
    #whitespaces -=1
    return True

def ispis_stabla(kor):
    print(kor)
    ispis_razine(kor.djeca, 1)

def ispis_razine(cvorovi, n):
    for cvor in cvorovi:
        for i in range(n):
            print(" ", end="")
        if(isinstance(cvor, List) or isinstance(cvor, ListEps)):
            print(cvor)
        elif(isinstance(cvor, UnutarnjiCvor)):
            print(cvor)
            ispis_razine(cvor.djeca, n + 1)


def redukcija_djece(cvor):
    lista_spasenih = ["<vanjska_deklaracija>", "<deklaracija>", "<definicija_funkcije>"]
    if isinstance(cvor, List) or isinstance(cvor, ListEps):
        return
    while len(cvor.djeca) == 1 and cvor.djeca[0].znak not in lista_spasenih:
        if isinstance(cvor.djeca[0], List) or isinstance(cvor.djeca[0], ListEps):
            return
        cvor.djeca = cvor.djeca[0].djeca
    for dijete in cvor.djeca:
        redukcija_djece(dijete)

def redukcija_djece2(cvor):
    lista_spasenih = ["<lista_parametara>", "<slozena_naredba>", "<init_deklarator>", "<init_deklarator>", "<deklaracija>", "<definicija_funkcije>"]
    if isinstance(cvor, UnutarnjiCvor):
        new_djeca = []
        for i in cvor.djeca:
            pov = redukcija_djece2(i)
            if isinstance(pov, list):
                new_djeca += pov
            else:
                new_djeca += [pov]
        if cvor.znak in lista_spasenih:
            cvor.djeca = new_djeca
            return cvor        
        elif len(new_djeca) == 1:
            return new_djeca[0]
        elif cvor.znak == "<lista_init_deklaratora>" or cvor.znak == "<lista_deklaracija>" or cvor.znak == "<lista_naredbi>"  or cvor.znak == "<lista_izraza_pridruzivanja>" or cvor.znak == "<izraz>":
            return new_djeca
        else:
            cvor.djeca = new_djeca
            return cvor
    else:
        if cvor.znak in ["ZAREZ", "TOCKAZAREZ", "L_ZAGRADA", "D_ZAGRADA", "L_UGL_ZAGRADA", "D_UGL_ZAGRADA", "L_VIT_ZAGRADA", "D_VIT_ZAGRADA"]:
            return []
        return cvor 

def semanticka_analiza(korijen_stabla):
    djelokrug = [djelokrugPodatak("GLOBAL", 1)]
    golablni_djelokrug_IDN = dict()
    provjeri(korijen_stabla, golablni_djelokrug_IDN, djelokrug)
    
    redukcija_djece2(korijen_stabla)
    ispis_stabla(korijen_stabla)

    return korijen_stabla

