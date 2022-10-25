import json

class Automat:
    def __init__(self):
        self.prijelazi = dict()
        self.broj_stanja = 0

    def novo_stanje(self):
        self.broj_stanja += 1
        return self.broj_stanja - 1
    
    def dodaj_prijelaz(self, lijevo, desno, znak):
        if lijevo not in self.prijelazi.keys():
            self.prijelazi[lijevo] = dict()
        if(znak not in self.prijelazi[lijevo].keys()):
            self.prijelazi[lijevo][znak] = []
        self.prijelazi[lijevo][znak] += [desno]
    
    def dodaj_epsilon(self, lijevo, desno):
        self.dodaj_prijelaz(lijevo, desno, '$')

    def __str__(self):
        return json.dumps(self.prijelazi)

def je_operator(izraz, i):
    br = 0
    while(i-1 >= 0 and izraz[i-1] == '\\'):
        br += 1
        i -= 1
    
    return br%2 == 0

def pretvori(izraz, automat):
    izbori = []
    br_zagrada = 0
    index_prethodnog_izbora = 0
    pronaden_op_izbora = False

    for i in range(len(izraz)):
        if(izraz[i] == '(' and je_operator(izraz, i)):
            br_zagrada += 1
        elif(izraz[i]==')' and je_operator(izraz, i)):
            br_zagrada -= 1
        elif(br_zagrada == 0 and izraz[i] == '|' and je_operator(izraz, i)):
            izbori += [izraz[index_prethodnog_izbora:i]]
            index_prethodnog_izbora = i + 1
            pronaden_op_izbora = True
    if(pronaden_op_izbora):
        izbori += [izraz[index_prethodnog_izbora:]]
    
    lijevo_stanje = automat.novo_stanje()
    desno_stanje = automat.novo_stanje()
    
    if(pronaden_op_izbora):
        for i in range(len(izbori)):
            priv_lijevo_stanje, priv_desno_stanje = pretvori(izbori[i], automat)
            automat.dodaj_epsilon(lijevo_stanje, priv_lijevo_stanje)
            automat.dodaj_epsilon(priv_desno_stanje, desno_stanje)
    else:
        prefiksirano = False
        zadnje_stanje = lijevo_stanje
        i = 0
        while(i < len(izraz)):
            a, b = None, None
            if(prefiksirano):
                prefiksirano = False
                prijelazni_znak = izraz[i]

                if(izraz[i] == 't'):
                    prijelazni_znak = '\t'
                elif(izraz[i] == 'n'):
                    prijelazni_znak = '\n'
                elif(izraz[i] == '_'):
                    prijelazni_znak = ' '
                a, b = automat.novo_stanje(),  automat.novo_stanje()
                automat.dodaj_prijelaz(a, b, prijelazni_znak)
            else:
                if(izraz[i] == '\\'):
                    prefiksirano = True
                    i += 1
                    continue
                if(izraz[i] != '('):
                    a = automat.novo_stanje()
                    b = automat.novo_stanje()
                    if(izraz[i] == '$'):
                        automat.dodaj_epsilon(a, b)
                    else:
                        automat.dodaj_prijelaz(a, b, izraz[i])
                else:
                    br_zagrada_t = 0
                    j = None

                    #Marin pristup
                    for k in range(i, len(izraz)): 
                        if(izraz[k] == '(' and je_operator(izraz, k)):
                            br_zagrada_t += 1
                        elif(izraz[k]==')' and je_operator(izraz, k)):
                            br_zagrada_t -= 1
                        if(br_zagrada_t == 0):
                            j = k
                            break #Marin dodatak

                    priv_t_lijevo, priv_t_desno = pretvori(izraz[i+1:j], automat)
                    a = priv_t_lijevo
                    b = priv_t_desno
                    i = j
            if(i+1 < len(izraz) and izraz[i+1]=='*'):
                x = a
                y = b
                
                a = automat.novo_stanje()
                b = automat.novo_stanje()
                automat.dodaj_epsilon(a, x)
                automat.dodaj_epsilon(y, b)
                automat.dodaj_epsilon(a, b)
                automat.dodaj_epsilon(y, x)
                i += 1
            
            automat.dodaj_epsilon(zadnje_stanje, a)
            zadnje_stanje = b
            i += 1
        automat.dodaj_epsilon(zadnje_stanje, desno_stanje)
    
    return lijevo_stanje, desno_stanje

#automat = Automat()
#pretvori("((ab)|b+c)", automat)
#for i in automat.prijelazi:
#    print(i, automat.prijelazi[i])

