import tweepy
import string
consumer_key = "Xj7vw0KHCsUD5BayMAbwirEUq"
consumer_secret = "rcdgisbfApExt50bZd6mVBkaN7wuQ3fzcvw9J4xmFTmOjNYNZ9"
access_token = "4915634062-Z3qzgIwBiTpZ93oN3bCnZCbroOLJsii62M7meLl"
access_token_secret = "0vSQlb1i9piqgOzZhAOGBnXmFmwRwzx30mdfFPTOpoD01"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

requete = "#esperanto"

nbpages = 1

fichier = open("minage.csv", "w")
for i in range(1,nbpages + 1):
    resultats = api.search(q=requete, rpp=100, since_id=i*100)
    for tweet in resultats:
        fichier.write(tweet.created_at.strftime("%d/%m/%Y %H:%M:%S"))
        fichier.write(";")
        fichier.write(tweet.user.screen_name)
        for mot in str.split(tweet.text):
            fichier.write(";")
            fichier.write(mot)
        fichier.write("\n")
            
fichier.close()
