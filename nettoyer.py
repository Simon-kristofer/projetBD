#!/usr/bin/env python3

import sys
import copy
import enum

if len(sys.argv) < 2:
    print("Erreur, nom du fichier csv requis en argument")
    sys.exit(-1)


entree = open(sys.argv[1], "r")
mots = open("motsinutiles.txt", "r")
sortie = open(sys.argv[1] + ".propre", "w")


dico = list()

for ligne in mots :
    dico.append(ligne[:-1])


for ligne in entree:
    for valeur in str.split(ligne,";"):
        if valeur in dico:
            continue
        sortie.write(valeur)
        sortie.write(";")
    sortie.write("\n")
        

entree.close()
mots.close()
sortie.close()
