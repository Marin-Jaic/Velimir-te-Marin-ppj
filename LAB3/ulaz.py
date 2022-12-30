from Stablo import *
import sys


def ulaz():
    # ulaz = sys.stdin.read().split("\n")
    file = open("./LAB3/ulazi/ulaz.sem", "r")
    ulaz = file.readlines()

    def stvori_cvor(line_index, depth):
        #print(line_index + 1, depth)
        line = ulaz[line_index]
        #print(line)
        tr_dub = next((index for index, char in enumerate(line) if not char.isspace()), None)
        #print(tr_dub)
        if(tr_dub != depth):
            return None

        split = line.strip().split(" ")
        #print(split)
        if(len(split) > 1):
            return List(split[0], split[1], split[2]), line_index + 1
        elif(len(split) == 1):
            if(split == "$"):
                return ListEps("$"), line_index + 1
            else:
                djeca = []
                li = line_index + 1
                li_pomak = li
                while(li < len(ulaz)):
                    dijete_li = stvori_cvor(li, depth + 1)
                    if(dijete_li == None):
                        #print("dijete je none ", li)
                        break
                    else:
                        dijete = dijete_li[0]
                        li = dijete_li[1]
                        djeca += [dijete]
                return UnutarnjiCvor(split[0], djeca), li

    return stvori_cvor(0, 0)[0]

#for ul in ulaz:
#    tr_raz = index = next((index for index, char in enumerate(ul) if not char.isspace()), None)
#    print(ul, tr_raz)


def ispis_razine(cvorovi, n):
    for cvor in cvorovi:
        for i in range(n):
            print(" ", end="")
        if(isinstance(cvor, List) or isinstance(cvor, ListEps)):
            print(cvor)
        elif(isinstance(cvor, UnutarnjiCvor)):
            print(cvor.znak)
            ispis_razine(cvor.djeca, n + 1)

ispis_razine(ulaz().djeca, 1)
