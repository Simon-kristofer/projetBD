#!/usr/bin/env python3
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Minage")
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
		self.nomfic.set_text("Nom fichier")
		self.lbl_nomfic = Gtk.Label("Nom fichier")
		self.freq_mi = Gtk.Entry()
		self.freq_mi.set_text("200")
		self.lbl_freq_mi = Gtk.Label("Fréquence mots inutiles")
		self.lbl_status = Gtk.Label("Sortie")
		self.btn_miner = Gtk.Button(label="Valider")
		self.btn_miner.connect("clicked", self.on_button_clicked)
		self.progres=Gtk.ProgressBar()
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
		nom_temp = "_tempfic_.csv"
		os.system("miner.py \"" + self.sujet.get_text() +
				"\" " + self.nbtweet.get_text() + " " +
				nom_temp )
		print("ca a marcher")

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
