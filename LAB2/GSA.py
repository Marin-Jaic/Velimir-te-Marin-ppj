import pretvorba

lr = pretvorba.generiraj_lr_parser()


sintaksni = open('analizator/SA.py', 'a')


sintaksni.write("\nulazni_niz = dohvati_ulazni_niz()")
sintaksni.write("\nlrparser = " + str(lr))
sintaksni.write("\nlrparser.parsiraj(ulazni_niz)")
sintaksni.write("\nlrparser.ispis_gen_stabla()")
sintaksni.close()