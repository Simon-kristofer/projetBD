import sys

if len(sys.argv) < 3 :
    print("erreur, utilisation :\n " + sys.argv[0] + " fichier.out")
    sys.exit(-1)



minConf=sys.argv[2]
minConf=int(minConf)




fichier_in=open(sys.argv[1],"r")
fichier_out=open(sys.argv[1]+".freq","w")
for ligne in fichier_in:
	val = str.split(ligne," ")[-1]
	val = int(val[1:-2])	
	if val >= minConf:
		 fichier_out.write(ligne)

fichier_in.close()
fichier_out.close()
