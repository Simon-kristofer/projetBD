#!/usr/bin/env python3

import tweepy
import string
import sys
consumer_key = "Xj7vw0KHCsUD5BayMAbwirEUq"
consumer_secret = "rcdgisbfApExt50bZd6mVBkaN7wuQ3fzcvw9J4xmFTmOjNYNZ9"
access_token = "4915634062-Z3qzgIwBiTpZ93oN3bCnZCbroOLJsii62M7meLl"
access_token_secret = "0vSQlb1i9piqgOzZhAOGBnXmFmwRwzx30mdfFPTOpoD01"



if len(sys.argv) < 4:
    print("utilisation : " + \
          sys.argv[0] + \
          " requete nombre_tweets fichier.csv\n")
    sys.exit(-1)

requete = sys.argv[1]
nbtweets = int(sys.argv[2])
nomfic = sys.argv[3]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

fichier = open(nomfic, "a")

for tweet in tweepy.Cursor(api.search, q=requete, lang="fr").items(nbtweets):
    fichier.write(tweet.created_at.strftime("%d/%m/%Y-%H:%M:%S"))
    fichier.write(";")
    fichier.write(tweet.user.screen_name)
    for mot in str.split(tweet.text):
        fichier.write(";")
        fichier.write(mot)
    fichier.write("\n")
            
fichier.close()
