import ulaz
import SemantickiAnalizator
from PomocniR import *
import Stablo



#>python Leksicki/LA.py < testovi/e_001/test.c | python Sintaksni/SA.py | python GeneratorKoda.py
korijen_gen_st = SemantickiAnalizator.semanticka_analiza(ulaz.ulaz())

asembler = open('frisc.a', 'w')



glob_f = []
glob_var = []
izrazi = ["<multiplikativni_izraz>", "<postfiks_izraz>", "<izraz_pridruzivanja>", "<primarni_izraz>", "<unarni_izraz>", "<log_ili_izraz>", "<log_i_izraz>", "<aditivni_izraz>", "<jednakosni_izraz>", "<bin_ili_izraz>", "<odnosni_izraz>", "<bin_i_izraz>", "<bin_xili_izraz>"]
jednobrojcani_irazi = ["<postfiks_izraz>", "<unarni_izraz>"]
id_lab = 1


def obilazak(cvor):
    global glob_f
    global glob_var

    if cvor.znak == "<deklaracija>":
        glob_var += [cvor]
    elif cvor.znak == "<definicija_funkcije>":
        glob_f += [cvor]
    elif isinstance(cvor, Stablo.UnutarnjiCvor):
        for dijete in cvor.djeca:
            obilazak(dijete)


def analiza_deklaracije(cvor, djelokrug, varijable, asembler):
    tip = "undefined"
    if isinstance(cvor.djeca[0], Stablo.UnutarnjiCvor):
        tip = cvor.djeca[0].djeca[1].vrijednost
    else:
        tip = cvor.djeca[0].vrijednost
    lokalne_varijable = []
    for deklarator in cvor.djeca[1:]:
        if deklarator.djeca[0].tip != None and deklarator.djeca[0].tip[0:4] == "niz(":
            if len(deklarator.djeca[0].djeca) > 1:
                velicina = deklarator.djeca[0].djeca[1].vrijednost
                for i in range(int(velicina)):
                    lokalne_varijable += [Varijabla(tip, deklarator.djeca[0].djeca[0].vrijednost+str(i), 0, djelokrug)]

                if len(deklarator.djeca) > 2:
                    inits = deklarator.djeca[2:]
                    if deklarator.djeca[2].znak == "<inicijalizator>":
                        inits = deklarator.djeca[2].djeca
                    elif deklarator.djeca[2].znak == "NIZ_ZNAKOVA":
                        inits = []
                        for znak in deklarator.djeca[2].vrijednost.strip("\""):
                            inits += [Stablo.List("ZNAK", None, znak)]
                    for i in range(len(inits)):
                        izracunaj_izraz(inits[i], djelokrug, asembler, lokalne_varijable + varijable)
                        asembler.write("\t\tPOP R0\n")
                        saveaj_var("R0", deklarator.djeca[0].djeca[0].vrijednost+str(i),  lokalne_varijable + varijable)

        else: # slučaj da nije niz
            lokalne_varijable += [Varijabla(tip, deklarator.djeca[0].vrijednost, 0, djelokrug)]
            if len(deklarator.djeca) > 1: #ako je definiran            
                izracunaj_izraz(deklarator.djeca[2], djelokrug, asembler, lokalne_varijable + varijable)
                asembler.write("\t\tPOP R0\n")
                saveaj_var("R0", deklarator.djeca[0].vrijednost, lokalne_varijable + varijable)
    
    return lokalne_varijable


def izracunaj_izraz(cvor, djelokrug, asembler, varijable):
    global id_lab
    global izrazi
    global jednobrojcani_irazi

    if cvor.znak in izrazi:
        if cvor.znak == "<primarni_izraz>":
            izracunaj_izraz(cvor.djeca[-1], djelokrug, asembler, varijable)
        else:
            if cvor.znak == "<unarni_izraz>":
                izracunaj_izraz(cvor.djeca[1], djelokrug, asembler, varijable)
                asembler.write("\t\tPOP R0\n")

            elif cvor.znak == "<postfiks_izraz>":
                if cvor.djeca[1].znak in ["OP_INC", "OP_DEC"]:
                    izracunaj_izraz(cvor.djeca[0], djelokrug, asembler, varijable)
                    asembler.write("\t\tPOP R0\n")
            
                else:
                    izracunaj_izraz(cvor.djeca[1], djelokrug, asembler, varijable)
                    asembler.write("\t\tPOP R1\n")
                    lab = getLabel(cvor.djeca[0].vrijednost +"0", varijable)
                    asembler.write("\t\tMOVE 0, R0\n")
                    asembler.write("\t\tADD R0, "+str(id_lab)+", R0\n")
                    asembler.write("P_"+str(id_lab)+"\t\tSUB R1, 1, R1\n")
                    asembler.write("\t\tJP_N D_"+str(id_lab)+"\n")
                    asembler.write("\t\tADD R0, 4, R0\n")
                    asembler.write("\t\tJP P_"+str(id_lab)+"\n")
                    asembler.write("D_"+str(id_lab))
                    asembler.write("\t\tLOAD R0, (R0)\n")
                    id_lab += 1

            else:
                izracunaj_izraz(cvor.djeca[0], djelokrug, asembler, varijable)
                izracunaj_izraz(cvor.djeca[2], djelokrug, asembler, varijable)
                asembler.write("\t\tPOP R0\n")
                asembler.write("\t\tPOP R1\n")

            if cvor.znak == "<aditivni_izraz>":
                if cvor.djeca[1].znak == "PLUS":
                    asembler.write("\t\tADD R0, R1, R0\n")
                elif cvor.djeca[1].znak == "MINUS":
                    asembler.write("\t\tSUB R1, R0, R0\n")
            
            elif cvor.znak == "<jednakosni_izraz>":
                if cvor.djeca[1].znak == "OP_EQ":
                    asembler.write("\t\tCMP R0, R1\n")
                    asembler.write("\t\tJP_NE FA_" + str(id_lab) + "\n")
                    asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                    asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                    asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                    asembler.write("DALJ_" + str(id_lab) + "\t\t")
                    id_lab += 1
                elif cvor.djeca[1].znak == "OP_NEQ":
                    asembler.write("\t\tCMP R0, R1\n")
                    asembler.write("\t\tJP_NE FA_" + str(id_lab) + "\n")
                    asembler.write("TR_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                    asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                    asembler.write("FA_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                    asembler.write("DALJ_" + str(id_lab) + "\t\t")
                    id_lab += 1        
            elif cvor.znak == "<bin_ili_izraz>":
                asembler.write("\t\tOR R0, R1, R0\n")
            elif cvor.znak == "<bin_i_izraz>":
                asembler.write("\t\tAND R0, R1, R0\n")
            elif cvor.znak == "<bin_xili_izraz>":
                asembler.write("\t\tXOR R0, R1, R0\n")
            elif cvor.znak == "<odnosni_izraz>":
                if cvor.djeca[1].znak == "OP_LT":
                    asembler.write("\t\tCMP R1, R0\n")
                    asembler.write("\t\tJP_SLT TR_" + str(id_lab) + "\n")
                    asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                    asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                    asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                    asembler.write("DALJ_" + str(id_lab) + "\t\t")
                    id_lab += 1
                elif cvor.djeca[1].znak == "OP_GT":
                    asembler.write("\t\tCMP R1, R0\n")
                    asembler.write("\t\tJP_SGT TR_" + str(id_lab) + "\n")
                    asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                    asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                    asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                    asembler.write("DALJ_" + str(id_lab) + "\t\t")
                    id_lab += 1 
                elif cvor.djeca[1].znak == "OP_GTE":
                    asembler.write("\t\tCMP R1, R0\n")
                    asembler.write("\t\tJP_SGE TR_" + str(id_lab) + "\n")
                    asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                    asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                    asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                    asembler.write("DALJ_" + str(id_lab) + "\t\t")
                    id_lab += 1   
                elif cvor.djeca[1].znak == "OP_LTE":
                    asembler.write("\t\tCMP R1, R0\n")
                    asembler.write("\t\tJP_SLE TR_" + str(id_lab) + "\n")
                    asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                    asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                    asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                    asembler.write("DALJ_" + str(id_lab) + "\t\t")
                    id_lab += 1   
            elif cvor.znak == "<log_i_izraz>":
                asembler.write("\t\tMOVE 0, R2\n")
                asembler.write("\t\tCMP R0, R2\n")
                asembler.write("\t\tJP_NE TR_" + str(id_lab) + "\n")
                asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                asembler.write("DALJ_" + str(id_lab) + "\t\t")
                id_lab += 1 
                asembler.write("\t\tCMP R1, R2\n")
                asembler.write("\t\tJP_NE TR_" + str(id_lab) + "\n")
                asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R1\n")
                asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R1\n")
                asembler.write("DALJ_" + str(id_lab) + "\t\t")
                id_lab += 1 
                asembler.write("\t\tAND R0, R1, R0\n")
            elif cvor.znak == "<log_ili_izraz>":
                asembler.write("\t\tMOVE 0, R2\n")
                asembler.write("\t\tCMP R0, R2\n")
                asembler.write("\t\tJP_NE TR_" + str(id_lab) + "\n")
                asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                asembler.write("DALJ_" + str(id_lab) + "\t\t")
                id_lab += 1 
                asembler.write("\t\tCMP R1, R2\n")
                asembler.write("\t\tJP_NE TR_" + str(id_lab) + "\n")
                asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R1\n")
                asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R1\n")
                asembler.write("DALJ_" + str(id_lab) + "\t\t")
                id_lab += 1 
                asembler.write("\t\tOR R0, R1, R0\n")
            elif cvor.znak == "<unarni_izraz>":
                if cvor.djeca[0].znak == "MINUS":
                    asembler.write("\t\tMOVE 0, R1\n")
                    asembler.write("\t\tSUB R1, 1, R1\n")
                    asembler.write("\t\tSUB R1, R0, R0\n")
                    asembler.write("\t\tADD R0, 1, R0\n")
                elif cvor.djeca[0].znak == "PLUS":
                    pass
                elif cvor.djeca[0].znak == "OP_NEG":
                    asembler.write("\t\tMOVE 0, R2\n")
                    asembler.write("\t\tCMP R0, R2\n")
                    asembler.write("\t\tJP_NE TR_" + str(id_lab) + "\n")
                    asembler.write("FA_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                    asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                    asembler.write("TR_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                    asembler.write("DALJ_" + str(id_lab) + "\t\t")
                    id_lab += 1 
                elif cvor.djeca[0].znak == "OP_INC":
                    asembler.write("\t\tADD R0, 1, R0\n")
                    saveaj_var("R0", cvor.djeca[1].vrijednost, varijable)
                elif cvor.djeca[0].znak == "OP_DEC":
                    asembler.write("\t\tSUB R0, 1, R0\n")
                    saveaj_var("R0", cvor.djeca[1].vrijednost, varijable)
                elif cvor.djeca[0].znak == "OP_TILDA":
                    asembler.write("\t\tMOVE 0, R1\n")
                    asembler.write("\t\tSUB R1, 1, R1\n")
                    asembler.write("\t\tSUB R1, R0, R0\n")
            elif cvor.znak == "<izraz_pridruzivanja>":
                saveaj_var("R0", cvor.djeca[0].vrijednost, varijable)
            
            elif cvor.znak == "<postfiks_izraz>":
                if cvor.djeca[1].znak == "OP_INC":
                    asembler.write("\t\tMOVE R0, R1\n")
                    asembler.write("\t\tADD R1, 1, R1\n")
                    saveaj_var("R1", cvor.djeca[0].vrijednost, varijable)
                elif cvor.djeca[1].znak == "OP_DEC":
                    asembler.write("\t\tMOVE R0, R1\n")
                    asembler.write("\t\tSUB R1, 1, R1\n")
                    saveaj_var("R1", cvor.djeca[0].vrijednost, varijable)
            elif cvor.znak == "<multiplikativni_izraz>":
                if cvor.djeca[1].znak == "OP_PUTA":
                    asembler.write("\t\tMOVE 0, R3\n")

                    asembler.write("\t\tCMP R0, 0\n")
                    asembler.write("\t\tJP_SGE DA_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R0, R0\n")
                    asembler.write("\t\tADD R0, 1, R0\n")
                    asembler.write("\t\tXOR R3, 1, R3\n")
                    asembler.write("DA_"+str(id_lab))
                    id_lab+=1
                    asembler.write("\t\tCMP R1, 0\n")
                    asembler.write("\t\tJP_SGE DA_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R1, R1\n")
                    asembler.write("\t\tADD R1, 1, R1\n")
                    asembler.write("\t\tXOR R3, 1, R3\n")
                    asembler.write("DA_"+str(id_lab))
                    asembler.write("\t\tMOVE R0, R2\n")
                    id_lab+=1
                    asembler.write("P_"+str(id_lab)+"\t\tSUB R1, 1, R1\n")
                    asembler.write("\t\tJP_Z D_"+str(id_lab)+"\n")
                    asembler.write("\t\tADD R0, R2, R0\n")
                    asembler.write("\t\tJP P_"+str(id_lab)+"\n")
                    asembler.write("D_"+str(id_lab))
                    id_lab += 1
                    asembler.write("\t\tCMP R3, 1\n")
                    asembler.write("\t\tJP_NE D_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R0, R0\n")
                    asembler.write("\t\tADD R0, 1, R0\n")
                    asembler.write("D_"+str(id_lab))
                    id_lab += 1
                elif cvor.djeca[1].znak == "OP_DIJELI":
                    asembler.write("\t\tMOVE R1, R3\n")
                    asembler.write("\t\tMOVE R0, R1\n")
                    asembler.write("\t\tMOVE R3, R0\n")
                    asembler.write("\t\tMOVE 0, R3\n")

                    asembler.write("\t\tCMP R0, 0\n")
                    asembler.write("\t\tJP_SGE DA_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R0, R0\n")
                    asembler.write("\t\tADD R0, 1, R0\n")
                    asembler.write("\t\tXOR R3, 1, R3\n")
                    asembler.write("DA_"+str(id_lab))
                    id_lab+=1
                    asembler.write("\t\tCMP R1, 0\n")
                    asembler.write("\t\tJP_SGE DA_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R1, R1\n")
                    asembler.write("\t\tADD R1, 1, R1\n")
                    asembler.write("\t\tXOR R3, 1, R3\n")
                    asembler.write("DA_"+str(id_lab))
                    asembler.write("\t\tMOVE 0, R2\n")
                    id_lab+=1
                    asembler.write("P_"+str(id_lab)+"\t\tCMP R0, R1\n")
                    asembler.write("\t\tJP_ULT D_"+str(id_lab)+"\n")
                    asembler.write("\t\tSUB R0, R1, R0\n")
                    asembler.write("\t\tADD R2, 1, R2\n")
                    asembler.write("\t\tJP P_"+str(id_lab)+"\n")
                    asembler.write("D_"+str(id_lab))
                    id_lab += 1
                    asembler.write("\t\tCMP R3, 1\n")
                    asembler.write("\t\tJP_NE D_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R0, R0\n")
                    asembler.write("\t\tADD R0, 1, R0\n")
                    asembler.write("D_"+str(id_lab)+"\t\tMOVE R2, R0\n")
                    id_lab += 1
                elif cvor.djeca[1].znak == "OP_MOD":
                    asembler.write("\t\tMOVE R1, R3\n")
                    asembler.write("\t\tMOVE R0, R1\n")
                    asembler.write("\t\tMOVE R3, R0\n")
                    asembler.write("\t\tMOVE 0, R3\n")

                    asembler.write("\t\tCMP R0, 0\n")
                    asembler.write("\t\tJP_SGE DA_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R0, R0\n")
                    asembler.write("\t\tADD R0, 1, R0\n")
                    asembler.write("\t\tXOR R3, 1, R3\n")
                    asembler.write("DA_"+str(id_lab))
                    id_lab+=1
                    asembler.write("\t\tCMP R1, 0\n")
                    asembler.write("\t\tJP_SGE DA_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R1, R1\n")
                    asembler.write("\t\tADD R1, 1, R1\n")
                    asembler.write("\t\tXOR R3, 1, R3\n")
                    asembler.write("DA_"+str(id_lab))
                    asembler.write("\t\tMOVE 0, R2\n")
                    id_lab+=1
                    asembler.write("P_"+str(id_lab)+"\t\tCMP R0, R1\n")
                    asembler.write("\t\tJP_ULT D_"+str(id_lab)+"\n")
                    asembler.write("\t\tSUB R0, R1, R0\n")
                    asembler.write("\t\tADD R2, 1, R2\n")
                    asembler.write("\t\tJP P_"+str(id_lab)+"\n")
                    asembler.write("D_"+str(id_lab))
                    id_lab += 1
                    asembler.write("\t\tCMP R3, 1\n")
                    asembler.write("\t\tJP_NE D_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R0, R0\n")
                    asembler.write("\t\tADD R0, 1, R0\n")
                    asembler.write("D_"+str(id_lab))
                    id_lab += 1
            asembler.write("\t\tPUSH R0\n")


    elif cvor.znak == "BROJ":
        asembler.write("\t\tMOVE %D "+ cvor.vrijednost +", R0\n")
        asembler.write("\t\tPUSH R0\n")
    elif cvor.znak == "IDN":
        loadaj_var("R0", cvor.vrijednost, varijable)
        asembler.write("\t\tPUSH R0\n")
    elif cvor.znak == "ZNAK":
        asembler.write("\t\tMOVE %D "+ str(ord(cvor.vrijednost.strip("\'"))) +", R0\n")
        asembler.write("\t\tPUSH R0\n")

def getLabel(naziv, vars):
    for var in vars:
        if var.naziv == naziv:
            return var.adr
    print("NIJEN AŠO")

def loadaj_var(reg, naziv, varijable, indeks=None):
    adr = getLabel(naziv, varijable)
    asembler.write("\t\tLOAD "+reg+", (" + adr + ")\n")


def saveaj_var(reg, naziv, varijable):
    adr = getLabel(naziv, varijable)
    asembler.write("\t\tSTORE "+reg+", (" + adr + ")\n")
    
    
def analiza_funkcije(cvor, djelokrug, asembler, globalne_var):
    blok = cvor.djeca[3]
    naziv_f = cvor.djeca[1].vrijednost.upper()
    deklaracije = []
    naredbe = []
    argumenti = cvor.djeca[2] 
    lokalne_var = []
    if argumenti.znak == "<lista_parametara>":
        tipovi = argumenti.tipovi
        imena = argumenti.imena
        for i in range(len(tipovi)):
            if not SemantickiAnalizator.jeNizX(tipovi[i]):
                lokalne_var += [Varijabla(tipovi[i], imena[i], 0, djelokrug + [naziv_f])]
    
    
    for dijete in blok.djeca:
        if dijete.znak == "<deklaracija>":
            deklaracije += [dijete]
        else:
            naredbe += [dijete]

    args = lokalne_var[:]
    asembler.write("F_" + naziv_f.upper())
    ugnijezdene_varijable = analiza_bloka(deklaracije, naredbe, djelokrug + [naziv_f], lokalne_var + globalne_var, asembler)
    return ugnijezdene_varijable

def rastav_bloka(naredba):
    new_dekl = []
    new_nar = []
    for dijete in naredba.djeca:
        if dijete.znak == "<deklaracija>":
            new_dekl += [dijete]
        else:
            new_nar += [dijete]
    return new_dekl, new_nar


def analiza_bloka(deklaracije, naredbe, djelokrug, varijable, asembler, petlja_pod = None):
    lokalne_var = []
    ugnijezdene_var = []
    for deklaracija in deklaracije:
        lokalne_var += analiza_deklaracije(deklaracija, djelokrug, lokalne_var + varijable, asembler)
    print(lokalne_var)
    global id_lab
    global izrazi
    for naredba in naredbe:
        if naredba.znak == "<naredba_skoka>":
            if naredba.djeca[0].znak == "KR_RETURN":
                izracunaj_izraz(naredba.djeca[1], djelokrug, asembler, lokalne_var + varijable)
                asembler.write("\t\tPOP R6\n")
                asembler.write("\t\tRET\n")
        elif naredba.znak in izrazi:
            izracunaj_izraz(naredba, djelokrug, asembler, lokalne_var + varijable)
            asembler.write("\t\tADD R7, 4, R7\n")
        elif naredba.znak == "<slozena_naredba>":
            new_dekl, new_nar = rastav_bloka(naredba)
            ugnijezdene_var += analiza_bloka(new_dekl, new_nar, djelokrug + [str(id_lab)], lokalne_var + varijable, asembler, petlja_pod)
            id_lab += 1
        elif naredba.znak == "<naredba_petlje>":
            if naredba.djeca[0].znak == "KR_WHILE":
                save_lab = id_lab
                id_lab += 1
                asembler.write("W"+str(save_lab))
                izracunaj_izraz(naredba.djeca[1], djelokrug, asembler, lokalne_var + varijable)

                asembler.write("\t\tPOP R0\n")
                asembler.write("\t\tCMP R0, 0\n")
                asembler.write("\t\tJP_EQ D_" + str(save_lab) + "\n")
                new_dekl, new_nar = rastav_bloka(naredba.djeca[2])
                new_petlja_pod = ("W"+str(save_lab), "D_"+str(save_lab))
                ugnijezdene_var += analiza_bloka(new_dekl, new_nar, djelokrug + [str(save_lab)], lokalne_var + varijable, asembler, new_petlja_pod)

                asembler.write("\t\tJP W"+str(save_lab)+"\n")
                asembler.write("D_" + str(save_lab))
            
            elif naredba.djeca[0].znak == "KR_FOR":
                if len(naredba.djeca[1].djeca) > 0:
                    izracunaj_izraz(naredba.djeca[1], djelokrug, asembler, lokalne_var + varijable)
                    asembler.write("\t\tADD R7, 4, R7\n")

                save_lab = id_lab
                id_lab += 1       
                asembler.write("F"+str(save_lab))
                if len(naredba.djeca[1].djeca) > 0:
                    izracunaj_izraz(naredba.djeca[2], djelokrug, asembler, lokalne_var + varijable)
                    asembler.write("\t\tPOP R0\n")
                    asembler.write("\t\tCMP R0, 0\n")
                    asembler.write("\t\tJP_EQ D_" + str(save_lab) + "\n")

                new_dekl, new_nar = rastav_bloka(naredba.djeca[4])
                new_petlja_pod = ("F"+str(save_lab), "D_"+str(save_lab))
                ugnijezdene_var += analiza_bloka(new_dekl, new_nar, djelokrug + [str(save_lab)], lokalne_var + varijable, asembler, new_petlja_pod)

                if len(naredba.djeca[3].djeca) > 0:
                    izracunaj_izraz(naredba.djeca[3], djelokrug, asembler, lokalne_var + varijable)
                    asembler.write("\t\tADD R7, 4, R7\n")
                asembler.write("\t\tJP F"+str(save_lab)+"\n")
                asembler.write("D_" + str(save_lab))
        elif naredba.znak == "KR_BREAK":
            asembler.write("\t\tJP "+petlja_pod[1]+"\n")
        elif naredba.znak == "KR_CONTINUE":
            asembler.write("\t\tJP "+petlja_pod[0]+"\n")
        elif naredba.znak == "<naredba_grananja>":
            save_lab = id_lab
            id_lab += 1

            izracunaj_izraz(naredba.djeca[1], djelokrug, asembler, lokalne_var + varijable)

            asembler.write("\t\tPOP R0\n")
            asembler.write("\t\tCMP R0, 0\n")
            asembler.write("\t\tJP_EQ D_" + str(save_lab) + "\n")

            new_dekl, new_nar = rastav_bloka(naredba.djeca[2])
            ugnijezdene_var += analiza_bloka(new_dekl, new_nar, djelokrug + [str(save_lab)], lokalne_var + varijable, asembler, petlja_pod)

            asembler.write("D_" + str(save_lab))
            if len(naredba.djeca) > 3:
                print(naredba.djeca[4])
                new_dekl, new_nar = [], [naredba.djeca[4]]
                ugnijezdene_var += analiza_bloka(new_dekl, new_nar, djelokrug + [str(save_lab)], lokalne_var + varijable, asembler, petlja_pod)


    return lokalne_var + ugnijezdene_var

obilazak(korijen_gen_st)


globalne_varijable = []
funkcije = []

asembler.write("\t\t`ORG 0\n")
asembler.write("\t\tMOVE 4000, R7\n")
for i in glob_var:
    globalne_varijable += analiza_deklaracije(i, ["G"], globalne_varijable, asembler)


asembler.write("\n\t\tCALL F_MAIN\n")
asembler.write("\t\tHALT\n\n")

for i in glob_f:
    funkcije += [analiza_funkcije(i, [], asembler, globalne_varijable)]



for var in globalne_varijable:
    asembler.write(var.kod())


for vars in funkcije:
    for var in vars:
        asembler.write(var.kod())
        
#glob_var = upis_golbalnih(glob_var, asembler)
#glob_f = upis_funkcija(glob_f, asembler)
