# Energieeffizienz für Gebäude

*** This project is in german, because the laws on energy efficiency this is referring to only apply to Germany ***

## Monatsbilanz zum Heizwärmebedarf nach 4108

### Zweck
Diese in Python programmierte Berechnung des Transmissionswärmeverlusts und des Heizwärmebedarfs soll es ermöglichen, Energieeffizienzberatung für Machine Learning und Data Science Anwendungen verfügbar zu machen. 

Der Transmissionswärmebedarf kann berechnet werden. Mit der derzeitigen Version ist es zwar auch schon möglich, den Heizwärmebedarf zu bestimmen. Der ist aber noch nicht ganz korrekt, weil die Nachtabschaltung noch nicht enthalten ist. Der berechnete Wert wird also höher sein, als der tatsächliche nach 4108. Heiztage können auch noch nicht berechnet werden. 

### Benutzung
Wenn alle Klassen der Monatsbilanzierung importiert sind, können damit R-Werte und U-Werte berechnet werden, Hüllflächenelemente erzeugt werden und eine Monatsbilanzierung nach DIN 4108-2 berechnet werden. Für die oben genannten Anwendungen gibt es jeweils eine eigene Klasse.

### Beispielhafte Anwendung und Analyse
Dadurch, dass Fenster deutlich niedrigere U-Werte haben aber gleichzeitig solare Wärmegewinne zulassen, kann hiermit berechnet werden, welche Fensterfläche je nach Ausrichtung am besten für die Energieeffizienz eines Gebäudes ist. Hierfür wurden die Standard-U-Werte des EnEV/GEG Referenzgebäudes verwendet.

![gesamt](https://user-images.githubusercontent.com/72806562/109390911-adf8c280-7914-11eb-9ab2-10f9ae8b1693.png)

Für Süden ist die Antwort klar: umso mehr Fensterfläche, desto besser.
Für Ost- und West hält es sich die Waage.
Im Norden ist es aus Energieeffizienz-Aspekten tendenziell sinnvoller, die Fensterfläche zu reduzieren.


## Wärmeerzeuger wählen

### Zweck
Mit diesem Modul soll es möglich sein, Entscheidungshilfen zur Wahl des Wärmeerzeugers für Gebäude zu erstellen. Dazu werden quantitative Aspekte betrachtet. Qualitative und subjektive Aspekte wie die Lärmemission einer Luft-Wasser-Wärmepumpe können natürlich nicht berücksichtigt werden.

### Benutzung


## Sommerlicher Wärmeschutz nach DIN 4108-2

### Zweck
Die Berechnung zum sommerlichen Wärmeschutz im vereinfachten Verfahren nach DIN 4108-2 ist nicht allzu kompliziert. Die Softwareumsetzung der gängigen 


### Benutzung

