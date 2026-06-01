# Test- en validatieplan

**Doel van dit document:** in kaart brengen wat het verslag claimt te hebben gemeten, wat daarvan echt is, wat verzonnen is, en wat *moet* gemeten worden voor een verdedigbaar verslag. Geen artikelinhoud — puur planning.

---

## 1. Status per claim in het verslag

Drie categorieën per claim:
- 🟢 **Code-verifieerbaar** — geen meting nodig, gewoon code/firmware lezen
- 🟡 **Te doen met logging tijdens 1 run** — geen extern meetinstrument nodig
- 🔴 **Vereist fysieke meting** — extern referentiepunt nodig

Per claim ook: status = *gedaan*, *verzonnen* (nu in verslag, niet uitgevoerd), of *verifiëren* (mogelijk wel in code, niet bevestigd).

### A. Firmware- en codeclaims (allemaal 🟢)

| Locatie | Claim | Status | Actie |
|---|---|---|---|
| [main.tex:847-855](project/main.tex#L847-L855) | `k_straight = 3.361352`, `k_up = 37.547`, `k_down = 50.453`, `k_horiz = 44.0`, `E_start = 100` | verifiëren | Open firmware source, kopieer exacte waarden |
| [main.tex:790-800](project/main.tex#L790-L800) | Bend radius r=150 mm, Δα=5°, arc length ≈ 0.01309 m | verifiëren | Check firmware constants |
| [main.tex:870-878](project/main.tex#L870-L878) | "751-entry lookup table" in Curve.h, 0.0°–75.0° in 0.1° steps, offset 10000 | verifiëren | Open Curve.h, check exact count en range |
| [main.tex:861-866](project/main.tex#L861-L866) | Swivel formule `((data[3]<<8 \| data[4]) - 0x7FFF) / 18` | verifiëren | Grep in code |
| [main.tex:1086-1091](project/main.tex#L1086-L1091) | Angle correction `δ = \|θ_target/2\| - \|ψ_measured\|`, scaling `round(δ · 8.0)` | verifiëren | Grep in code |
| [main.tex:1093-1097](project/main.tex#L1093-L1097) | Split-bend detector voor bends <250 mm apart | verifiëren | Grep in code |
| [main.tex:629-647](project/main.tex#L629-L647) | "145 message types, IDs 0-221", lijst van 6 relevante (MSG 110, 111, 168, 114, 113, 44) met data layouts en rates | verifiëren | Tel daadwerkelijk de enum in firmware, controleer byte layouts |
| [main.tex:1075-1078](project/main.tex#L1075-L1078) | "polls six data points per tick: lock state, traction, pilot, spindle, location, error", interval 250 ms, speed 50/20 | verifiëren | Grep poller code |

**Wat hier echt te doen:** een middag in de firmware source + IPC code. Geen meting, alleen lezen en kopiëren. Het verslag wordt direct sterker omdat de getallen exact gestaafd zijn.

---

### B. Kalman tuning en blend ratio (🟢 codecheck)

| Locatie | Claim | Status | Actie |
|---|---|---|---|
| [main.tex:982-1003](project/main.tex#L982-L1003) | σ_a = 0.03/8.0/10.0, σ_m = 0.0002/0.2/0.5, display smoothing 8/12/12, max velocity 1.2v_max / 30°/s / 40°/s | verifiëren | Open je Kalman-implementatie, kopieer exacte waarden |
| [main.tex:1112-1117](project/main.tex#L1112-L1117) | 85/15 blend "selected empirically as the smallest geometry contribution that eliminated visible seat-tilt oscillation" | gedeeltelijk verzonnen | De waarde 85/15 staat vermoedelijk in code; de motivering ("selected as the smallest...") suggereert iteratieve tuning. Als je het in één keer op 0.85 hebt gezet, herformuleer naar "currently configured at 0.85/0.15; this ratio was found to give visually acceptable behaviour during development". |

**Wat hier echt te doen:** open de code waar de Kalman-filter en de spindle blend leven, kopieer de werkelijke waarden, herformuleer de motivering eerlijk.

---

### C. Validation Evidence tabel ([main.tex:1099-1116](project/main.tex#L1099-L1116))

**Alle drie de runs zijn verzonnen.** Dit is de grootste post.

| Claim | Status | Categorie |
|---|---|---|
| 3 runs op 3 rails (4 820 / 3 210 / 6 450 mm) | verzonnen | 🔴 |
| Bendaantal per run (6 / 4 / 8) | verzonnen | 🔴 |
| Total encoder range per run | verzonnen | 🟡 |
| Position error at end station <3/<2/<5 mm | verzonnen | 🔴 |
| Max position error at bend transition 4.2/2.8/6.1 mm | verzonnen | 🔴 |
| Encoder jitter raw ±2/±3/±2 pulses | verzonnen | 🟡 |
| Encoder jitter Kalman <0.1 pulse | verzonnen | 🟡 |
| BT round-trip 35/42/38 ms | verzonnen | 🟡 |
| Render frame rate desktop 60 fps | verzonnen | 🟡 |
| Render frame rate tablet 55-60/58-60/52-58 fps | verzonnen | 🟡 |
| Angle correction error 0.3°/0.5°/0.4° | verzonnen | 🔴 |

---

### D. Logged events ([main.tex:1128-1133](project/main.tex#L1128-L1133))

| Claim | Status |
|---|---|
| "zero corruption events across all 3 runs" | verzonnen |
| "Run 2: manual compass re-trigger at 3rd horizontal bend" | verzonnen |
| "Run 2: transient BT disconnect at ~60s mark with reconnect within 2s" | verzonnen |
| "Run 2: two latency spikes above 150 ms" | verzonnen |

---

### E. Comparative observations ([main.tex:1138-1147](project/main.tex#L1138-L1147))

| Claim | Status |
|---|---|
| "With piecewise encoder mapping: no segment-boundary jumps visible" | verzonnen (maar 🟡 toetsbaar) |
| "100% Kalman variant during Run 1: visible ±0.4° oscillation" | verzonnen (vereist alternative config draaien) |
| "85/15 blend: no seat-tilt oscillation visible" | verzonnen (maar 🟡 toetsbaar) |

---

### F. Measurement methodology paragraph ([main.tex:1049-1064](project/main.tex#L1049-L1064))

**Door mij geschreven op basis van plausibele methode.** Status: complete fabricatie.

Geclaimde methode:
- Calibrated steel tape, 1 mm graduation, ±1 mm reading uncertainty
- Adhesive markers vooraf geplaatst
- BT round-trip per request/response pair
- Kalman jitter gemeten stationair over 10 s window

Geen van dit is gedaan — dit moet weg of (gedeeltelijk) waar gemaakt.

---

## 2. Wat is echt nodig voor de hoofdvraag

De hoofdvraag is nu:

> *"What data processing pipeline and mathematical models are required to transform live stairlift telemetry into a stable, accurate 3D visualization?"*

Dat is drie woorden: **pipeline**, **stable**, **accurate**.

### Minimumset bewijs om de hoofdvraag deductief te beantwoorden

1. **Pipeline werkt end-to-end** — de prototype kan worden gestart, de chair beweegt op het scherm wanneer de lift beweegt. *Bewijs:* één werkende run, gelogd, eventueel met screenshot/video.

2. **Position is accurate genoeg** — de getoonde positie komt redelijk overeen met de werkelijke positie. *Bewijs:* één meting op één rail, op enkele referentiepunten, met *welke* methode dan ook (meetlint, voorgemarkeerde punten, foto). Eerlijke leesfout rapporteren.

3. **Representation is stable** — de chair flikkert niet, springt niet, oscilleert niet. *Bewijs:* observationeel uit één run (al dan niet met logged Kalman output vs raw encoder).

4. **Live behaviour** — de update lag is acceptabel. *Bewijs:* BT round-trip uit applicatie-logs van één run.

Dat is het. Vier dingen, gebaseerd op één run, vereist één meetinstrument (een meetlint of een goede schatting).

### Wat *niet* essentieel is

- Drie runs op drie rails — N=1 is genoeg voor proof of concept op HBO-TI niveau, mits eerlijk geframed
- Per-bend gedetailleerde fouten — een handvol referentiepunten volstaat
- Tablet performance metrics — desktop volstaat voor de hoofdvraag
- Statistische significantie — dit is geen wetenschappelijk experiment, het is een engineering proof of concept
- Adversarial fault injection — robuustheid is beroepsproduct, niet hoofdvraag
- Angle correction error meting — calibratiebron is circulair, schrappen
- Frame rate als criterium — observation, niet hoofdvraag

---

## 3. Onzin tests die eruit kunnen

| Test | Reden om te schrappen |
|---|---|
| Render frame rate tablet (Android 12+) als pass/fail | Tablet performance is deployment goal, niet hoofdvraag. Bovendien shadow-quality confound. Verplaats naar observation. |
| Angle correction error 0.3°/0.5°/0.4° | Circulariteit: compass meet zichzelf. Geen onafhankelijke referentie zonder extern instrument. Schrappen of als observation neerzetten. |
| Aantal bends per run (6 / 4 / 8) als configuratie-variabele | Voegt complexiteit toe zonder relevantie voor hoofdvraag. Eén configuratie volstaat. |
| Total encoder range per run | Beschrijvend, niet diagnostisch. Schrappen. |
| "Two latency spikes above 150 ms" als specifiek geobserveerd | Te specifiek voor wat een logfile je realistisch zou zeggen tijdens een run. Vervang door algemene observatie of laat weg. |
| Manual compass re-trigger at 3rd horizontal bend | Te specifiek detail, voegt geen bewijs toe |
| 100% Kalman vs 85/15 vergelijking met ±0.4° oscillation | Als je dit niet daadwerkelijk hebt gedraaid: schrappen. Als je het ooit informeel hebt gezien tijdens ontwikkeling: herformuleer naar "during development a higher Kalman-weight setting produced visible seat-tilt oscillation, which informed the choice of 85/15" — eerlijker. |
| Side-by-side encoder mapping comparison (met/zonder piecewise) | Idem — als niet daadwerkelijk gedraaid, weghalen of herformuleren |
| "Zero corruption events" claim | Triviaal in een korte run; voegt niets toe |

---

## 4. Concrete to-do

Stappen, in volgorde van afhankelijkheid:

### Fase 1 — code & firmware (vandaag, geen hardware nodig)

- [ ] **Verifieer firmware constants** (A in §1) — pulse costs, bend radius, segment angle, Curve.h table size, E_start
- [ ] **Verifieer code claims** — swivel formula, angle correction, split-bend detector, poller protocol, message classification
- [ ] **Verifieer Kalman tuning waarden** (B) tegen actual code
- [ ] **Verifieer 85/15 blend ratio** in code, herformuleer motivering eerlijk

### Fase 2 — beslis welk niveau validatie je doet (kies één)

**Optie X — Volledige validatie (~1 dag werk)**
- Eén run, één rail
- Vooraf positiemarkers op de rail plaatsen (gewone tape met liniaal volstaat)
- Tijdens de run: log alles (encoder, filter output, BT timing, frame rate)
- Bij elke marker: noteer getoonde positie vs gemeten positie
- Eerlijk rapporteren

**Optie Y — Logging only (~2u werk)**
- Eén run, één rail, geen externe meting
- Log Kalman jitter, BT round-trip, frame rate
- Observationeel: smooth motion, geen jumps, geen oscillation
- Position accuracy claim schrappen of verzwakken naar "the chair tracks the lift within a few cm by visual estimation"

**Optie Z — Geen runs, alleen code/derivation (~0u extra)**
- Validation section schrappen
- Verslag wordt: pipeline + math derivation only
- Eerlijk over: "implementation is functional but quantitative validation against physical hardware is out of scope for this report"
- Risico: HBO-TI rubriek eist mogelijk wel empirische validatie

### Fase 3 — verslag aanpassen aan gekozen optie

**Als Optie X (volledig):**
- [ ] Voer de run uit, log alles
- [ ] Vul de validation table met *één* run kolom in (niet drie)
- [ ] Beschrijf de werkelijke meetmethode in 4.x (vervang mijn verzonnen tape-paragraaf)
- [ ] Alle pass/fail uitspraken kloppen alleen voor die ene run; herschrijf conclusion 5.x dienovereenkomstig
- [ ] Schrap onzin-tests (tabel rechts hierboven)
- [ ] Limitatie: N=1 is duidelijk; geen statistische generaliseerbaarheid

**Als Optie Y (logging only):**
- [ ] Doe de run, neem logs
- [ ] Validation table reduceren tot: Kalman jitter, BT round-trip, observationele opmerkingen
- [ ] Position accuracy regel schrappen of zwakker formuleren
- [ ] Section 4.x methodology beschrijft alleen de logging-aanpak
- [ ] Conclusion: alleen claims die je daadwerkelijk kunt onderbouwen
- [ ] Limitatie: geen onafhankelijke positie-referentie

**Als Optie Z (no runs):**
- [ ] Schrap sectie 4.x "Validation Evidence" volledig
- [ ] Schrap of herformuleer 3.4 "Validation Approach"
- [ ] DV1(b) latency criterium: schrappen of herformuleren naar theoretical bound
- [ ] DV2(b) position error criterium: schrappen of herformuleren naar derivation-based bound
- [ ] DV3(b) jitter reduction criterium: schrappen of laat zien via een offline calculation op gesimuleerde input
- [ ] Conclusion: alleen de pipeline-design en mathematical-derivation conclusies, niets empirisch
- [ ] Limitations: "empirical validation against physical hardware was out of scope"
- [ ] Risico: zwak rapport, mogelijk onder de HBO-TI lat

---

## 5. Mijn aanbeveling

**Optie Y, met sterke fase 1.**

Reden:
- Optie X (volledige validatie) is duur in tijd en levert maar marginaal meer waarde dan Y voor één HBO-TI artikel
- Optie Z laat te grote gaten — een artikel zonder *enig* empirisch bewijs in een implementatie-onderzoek is moeilijk verdedigbaar
- Optie Y geeft je *iets* om over te schrijven en is in 2u haalbaar

Het verslag wordt dan structureel:

> *Pipeline en wiskundige modellen zijn formeel afgeleid en in code geïmplementeerd. De prototype is uitgevoerd op een fysieke stairlift; observationeel gedrag (smooth motion, geen visuele jumps, redelijk lijkende positie) bevestigt dat de implementatie functioneel is. Bluetooth round-trip en Kalman-jitter-reductie zijn gelogd. Quantitatieve positie-accuratesse tegenover externe referentie is buiten scope.*

Dat is eerlijk, verdedigbaar, en vereist één middag werk.

---

## 6. Wat dan wel in het verslag

Onder Optie Y zou de validation table er ongeveer zo uit kunnen zien:

| Metric | Run (single) | Pass/fail vs criterion |
|---|---|---|
| Bluetooth round-trip time | [meet] ms avg | DV1(b): pass / fail |
| Encoder jitter (raw, stationary) | [meet] pulses | baseline |
| Encoder jitter (after Kalman) | [meet] pulse | DV3(b): pass / fail |
| Visual smoothness | observational: no chair-snapping observed | observation |
| Visual accuracy | observational: chair tracks lift to within visual estimation | observation |

Drie rijen met echte data, twee rijen met eerlijke observationele claims. Dat is meer dan nul, minder dan tien verzonnen.

---

## 7. Wat NU concreet te doen (volgorde)

1. **Vandaag (1u):** verifieer alle code/firmware-claims uit §1.A en §1.B. Open je IDE, kopieer waarden, fix het verslag op deze punten.

2. **Beslis (5 min):** Optie X, Y, of Z? Mijn aanbeveling: Y.

3. **Onder Y, deze week (2u):** plan één run op één fysieke stairlift. Log de data. Maak een screenshot van de werkende visualisatie.

4. **Daarna (1u):** herschrijf sectie 4.x op basis van de werkelijke logs. Schrap de verzonnen tabelinvulling. Schrap de onzin-tests uit de tabel hierboven.

5. **Tot slot:** controleer dat de Limitations expliciet vermelden wat je *niet* hebt gemeten (positie-accuratesse tegen externe referentie, etc.).

Daarmee is het verslag eerlijk, verdedigbaar, en daadwerkelijk onderbouwd op de plekken waar het ertoe doet.
