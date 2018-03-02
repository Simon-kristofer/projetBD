#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    print("erreur, utilisation :\n " + sys.argv[0] + " fic.csv")
    sys.exit(-1)

fic_entree = open(sys.argv[1], "r")
fic_sortie = open(sys.argv[1] + ".trans", "w")
fic_dico = open(sys.argv[1] + ".dico", "w")

dico = dict()
i = 0

print("Écriture de la sortie\n")
for ligne in fic_entree:
    for valeur in str.split(ligne,";"):
        if valeur not in dico:
            dico[valeur] = i
            i += 1
        fic_sortie.write(str(dico[valeur]) + " ")
    fic_sortie.write("\n")

print("Écriture du dictionnaire\n")
for clef in dico:
    fic_dico.write(str(dico[clef]) + " : " + clef + "\n")

fic_entree.close()
fic_sortie.close()
fic_dico.close()
