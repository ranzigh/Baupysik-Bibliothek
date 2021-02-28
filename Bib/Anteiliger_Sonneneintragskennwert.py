class Fenster:
	def __init__(self, breite, hoehe, orientierung="ESW", neigung=90,g_Wert=0.50, Fc_Wert=1.00, 
		Fs_Wert = 1.00):

		self.breite = breite
		self.hoehe = hoehe
		self.orientierung = orientierung
		self.neigung = neigung
		self.g_Wert = g_Wert
		self.Fc_Wert = Fc_Wert
		self.Fs_Wert = Fs_Wert
		gtot = self.Fc_Wert * self.Fs_Wert * self.g_Wert
		wert = self.breite * self.hoehe * gtot
		self.wert = wert



	def Fensterwert(self):
		gtot = self.Fc_Wert * self.Fs_Wert * self.g_Wert
		wert = self.breite * self.hoehe * gtot
		return wert


class Raum:
	def __init__(self,*args,name, raumflaeche, nutzung="wohnen", nachtluftung="erhoht", 
		klimazone= "b", bauart="mittel", passivkuhlung="nein"):
		self.args = args
		self.name = name
		self.raumflaeche = raumflaeche
		self.nutzung = nutzung
		self.nachtluftung = nachtluftung
		self.klimazone = klimazone
		self.bauart = bauart
		self.passivkuhlung = passivkuhlung

		fges = 0 # gesamte Fensterfläche dummy
		fneig = 0 # Fensterfläche mit Neigung 60 oder weniger dummy
		fgtot04 = 0 # Fensterfläche mit g-Wert 0,40 oder weniger dummy
		fnord = 0 # Fensterfläche mit Ausrichtung Nord dummy
		for i in range(len(self.args)):
			fges = fges + (self.args[i].breite * self.args[i].hoehe)
			if self.args[i].neigung <= 60:
				fneig = fneig + (self.args[i].breite * self.args[i].hoehe)
			if self.args[i].g_Wert <= 0.4:
				fgtot04 = fgtot04 + (self.args[i].breite * self.args[i].hoehe)
			if self.args[i].orientierung == "N":
				fnord = fnord + (self.args[i].breite * self.args[i].hoehe)
		
		self.fges = fges
		self.fneig = fneig
		self.fgtot04 = fgtot04
		self.fnord = fnord

	def Szul(self):
		Szul = self.Sx1() + self.Sx2() + self.Sx3() + self.Sx4() + self.Sx5() + self.Sx6()
		return Szul

	def Nachweis(self):
		Svorh = 0
		for i in range(len(self.args)):
			Svorh = Svorh + self.args[i].wert
		Svorh = Svorh/self.raumflaeche
		if Svorh <= self.Szul():
			print(self.name)
			print("Svorh: ", round(Svorh,3), "\nSzul: ", round(self.Szul(), 3))
			print("Nachweis eingehalten!\n")
		else:
			print(self.name)
			print("Svorh: ", round(Svorh,3), "\nSzul: ", round(self.Szul(), 3))
			print("Nachweis nicht eingehalten!\n")



	def Sx1(self):
		#S1 = 0
		if self.nutzung == "wohnen":
			if self.nachtluftung == "ohne":
				if self.bauart == "leicht" and self.klimazone == "a":
					S1 = 0.071
				elif self.bauart == "leicht" and self.klimazone == "b":
					S1 = 0.056
				elif self.bauart == "leicht" and self.klimazone == "c":
					S1 = 0.041
				elif self.bauart == "mittel" and self.klimazone == "a":
					S1 = 0.080
				elif self.bauart == "mittel" and self.klimazone == "b":
					S1 = 0.067
				elif self.bauart == "mittel" and self.klimazone == "c":
					S1 = 0.054
				elif self.bauart == "schwer" and self.klimazone == "a":
					S1 = 0.087
				elif self.bauart == "schwer" and self.klimazone == "b":
					S1 = 0.074
				elif self.bauart == "schwer" and self.klimazone == "c":
					S1 = 0.061
			elif self.nachtluftung == "erhoht":
				if self.bauart == "leicht" and self.klimazone == "a":
					S1 = 0.098
				elif self.bauart == "leicht" and self.klimazone == "b":
					S1 = 0.088
				elif self.bauart == "leicht" and self.klimazone == "c":
					S1 = 0.078
				elif self.bauart == "mittel" and self.klimazone == "a":
					S1 = 0.114
				elif self.bauart == "mittel" and self.klimazone == "b":
					S1 = 0.103
				elif self.bauart == "mittel" and self.klimazone == "c":
					S1 = 0.092
				elif self.bauart == "schwer" and self.klimazone == "a":
					S1 = 0.125
				elif self.bauart == "schwer" and self.klimazone == "b":
					S1 = 0.113
				elif self.bauart == "schwer" and self.klimazone == "c":
					S1 = 0.101
			elif self.nachtluftung == "hoch":
				if self.bauart == "leicht" and self.klimazone == "a":
					S1 = 0.128
				elif self.bauart == "leicht" and self.klimazone == "b":
					S1 = 0.117
				elif self.bauart == "leicht" and self.klimazone == "c":
					S1 = 0.105
				elif self.bauart == "mittel" and self.klimazone == "a":
					S1 = 0.160
				elif self.bauart == "mittel" and self.klimazone == "b":
					S1 = 0.152
				elif self.bauart == "mittel" and self.klimazone == "c":
					S1 = 0.143
				elif self.bauart == "schwer" and self.klimazone == "a":
					S1 = 0.181
				elif self.bauart == "schwer" and self.klimazone == "b":
					S1 = 0.171
				elif self.bauart == "schwer" and self.klimazone == "c":
					S1 = 0.160
		elif self.nutzung == "nichtwohnen":
			if self.nachtluftung == "ohne":
				if self.bauart == "leicht" and self.klimazone == "a":
					S1 = 0.013
				elif self.bauart == "leicht" and self.klimazone == "b":
					S1 = 0.007
				elif self.bauart == "leicht" and self.klimazone == "c":
					S1 = 0
				elif self.bauart == "mittel" and self.klimazone == "a":
					S1 = 0.020
				elif self.bauart == "mittel" and self.klimazone == "b":
					S1 = 0.013
				elif self.bauart == "mittel" and self.klimazone == "c":
					S1 = 0.006
				elif self.bauart == "schwer" and self.klimazone == "a":
					S1 = 0.025
				elif self.bauart == "schwer" and self.klimazone == "b":
					S1 = 0.018
				elif self.bauart == "schwer" and self.klimazone == "c":
					S1 = 0.011
			elif self.nachtluftung == "erhoht":
				if self.bauart == "leicht" and self.klimazone == "a":
					S1 = 0.071
				elif self.bauart == "leicht" and self.klimazone == "b":
					S1 = 0.060
				elif self.bauart == "leicht" and self.klimazone == "c":
					S1 = 0.048
				elif self.bauart == "mittel" and self.klimazone == "a":
					S1 = 0.089
				elif self.bauart == "mittel" and self.klimazone == "b":
					S1 = 0.081
				elif self.bauart == "mittel" and self.klimazone == "c":
					S1 = 0.072
				elif self.bauart == "schwer" and self.klimazone == "a":
					S1 = 0.101
				elif self.bauart == "schwer" and self.klimazone == "b":
					S1 = 0.092
				elif self.bauart == "schwer" and self.klimazone == "c":
					S1 = 0.083
			elif self.nachtluftung == "hoch":
				if self.bauart == "leicht" and self.klimazone == "a":
					S1 = 0.090
				elif self.bauart == "leicht" and self.klimazone == "b":
					S1 = 0.082
				elif self.bauart == "leicht" and self.klimazone == "c":
					S1 = 0.074
				elif self.bauart == "mittel" and self.klimazone == "a":
					S1 = 0.135
				elif self.bauart == "mittel" and self.klimazone == "b":
					S1 = 0.124
				elif self.bauart == "mittel" and self.klimazone == "c":
					S1 = 0.113
				elif self.bauart == "schwer" and self.klimazone == "a":
					S1 = 0.170
				elif self.bauart == "schwer" and self.klimazone == "b":
					S1 = 0.158
				elif self.bauart == "schwer" and self.klimazone == "c":
					S1 = 0.145				
		return S1

	def Sx2(self):
		if self.nutzung == "wohnen":
			S2 = 0.06 - (0.231 * (self.fges/self.raumflaeche))
		else:
			S2 = 0.03 - (0.115 * (self.fges/self.raumflaeche))
		return S2

	def Sx3(self):
		S3 = 0.03 * (self.fgtot04/self.fges)
		return S3
		
	def Sx4(self):
		S4 = -0.035 * (self.fneig/self.fges)
		return S4

	def Sx5(self):
		S5 = 0.1 * (self.fnord/self.fges)
		return S5

	def Sx6(self):
		if self.passivkuhlung == "ja" :
			if self.bauart == "leicht":
				S6 = 0.02
			elif self.bauart == "mittel":
				S6 = 0.04
			elif self.bauart == "schwer":
				S6= 0.06
		else:
			S6 = 0
		return S6




