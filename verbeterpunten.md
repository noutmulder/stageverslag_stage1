# Verbeterpunten verslag

Huidig cijfer: **7.5/10**

---

## Tier 1: Naar een 8.5 (direct doen-baar)

### 1. Placeholder afbeeldingen vervangen
- [ ] `rail_segment_types.png` - Screenshot of diagram van de drie railsegment-types (recht, verticale bocht, horizontale bocht) met hun arc-tracing geometrie
- [ ] `calibration_run.png` - Screenshot van een calibratierun in actie, bij voorkeur op een horizontale bocht

### 2. Vooronderzoek uitdiepen
Elke oplossingsrichting-vergelijking is nu ~5 regels. Moet ~15 worden met:
- [ ] State estimation: noem een concreet paper waar moving average wel werkt (bijv. langzame systemen), en leg uit waarom het hier niet werkt (20Hz async, moet extrapoleren)
- [ ] Spline interpolatie: noem een toepassing waar B-splines beter zijn (bijv. CAD/NURBS), en waarom Catmull-Rom hier beter past (moet door de punten heen)
- [ ] Rotatie: noem een geval waar Euler angles voldoen (bijv. 1-as rotatie), en waarom quaternions hier nodig zijn (4 assen tegelijk, gimbal lock risico)

### 3. Methode-instrumenten aanscherpen met concrete thresholds
- [ ] Q1 (Fault Relevance): "Classificatie is compleet wanneer elke message met een positie-gerelateerd veld is geidentificeerd en beoordeeld op spatiale relevantie"
- [ ] Q4 (Mathematical Models): "Model is correct wanneer voorspelde positie op 5 bekende referentiepunten <5mm afwijkt van werkelijke positie"
- [ ] Q5 (Rendering): Voeg een vergelijkingstabel toe met kolommen: techniek, doel, voordeel, nadeel, geschiktheid voor foutdiagnose
- [ ] Q6 (Validation): "Experiment slaagt als framerate >55fps, positie-error <5mm op alle referentiepunten, en hoek-correctie <1 graad afwijking"

### 4. Validatietabel eerlijker maken
- [ ] Voeg een kolom "Opmerkingen" toe met wat er misging per run (BT disconnecties, onverwachte waarden, handmatige interventies)
- [ ] Noteer waar resultaten afweken van verwachting en waarom
- [ ] Voeg standaarddeviatie toe waar van toepassing (bijv. latentie: 38 +/- 12ms)

---

## Tier 2: Naar een 9+ (meer onderzoekswerk nodig)

### 5. Formele sensitivity analysis Kalman parameters
- [ ] Varieer sigma_a van 0.01 tot 0.1, meet positie-error per waarde
- [ ] Varieer sigma_m van 0.0001 tot 0.001, meet jitter per waarde
- [ ] Varieer spindle blend ratio van 70/30 tot 95/5, meet oscillatie
- [ ] Plot de resultaten als grafiek in het verslag
- [ ] Bepaal het "veilige bereik" per parameter

### 6. Gecontroleerd user experiment
- [ ] Ontwerp 5 foutscenario's (positie-afwijking, stoel scheef, vastzittend in bocht, swivel fout, encoder offset)
- [ ] Laat 3-5 collega's dezelfde scenario's diagnosticeren: groep A met tekstuele codes, groep B met 3D visualisatie
- [ ] Meet per scenario: diagnosetijd (seconden) en correctheid (juist/onjuist)
- [ ] Presenteer resultaten in tabel + staafdiagram
- [ ] Dit converteert de inductieve conclusie naar meetbaar bewijs

### 7. Meer calibratieruns
- [ ] Minimaal 8-10 runs op verschillende railconfiguraties
- [ ] Statistische analyse: gemiddelde, standaarddeviatie, 95% betrouwbaarheidsinterval per metric
- [ ] Test specifiek op edge cases: zeer lange rail (>8m), veel bochten (>10), alleen horizontaal, alleen verticaal

---

## Tier 3: Naar een 10 (theoretisch, vereist afgerond onderzoek)

### 8. Alle bovenstaande punten afgerond

### 9. Hogere-orde arc-tracing
- [ ] Vervang de trapezoide midpoint-benadering door Simpson's rule
- [ ] Meet verschil in cumulatieve fout op lange rails
- [ ] Presenteer vergelijking oud vs nieuw in tabel

### 10. Automatische Kalman tuning
- [ ] Ontwerp een auto-tuning algoritme dat sigma_a en sigma_m aanpast op basis van railconfiguratie
- [ ] Valideer op 3+ rails dat auto-tuning vergelijkbare of betere resultaten geeft dan handmatige tuning

### 11. Volledige reproduceerbaarheid
- [ ] Alle testdata (encoder logs, compass data, referentiepunten) als bijlage bij het verslag
- [ ] Stap-voor-stap instructies om het experiment te herhalen
- [ ] Code-referenties naar specifieke commits in de git repository
