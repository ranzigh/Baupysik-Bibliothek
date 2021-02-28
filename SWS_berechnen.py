from Bib.Anteiliger_Sonneneintragskennwert import *

# Erläuterung: 
# orientierung= "ESW" oder "N"

Musterfenster = Fenster(breite=2, hoehe=2, orientierung="ESW", neigung=90,g_Wert=0.50, Fc_Wert=1.00, 
		Fs_Wert = 1.00)


# Erläuterung: 
# nutzung = "wohnen", "nichtwohnen"
# nachtluftung= "ohne", "erhoht", "hoch"
# bauart= "leicht", "mittel", "schwer"
# klimazone = "a", "b", "c"
# passivkuhlung = "nein", "ja"

Musterraum = Raum(Musterfenster, name= "Musterraum", raumflaeche=20, nutzung="wohnen", 
	nachtluftung="erhoht", klimazone= "b", bauart="mittel", passivkuhlung="nein")

#________________________________________________________________________________________

# Nachweismöglichkeit 1: Fenster vorher definieren und dann in die Nachweisberechnung einfügen

F1 = Fenster (breite=1, hoehe=1.5)
F2 = Fenster (breite=2, hoehe=1)

b = Raum(F1, F1, F1, F1,
	name="b", raumflaeche=20, nachtluftung="erhoht", nutzung="wohnen", bauart="mittel")
b.Nachweis()

# Nachweismöglichkeit 2: Die Fenster direkt in den call der Funktion einfügen

c = Raum(
	Fenster(breite=1, hoehe=1.5), 
	Fenster(breite=2, hoehe=1.5),
	name="c",
	raumflaeche=20, nachtluftung="erhoht", nutzung="wohnen", bauart="mittel")
c.Nachweis()

#________________________________________________________________________________________

