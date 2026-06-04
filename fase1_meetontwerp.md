# Fase 1 — Meetontwerp validatiecampagne (pre-registratie)

**Status:** pre-registratie. Dit document legt de meetopzet en pass/fail-criteria vast
**vóór** de campagne wordt uitgevoerd. De commit-datum van dit bestand in git geldt als
het pre-registratiemoment. Wijk je tijdens de runs af, noteer dat dan expliciet (afwijking +
reden) — niet stilzwijgend de criteria bijstellen.

**Waarom dit document:** de review zag dat in de vorige ronde geen van de drie empirische
criteria zijn vooraf-vastgelegde, kwantitatieve vorm onveranderd haalde (DV1/DV3 werden
post-hoc observationeel; DV2 verschoof van display-vs-fysiek naar display-vs-firmware). Dit
ontwerp herstelt dat: kwantitatief, vooraf, op meerdere rails.

**Verhouding tot het verslag:** `main.tex` wordt **niet** in Fase 1 aangepast. De
method-secties (DV-criteria, validatie-aanpak) én de Results/Conclusie worden in **Fase 3**
samen herschreven met de nieuwe data, zodat het verslag op elk moment intern consistent blijft.

---

## 1. Pre-registered criteria (DV1–DV3, v2)

Drempels zijn **engineering-targets afgeleid van de eis**, niet van eerder gemeten waarden.
Getallen met ⚠️ wil ik door jou laten sanity-checken voordat je gaat meten.

### DV1(b) — Live-gedrag / latency (kwantitatief)
- **DV1(b)-link:** Bluetooth round-trip per request/response-paar, gerapporteerd als
  **mean, P95, P99, max** per rail. Pass: **P95 < 150 ms ⚠️ en P99 < 250 ms ⚠️** per run.
  Onderbouwing: de dead-reckoning velocity-decay zet pas in na 0.8 s (`VELOCITY_DECAY_AFTER`);
  P99 < 250 ms houdt elke gap ruim onder die horizon, dus de extrapolatie blijft binnen het
  bereik waarvoor ze is ontworpen.
- **DV1(b)-lag (eind-gebruikerseigenschap):** als high-speed video beschikbaar is (zie §4),
  de **offset tussen fysieke en getoonde chairpositie tijdens steady-state rijden** < **1 frame
  aan beweging bij pilotsnelheid ⚠️** (kwantitatief, uit videoframes). Geen video → terugval
  op observatie O3, expliciet gelabeld als kwalitatief.

### DV2(b) — Positie-accuratesse (kwantitatief, primair = display-vs-fysiek)
- **Primair:** **display-vs-fysieke** positie (steel tape ±1 mm) op elke referentiemarker,
  **beide rijrichtingen, alle rails**. Pass: **< 5 mm op rails ≤ 5 m; < 10 mm op langere rails**.
  Dit is inclusief de configurator-bijdrage, dus de "echte" fout die een monteur zou zien.
- **Secundair (pipeline-isolatie):** **display-vs-firmware-encoded** positie (zoals nu), naast
  het primaire getal. Het verschil tussen beide = de configurator-bijdrage, expliciet
  gerapporteerd i.p.v. weggemoffeld.
- Rapporteer per rail én **per segmenttype** (straight / vertical up / vertical down /
  horizontal): mean, SD, max, 95%-CI; en per rijrichting.

### DV3(b) — Smoothness (kwantitatief, frame-level, **snelheids-gebaseerd**)
> Gecorrigeerd na de eerste frame-log: de framerate is variabel (~52 fps, interval 21–32 ms), dus
> de rauwe per-frame-stap `|Δp|` schaalt mee met dt én met echte snelheidswisselingen (bocht 20% vs
> recht 50%) — daardoor is een p99/mediaan-stap-ratio misleidend. Gebruik **snelheid**, die is
> frame-rate-onafhankelijk.
- Reken per frame `v[i] = (p[i+1] − p[i]) / Δt[i]` (uit `[FRAME]`-timestamps).
- **Geen staircase:** tijdens continue beweging **0 snelheidspieken > 5× de mediane |v| ⚠️**
  (een last-value-hold zou ~1 piek per ~10 frames geven). Equivalent: het overgrote deel van de
  frames beweegt (geen bevroren-dan-springen-patroon).
- **Begrensde jerk:** rapporteer mediaan + p99 van `|v[i+1] − v[i]|`.
- **Render-gezondheid apart:** rapporteer de Δt-verdeling (effectieve fps) — lage/variabele fps is
  een prestatiekwestie, geen smoothness-kwestie.
- Stationaire baseline (≥ 13 s): bevestig **0 puls-variatie** op de ruwe encoder (zoals vorige run),
  zodat duidelijk blijft dat DV3 over *gap-filling*-smoothness gaat, niet over ruisonderdrukking.

> De oude DV3-formulering "Kalman-jitter ≥ 10× kleiner dan raw" vervalt definitief: op een
> digitale puls-encoder is raw-jitter nul, dus die ratio is ondefinieerbaar. De frame-level
> stap-criteria meten wat DV3 werkelijk moet borgen.

---

## 2. Logging-checklist (per run, automatisch via TestLogger)

Vink af dat élke run dit vastlegt (ms-timestamps). Items met 🆕 vereisen mogelijk een kleine
code-toevoeging aan TestLogger — **check dit vóór de campagne**, anders mis je de data weer.

- [ ] Ruwe encoder per as (traction / spindle / swivel)
- [ ] Gefilterde (Kalman) positie + **velocity** per as
- [ ] 🆕 **Getoonde (display) positie per render-frame + frame-timestamp** (nodig voor DV3 + DV1-lag)
- [ ] Bluetooth round-trip per request/response-paar
- [ ] **Inter-sample gap** per as (afgeleid uit arrival-timestamps) 🆕 of achteraf berekenbaar uit (1)
- [ ] Hoek-correctie per horizontale bocht (`δ`, `ψ_measured`, `θ_bend`)
- [ ] Frame-interval / fps
- [ ] Event-markers: marker-passage, start/stop, eventuele disconnects/checksum-errors

Inter-sample gap + velocity-profiel zijn óók nodig voor Fase 3.3 (filter-tuning onderbouwen).

---

## 3. Rail-set — kies op dekking, niet op aantal

Doel: elk segmenttype op **≥ 2 verschillende rails**, variërend in lengte en bochtaantal.
Richtgetal **3–5 rails**. Vul vóór de campagne in welke trapliften beschikbaar zijn:

| Rail-ID | Lengte (mm) | #straight | #vert. up | #vert. down | #horiz. | Notities |
|---|---|---|---|---|---|---|
| (vorige run) | 3403 | — | — | — | 1 (90° L) | al gemeten, 1 bocht |
| ? | | | | | | |
| ? | | | | | | |
| ? | | | | | | |

Dekkings-check vóór je gaat: heeft de set ≥ 2 rails met een **vertical up**, ≥ 2 met
**vertical down**, ≥ 2 met **horizontal**, en variatie in **lengte** (kort < 2 m én lang > 5 m
indien beschikbaar — de 10 mm-drempel geldt juist voor lange rails)?

---

## 4. Meetprocedure per traplift (identiek protocol)

1. **Markers plaatsen** vóór de run: meerdere referentiemarkers verspreid over **alle**
   segmenttypes (niet alleen op straights), offset met steel tape (±1 mm) genoteerd.
2. **Stationaire baseline** ≥ 13 s (encoder-baseline + 0-jitter-check).
3. **B→T** volledige rit, daarna **T→B** volledige rit. Logging continu aan.
4. **Bij elke marker, beide richtingen:** noteer **fysieke** positie (tape), **getoonde** positie,
   en **firmware-encoded** positie. → primaire en secundaire DV2-fout.
5. **Per rail noteren:** configuratie (tabel §3), bijzonderheden, afwijkingen van dit protocol.

### Aanbevolen extra's (verhogen de bewijskracht — beslis per beschikbaarheid)
- [ ] **1.5 Externe hoekreferentie** (digitale gradenboog / laser-hoekmeter) bij horizontale
  bochten → maakt de compass-correctie niet langer self-referentieel (nu een Limitation).
- [ ] **1.6 High-speed video** fysiek-vs-display tijdens rijden → kwantitatieve DV1-lag.
- [ ] **1.7 Tweede waarnemer** scoort onafhankelijk de pass/fail + observaties O1–O3 →
  ontkracht de self-validation-Limitation.

---

## 5. Wat dit in Fase 3 oplevert (vooruitblik, niet nu uitvoeren)

- Aggregatie over rails: DV2-fout per rail / per segmenttype / per richting (mean/SD/CI).
- Grafieken: **positie-vs-tijd** (DV3-smoothness), **RTT-histogram** (DV1), **fout-per-rail/segmenttype**,
  **inter-sample-gap-verdeling** + **velocity-profiel** (voor tuning-onderbouwing).
- Method-secties van `main.tex` herschreven naar deze pre-registered criteria; Results/Conclusie
  met de nieuwe multi-rail data; generaliseerbaarheid-Limitation versmald.

---

## 6. Beslispunten vóór je de lift in gaat

**Gekozen meetmethoden (vast):** tractie = markers (T-TRAC), spindel = digitale waterpas (T-SPIN),
swivel = kompas + tablet op de zitting, draaien met de fysieke knoppen (T-SWIV). Nog te bevestigen:

1. Bevestig/pas de ⚠️-drempels aan: DV1 P95/P99 + DV1-lag, DV3 (snelheidspieken > 5× mediaan = 0;
   géén stap-ratio meer), en de **hoek-drempels** (spindel ~1–2°, swivel **~±3,5°** = encoder↔fysiek-tolerantie).
2. Welke trapliften zijn beschikbaar? Vul §3 in en check de dekking.
3. Welke aanbevolen extra's (1.5/1.6/1.7) zijn haalbaar qua tijd/instrumenten?
4. Check of TestLogger de 🆕-items al logt — incl. `θ_spindle` én `θ_swivel` op het capture-moment;
   zo niet, klein loggingscript toevoegen vóór de campagne.

---

## 7. Meetinstructies — hoe je elk ding precies meet

Drie categorieën: **software-only** (alleen loggen + achteraf rekenen), **fysiek + app-capture**
(de positie-meting), en **extra instrumenten**.

> **Belangrijkste voorbereiding (anders mislukt DV2 weer):** de app moet
> (a) de **getoonde positie** numeriek kunnen loggen (als afstand-langs-rail in mm, of als
> genormaliseerde `t∈[0,1]` die je ×`d_total` naar mm omrekent), en (b) op een **"marker
> capture"-knop** één logregel wegschrijven met `{timestamp, display_pos, raw_encoder,
> firmware_pos}`. Zonder die knop kun je display- en fysieke positie niet op hetzelfde moment
> aan elkaar koppelen. Dit is het ene code-dingetje dat vóór de campagne af moet.

### A. DV2 accuratesse — drie assen (tractie, spindel, swivel)
De lift heeft drie aangestuurde assen. Door van alle drie de **getoonde waarde** tegen een
**onafhankelijke fysieke referentie** te leggen, valideer je niet alleen de positie maar de hele
oriëntatie-pijplijn (encoder-mapping, spindle-lookup, swivel-formule, quaternion-compositie).
Twee dingen scherp houden per as:
- meet **accuratesse statisch** (klopt de waarde bij een vaste, ingesteld-en-uitgesettelde stand?);
- houd **latency** (hoe snel volgt het scherm?) daarvan **gescheiden** — dat is een DV1/DV3-vraag, niet DV2.

Sinds de code-update interpoleren **spindel en swivel** ook mee met dead-reckoning; lees de statische
accuratesse daarom pas **na uitsettelen** af.

#### A1 / T-TRAC — Tractie (positie langs de rail): markers + app-capture
1. **Eén vast carriage-referentiepunt** kiezen (bv. voorkant voetplaat) + een dunne **pointer/naaldwijzer**.
   Gebruik exact dit punt voor álle markers en **beide rijrichtingen** (anders krijg je weer de
   B→T/T→B-asymmetrie).
2. **Markers plaatsen en inmeten:** meet per marker de **cumulatieve afstand-langs-rail** vanaf
   een vast nulpunt (onderstation) met steel tape. Op straights recht meten; door bochten een
   **flexibel lint langs het railoppervlak** leggen, of markers op **bocht-entry/exit** zetten en
   de afstand uit de geometrie halen + met het lint controleren. Dit getal = `d_phys`.
3. **Uitlijnen + capturen:** rijd in **jog/lage snelheid**, stop wanneer de pointer exact op de
   marker staat, druk **"capture"**. De app logt `display_pos` + `raw_encoder` op dat moment.
4. Herhaal elke marker, **B→T én T→B**.
5. **Foutberekening:** `display − d_phys` (= primaire DV2, incl. configurator),
   `display − firmware` (= secundaire pipeline-fout), `firmware − d_phys` (= configurator-bijdrage).
   - **Valkuilen:** lees de pointer **recht van boven** (parallax); stop zonder nadraai (jog, niet vol
     tempo); houd de pointer-offset constant; noteer de markerpositie per **segmenttype**.

#### A2 / T-SPIN — Spindel (zithoek): digitale waterpas, statisch op meerdere standen
- *Referentie:* een **digitale inclinometer/waterpas** op een vlak, meedraaiend referentievlak van de
  zitting; die meet de echte kanteling t.o.v. de zwaartekracht — onafhankelijk van de spindle-encoder.
- *Doe het op een **vlak railstuk*** (rail-pitch ≈ 0), zodat de railhelling de meting niet vervuilt.
- ⚠️ *Valideer de mapping, niet de render:* vergelijk de waterpas met de **gelogde `θ_spindle`** (de
  uitkomst van de 751-punts lookup), **niet** met de gerenderde ghost-kanteling. De render mengt er via
  de 85/15-blend de railgeometrie doorheen; die blend is bewust en mag niet als "fout" worden geteld.
  Je test hier of de **lookup-tabel** zelf klopt.
- *Procedure:* zet de spindel op een reeks standen over het bereik (bv. **0°, 15°, 30°, 45°, 60°, 75°**),
  laat uitsettelen, en leg per stand de **waterpas-waarde naast de getoonde `θ_spindle`** vast met een
  **foto** (beide in één beeld). Meet elke stand **oplopend én aflopend** (check op speling/hysterese).
  Fout = |waterpas − `θ_spindle`| per stand → een accuratesse-**curve**, niet één punt.
- *Pass:* |waterpas − `θ_spindle`| < [drempel ⚠️, bv. 1–2°] op elke stand.
- *Latency (optioneel, los van accuratesse):* jouw video-idee past hier precies — film waterpas + tablet,
  markeer **test-start op de tablet**, en lees uit de frames hoe lang het scherm achterloopt op een
  commando. Dat beantwoordt "hoe snel volgt het", niet "klopt de hoek".

#### A3 / T-SWIV — Swivel (zitdraaiing): **kompas + tablet op de zitting** (gekozen methode)
- *Referentie (gekozen):* de **kompas/gyro van de tablet**, plat op de zitting gelegd; je draait de
  swivel met de **fysieke knoppen op de traplift** en recordt de beweging. Vergelijk de gemeten rotatie
  met de **gelogde `θ_swivel`** (uit MSG 168).
- *Procedure:* tablet plat op de zitting, kompas/gyro **nullen** vlak vóór de meting → draai met de
  knoppen naar een bekende eindstand → laat **uitsettelen** → lees de gyro-rotatie naast `θ_swivel`.
  Doe **meerdere standen, beide draairichtingen**.
- ⚠️ *Eerlijk benoemen:* de gyro is een *andere* sensor dan de swivel-encoder (dus geen pure
  zelf-controle), maar consumentenkwaliteit en **drift** bij integratie → **nul vlak vóór elke meting**
  en **meet kort**. Daarom een ruimere drempel dan bij de spindel.
- ⚠️ *Vooraf weten (encoder↔fysiek-tolerantie):* de swivel-encoder komt sowieso niet exact overeen
  met de fysieke hoek — bij ~60° software draait hij in de praktijk ~58,5° (of bv. 61°), een inherente
  **±3,5°** marge. Dit is een **hardware-eigenschap** (encoder, niet de pipeline) en wordt als
  context/limitation gerapporteerd, niet als pipeline-fout. De pipeline geeft de encoderwaarde getrouw
  weer; de test toetst dat er **geen gróve afwijking** is, niet sub-graad-precisie.
- *Pass:* |gyro-rotatie − `θ_swivel`| binnen de encoder-tolerantie (**~±3,5°**); een gróve mismatch
  (bv. 50° tonen bij 60° fysiek, > 5°) = echte fout.
- *Optioneel sterker:* een **fysieke gradenboog-template** op de vaste voet + wijzer op de zitting geeft
  een driftvrije, écht onafhankelijke controle naast de gyro — als de tijd het toelaat haalt dat de
  "angle-correction is self-referentieel"-Limitation deels weg.

**Loggen voor A1–A3:** zorg dat de app per as de getoonde waarde logt op het capture-moment —
`display_pos` (tractie), `θ_spindle` (spindel), `θ_swivel` (swivel) — plus `raw_encoder` en
`firmware`-waarde, zodat je ook hier pipeline-fout en mapping-fout kunt scheiden.

### B. DV1 round-trip latency — software-only
- De app meet al RTT per request/response-paar (vorige run: 5295 paren). Zorg dat **elk paar**
  `send_ts` en `response_ts` logt → `RTT = response_ts − send_ts`.
- Achteraf: bereken **mean / P95 / P99 / max** uit de RTT-array (script). Geen fysiek instrument nodig.

### C. DV3 smoothness — software-only (**snelheids-gebaseerd**)
- Log de **getoonde positie per render-frame** + frame-timestamp tijdens rijden (knop **F**).
- Achteraf, frame-rate-onafhankelijk: snelheid `v[i] = (p[i+1] − p[i]) / Δt[i]`.
  - Staircase-test: **0 pieken > 5× mediane |v|** tijdens continue beweging.
  - Jerk: mediaan + p99 van `|v[i+1] − v[i]|`.
  - Render-gezondheid apart: Δt-verdeling (effectieve fps).
- ⚠️ Gebruik **niet** de rauwe per-frame-stap `|Δp|`: die schaalt mee met de variabele framerate én
  met echte snelheidswisselingen (bocht 20% vs recht 50%), dus de p99/mediaan-ratio is misleidend.
  (Op de eerste frame-log gaf `|Δp|` 2,56 = "fail" terwijl de snelheidsanalyse 0 pieken/geen staircase
  gaf — de motion was wél vloeiend.)

### D. Inter-sample gap + velocity-profiel — software-only (voor tuning, Fase 3.3)
- **Gap:** uit de **arrival-timestamps** van de encoder-samples per as: `gap[i] = t[i] − t[i−1]`.
- **Velocity:** de Kalman-`v` (al gelogd) of `Δpos/Δt`. Plot de verdeling van beide.

### E. 1.5 Externe hoekreferentie — extra instrument
- **Digitale hoekmeter/inclinometer met magneetvoet** op een vlak, meedraaiend vlak van de carriage:
  lees de hoek **vóór** en **ná** een horizontale bocht; het verschil = de **werkelijke** yaw-verandering.
- Vergelijk met de gyro-`ψ_measured` (gelogd) en de firmware-`θ_bend`. Alternatief: een **laser**
  vanaf de carriage op een **gradenboog-template** op de vloer/wand, lees de geveegde hoek af.

### F. 1.6 High-speed video — extra instrument (kwantitatieve lag)
- Eén camera die **zowel de fysieke chair (met markeredge) als het tabletscherm** in beeld heeft,
  op **120 of 240 fps** (slow-mo van een moderne telefoon volstaat).
- **Methode (tijd):** zoek het frame waarop de **fysieke** chair een marker passeert (`t_phys`) en
  het frame waarop de **ghost** dezelfde marker passeert (`t_display`); `lag = t_display − t_phys`
  (in ms = Δframes ÷ fps). Eventueel ×chairsnelheid → mm.
- **Methode (ruimte):** in één frame de offset tussen fysieke en getoonde chair meten, geschaald via
  de marker die in beide zichtbaar is.
- **Sync** (bij twee camera's): gebruik een **LED-flits of handklap** als gezamenlijk sync-event.

### G. 1.7 Tweede waarnemer — geen instrument
- Een collega vult **onafhankelijk** hetzelfde observatieblad in (O1–O3 pass/fail) en leest desnoods
  de marker-uitlijningen mee. Puur een tweede, los genoteerde beoordeling.

### Analyse achteraf
Voor B/C/D (en de DV2-tabel) is een klein **post-processing script** handig dat de logbestanden
inleest en RTT-percentielen, frame-stap-statistiek, de DV2-foutentabel en de gap/velocity-verdeling
+ de Fase 3-grafieken uitrekent. (Kan ik voor je schrijven zodra de logformaten vastliggen.)
