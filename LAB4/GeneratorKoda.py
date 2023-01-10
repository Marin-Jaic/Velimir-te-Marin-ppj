import ulaz
import SemantickiAnalizator
from PomocniR import *
import Stablo



#>python Leksicki/LA.py < testovi/e_001/test.c | python Sintaksni/SA.py | python GeneratorKoda.py
korijen_gen_st = SemantickiAnalizator.semanticka_analiza(ulaz.ulaz())

asembler = open('a.frisc', 'w')



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


def analiza_deklaracije(cvor, djelokrug, varijable, asembler, funkcije, tr_f):
    tip = "undefined"
    if isinstance(cvor.djeca[0], Stablo.UnutarnjiCvor):
        tip = cvor.djeca[0].djeca[1].vrijednost
    else:
        tip = cvor.djeca[0].vrijednost
    lokalne_varijable = []
    for deklarator in cvor.djeca[1:]:
        if isinstance(deklarator.djeca[0].tip, str) and (deklarator.djeca[0].tip != None and deklarator.djeca[0].tip[0:4] == "niz("):
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
                        lokalne_varijable += izracunaj_izraz(inits[i], djelokrug, asembler, lokalne_varijable + varijable, funkcije, tr_f)
                        asembler.write("\t\tPOP R0\n")
                        saveaj_var("R0", deklarator.djeca[0].djeca[0].vrijednost+str(i),  lokalne_varijable + varijable)

        elif not isinstance(deklarator.djeca[0].tip, Stablo.Funkcija): # slučaj da nije niz
            lokalne_varijable += [Varijabla(tip, deklarator.djeca[0].vrijednost, 0, djelokrug)]
            if len(deklarator.djeca) > 1: #ako je definiran            
                lokalne_varijable += izracunaj_izraz(deklarator.djeca[2], djelokrug, asembler, lokalne_varijable + varijable, funkcije, tr_f)
                asembler.write("\t\tPOP R0\n")
                saveaj_var("R0", deklarator.djeca[0].vrijednost, lokalne_varijable + varijable)
        else:#je poziv funkcije
            if deklarator.djeca[0].znak == "<izravni_deklarator>":
                continue

            lokalne_varijable += [Varijabla(tip, deklarator.djeca[0].vrijednost, 0, djelokrug)]
            lokalne_varijable += izracunaj_izraz(deklarator.djeca[2], djelokrug, asembler, lokalne_varijable + varijable, funkcije, tr_f)
            asembler.write("\t\tPOP R0\n")
            saveaj_var("R0", deklarator.djeca[0].vrijednost, lokalne_varijable + varijable)
            

    return lokalne_varijable


def izracunaj_izraz(cvor, djelokrug, asembler, varijable, funkcije, tr_f, adr=False):
    global id_lab
    global izrazi
    global jednobrojcani_irazi
    consts = []

    if cvor.znak in izrazi:

        if cvor.znak == "<primarni_izraz>":
            consts += izracunaj_izraz(cvor.djeca[-1], djelokrug, asembler, varijable, funkcije, tr_f)
        else:
            if cvor.znak == "<unarni_izraz>":
                if cvor.djeca[1].znak == "<postfiks_izraz>":
                    consts += izracunaj_izraz(cvor.djeca[1], djelokrug, asembler, varijable, funkcije, tr_f, True)
                    asembler.write("\t\tPOP R0\n")

                else:
                    consts += izracunaj_izraz(cvor.djeca[1], djelokrug, asembler, varijable, funkcije, tr_f)
                    asembler.write("\t\tPOP R0\n")
            
            elif cvor.znak == "<izraz_pridruzivanja>" and cvor.djeca[0].znak == "<postfiks_izraz>":
                consts += izracunaj_izraz(cvor.djeca[0], djelokrug, asembler, varijable, funkcije, tr_f, True)
                consts += izracunaj_izraz(cvor.djeca[2], djelokrug, asembler, varijable, funkcije, tr_f)
                asembler.write("\t\tPOP R0\n")
                asembler.write("\t\tPOP R1\n")


            elif cvor.znak == "<postfiks_izraz>":
                if cvor.djeca[0].znak == "<postfiks_izraz>":
                    consts += izracunaj_izraz(cvor.djeca[0], djelokrug, asembler, varijable, funkcije, tr_f, True)
                    asembler.write("\t\tPOP R0\n")

                elif cvor.djeca[1].znak in ["OP_INC", "OP_DEC"]:
                    consts += izracunaj_izraz(cvor.djeca[0], djelokrug, asembler, varijable, funkcije, tr_f)
                    asembler.write("\t\tPOP R0\n")
                
        
                elif cvor.jePozivFunkcije:
                    f = getFunc(cvor.djeca[0].vrijednost, funkcije)
                    if tr_f.args != []:
                        for arg in tr_f.args:
                            asembler.write("\t\tLOAD R0, ("+arg.adr+")\n")
                            asembler.write("\t\tSTORE R0, (R5)\n")
                            asembler.write("\t\tSUB R5, 4, R5\n")


                    if f.args != []:
                        predani = cvor.djeca[1:]

                        for i in range(len(f.args)):
                            if f.args[i].jePointer:
                                var = getVar(predani[i].vrijednost, varijable)
                                if var != None and var.jePointer:
                                    lab = getLabel(predani[i].vrijednost, varijable)
                                    asembler.write("\t\tLOAD R0, ("+lab+")\n")
                                else:
                                    lab = getLabel(predani[i].vrijednost + "0", varijable)
                                    asembler.write("\t\tMOVE 0, R0\n")
                                    asembler.write("\t\tADD R0, "+lab+", R0\n")
                                asembler.write("\t\tSTORE R0, ("+ f.args[i].adr +")\n")

                            else:
                                izracunaj_izraz(predani[i], djelokrug, asembler, varijable, funkcije, tr_f)
                                asembler.write("\t\tPOP R0\n")
                                asembler.write("\t\tSTORE R0, ("+f.args[i].adr+")\n")

                    asembler.write("\t\tCALL "+f.adr+"\n")

                    if tr_f.args != []:
                        for arg in reversed(tr_f.args):
                            asembler.write("\t\tADD R5, 4, R5\n")
                            asembler.write("\t\tLOAD R0, (R5)\n")

                            asembler.write("\t\tSTORE R0, ("+arg.adr+")\n")
                    
                    asembler.write("\t\tPUSH R6\n")
                    return consts

                else:
                    var = getVar(cvor.djeca[0].vrijednost, varijable)

                    if adr:
                        if var == None or not var.jePointer:

                            consts += izracunaj_izraz(cvor.djeca[1], djelokrug, asembler, varijable, funkcije, tr_f)
                            asembler.write("\t\tPOP R1\n")

                            lab = getLabel(cvor.djeca[0].vrijednost +"0", varijable)
                            asembler.write("\t\tMOVE 0, R0\n")
                            asembler.write("\t\tADD R0, "+str(lab)+", R0\n")
                            asembler.write("P_"+str(id_lab)+"\t\tSUB R1, 1, R1\n")
                            asembler.write("\t\tJP_N D_"+str(id_lab)+"\n")
                            asembler.write("\t\tADD R0, 4, R0\n")
                            asembler.write("\t\tJP P_"+str(id_lab)+"\n")
                            asembler.write("D_"+str(id_lab)+"\n")
                            id_lab += 1
                        else:
                            consts += izracunaj_izraz(cvor.djeca[1], djelokrug, asembler, varijable, funkcije, tr_f)
                            asembler.write("\t\tPOP R1\n")
                            lab = getLabel(cvor.djeca[0].vrijednost, varijable)
                            asembler.write("\t\tLOAD R0, ("+str(lab)+")\n")
                            asembler.write("P_"+str(id_lab)+"\t\tSUB R1, 1, R1\n")
                            asembler.write("\t\tJP_N D_"+str(id_lab)+"\n")
                            asembler.write("\t\tADD R0, 4, R0\n")
                            asembler.write("\t\tJP P_"+str(id_lab)+"\n")
                            asembler.write("D_"+str(id_lab)+"\n")

                            id_lab += 1
                    else:

                        if var == None or not var.jePointer:
                            consts += izracunaj_izraz(cvor.djeca[1], djelokrug, asembler, varijable, funkcije, tr_f)
                            asembler.write("\t\tPOP R1\n")
                            lab = getLabel(cvor.djeca[0].vrijednost +"0", varijable)
                            asembler.write("\t\tMOVE 0, R0\n")
                            asembler.write("\t\tADD R0, "+str(lab)+", R0\n")
                            asembler.write("P_"+str(id_lab)+"\t\tSUB R1, 1, R1\n")
                            asembler.write("\t\tJP_N D_"+str(id_lab)+"\n")
                            asembler.write("\t\tADD R0, 4, R0\n")
                            asembler.write("\t\tJP P_"+str(id_lab)+"\n")
                            asembler.write("D_"+str(id_lab))
                            asembler.write("\t\tLOAD R0, (R0)\n")
                            id_lab += 1
                        else:
                            consts += izracunaj_izraz(cvor.djeca[1], djelokrug, asembler, varijable, funkcije, tr_f)
                            asembler.write("\t\tPOP R1\n")
                            lab = getLabel(cvor.djeca[0].vrijednost, varijable)
                            asembler.write("\t\tLOAD R0, ("+str(lab)+")\n")
                            asembler.write("P_"+str(id_lab)+"\t\tSUB R1, 1, R1\n")
                            asembler.write("\t\tJP_N D_"+str(id_lab)+"\n")
                            asembler.write("\t\tADD R0, 4, R0\n")
                            asembler.write("\t\tJP P_"+str(id_lab)+"\n")
                            asembler.write("D_"+str(id_lab)+"\n")
                            asembler.write("\t\tLOAD R0, (R0)\n")

                            id_lab += 1
            elif cvor.znak == "<log_i_izraz>":
                consts += izracunaj_izraz(cvor.djeca[0], djelokrug, asembler, varijable, funkcije, tr_f)
                id_save = id_lab
                asembler.write("\t\tPOP R0\n")
                asembler.write("\t\tCMP R0, 0\n")
                asembler.write("\t\tJP_NE TR_" + str(id_lab) + "\n")
                asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                asembler.write("\t\tJP KR" + str(id_lab)+"\n")
                asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                asembler.write("DALJ_" + str(id_lab) + "\n")

                id_lab += 1 
                asembler.write("\t\t;izraz p\n")
                consts += izracunaj_izraz(cvor.djeca[2], djelokrug, asembler, varijable, funkcije, tr_f)
                asembler.write("\t\t;izraz k\n")
                asembler.write("\t\tPOP R1\n")

                asembler.write("\t\tCMP R1, 0\n")
                asembler.write("\t\tJP_NE TR_" + str(id_lab) + "\n")
                asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R1\n")
                asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R1\n")
                asembler.write("DALJ_" + str(id_lab) + "\t\t")
                asembler.write("\t\tAND R0, R1, R0\n")
                asembler.write("KR"+str(id_save)+"\n")

                id_lab += 1 
            
            elif cvor.znak == "<log_ili_izraz>":
                consts += izracunaj_izraz(cvor.djeca[0], djelokrug, asembler, varijable, funkcije, tr_f)
                id_save = id_lab
                asembler.write("\t\tPOP R0\n")
                asembler.write("\t\tCMP R0, 0\n")
                asembler.write("\t\tJP_NE TR_" + str(id_lab) + "\n")
                asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                asembler.write("\t\tJP KR" + str(id_lab)+"\n")
                asembler.write("DALJ_" + str(id_lab) + "\t\t")

                id_lab += 1 
                asembler.write("\t\t;izraz p\n")
                consts += izracunaj_izraz(cvor.djeca[2], djelokrug, asembler, varijable, funkcije, tr_f)
                asembler.write("\t\t;izraz k\n")
                asembler.write("\t\tPOP R1\n")

                asembler.write("\t\tCMP R1, 0\n")
                asembler.write("\t\tJP_NE TR_" + str(id_lab) + "\n")
                asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R1\n")
                asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R1\n")
                asembler.write("DALJ_" + str(id_lab) + "\t\t")
                asembler.write("\t\tOR R0, R1, R0\n")
                asembler.write("KR"+str(id_save)+"\n")

                id_lab += 1 

            else:
                consts += izracunaj_izraz(cvor.djeca[0], djelokrug, asembler, varijable, funkcije, tr_f)
                consts += izracunaj_izraz(cvor.djeca[2], djelokrug, asembler, varijable, funkcije, tr_f)
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
                    asembler.write("DALJ_" + str(id_lab) + "\n")
                    id_lab += 1
                elif cvor.djeca[1].znak == "OP_NEQ":
                    asembler.write("\t\tCMP R0, R1\n")
                    asembler.write("\t\tJP_NE FA_" + str(id_lab) + "\n")
                    asembler.write("TR_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                    asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                    asembler.write("FA_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                    asembler.write("DALJ_" + str(id_lab) + "\n")
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
                    asembler.write("DALJ_" + str(id_lab) + "\n")
                    id_lab += 1
                elif cvor.djeca[1].znak == "OP_GT":
                    asembler.write("\t\tCMP R1, R0\n")
                    asembler.write("\t\tJP_SGT TR_" + str(id_lab) + "\n")
                    asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                    asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                    asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                    asembler.write("DALJ_" + str(id_lab) + "\n")
                    id_lab += 1 
                elif cvor.djeca[1].znak == "OP_GTE":
                    asembler.write("\t\tCMP R1, R0\n")
                    asembler.write("\t\tJP_SGE TR_" + str(id_lab) + "\n")
                    asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                    asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                    asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                    asembler.write("DALJ_" + str(id_lab) + "\n")
                    id_lab += 1   
                elif cvor.djeca[1].znak == "OP_LTE":
                    asembler.write("\t\tCMP R1, R0\n")
                    asembler.write("\t\tJP_SLE TR_" + str(id_lab) + "\n")
                    asembler.write("FA_" + str(id_lab) + "\t\tMOVE 0, R0\n")
                    asembler.write("\t\tJP DALJ_" + str(id_lab) + "\n")
                    asembler.write("TR_" + str(id_lab) + "\t\tMOVE 1, R0\n")
                    asembler.write("DALJ_" + str(id_lab) + "\n")
                    id_lab += 1   
            
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
                    asembler.write("DALJ_" + str(id_lab) + "\n")
                    id_lab += 1 
                elif cvor.djeca[0].znak == "OP_INC":
                    if cvor.djeca[1].znak == "<postfiks_izraz>":
                        asembler.write("\t\tLOAD R1, (R0)\n")

                        asembler.write("\t\tADD R1, 1, R1\n")
                        asembler.write("\t\tSTORE R1, (R0)\n")
                        asembler.write("\t\tMOVE R1, R0\n")

                    else:
                        asembler.write("\t\tADD R0, 1, R0\n")
                        saveaj_var("R0", cvor.djeca[1].vrijednost, varijable)

                elif cvor.djeca[0].znak == "OP_DEC":
                    if cvor.djeca[1].znak == "<postfiks_izraz>":
                        asembler.write("\t\tLOAD R1, (R0)\n")

                        asembler.write("\t\tSUN R1, 1, R1\n")
                        asembler.write("\t\tSTORE R1, (R0)\n")
                        asembler.write("\t\tMOVE R1, R0\n")

                    else:
                        asembler.write("\t\tSUB R0, 1, R0\n")
                        saveaj_var("R0", cvor.djeca[1].vrijednost, varijable)
                elif cvor.djeca[0].znak == "OP_TILDA":
                    asembler.write("\t\tMOVE 0, R1\n")
                    asembler.write("\t\tSUB R1, 1, R1\n")
                    asembler.write("\t\tSUB R1, R0, R0\n")
            elif cvor.znak == "<izraz_pridruzivanja>":
                if cvor.djeca[0].znak == "<postfiks_izraz>":
                    asembler.write("\t\tSTORE R0, (R1)\n")
                else:
                    saveaj_var("R0", cvor.djeca[0].vrijednost, varijable)
            
            elif cvor.znak == "<postfiks_izraz>":
                if cvor.djeca[1].znak == "OP_INC":
                    #R0 je adresa, R1 niš
                    if cvor.djeca[0].znak == "<postfiks_izraz>":
                        asembler.write("\t\tLOAD R1, (R0)\n")
                        asembler.write("\t\tMOVE R1, R2\n")

                        asembler.write("\t\tADD R1, 1, R1\n")
                        asembler.write("\t\tSTORE R1, (R0)\n")
                        asembler.write("\t\tMOVE R2, R0\n")

                    else:
                        asembler.write("\t\tMOVE R0, R1\n")
                        asembler.write("\t\tADD R1, 1, R1\n")
                        saveaj_var("R1", cvor.djeca[0].vrijednost, varijable)
                
                elif cvor.djeca[1].znak == "OP_DEC":
                    if cvor.djeca[0].znak == "<postfiks_izraz>":
                        asembler.write("\t\tLOAD R1, (R0)\n")
                        asembler.write("\t\tMOVE R1, R2\n")

                        asembler.write("\t\tSUB R1, 1, R1\n")
                        asembler.write("\t\tSTORE R1, (R0)\n")
                        asembler.write("\t\tMOVE R2, R0\n")

                    else:
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
                    asembler.write("DA_"+str(id_lab)+"\n")
                    id_lab+=1
                    asembler.write("\t\tCMP R1, 0\n")
                    asembler.write("\t\tJP_SGE DA_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R1, R1\n")
                    asembler.write("\t\tADD R1, 1, R1\n")
                    asembler.write("\t\tXOR R3, 1, R3\n")
                    asembler.write("DA_"+str(id_lab)+"\n")
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
                    asembler.write("D_"+str(id_lab)+"\n")
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
                    asembler.write("DA_"+str(id_lab)+"\n")
                    id_lab+=1
                    asembler.write("\t\tCMP R1, 0\n")
                    asembler.write("\t\tJP_SGE DA_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R1, R1\n")
                    asembler.write("\t\tADD R1, 1, R1\n")
                    asembler.write("\t\tXOR R3, 1, R3\n")
                    asembler.write("DA_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0, R2\n")
                    id_lab+=1
                    asembler.write("P_"+str(id_lab)+"\t\tCMP R0, R1\n")
                    asembler.write("\t\tJP_ULT D_"+str(id_lab)+"\n")
                    asembler.write("\t\tSUB R0, R1, R0\n")
                    asembler.write("\t\tADD R2, 1, R2\n")
                    asembler.write("\t\tJP P_"+str(id_lab)+"\n")
                    asembler.write("D_"+str(id_lab)+"\n")
                    id_lab += 1
                    asembler.write("\t\tCMP R3, 1\n")
                    asembler.write("\t\tJP_NE D_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R3\n")
                    asembler.write("\t\tSUB R3, R2, R2\n")
                    asembler.write("\t\tADD R2, 1, R2\n")
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
                    asembler.write("DA_"+str(id_lab)+"\n")
                    id_lab+=1
                    asembler.write("\t\tCMP R1, 0\n")
                    asembler.write("\t\tJP_SGE DA_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R1, R1\n")
                    asembler.write("\t\tADD R1, 1, R1\n")
                    asembler.write("DA_"+str(id_lab))
                    asembler.write("\t\tMOVE 0, R2\n")
                    id_lab+=1
                    asembler.write("P_"+str(id_lab)+"\t\tCMP R0, R1\n")
                    asembler.write("\t\tJP_ULT D_"+str(id_lab)+"\n")
                    asembler.write("\t\tSUB R0, R1, R0\n")
                    asembler.write("\t\tADD R2, 1, R2\n")
                    asembler.write("\t\tJP P_"+str(id_lab)+"\n")
                    asembler.write("D_"+str(id_lab)+"\n")
                    id_lab += 1
                    asembler.write("\t\tCMP R3, 1\n")
                    asembler.write("\t\tJP_NE D_"+str(id_lab)+"\n")
                    asembler.write("\t\tMOVE 0FFFFFFFF, R2\n")
                    asembler.write("\t\tSUB R2, R0, R0\n")
                    asembler.write("\t\tADD R0, 1, R0\n")
                    asembler.write("D_"+str(id_lab)+"\n")
                    id_lab += 1
            asembler.write("\t\tPUSH R0\n")

    elif cvor.znak == "BROJ":
        if int(cvor.vrijednost) > 524287 or int(cvor.vrijednost) < -524288:
            v = Varijabla("int", "K_"+str(id_lab), int(cvor.vrijednost), djelokrug)
            consts += [v]
            id_lab += 1
            asembler.write("\t\tLOAD R0, (" + v.adr + ")\n")
            asembler.write("\t\tPUSH R0\n")
        else:
            asembler.write("\t\tMOVE %D "+ cvor.vrijednost +", R0\n")
            asembler.write("\t\tPUSH R0\n")
    elif cvor.znak == "IDN":
        loadaj_var("R0", cvor.vrijednost, varijable)
        asembler.write("\t\tPUSH R0\n")
    elif cvor.znak == "ZNAK":
        asembler.write("\t\tMOVE %D "+ str(ord(cvor.vrijednost.strip("\'"))) +", R0\n")
        asembler.write("\t\tPUSH R0\n")

    return consts

def getFunc(naziv, funkcije):
    for funkcija in funkcije:
        if funkcija.ime == naziv:
            return funkcija

def getLabel(naziv, vars):
    for var in vars:
        if var.naziv == naziv:
            return var.adr
    #getFunc(naziv, vars)

def getVar(naziv, vars):
    for var in vars:
        if var.naziv == naziv:
            return var

def loadaj_var(reg, naziv, varijable, indeks=None):
    adr = getLabel(naziv, varijable)
    asembler.write("\t\tLOAD "+reg+", (" + adr + ")\n")


def saveaj_var(reg, naziv, varijable):
    adr = getLabel(naziv, varijable)
    asembler.write("\t\tSTORE "+reg+", (" + adr + ")\n")


def pred_analiza_funkcije(cvor, djelokrug):
    naziv_og = cvor.djeca[1].vrijednost
    naziv_f = cvor.djeca[1].vrijednost.upper()[0] + str(id_lab)
    argumenti = cvor.djeca[2] 
    lokalne_var = []

    if argumenti.znak == "<lista_parametara>":
        tipovi = argumenti.tipovi
        imena = argumenti.imena
        for i in range(len(tipovi)):
            if SemantickiAnalizator.jeNizX(tipovi[i]):
                lokalne_var += [Varijabla(tipovi[i], imena[i], 0, djelokrug + [naziv_f], True)]
            else:
                lokalne_var += [Varijabla(tipovi[i], imena[i], 0, djelokrug + [naziv_f])]

    blok = cvor.djeca[3]
    if blok.djeca[-1].znak not in ["KR_RETURN", "<naredba_skoka>"]:
        blok.djeca += [Stablo.List("KR_RETURN", None, "return")]
    return Funkcija(naziv_og, lokalne_var, "F_" + naziv_og.upper())

    
def analiza_funkcije(cvor, djelokrug, asembler, lokalne_var, globalne_var, funkcije):
    blok = cvor.djeca[3]
    global id_lab
    naziv_og = cvor.djeca[1].vrijednost
    naziv_f = cvor.djeca[1].vrijednost.upper()[0] + str(id_lab)
    deklaracije = []
    naredbe = []
    argumenti = cvor.djeca[2] 
    
    for dijete in blok.djeca:
        if dijete.znak == "<deklaracija>":
            deklaracije += [dijete]
        else:
            naredbe += [dijete]

    tr_f =  Funkcija(naziv_og, lokalne_var, "F_" + naziv_og.upper())

    asembler.write("F_" + naziv_og.upper())

    ugnijezdene_varijable = analiza_bloka(deklaracije, naredbe, djelokrug + [naziv_f], lokalne_var + globalne_var, asembler, funkcije, tr_f)
    return ugnijezdene_varijable + lokalne_var

def rastav_bloka(naredba):
    if not isinstance(naredba, Stablo.UnutarnjiCvor):
        return [], [naredba]

    new_dekl = []
    new_nar = []
    for dijete in naredba.djeca:
        if dijete.znak == "<deklaracija>":
            new_dekl += [dijete]
        else:
            new_nar += [dijete]
    return new_dekl, new_nar


def analiza_bloka(deklaracije, naredbe, djelokrug, varijable, asembler, funkcije, tr_f, petlja_pod = None):
    lokalne_var = []
    ugnijezdene_var = []
    for deklaracija in deklaracije:
        lokalne_var += analiza_deklaracije(deklaracija, djelokrug, lokalne_var + varijable, asembler, funkcije, tr_f)
    global id_lab
    global izrazi
    for naredba in naredbe:
        if naredba.znak == "<naredba_skoka>":
            if naredba.djeca[0].znak == "KR_RETURN":
                ugnijezdene_var += izracunaj_izraz(naredba.djeca[1], djelokrug, asembler, lokalne_var + varijable, funkcije, tr_f)

                asembler.write("\t\tPOP R6\n")
                asembler.write("\t\tRET\n")
        elif naredba.znak == "KR_RETURN":
            asembler.write("\t\tRET\n")


        elif naredba.znak in izrazi:
            ugnijezdene_var += izracunaj_izraz(naredba, djelokrug, asembler, lokalne_var + varijable, funkcije, tr_f)
            asembler.write("\t\tADD R7, 4, R7\n")
        elif naredba.znak == "<slozena_naredba>":
            new_dekl, new_nar = rastav_bloka(naredba)
            ugnijezdene_var += analiza_bloka(new_dekl, new_nar, djelokrug + [str(id_lab)], lokalne_var + varijable, asembler, funkcije, tr_f, petlja_pod, )
            id_lab += 1
        elif naredba.znak == "<naredba_petlje>":
            if naredba.djeca[0].znak == "KR_WHILE":
                save_lab = id_lab
                id_lab += 1
                asembler.write("W"+str(save_lab))
                ugnijezdene_var += izracunaj_izraz(naredba.djeca[1], djelokrug, asembler, lokalne_var + varijable, funkcije, tr_f)

                asembler.write("\t\tPOP R0\n")
                asembler.write("\t\tCMP R0, 0\n")
                asembler.write("\t\tJP_EQ D_" + str(save_lab) + "\n")
                new_dekl, new_nar = rastav_bloka(naredba.djeca[2])
                new_petlja_pod = ("W"+str(save_lab), "D_"+str(save_lab))
                ugnijezdene_var += analiza_bloka(new_dekl, new_nar, djelokrug + [str(save_lab)], lokalne_var + varijable, asembler, funkcije, tr_f, new_petlja_pod)

                asembler.write("\t\tJP W"+str(save_lab)+"\n")
                asembler.write("D_" + str(save_lab))
            
            elif naredba.djeca[0].znak == "KR_FOR":
                if len(naredba.djeca[1].djeca) > 0:
                    ugnijezdene_var += izracunaj_izraz(naredba.djeca[1], djelokrug, asembler, lokalne_var + varijable, funkcije, tr_f)
                    asembler.write("\t\tADD R7, 4, R7\n")

                save_lab = id_lab
                id_lab += 1       
                asembler.write("F"+str(save_lab))
                if len(naredba.djeca[2].djeca) > 0:
                    ugnijezdene_var += izracunaj_izraz(naredba.djeca[2], djelokrug, asembler, lokalne_var + varijable, funkcije, tr_f)
                    asembler.write("\t\tPOP R0\n")
                    asembler.write("\t\tCMP R0, 0\n")
                    asembler.write("\t\tJP_EQ D_" + str(save_lab) + "\n")
                
                if naredba.djeca[3].znak == "<slozena_naredba>":
                    new_dekl, new_nar = rastav_bloka(naredba.djeca[3])
                    new_petlja_pod = ("F"+str(save_lab), "D_"+str(save_lab))
                    ugnijezdene_var += analiza_bloka(new_dekl, new_nar, djelokrug + [str(save_lab)], lokalne_var + varijable, asembler, funkcije, tr_f, new_petlja_pod)

                else:
                    new_dekl, new_nar = rastav_bloka(naredba.djeca[4])
                    new_petlja_pod = ("C_"+str(save_lab), "D_"+str(save_lab))
                    ugnijezdene_var += analiza_bloka(new_dekl, new_nar, djelokrug + [str(save_lab)], lokalne_var + varijable, asembler, funkcije, tr_f, new_petlja_pod)

                    asembler.write("\nC_"+str(save_lab))
                    ugnijezdene_var += izracunaj_izraz(naredba.djeca[3], djelokrug, asembler, lokalne_var + varijable, funkcije, tr_f)
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

            ugnijezdene_var += izracunaj_izraz(naredba.djeca[1], djelokrug, asembler, lokalne_var + varijable, funkcije, tr_f)

            asembler.write("\t\tPOP R0\n")
            asembler.write("\t\tCMP R0, 0\n")
            asembler.write("\t\tJP_EQ D_" + str(save_lab) + "\n")
            if naredba.djeca[2].znak == "<slozena_naredba>":
                new_dekl, new_nar = rastav_bloka(naredba.djeca[2])
                ugnijezdene_var += analiza_bloka(new_dekl, new_nar, djelokrug + [str(save_lab)], lokalne_var + varijable, asembler, funkcije, tr_f, petlja_pod)

            else:
                new_nar = [naredba.djeca[2]]
                ugnijezdene_var += analiza_bloka([], new_nar, djelokrug + [str(save_lab)], lokalne_var + varijable, asembler, funkcije, tr_f, petlja_pod)

            asembler.write("D_" + str(save_lab)+"\n")
            if len(naredba.djeca) > 3:
                new_dekl, new_nar = [], [naredba.djeca[4]]
                ugnijezdene_var += analiza_bloka(new_dekl, new_nar, djelokrug + [str(save_lab)], lokalne_var + varijable, asembler, funkcije, tr_f, petlja_pod)


    return lokalne_var + ugnijezdene_var

obilazak(korijen_gen_st)


globalne_varijable = []
funkcije_vars = []
funkcije = []

asembler.write("\t\t`ORG 0\n")
asembler.write("\t\tMOVE 4000, R7\n")
asembler.write("\t\tMOVE 3000, R5\n")
for i in glob_var:
    globalne_varijable += analiza_deklaracije(i, ["G"], globalne_varijable, asembler, [], [])


asembler.write("\n\t\tCALL F_MAIN\n")
asembler.write("\t\tHALT\n\n")

for i in range(len(glob_f)):
    f = pred_analiza_funkcije(glob_f[i], [])
    funkcije += [f]
    #globalne_varijable += f.args
for i in range(len(glob_f)):
    funkcije_vars += [analiza_funkcije(glob_f[i], [], asembler, funkcije[i].args, globalne_varijable, funkcije)]

for var in globalne_varijable:
    asembler.write(var.kod())

#for f in funkcije:
#    for a in f.args:
#        asembler.write(a.kod())


for vars in funkcije_vars:
    for var in vars:
        asembler.write(var.kod())
    
asembler.close()
#glob_var = upis_golbalnih(glob_var, asembler)
#glob_f = upis_funkcija(glob_f, asembler)
