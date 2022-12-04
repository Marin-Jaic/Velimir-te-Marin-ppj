class Gramatika: #kinda beskorisna in the grand scheme of things, pomogla mi je s formatiranjem ulaza
    def __init__(self, nezavrsni_znakovi, zavrsni_znakovi, produkcije):
        self.nezavrsni_znakovi = nezavrsni_znakovi
        self.zavrsni_znakovi = zavrsni_znakovi
        self.produkcije = produkcije
        self.t_skup = self.zapocinje()
        # self.t_skup = {}

        # info = {}
        # for znak in nezavrsni_znakovi:
        #     info = self.t(znak, info)

    def zapocinje(self):
        zapocinje_skup = {}
        for znak in self.nezavrsni_znakovi:
            zapocinje_skup[znak] = set()
            
            for produkcija in self.produkcije[znak]:

                if produkcija.ds == ["$"] and znak == self.nezavrsni_znakovi[0]:
                    zapocinje_skup[znak].add("$")
                elif produkcija.ds != ["$"]:     
                    dont_break = True
                    index = 0
                    while dont_break and index < len(produkcija.ds):
                        zapocinje_skup[znak].add(produkcija.ds[index]) 
                        dont_break = False

                        if produkcija.ds[index] in self.nezavrsni_znakovi: 
                            for produkcija2 in self.produkcije[produkcija.ds[index]]:
                                if produkcija2.ds == ["$"]:
                                    dont_break = True
                        
                        index += 1
                    if dont_break and znak == self.nezavrsni_znakovi[0]:
                        zapocinje_skup[znak].add("$")

        ima_nezavrsnih = True
        while(ima_nezavrsnih):
            ima_nezavrsnih = False

            for znak in self.nezavrsni_znakovi:
                novi_skup = set()
                novi_skup = zapocinje_skup[znak].copy()
                for zapocinje_znak in zapocinje_skup[znak]:
                    
                    if zapocinje_znak in self.nezavrsni_znakovi:
                        ima_nezavrsnih = True
                        novi_skup.update(zapocinje_skup[zapocinje_znak])

                        if znak in novi_skup:
                            novi_skup.remove(znak)
                        if zapocinje_znak in novi_skup:
                            novi_skup.remove(zapocinje_znak)

                zapocinje_skup[znak] = novi_skup

        for key in zapocinje_skup.keys():
            zapocinje_skup[key] = list(zapocinje_skup[key])
        return zapocinje_skup

        
    # def t(self, znak, info):
    #     if znak not in self.t_skup.keys():
    #         self.t_skup[znak] = []
    #         info[znak] = [znak]

    #         for produkcija in self.produkcije[znak]:
    #             if produkcija.ds[0] in self.nezavrsni_znakovi and produkcija.ds[0] not in info[znak]:
    #                 info = self.t(produkcija.ds[0], info)
    #                 for zavrsni_znak in self.t_skup[produkcija.ds[0]]:
    #                     self.t_skup[znak].append(zavrsni_znak)
    #             elif produkcija.ds[0] not in self.t_skup[znak]:
    #                 self.t_skup[znak].append(produkcija.ds[0])
        
    #     return info



    def __str__(self):
        output = ""
        first = True
        for key in self.produkcije.keys():
            # output += key + " ::="

            if not first:
                output += "\n"

            first = False

            output += key + " ->"

            for i in range(len(self.produkcije[key])):
                for j in range(len(self.produkcije[key][i].ds)):
                    if j == 0:
                        output += " #" + str(self.produkcije[key][i].id)
                    # if self.produkcije[key][i][j] == "$":
                    #     output += " \"\""
                    # else:
                    #     output += " " + self.produkcije[key][i][j]
                    
                    output += " " + self.produkcije[key][i].ds[j]
                    
                if i + 1 != len(self.produkcije[key]):
                    output += " |"
                
        return output
                    
class produkcija:
     def __init__(self, id, ls, ds):
        self.id = id
        self.ls = ls
        self.ds = ds


def ulaz():
    file_object = open('test/input2.txt', 'r')
    lines = file_object.read().splitlines()
    file_object.close()

    nezavrsni_znakovi = lines[0][2:].strip().split(" ")
    zavrsni_znakovi = lines[1][2:].strip().split(" ")
    syn_znakovi = lines[2][4:].strip().split(" ")

    lines = lines[3:]

    produkcije = {}
    trenutni_lijevi = ""
    trenutni_line = ""
    counter = 1

    for line in lines:
        if line[0] == "<":
            # trenutni_lijevi = line[0:4] # štae ovo marine
            trenutni_lijevi = line[0:line.index(">") + 1]
            continue
        else:
            trenutni_line = line[0:]
            
            if trenutni_lijevi in produkcije.keys():
                produkcije[trenutni_lijevi] += [produkcija(counter, trenutni_lijevi, trenutni_line.strip().split(" "))]

            else:
                produkcije[trenutni_lijevi] = [produkcija(counter, trenutni_lijevi, trenutni_line.strip().split(" "))]
        
        counter += 1

    return nezavrsni_znakovi, zavrsni_znakovi, syn_znakovi, produkcije

# nezavrsni_znakovi, zavrsni_znakovi, syn_znakovi, produkcije = ulaz()
# gramatika = Gramatika(nezavrsni_znakovi, zavrsni_znakovi, produkcije)

#print(nezavrsni_znakovi)
# print(zavrsni_znakovi)
# print(syn_znakovi)
#print(gramatika.t_skup)
