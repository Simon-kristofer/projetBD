#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    print("Erreur : frequence min requise")
    sys.exit(-1)

freq = float(sys.argv[1])

try :
    freq_mot = open("frequence_mots.txt", "r")
    mot_inutile = open("mots_inutiles.txt.out", "w")
except e:
    print(e)

for ligne in freq_mot:
    mots = str.split(ligne,"\t")
    if float(mots[1]) > freq:
        mot_inutile.write(mots[0] + "\n")
 
    
freq_mot.close()
mot_inutile.close()

