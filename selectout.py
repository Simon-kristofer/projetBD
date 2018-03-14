import sys

if len(sys.argv) < 3 :
    print("erreur, utilisation :\n " + sys.argv[0] + " fichier.out")
    sys.exit(-1)



minConf=sys.argv[2]
minConf=int(minConf)




fichier_in=open(sys.argv[1],"r")

for ligne in fichier_in:
	val = str.split(ligne," ")[-1]
	val = int(val[1:-2])	
	if val >= minConf:
		print (ligne[:-1])

fichier_in.close()
