#!/usr/bin/env python3
import gi
import os
import threading

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Minage",
                            default_width=320)
        self.boite = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sujet = Gtk.Entry()
        self.sujet.set_text("Python")
        self.lbl_sujet = Gtk.Label("Recherche")
        self.nbtweet = Gtk.Entry()
        self.nbtweet.set_text("200")
        self.lbl_tweet = Gtk.Label("Nombre de tweets")
        self.frequence = Gtk.Entry()
        self.frequence.set_text("30")
        self.lbl_frequence = Gtk.Label("Fréquence")
        self.nomfic = Gtk.Entry()
        self.nomfic.set_text("monfichier.final.csv")
        self.lbl_nomfic = Gtk.Label("Nom fichier")
        self.freq_mi = Gtk.Entry()
        self.freq_mi.set_text("200")
        self.lbl_freq_mi = Gtk.Label("Fréquence mots inutiles")
        self.lbl_status = Gtk.Label("Sortie")
        self.btn_miner = Gtk.Button(label="Valider")
        self.btn_miner.connect("clicked", self.on_button_clicked)
        self.progres=Gtk.ProgressBar()

        self.sc = threading.Semaphore()
        
        self.add(self.boite)
        self.boite.add(self.lbl_sujet)
        self.boite.add(self.sujet)
        self.boite.add(self.lbl_tweet)
        self.boite.add(self.nbtweet)
        self.boite.add(self.lbl_frequence)
        self.boite.add(self.frequence)
        self.boite.add(self.lbl_nomfic)
        self.boite.add(self.nomfic)
        self.boite.add(self.lbl_freq_mi)
        self.boite.add(self.freq_mi)
        self.boite.add(self.btn_miner)
        self.boite.add(self.progres)
        self.boite.add(self.lbl_status)
        
    def on_button_clicked(self, widget):
        threading.Thread(target=self.miner).start()
        
    def miner(self):
        self.sc.acquire()
        self.progres.set_fraction(0)
        self.lbl_status.set_text("Récupération des tweets")
        nom_temp = "_tempfic_.csv"
        os.system("rm "+nom_temp)
        os.system("./miner.py \"" + self.sujet.get_text() +
                  "\" " + self.nbtweet.get_text() + " " +   nom_temp )
        self.lbl_status.set_text("Génération mots inutiles")
        self.progres.set_fraction(0.15)
        os.system("./generer_inutiles.py " +
                  self.freq_mi.get_text())
        self.lbl_status.set_text("Nettoyage CSV")
        self.progres.set_fraction(0.30)
        os.system("./nettoyer.py " + nom_temp)
        self.lbl_status.set_text("Conversion en .trans")
        self.progres.set_fraction(0.45)
        os.system("./csvtotrans.py " + nom_temp + ".propre")
        self.lbl_status.set_text("Recherche motifs fréquents")
        self.progres.set_fraction(0.60)
        os.system("./apriori/apriori " +
                  nom_temp + ".propre.trans 30 " +
                  nom_temp + ".out")
        self.lbl_status.set_text("Tri par fréquence")
        self.progres.set_fraction(0.75)
        os.system("./selectout.py " + nom_temp + ".out " +
                  self.frequence.get_text())
        self.lbl_status.set_text("Génération CSV")
        self.progres.set_fraction(0.92)
        os.system("./outtocsv.py " + nom_temp + ".out.freq "
                  + nom_temp + ".propre.dico")
        os.system("mv " + nom_temp + ".out.freq.csv "
                  + self.nomfic.get_text())
        self.progres.set_fraction(1)
        self.lbl_status.set_text("Fichier généré : " +
                                 self.nomfic.get_text())
        self.sc.release()

GObject.threads_init()
win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
