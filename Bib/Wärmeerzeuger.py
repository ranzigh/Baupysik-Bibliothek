import pandas as pd
import numpy as np


def strompreis (Anfangsstrompreis, Energiepreissteigerung):
    preis = [Anfangsstrompreis]
    for i in range (14):
        preis.append(preis[i]*Energiepreissteigerung)
    return preis

def gaspreis (Anfangsgaspreis, Energiepreissteigerung):
    preis = [Anfangsgaspreis]
    for i in range (14):
        preis.append(preis[i]*Energiepreissteigerung)
    return preis

def pelletpreis (Anfangspelletpreis, Energiepreissteigerung):
    preis = [Anfangspelletpreis]
    for i in range (14):
        preis.append(preis[i]*Energiepreissteigerung)
    return preis

def energiepreis(preis_pro_kwh, bedarf_in_kwh, JAZ):
    preis=[]
    for i in range(15):
        preis.append(preis_pro_kwh[i]*(bedarf_in_kwh/JAZ))
    return preis

def co2ausstoss(ausstoss_spezifisch, energiebedarf, JAZ):
    ausstoss_absolut=[]
    for i in range (15):
        ausstoss_absolut.append((ausstoss_spezifisch[i]*(energiebedarf/JAZ))/1000000)
    return ausstoss_absolut

def co2steuer(CO2_Steuer, co2ausstoss):
    steuer=[]
    for i in range(15):
        steuer.append(CO2_Steuer[i]*(co2ausstoss[i]))
    return steuer

def gesamtco2(CO2_Ausstoss):
    gesamt=[CO2_Ausstoss[0]]
    for i in range(14):
        gesamt.append(gesamt[i]+CO2_Ausstoss[i+1])
    return gesamt

def gesamtkosten(Investkosten, Kosten_pro_Jahr):
    gesamt=[Investkosten+Kosten_pro_Jahr[0]]
    for i in range(14):
        gesamt.append(gesamt[i]+Kosten_pro_Jahr[i+1])
    return gesamt

def allgemeines(CO2_Steuer,Strommix_Erneuerbar,CO2_Strom_GEG,CO2_Strom_real,CO2_Gas_GEG, Anfangsstrompreis,Energiepreissteigerung,Anfangsgaspreis,Anfangspelletpreis):
    Allgemeines = pd.DataFrame({'CO2_Steuer': CO2_Steuer,
                      'Strommix_Erneuerbar':Strommix_Erneuerbar,
                      'CO2_Strom_GEG': CO2_Strom_GEG, 
                      'CO2_Strom_real':CO2_Strom_real,
                      'CO2_Gas': CO2_Gas_GEG, 
                      'Strompreis': strompreis (Anfangsstrompreis, Energiepreissteigerung),
                      'Gaspreis':gaspreis (Anfangsgaspreis, Energiepreissteigerung),
                      'Pelletpreis':pelletpreis (Anfangspelletpreis, Energiepreissteigerung)
                      })
    return Allgemeines

def Wärmepumpe(Heiwärmebedarf,TWW_Bedarf, Strompreis,JAZ, Investkosten, Wartungskosten, CO2_Strom_real, CO2_Strom_GEG, CO2_Steuer):
    Energiebedarf = Heiwärmebedarf + TWW_Bedarf
    WP = pd.DataFrame({'Energiekosten':energiepreis(Strompreis, Energiebedarf, JAZ),
                      'Wartungskosten':(Investkosten*Wartungskosten),
                      'CO2_Ausstoss_real':co2ausstoss(CO2_Strom_real, Energiebedarf, JAZ),
                      'CO2_Ausstoss_GEG':co2ausstoss(np.full(shape=15,fill_value=CO2_Strom_GEG), Energiebedarf, JAZ),
                      })
    WP['CO2_Ausstoss_Gesamt'] = gesamtco2(WP["CO2_Ausstoss_real"])
    WP['CO2_Steuer_real'] = co2steuer(CO2_Steuer, WP["CO2_Ausstoss_real"])
    WP['CO2_Steuer_GEG'] = co2steuer(CO2_Steuer, WP["CO2_Ausstoss_GEG"])
    WP['Kosten_pro_Jahr'] = (WP['Energiekosten']+WP["Wartungskosten"]+WP["CO2_Steuer_real"])
    WP['Gesamtkosten'] = gesamtkosten(Investkosten, WP['Kosten_pro_Jahr'])
    return WP

def Brennwert(Heiwärmebedarf,TWW_Bedarf, Gaspreis,JAZ, Investkosten, Wartungskosten, CO2_Gas, CO2_Steuer):
    Energiebedarf = Heiwärmebedarf + TWW_Bedarf
    Brennwert = pd.DataFrame({'Energiekosten':energiepreis(Gaspreis, Energiebedarf, JAZ),
                      'Wartungskosten':(Investkosten*Wartungskosten),
                      'CO2_Ausstoss_GEG':co2ausstoss(np.full(shape=15,fill_value=CO2_Gas), Energiebedarf, JAZ),
                      })
    Brennwert['CO2_Ausstoss_Gesamt'] = gesamtco2(Brennwert["CO2_Ausstoss_GEG"])
    Brennwert['CO2_Steuer_GEG'] = co2steuer(CO2_Steuer, Brennwert["CO2_Ausstoss_GEG"])
    Brennwert['Kosten_pro_Jahr'] = (Brennwert['Energiekosten']+Brennwert["Wartungskosten"]+Brennwert["CO2_Steuer_GEG"])
    Brennwert['Gesamtkosten'] = gesamtkosten(Investkosten, Brennwert['Kosten_pro_Jahr'])
    return Brennwert

def PV_ergänzen(Wärmeerzeuger, Allgemeines, Stromertrag_PV, Eigennutzungsgrad_PV, Investkosten, Investkosten_PV, Wartungskosten, CO2_Steuer):
    Wärmeerzeuger_PV = Wärmeerzeuger.copy()
    invest = Investkosten + Investkosten_PV
    for i in range(15):
        Wärmeerzeuger_PV["Energiekosten"].iloc[i] = Wärmeerzeuger["Energiekosten"].iloc[i] - (Allgemeines["Strompreis"].iloc[i]*Stromertrag_PV*Eigennutzungsgrad_PV)
        Wärmeerzeuger_PV["Wartungskosten"].iloc[i] = Wärmeerzeuger["Wartungskosten"].iloc[i] + Investkosten_PV*Wartungskosten
        Wärmeerzeuger_PV["CO2_Ausstoss_real"].iloc[i] = Wärmeerzeuger["CO2_Ausstoss_real"].iloc[i] * (1-Eigennutzungsgrad_PV)
        Wärmeerzeuger_PV["CO2_Ausstoss_GEG"].iloc[i] = Wärmeerzeuger["CO2_Ausstoss_GEG"].iloc[i] * (1-Eigennutzungsgrad_PV)

    Wärmeerzeuger_PV['CO2_Steuer_real'] = co2steuer(CO2_Steuer, Wärmeerzeuger_PV["CO2_Ausstoss_real"])
    Wärmeerzeuger_PV['CO2_Steuer_GEG'] = co2steuer(CO2_Steuer, Wärmeerzeuger_PV["CO2_Ausstoss_GEG"])    
    Wärmeerzeuger_PV['CO2_Ausstoss_Gesamt'] = gesamtco2(Wärmeerzeuger_PV["CO2_Ausstoss_real"])    
    Wärmeerzeuger_PV['Kosten_pro_Jahr'] = Wärmeerzeuger_PV['Energiekosten'] + Wärmeerzeuger_PV["Wartungskosten"] + Wärmeerzeuger_PV["CO2_Steuer_real"]
    Wärmeerzeuger_PV['Gesamtkosten'] = gesamtkosten(invest, Wärmeerzeuger_PV['Kosten_pro_Jahr'])
    return Wärmeerzeuger_PV