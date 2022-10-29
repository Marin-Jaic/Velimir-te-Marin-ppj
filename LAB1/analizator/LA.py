from automat_akcija import *
import sys

    #GRESKA ILI NE GRESKA SE JAVLJA U C U LINIJI 36 za tri jednostruka navodnika '''
    #POPRAVLJENO, ALI PAZI NA JOS SPECIJALNIH ZNAKOVA

def analiza(pocetno_stanje, stanja, akcije):
    

    trenutno_stanje = pocetno_stanje
    index = 0
    red_counter = 1

    #counter = 0 #SAMO ZA TEST, MAKNI

    #file_object = open('test/input2.txt', 'r')
    #ulaz = file_object.read()
    #file_object.close()

    ulaz = sys.stdin.read()

    while(index < len(ulaz)):
        najveca_duljina = 0
        izvrsi_akciju = None
        
        for akcija in akcije:

            if akcija.stanje == trenutno_stanje:
                akcija.automat.reset()
                akcija.automat.epsilon_prijelaz()

                i = index
                zadnja_duljina = 0

                while(i < len(ulaz) and akcija.automat.prijelaz(ulaz[i])): 
                    i += 1 #brojim na pocetku jer mi je na taj nacin zadnji index veci za jedan sto je pogodnije za [nesto:zadnji index]

                    if(akcija.automat.izraz_prihvacen):
                        zadnja_duljina = i - index

                
                if zadnja_duljina > najveca_duljina or izvrsi_akciju is not None and zadnja_duljina == najveca_duljina and izvrsi_akciju.id > akcija.id:
                    izvrsi_akciju = akcija
                    najveca_duljina = zadnja_duljina
        
        if izvrsi_akciju is None:
            print(ulaz[index], file = sys.stderr)
            index += 1

        else:
            if izvrsi_akciju.vrati_se != -1: #testiranje s None i/ili -1
                najveca_duljina = int(izvrsi_akciju.vrati_se)
            
            if izvrsi_akciju.udji_u_stanje is not None:
                trenutno_stanje = izvrsi_akciju.udji_u_stanje
            
            if izvrsi_akciju.novi_redak:
                red_counter += 1
                
            if izvrsi_akciju.lex != "":
                print(izvrsi_akciju.lex + " " + str(red_counter) + " " + ulaz[index:index + najveca_duljina])
                # print(izvrsi_akciju.lex)
                #counter += 1

            index += najveca_duljina

    #print("Ukupno jedinki: ", counter)


