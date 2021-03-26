import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# # %matplotlib inline
# plt.style.use("classic")

#_____________________________________________________________________________

class R_Wert:
     def __init__(self, stärke,l, name="R"):
        self.name = name
        self.stärke = stärke
        self.l = l
        
     def R_berechnen(self):
        R = self.stärke / self.l
        return R

#_____________________________________________________________________________

class U_Wert:
    def __init__(self, *args, frsi=0.17, frse=0.04):
        self.args = args
        self.frsi = frsi
        self.frse = frse
    def U_berechnen(self):
        Rges = self.frsi + self.frse
        for i in range(len(self.args)):
            Rges = Rges + self.args[i].R_berechnen()
        U = 1/Rges
        return U


#__________________________________________________________________________________________________________

# Ich versuche mal Hüllflächenelemente als Klassen
class Dach:
    def __init__(self, name="Dach", fläche=0, orientierung=0, neigung=0, U_Wert=0.20, Fx=1, Fen=False):
        self.name = name
        self.fläche = fläche
        self.orientierung = orientierung
        self.neigung = neigung
        self.U_Wert = U_Wert
        self.Fx = Fx
        self.Fen= Fen
class OGD:
    def __init__(self, name="OGD", fläche=0, orientierung=0, neigung=0, U_Wert=0.20, Fx=0.8, Fen=False):
        self.name = name
        self.fläche = fläche
        self.orientierung = orientierung
        self.neigung = neigung
        self.U_Wert = U_Wert
        self.Fx = Fx
        self.Fen= Fen
#     def fläche_abrufen(self):
#         print(fläche)
class Außenwand:
    def __init__(self, name="Außenwand", fläche=0, orientierung=90, neigung=90, U_Wert=0.28, Fx=1, Fen=False):
        self.name = name
        self.fläche = fläche
        self.orientierung = orientierung
        self.neigung = neigung
        self.U_Wert = U_Wert
        self.Fx = Fx
        self.Fen= Fen
class Fenster:
    def __init__(self, name="Fenster", fläche=0, orientierung=90, neigung=90, U_Wert=1.30, Fx=1, 
                 rahmenanteil=0.7, verschattung=0.9,sonnenschutz=1, strahlungseinfall=0.9,g_Wert=0.6, 
                 Fen=True):
        self.name = name
        self.fläche = fläche
        self.orientierung = orientierung
        self.neigung = neigung
        self.U_Wert = U_Wert
        self.Fx = Fx
        self.rahmenanteil = rahmenanteil
        self.verschattung = verschattung
        self.sonnenschutz = sonnenschutz
        self.strahlungseinfall = strahlungseinfall
        self.g_Wert = g_Wert
        self.Fen= Fen
class Bodenplatte:
    def __init__(self, name="Bodenplatte", fläche=0, orientierung=0, neigung=0, U_Wert=0.30, Fx=0.5, Fen=False):
        self.name = name
        self.fläche = fläche
        self.orientierung = orientierung
        self.neigung = neigung
        self.U_Wert = U_Wert
        self.Fx = Fx
        self.Fen= Fen        

#_____________________________________________________________________________________________________________


class Monatsbilanz():
    def __init__(self, *args, name="Projekt", geschossanzahl=2, geschosshöhe=2.9, wärmebrückenzuschlag=0.05, 
                 luftwechsel=0.6, einfamilienhaus=False, schweresGebäude=True):
        self.name = name
        self.geschossanzahl = geschossanzahl
        self.geschosshöhe = geschosshöhe
        self.wärmebrückenzuschlag = wärmebrückenzuschlag
        self.luftwechsel = luftwechsel
        self.einfamilienhaus = einfamilienhaus
        self.schweresGebäude = schweresGebäude
        self.args = args
    
    def konstanten_berechnen(self, a_boden):
        global Luftdichte
        Luftdichte = 1.2041 # in kg/m³
        global Innentemperatur
        Innentemperatur = 19
        global CwirkLuft
        CwirkLuft = 0.0002778 # in kWh/kgK

        global volumen
        volumen = self.geschossanzahl * self.geschosshöhe * a_boden

        global Cwirk
        if self.schweresGebäude == True:
            Cwirk = 50*volumen # in Wh//m³K multipliziert mit Volumen kürzt sich m³ weg
        else:
            Cwirk = 15*volumen
        

        if self.einfamilienhaus == True & self.geschossanzahl < 4:
            luftvolumen = 0.76 * volumen
        else:
            luftvolumen = 0.8 * volumen

        global nutzfläche
        nutzfläche = 0.32 * volumen
        
        # Hv = Dichte der Luft (= 1,2041) [kg/m³] * spezifische Wärmekapazität[kJ/kgK] * Luftstrom des beheizten Raumes[m³/h]
        global Hv
        Hv = 0.34*self.luftwechsel*luftvolumen     

        return Luftdichte, Innentemperatur, CwirkLuft, volumen, Cwirk, luftvolumen, nutzfläche, Hv


    def bauteilliste_erstellen(self): #muss das hier eigentlich eine Funktion sein?
        global bauteilliste
        bauteilliste = pd.DataFrame(columns= ["Bauteilbezeichnung", 
                                              "Orientierung", 
                                              "Neigung", 
                                              "Fläche", 
                                              "U-Wert", 
                                              "Fx", 
                                              "W/K"])
        for i in range(len(self.args)):
            zwischen_df = pd.DataFrame([[self.args[i].name,
                                         self.args[i].orientierung,
                                         self.args[i].neigung,
                                         self.args[i].fläche,
                                         self.args[i].U_Wert,
                                         self.args[i].Fx, 
                                         (self.args[i].fläche*self.args[i].U_Wert*self.args[i].Fx)]],
                                       columns= bauteilliste.columns)
            bauteilliste = bauteilliste.append (zwischen_df, ignore_index=True)
        
        bauteilliste.index = bauteilliste.index + 1
        global hüllfläche
        hüllfläche = bauteilliste["Fläche"].sum()
        global a_v_verhältnis
        a_v_verhältnis = hüllfläche/volumen
        return bauteilliste, hüllfläche, a_v_verhältnis

    def fensterliste_erstellen(self):
        global fenster
        fenster = []
        for i in self.args:
            if i.Fen == True:
                fenster.append(i)
        
        global fensterliste
        fensterliste = pd.DataFrame(columns=["Bezeichnung", 
                                             "Fläche", 
                                             "Orientierung", 
                                             "Neigung", 
                                             "Faktor_Rahmenanteil",
                                             "Verschattung", 
                                             "Sonnenschutz", 
                                             "Nichtsenkrechter_Strahlungseinfall",
                                             "Energie_Durchlassgrad",
                                             "effekt.Fläche"
                                            ])
        for i in range(len(fenster)):
            zwischen_df = pd.DataFrame([[fenster[i].name,
                                         fenster[i].fläche,
                                         fenster[i].orientierung,
                                         fenster[i].neigung,
                                         fenster[i].rahmenanteil,
                                         fenster[i].verschattung,
                                         fenster[i].sonnenschutz,
                                         fenster[i].strahlungseinfall,
                                         fenster[i].g_Wert,
                                         (fenster[i].fläche*fenster[i].rahmenanteil*fenster[i].verschattung*fenster[i].sonnenschutz*fenster[i].strahlungseinfall*fenster[i].g_Wert
                                         )
                                         ]],
                                       columns= fensterliste.columns)

            fensterliste = fensterliste.append (zwischen_df, ignore_index=True)
            
        fensterliste.index = fensterliste.index + 1
        return fensterliste        


    def monatsbilanzierung_erstellen(self):
        monatsbilanzierung = pd.DataFrame(columns=["Jan", "Feb", "Mrz", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", 
                                   "Okt", "Nov", "Dez"])
        monatsbilanzierung.loc["Tage_pro_Monat"] = [31,28,31,30,31,30,31,31,30,31,30,31]
        Referenzklima_Potsdam = pd.read_csv("Daten/Referenzklima_Potsdam.csv")
        mittl_temp = Referenzklima_Potsdam.to_numpy().reshape(-1)
        monatsbilanzierung.loc["Mittl.Außentemp."] = mittl_temp
        strahlungsangebot = pd.read_csv("Daten/Strahlungsangebot_Potsdam.csv",index_col="Ausrichtung")
		# 5 W/m² interne Wärmegewinne
        monatsbilanzierung.loc["Interne_Gewinne"] = (5*24*monatsbilanzierung.loc["Tage_pro_Monat"]*nutzfläche)/1000

        for f in fenster:
            	if f.orientierung <= 45 or f.orientierung > 315:
            		monatsbilanzierung.loc[f.name] = strahlungsangebot.loc["Nord"] * f.fläche
            	elif f.orientierung <= 135 and f.orientierung > 45:
            		monatsbilanzierung.loc[f.name] = strahlungsangebot.loc["Ost"] * f.fläche
            	elif f.orientierung <= 225 and f.orientierung > 135:
            		monatsbilanzierung.loc[f.name] = strahlungsangebot.loc["Süd"] * f.fläche
            	elif f.orientierung <= 315 and f.orientierung > 225:
            		monatsbilanzierung.loc[f.name] = strahlungsangebot.loc["West"] * f.fläche

        monatsbilanzierung.loc["Solare_Gewinne"] = monatsbilanzierung.iloc[3:].sum()

        monatsbilanzierung.loc["Gesamtgewinne"] = monatsbilanzierung.iloc[-1] + monatsbilanzierung.iloc[2]

        monatsbilanzierung.loc["Tranmissionsverluste"] = (monatsbilanzierung.loc["Tage_pro_Monat"]*24*bauteilliste["W/K"].sum()*(Innentemperatur-monatsbilanzierung.loc["Mittl.Außentemp."]))/1000
        monatsbilanzierung.loc["Wärmebrückenverluste"] = (monatsbilanzierung.loc["Tage_pro_Monat"]*24*self.wärmebrückenzuschlag*hüllfläche*(Innentemperatur-monatsbilanzierung.loc["Mittl.Außentemp."]))/1000
        monatsbilanzierung.loc["Summe"] = monatsbilanzierung.loc["Tranmissionsverluste"] + monatsbilanzierung.loc["Wärmebrückenverluste"]
		# Red.VerlusteNachtabschaltung:
        # # Nachtabschaltung auch in DIN 4108-6 nachschlagen ?
        monatsbilanzierung.loc["Red.VerlusteNachtabschaltung"] = 0
        # Lüftungsverluste (Phi) = Hv * (Innentemperatur - Norm-Außentemperatur)
        monatsbilanzierung.loc["Lüftungsverluste"] = Hv*(Innentemperatur-monatsbilanzierung.loc["Mittl.Außentemp."])*monatsbilanzierung.loc["Tage_pro_Monat"]*24/1000
        # Gesamtverluste
        monatsbilanzierung.loc["Gesamtverluste"] = monatsbilanzierung.loc["Summe"]+monatsbilanzierung.loc["Lüftungsverluste"]+monatsbilanzierung.loc["Red.VerlusteNachtabschaltung"]
        # Gewinne_Gesamt
        monatsbilanzierung.loc["Gewinne_Gesamt"] = monatsbilanzierung.loc["Solare_Gewinne"]+monatsbilanzierung.loc["Interne_Gewinne"]

        
        # Alpha berechnen. Brauche ich für folgende Berechnungen. Nach DIN 4108-6:2003-06
        global Ht
        Ht = bauteilliste["W/K"].sum() + (self.wärmebrückenzuschlag*hüllfläche)
        H = Ht + Hv
        zeitkonstante = Cwirk / H
        idxkonst = ["gamma"]
        konst = pd.DataFrame(columns=monatsbilanzierung.columns, index = idxkonst)
        
        verluste = monatsbilanzierung.loc["Gesamtverluste"]
        for i in range(len(verluste)):
        	if verluste[i] == 0:
        		verluste[i] = 0.0001
        
        konst.loc["gamma"] = monatsbilanzierung.loc["Gewinne_Gesamt"]/monatsbilanzierung.loc["Gesamtverluste"]

        # for col in konst:
        # 	konst[col].loc["gamma"] = monatsbilanzierung[col].loc["Gewinne_Gesamt"]/monatsbilanzierung[col].loc["Gesamtverluste"]
        	# if konst[col].loc["gamma"] >1:
        	# 	konst[col].loc["gamma"] = 1
        alpha = 1 + zeitkonstante/16

        monatsbilanzierung.loc["Ausnutzungsgrad_Gewinne"] = 0
        # Ausnutzungsgrad Gewinne. Nicht klar, wie der Wert ermittelt wird
        # Wenn Tau größer 1 dann sind die Gewinne größer als die Verluste, d.h. das gilt für Sommer
        for col in monatsbilanzierung:
        	if konst[col].loc["gamma"] != 1:
        		monatsbilanzierung[col].loc["Ausnutzungsgrad_Gewinne"] = (1-(konst[col].loc["gamma"]**alpha))/(1-(konst[col].loc["gamma"]**(alpha+1)))
        	else:
        		monatsbilanzierung[col].loc["Ausnutzungsgrad_Gewinne"] = 0

        # Heizwärmebedarf
        monatsbilanzierung.loc["Heizwärmebedarf"] = monatsbilanzierung.loc["Gesamtverluste"] -(monatsbilanzierung.loc["Ausnutzungsgrad_Gewinne"]*monatsbilanzierung.loc["Gewinne_Gesamt"])

        # Heizgrenztemp = Tagesmitteltemperatur, ab der ein Gebäude beheizt werden muss. 
        # Kann nach DIN 18599-5:2011-12 berechnet werden aber das ist viel zu kompliziert
        # Nach DIN 4108-6:2003-06:
        ausnutz = alpha/(alpha+1)
        monatsbilanzierung.loc["Heizgrenztemp."]=Innentemperatur-(monatsbilanzierung.loc["Ausnutzungsgrad_Gewinne"]*ausnutz*monatsbilanzierung.loc["Gewinne_Gesamt"])/(0.024*H*monatsbilanzierung.loc["Tage_pro_Monat"]) # 0,024 in Wd Watttagen
        
        # Heiztage gemäß 4108-6:2003-06 Abschnitt 5.5.3:
        # Falls die Heizgrenztemperatur größer ist als die Außenlufttemperatur, zählen die Heiztage zur Heizzeit. 
		# Die genaue  Bestimmung  geschieht  mittels  linearer  Interpolation  zwischen  den  Monaten,  in  denen sich  dieser Wechsel vollzieht, also im Frühjahr und im Herbst.

        for col in monatsbilanzierung:
        	monatsbilanzierung[col].loc["Tranmissionsverluste"] = round(monatsbilanzierung[col].loc["Tranmissionsverluste"],0)
        	monatsbilanzierung[col].loc["Wärmebrückenverluste"] = round(monatsbilanzierung[col].loc["Wärmebrückenverluste"],0)
        	monatsbilanzierung[col].loc["Summe"] = round(monatsbilanzierung[col].loc["Summe"],0)
        	monatsbilanzierung[col].loc["Lüftungsverluste"] = round(monatsbilanzierung[col].loc["Lüftungsverluste"],0)
        	monatsbilanzierung[col].loc["Gesamtverluste"] = round(monatsbilanzierung[col].loc["Gesamtverluste"],0)
        	monatsbilanzierung[col].loc["Interne_Gewinne"] = round(monatsbilanzierung[col].loc["Interne_Gewinne"],0)
        	monatsbilanzierung[col].loc["Solare_Gewinne"] = round(monatsbilanzierung[col].loc["Solare_Gewinne"],0)   
        	monatsbilanzierung[col].loc["Gewinne_Gesamt"] = round(monatsbilanzierung[col].loc["Gewinne_Gesamt"],0)   
        	monatsbilanzierung[col].loc["Heizwärmebedarf"] = round(monatsbilanzierung[col].loc["Heizwärmebedarf"],0)   
        	monatsbilanzierung[col].loc["Heizgrenztemp."] = round(monatsbilanzierung[col].loc["Heizgrenztemp."],2)   
        	monatsbilanzierung[col].loc["Ausnutzungsgrad_Gewinne"] = round(monatsbilanzierung[col].loc["Ausnutzungsgrad_Gewinne"],2)

        return monatsbilanzierung


