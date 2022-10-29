import json
import sys
import pretvorba
import itertools


class Regex:
    def __init__(self, name, expression):
        self.name, self.expression = name, expression

    def __str__(self):
        return "Naziv: " + self.name + "\nIzraz: " + self.expression


class Akcija:
    brojac_id = itertools.count()
    def __init__(self,stanje, regex, lex, args):
        self.id = next(Akcija.brojac_id)
        self.stanje = stanje
        self.regex = regex
        self.lex = "" if lex == '-' else lex
        self.novi_redak = False
        self.udji_u_stanje = None
        self.vrati_se = -1    #Marin se zajebaje s ovim
        self.automat = pretvorba.Automat()
        self.pocetno, self.prihvatljivo = pretvorba.pretvori(self.regex, self.automat)

        for arg in args:
            if(arg[0] == 'N'): #NOVI_REDAK
                self.novi_redak = True
            elif(arg[0] == 'U'): #UDJI_U_STANJE
                self.udji_u_stanje = arg.split(" ")[1]
            elif(arg[0] == 'V'): #VRATI_SE
                self.vrati_se = arg.split(" ")[1]
            else:
                print("Nepoznat argument akcije: " + arg, sys.stderr)

    def ukloni_navodnike(self, string):
        new_string = ""

        for i in range(len(string)):
            if(string[i] == "\"" and (string[i - 1].isnumeric() or string[i + 1].isnumeric())):
                continue
            else:
                new_string += string[i]
        return new_string


    def __str__(self):
        string = json.dumps(self.id) + ", " + json.dumps(self.stanje) + ", " + json.dumps(self.regex) + ", " + json.dumps(self.lex) + ", " + ("True" if (self.novi_redak) else "False") + ", "
        string += ("None" if self.udji_u_stanje == None else json.dumps(self.udji_u_stanje)) + ", " + json.dumps(self.vrati_se) + ", " 
        #string += self.ukloni_navodnike(self.automat.__str__()) + ", " + json.dumps(self.pocetno) + ", " + json.dumps(self.prihvatljivo)
        string += self.automat.__str__() + ", " + json.dumps(self.pocetno) + ", " + json.dumps(self.prihvatljivo)
        return string

def ulaz():
    file_object = open('test/input.txt', 'r')
    lines = file_object.read().split("\n")
    file_object.close()
    
    #lines = sys.stdin.read().split("\n")
    #print(lines)

    regexi = []
    stanja = []
    lexevi = []
    akcije = []
    
    i = 0
    while(lines[i][0] != '%' and lines[i][1] != 'X'):
        line = lines[i]
        regex = Regex(line[1:line.find('}')], line[line.find('}')+1:].strip())

        for prev_regex in regexi:
            regex.expression = regex.expression.replace("{" + prev_regex.name + "}", "(" + prev_regex.expression + ")")

        regexi += [regex]
        i += 1
    
    stanja += lines[i].split()[1:]
    
    i += 1
    while(lines[i][0] != '%' and lines[i][1] != 'L'):
        i += 1
    
    lexevi += lines[i].split()[1:]

    i+=1
    while(i < len(lines)):
        line = lines[i]
        if(line[0] == "<"):
            stanje = line[1:line.find('>')]
            regex = line[line.find('>') + 1:]
            for st_regex in regexi:
                regex = regex.replace("{" + st_regex.name + "}", "(" + st_regex.expression + ")")
            i+=2
            lex = lines[i]
            i+=1
            args = []
            while(lines[i][0] != '}'):
                args += [lines[i]]
                i+=1

            akcija = Akcija(stanje, regex, lex, args)
            akcije += [akcija]
            #print(akcija)
            #print()

            i+=1

    return stanja[0], stanja, akcije     #pocetno stanje, stanja i akcije
