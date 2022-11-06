class Gramatika:
    def __init__(self, produkcije):
        self.produkcije = produkcije
    
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
                for j in range(len(self.produkcije[key][i])):
                    # if self.produkcije[key][i][j] == "$":
                    #     output += " \"\""
                    # else:
                    #     output += " " + self.produkcije[key][i][j]
                    
                    output += " " + self.produkcije[key][i][j]
                    
                if i + 1 != len(self.produkcije[key]):
                    output += " |"
                
        return output
                    

def ulaz():
    file_object = open('test/input.txt', 'r')
    lines = file_object.read().splitlines()
    file_object.close()

    nezavrsni_znakovi = lines[0][2:].strip().split(" ")
    zavrsni_znakovi = lines[1][2:].strip().split(" ")
    syn_znakovi = lines[2][4:].strip().split(" ")

    lines = lines[3:]

    produkcije = {}
    trenutni_lijevi = ""
    trenutni_line = ""
    
    for line in lines:
        if line[0] == "<":
            trenutni_lijevi = line[0:4]
            continue
        else:
            trenutni_line = line[0:]
            
            if trenutni_lijevi in produkcije.keys():
                produkcije[trenutni_lijevi] += [trenutni_line.strip().split(" ")]
            else:
                produkcije[trenutni_lijevi] = [trenutni_line.strip().split(" ")]

    return nezavrsni_znakovi, zavrsni_znakovi, syn_znakovi, produkcije

nezavrsni_znakovi, zavrsni_znakovi, syn_znakovi, produkcije = ulaz()
gramatika = Gramatika(produkcije)

print(nezavrsni_znakovi)
print(zavrsni_znakovi)
print(syn_znakovi)
print(gramatika) 

