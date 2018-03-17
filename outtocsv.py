#!/usr/bin/env python3
import sys

if len(sys.argv) < 3:
    print("Erreur utilisation : ./" + sys.argv[0]
          + " fic.out fic.dico")
    sys.exit(-1)

fic = open(sys.argv[1], "r")
ficdic = open(sys.argv[2], "r")
ficout = open(sys.argv[1] + ".csv", "w")

dico = dict()
for ligne in ficdic :
    spl = str.split(ligne)
    if len(spl) == 3 :
        dico[int(spl[0])] = spl[2]
    elif len(spl) == 2 :
        dico[int(spl[0])] = ""
    else:
        continue

for ligne in fic:
    spl = str.split(ligne)
    f = spl.pop()
    for mot in spl:
        ficout.write(dico[int(mot)])
        ficout.write(";")
    ficout.write(f)
    ficout.write("\n")

fic.close()
ficdic.close()
ficout.close()
