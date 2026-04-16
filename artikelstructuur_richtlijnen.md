# Artikelstructuur Richtlijnen - Inholland TI-Ingenieurschap

Gebaseerd op: Onderzoeksartikelformat v.2223, Ingenieurschap Artikel Les 1-5 (Bastiaan Vergouw / A.M. Gieling)

---

## Verplichte structuur (Onderzoeksartikelformat TI-ingenieurs)

Het artikel volgt de APA-richtlijnen voor structuur en IEEE-richtlijnen voor verwijzingen.

### 1. INLEIDING

De inleiding bevat de volgende onderdelen (expliciet of organisch verwerkt):

| Onderdeel | Wat erin moet | Toepassing op ons verslag |
|---|---|---|
| **Onderwerp** | Context en thema. Functionele kant: voor wie is er een probleem, onder welke omstandigheden, wat zijn oorzaken en gevolgen? | DeVi Comfort maakt trapliften. Bij service/onderhoud is snel inzicht in positie en status essentieel. Fouten worden nu als tekst/codes getoond. |
| **Probleem** | Het **technische** (TI-)probleem isoleren uit het functionele probleem. Welke systemen hebben 'last'? Reduceer tot wat oplosbaar is voor TI. | Foutcodes en statusbits zijn niet direct ruimtelijk interpreteerbaar. Er ontbreekt een real-time 3D-mapping van telemetrydata naar een visuele representatie. |
| **Relevantie** | Wie heeft baat bij technische oplossing? Impact? | Snellere diagnose = minder downtime, lagere servicekosten. Engineers en monteurs kunnen direct zien waar de lift zich bevindt en wat afwijkt. |
| **Doel** | Welk aandeel van het technisch probleem los JIJ op? Hoofdvraag in een zin. Zoek naar een **ontwikkelopdracht**, niet configuratie. | Ontwikkelen van de wiskundige en softwarematige pipeline die live telemetry (encoder, spindle, swivel) omzet in een betrouwbare 3D ghost-visualisatie. |
| **Methode** | Kort vooruitkijken op aanpak (zonder details). Beschrijf **ontwikkel-/onderzoeksaanpak**, niet je oplossing. | Iteratief prototypen met formele analyse (wiskunde), ontwerp (architectuur), en experiment (calibratierun validatie). |
| **Overzicht** | Voorbespreking rode draad per sectie. Verwachtingsmanagement voor de lezer. | "Sectie 2 beschrijft de probleemstelling... Sectie 3 presenteert het theoretisch kader..." |

**BELANGRIJK uit de cursus:**
- Schrijf NIET in termen van oplossingen ("we gebruiken Godot en Kalman Filters")
- Beschrijf het PROBLEEM, niet het product
- Vermijd bedrijfs-/implementatiespecifieke termen in de probleemomschrijving

---

### 2. PROBLEEMSTELLING

De probleemstelling bestaat uit **drie delen**:

#### 2a. Probleemanalyse (= het probleembeschrijvende deel van het Theoretisch Kader)

- Verzamel bestaand wetenschappelijk werk dat helpt bij het **afkaderen** van het technisch probleem
- Schrijf in technische vaktermen voor een **peer** (mede-TI-er)
- Vermijd bedrijfsdocumentatie (die beschrijft oplossingen, niet problemen)
- Gebruik algemene, gangbare termen (niet "Godot" maar "game engine" of "real-time 3D omgeving")
- Vermijd schrijven in termen van oplossingen

**Voor ons verslag:** Beschrijf het generieke probleem van real-time visualisatie van mechatronisch systeem-telemetry. Benoem de uitdaging van noisy sensor data, encoder-naar-positie mapping bij niet-lineaire trajecten, en de noodzaak van filtering.

#### 2b. Vooronderzoek (= het oplossingsbeschrijvende deel van het Theoretisch Kader)

- Verzamel bestaand werk dat helpt bij het **oplossen** van het technisch probleem
- Bespreek **oplossingsrichtingen** uit wetenschappelijke bronnen
- Benoem voor- en nadelen per richting
- Motiveer welke richting je uitdiept
- Bespreek eerder gedaan onderzoek van collega's

**Voor ons verslag:**
- Kalman Filtering vs. simpele moving average vs. complementary filter → waarom Kalman?
- Catmull-Rom vs. B-splines vs. lineaire interpolatie → waarom Catmull-Rom tangent?
- Quaternions vs. Euler angles → waarom quaternions voor gimbal lock-vrije rotatie?
- TCP/BT protocol design → bestaande patronen uit embedded systems literatuur

#### 2c. Vraagstelling (deelvragen)

**Regels voor deelvragen:**
1. Elke deelvraag moet resulteren in een **onderzoeksproduct** (niet een beroepsproduct!)
   - Onderzoeksproduct = naslagwerk waaruit besluiten systematisch zijn vastgelegd
   - Voorbeelden: formele analyse/afleiding, verzameling metingen, formeel ontwerp, experiment-beschrijving
2. Elk onderzoeksproduct levert een aanwijsbare bijdrage aan beantwoording van de centrale vraag
3. Onderzoeksproducten hebben een logische plek in de reis naar de oplossing
4. Formuleer NIET in termen van oplossingen ("Hoe implementeer je een Kalman Filter?" is FOUT)
5. Deelvragen komen NIET uit de ijle lucht - gemotiveerd door TK

**Huidige deelvragen beoordeeld:**

| # | Huidige vraag | Beoordeling | Verbetering nodig? |
|---|---|---|---|
| Q1 | Welke storingen/waarschuwingen zijn het meest relevant om te visualiseren? | OK - leidt tot observatiestudie/interview | Formulering iets scherper |
| Q2 | Welke technische inputs zijn nodig voor een betrouwbare 3D-representatie? | OK - leidt tot requirements-analyse | Specificeer "betrouwbaar" meetbaar |
| Q3 | Hoe wordt de verwachte positie bepaald en verschil berekend? | OK - leidt tot formele analyse | Goed, dit is de wiskundekern |
| Q4 | Welke visualisatievormen maken afwijkingen het best begrijpelijk? | Meer functioneel dan technisch | Maak technischer: "welke rendering-technieken..." |
| Q5 | Hoe kan het prototype gevalideerd worden met praktijkscenario's? | OK - leidt tot experiment | Specificeer meetbare criteria |
| Q6 (nieuw) | Welke wiskundige modellen zijn nodig om live telemetry om te zetten naar een betrouwbare 3D-representatie? | STERK - kernvraag, leidt tot formele analyse | Toevoegen! |

**LET OP:** Q3 en Q6 overlappen. Voorstel: maak Q3 specifieker over encoder-mapping en verwachte-vs-gemeten positie, en Q6 over de wiskundige filtering en interpolatie.

---

### 3. METHODEN

Per deelvraag kies je een of meer onderzoeksmethoden. Het methode-hoofdstuk bevat **vier lagen**:

| Laag | Vraag | Voorbeeld voor ons |
|---|---|---|
| **Methode** | Welke methode zet je in? | Formele analyse, ontwerp, experiment |
| **Verantwoording** | Waarom is deze methode passend? (theoretisch) | "Omdat de telemetry-pipeline een deterministisch systeem is met meetbare in- en outputs, is formele analyse de passende methode..." |
| **Concrete aanpak** | Hoe en waarom precies zo? (reproduceerbaarheid) | "De Kalman Filter wordt geimplementeerd als 2D constant-velocity model. Telemetry wordt gepolled via Bluetooth op 20Hz..." |
| **Instrumentdefinitie** | Maak aanpak meetbaar en controleerbaar. Wanneer klaar? | "Succes wordt gemeten aan: positie-afwijking <5mm, latentie <100ms, geen visuele sprongen bij 60fps" |

**Primaire methoden voor TI-ingenieurs:**

| Methode | Wanneer | Onderzoeksproduct | Toepassing in ons verslag |
|---|---|---|---|
| **Steekproef / observatiestudie** | Data verzamelen uit bestaand systeem, huidige situatie in kaart brengen | Meetrapport | Q1: welke fouten komen voor, hoe vaak, hoe lang duurt diagnose nu? |
| **Formele analyse** | Wiskundige/logische analyse, ALTIJD formeel op te schrijven | Berekening, afleiding, bewijs | Q3/Q6: Kalman Filter afleiden, encoder mapping, quaternion transforms |
| **Ontwerp** | Procedureel of architectureel ontwerp | PSD, architectuurdiagram, blokdiagram | Q2: data-pipeline architectuur, IPC protocol ontwerp |
| **Experiment** | Hypothese-gedreven meting | Meetresultaten, grafieken | Q5: calibratierun met meetbare criteria |

**BELANGRIJK:**
- Formele analyse is **altijd formeel op te schrijven**: wiskundige notatie, afleidingen, bewijzen
- Kan in (semi-)formele taal: wiskundige notatie, 2D xy-vlak, blokdiagram, modelleertaal
- Requirements-analyse is GEEN technisch onderzoek (dat is functioneel)
- Gebruik het artikel NIET als podium om je applicatie te showcasen

---

### 4. RESULTATEN

Per gebruikte methode het juiste type resultaat:

| Methode | Type resultaat | Presentatievorm |
|---|---|---|
| Literatuurstudie | Samenvatting, uitleg, procedurebeschrijving, rekenvoorbeeld | Tekst met vergelijkingen en verwijzingen |
| Interview/survey | Lijst met antwoorden, tabel met scores | Tabellen, grafieken |
| Steekproef/observatiestudie | Ingevuld meetrapport | Tabel in vast format (leeg instrument in bijlage) |
| Formele analyse | Wiskundige afleiding, diagram, bewijs | Vergelijkingen, blokdiagrammen, grafieken |
| Ontwerp | PSD, architectuurdiagram | Structuurdiagrammen (in LaTeX, bv. struktex) |
| Experiment | Meetresultaten | Grafieken, tabellen met meetwaarden |

**Regels:**
- Bevat **analyse** die leidt tot beantwoording van de onderzoeksvraag
- Presenteer **objectief** (geen mening, geen evaluatie - dat is voor de conclusie)
- Elke figuur/tabel/vergelijking MOET verwezen worden in de tekst
- Vraag jezelf af: *waarom moet mijn lezer dit weten?*

**Voor ons verslag - concrete resultaten per deelvraag:**

| Deelvraag | Resultaat dat we kunnen presenteren |
|---|---|
| Q1 | Overzicht van fouttypen uit telemetry poller (traction, spindle, swivel, chair status) |
| Q2 | Blokdiagram van de complete data-pipeline (BT → parser → poller → KF → ghost) |
| Q3 | Formele afleiding encoder-mapping (piecewise interpolatie), verwachte vs gemeten positie |
| Q4 | Vergelijking rendering-technieken (ghost shader, cel-shading, dither clip) met screenshots |
| Q5 | Meetresultaten calibratierun: positie-nauwkeurigheid, latentie, hoek-correcties |
| Q6 | Volledige wiskundige afleiding: Kalman Filter, Catmull-Rom, quaternions, arc-tracing |

---

### 5. CONCLUSIE

**Functie:** Interpreteren van resultaten, NIET samenvatten!

**Onderdelen:**
1. **Vat resultaten kort samen** (afwegingen, niet feiten herhalen)
2. **Bespreek gevolgen** in het licht van theoretisch kader
3. **Mogelijke observaties** buiten de scope van het instrument
4. **Korte analyse** van de resultaten
5. **Verantwoording oplossingsrichting** (besluit)
6. **Reflecteer op verwachtingen/hypotheses** uit de probleemstelling
7. **Geef antwoord op deelvragen EN hoofdvraag**

**Conclusietypen:**
- **Deductief:** Logische gevolgtrekking (als A dan B, niet-B, dus niet-A). Waar als premissen waar zijn.
- **Inductief:** Generaliserende gevolgtrekking. Voorspellend, met mate van waarschijnlijkheid. Let op: klein aantal waarnemingen = zwakke conclusie.

**NIET doen:**
- Samenvatting van methoden en resultaten (dat is geen conclusie!)
- Nieuwe informatie introduceren
- Meningen zonder onderbouwing

---

### 6. AANBEVELINGEN

- Voortbordurend op conclusie
- Concrete suggesties voor vervolg
- Gebaseerd op bevindingen, niet op wensen

---

## Vergelijking: huidig verslag vs. vereist format

| Sectie | Huidig verslag | Wat moet veranderen |
|---|---|---|
| **Inleiding** | Bevat context, motivatie, doel, leeswijzer | Mist: expliciet technisch probleem isoleren, relevantie concreter, methode-vooruitblik, NIET in termen van oplossing schrijven |
| **Probleemstelling** | Heeft hoofdvraag + 5 deelvragen | Mist: probleemanalyse (TK deel 1), vooronderzoek (TK deel 2). Deelvragen moeten gemotiveerd zijn door TK. Q6 toevoegen. |
| **Theoretisch Kader** | Zeer dun (3 korte alinea's) | Moet VEEL uitgebreider: split in probleemanalyse + vooronderzoek. Literatuur over Kalman filtering, spline interpolatie, real-time 3D visualisatie, embedded telemetry. |
| **Methode** | Generiek ("iteratief met prototyping") | Moet per deelvraag: welke methode, verantwoording, concrete aanpak, instrumentdefinitie |
| **Resultaten** | Leeg ("to be completed") | Invullen met formele analyses, meetrapporten, ontwerpen, experimentresultaten |
| **Conclusie** | Leeg | Schrijven: antwoord op elke deelvraag + hoofdvraag, deductief/inductief |

---

## Kritieke aandachtspunten uit de cursus

1. **Schrijf NIET in termen van oplossingen** - beschrijf het probleem
2. **Formele analyse = formeel opschrijven** - wiskundige notatie verplicht
3. **Elke deelvraag → onderzoeksproduct** (niet beroepsproduct)
4. **Geen websites als bronnen** - gebruik wetenschappelijke artikelen/boeken
5. **Figuren/tabellen alleen als ernaar verwezen wordt in tekst**
6. **LaTeX verplicht** (al ingesteld)
7. **IEEE-verwijzingen** (nummerverwijzingen [1], [2], etc.)
8. **Vermijd bedrijfsdocumentatie** in probleemanalyse
9. **Requirements-analyse hoort NIET in technisch onderzoek**
10. **Gebruik het artikel niet als showcase voor je applicatie**

---

## Voorgestelde herstructurering van het verslag

```
1. INLEIDING
   1.1 Context (DeVi Comfort, trapliften, service-uitdaging)
   1.2 Technisch Probleem (real-time sensor→3D mapping)
   1.3 Relevantie (diagnose-efficiëntie)
   1.4 Onderzoeksdoel + Hoofdvraag
   1.5 Aanpak (kort)
   1.6 Overzicht

2. PROBLEEMSTELLING
   2.1 Probleemanalyse (Theoretisch Kader - probleemkant)
       - Real-time visualisatie van mechatronische systemen
       - Uitdagingen bij sensor-naar-positie mapping
       - Ruis in telemetrydata en noodzaak van filtering
   2.2 Vooronderzoek (Theoretisch Kader - oplossingskant)
       - State estimation: Kalman Filter vs alternatieven
       - Spline interpolatie voor smooth trajecten
       - Quaternion rotatie vs Euler angles
       - IPC protocol design patterns
   2.3 Vraagstelling
       - Hoofdvraag
       - Deelvragen Q1-Q6 (gemotiveerd door 2.1 en 2.2)

3. METHODEN
   3.1 Q1: Observatiestudie (foutanalyse bestaand systeem)
   3.2 Q2: Ontwerp (data-pipeline architectuur)
   3.3 Q3: Formele analyse (encoder mapping, positievergelijking)
   3.4 Q4: Ontwerp + Experiment (visualisatietechnieken)
   3.5 Q5: Experiment (calibratierun validatie)
   3.6 Q6: Formele analyse (Kalman Filter, splines, quaternions)

4. RESULTATEN
   4.1 Foutanalyse resultaten (Q1)
   4.2 Data-pipeline architectuur (Q2)
   4.3 Encoder-positie mapping afleiding (Q3)
   4.4 Visualisatietechnieken vergelijking (Q4)
   4.5 Calibratierun meetresultaten (Q5)
   4.6 Wiskundige modellen telemetry pipeline (Q6)

5. CONCLUSIE
   5.1 Antwoord op deelvragen
   5.2 Antwoord op hoofdvraag
   5.3 Reflectie en aanbevelingen

BIBLIOGRAFIE
BIJLAGEN (instrumenten, meetrapporten, code-fragmenten)
```
