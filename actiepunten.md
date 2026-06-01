# Actie-overzicht

Concrete to-do voor een verdedigbaar verslag. Twee delen:
- **A** — wijzigingen in het verslag (geen meting nodig, gewoon code/firmware checken of tekst aanpassen)
- **B** — wat je daadwerkelijk moet testen op de hardware

Aannames bij dit overzicht:
- Je doet **één run** op één fysieke stairlift (niet drie). Eerlijker en haalbaar.
- Je doet **logging tijdens die run** voor wat zonder extern instrument meetbaar is.
- Je doet **één eenvoudige positie-meting** met meetlint of voorgemarkeerde punten (geen laser).
- Alles wat niet onderbouwd kan worden → eruit of als observatie geframed.

---

## Deel A — Wijzigingen in het verslag

### A1. Code/firmware verificatie (geen meting, alleen lookup)

Per regel: open het bestand, kopieer de werkelijke waarde, vervang in het verslag.

| # | Locatie in verslag | Wat checken | Bron |
|---|---|---|---|
| A1.1 | [main.tex:847-855](project/main.tex#L847-L855) — pulse cost constants | `k_straight`, `k_up`, `k_down`, `k_horiz`, `E_start` | Firmware source, zoek op de namen |
| A1.2 | [main.tex:790-800](project/main.tex#L790-L800) — bend geometry | Bend radius (150 mm?), segment angle (5°?), arc length | Firmware constants |
| A1.3 | [main.tex:870-878](project/main.tex#L870-L878) — Curve.h lookup table | Aantal entries (751?), range (0-75°?), step (0.1°?), offset (10 000?) | `Curve.h` openen |
| A1.4 | [main.tex:861-866](project/main.tex#L861-L866) — swivel formule | `((data[3]<<8 \| data[4]) - 0x7FFF) / 18` exact zo? | Grep swivel code |
| A1.5 | [main.tex:1086-1091](project/main.tex#L1086-L1091) — angle correction | `δ = \|θ_target/2\| - \|ψ_measured\|`, scaling `round(δ · 8.0)`? | Grep angle correction code |
| A1.6 | [main.tex:1093-1097](project/main.tex#L1093-L1097) — split-bend detector | Drempel <250 mm? Bestaat de detector? | Grep poller/calibration code |
| A1.7 | [main.tex:629-647](project/main.tex#L629-L647) — message classification | "145 message types, IDs 0-221", 6 relevant messages | Firmware enumeration tellen |
| A1.8 | [main.tex:1075-1078](project/main.tex#L1075-L1078) — calibration polling | 6 data points per tick (welke?), 250 ms interval, speeds 50/20 | Poller code |
| A1.9 | [main.tex:982-1003](project/main.tex#L982-L1003) — Kalman tuning waarden | σ_a, σ_m, smoothing rate, max velocity per axis | Kalman implementatie |
| A1.10 | [main.tex:1112-1117](project/main.tex#L1112-L1117) — 85/15 blend ratio | Werkelijke waarde + eerlijke motivering | Spindle code |

**Tijd:** 1u, hele tafel in één sessie.

---

### A2. Verzonnen content verwijderen

Deze regels uit het verslag moeten weg omdat er geen onderbouwing voor is.

| # | Wat | Locatie | Actie |
|---|---|---|---|
| A2.1 | Drie runs in validation table | [main.tex:1099-1116](project/main.tex#L1099-L1116) | Reduceren tot één kolom (jouw werkelijke run) |
| A2.2 | "no data corruption detected by parser checksum in any case" | [main.tex:1130](project/main.tex#L1130) | Schrappen (of rapporteren wat je werkelijk in de log ziet) |
| A2.3 | "Run 2: manual compass re-trigger at 3rd horizontal bend" | [main.tex:1131-1132](project/main.tex#L1131-L1132) | Schrappen |
| A2.4 | "Run 2: transient BT disconnect with auto-reconnect within 2s" | [main.tex:1131-1132](project/main.tex#L1131-L1132) | Schrappen of vervangen door je werkelijke observaties |
| A2.5 | "two latency spikes above 150 ms" | [main.tex:1132-1133](project/main.tex#L1132-L1133) | Schrappen of vervangen |
| A2.6 | "100% Kalman variant during Run 1: visible ±0.4° oscillation" | [main.tex:1144-1147](project/main.tex#L1144-L1147) | Schrappen, OF zwak herformuleren als "during development a higher Kalman weight produced visible oscillation" |
| A2.7 | "no segment-boundary jumps with piecewise mapping enabled" | [main.tex:1142-1144](project/main.tex#L1142-L1144) | Hou aan als je dit echt observeert tijdens je run; anders schrappen |
| A2.8 | Mijn meetmethode-paragraaf (steel tape ±1mm etc.) | [main.tex:1049-1064](project/main.tex#L1049-L1064) | Herschrijven naar wat je werkelijk doet |

**Tijd:** 30 min, na A1.

---

### A3. Onzin-tests eruit (niet relevant voor hoofdvraag)

| # | Wat | Reden |
|---|---|---|
| A3.1 | Tablet frame rate als pass/fail criterium | Tablet performance is deployment goal, niet hoofdvraag. Houd als observation, geen criterium. |
| A3.2 | Angle correction error als pass/fail | Circulariteit (compass meet zichzelf). Schrappen of als observation. |
| A3.3 | Variatie in aantal bends (6/4/8) | Niet relevant voor één run. |
| A3.4 | Total encoder range rij | Descriptief, geen criterium. Mag weg. |
| A3.5 | Render frame rate desktop als criterium | Implementatie-detail. Houd als observation. |

**Tijd:** 15 min, gelijktijdig met A2.

---

### A4. Structuur-edits die je houdt (al gedaan, niet committed)

Deze zijn al doorgevoerd en zijn goed, ongeacht welke tests je doet:

- 4 DV's → 3 DV's (DV4 als methodologie i.p.v. zelfstandige vraag)
- Centrale vraag: inductieve "faster and more intuitive" claim eruit
- DV1 criteria: alleen classificatie + BT round-trip
- DV2 criteria: mapping + position error met 5/10mm split naar raillengte
- DV3 criteria: derivaties + Kalman jitter reductie (quaternion-singulariteit eruit)
- Limitations uitgebreid met self-validation, circulariteit, frame rate confound

**Tijd:** 0 — al gedaan.

---

## Deel B — Wat je moet testen

### B1. Met logging only, één run (geen extern instrument)

Tijdens één run de prototype draaien en deze data loggen:

| # | Data | Hoe loggen | Voor welk DV-criterium |
|---|---|---|---|
| B1.1 | Bluetooth round-trip time per request/response | Timestamp diff in applicatie | DV1(b) — pass/fail < 100 ms |
| B1.2 | Raw encoder values (stationair, 5-10 s window) | Log raw encoder feed met chair stilstaand | DV3(b) baseline |
| B1.3 | Kalman-filtered position (stationair, zelfde window) | Log filter output op dezelfde periode | DV3(b) — pass/fail ≥ 10× reductie |
| B1.4 | Render frame rate (desktop) | Engine internal counter, gemiddelde over de run | Observation |
| B1.5 | Visuele observatie: smoothness | Tijdens de run kijken naar het scherm + screenshot/video | Observation in conclusion |

**Tijd:** 30-60 min (setup) + de duur van de run zelf.

---

### B2. Met simpele fysieke meting (één meetinstrument)

Wat je nodig hebt:
- Een meetlint of vooraf gemarkeerde punten op de rail
- Een manier om de "displayed position" te lezen tijdens de run (screenshot, log timestamp, of getuige)

| # | Wat meten | Hoe | Voor welk DV-criterium |
|---|---|---|---|
| B2.1 | Positie van chair bij vooraf gekozen referentiepunten | Markers op rail (bv. bottom, midden, top, eventueel bij elke bend). Bij elk punt: noteer wat je in de visualisatie ziet vs waar de chair fysiek is. | DV2(b) — pass/fail 5mm/10mm |
| B2.2 | Aantal referentiepunten | Minimaal 3 (bottom, midden, top). Idealiter elke bend-entry en bend-exit ook. | DV2(b) |

**Wat je *niet* hoeft:**
- Laser of digitale waterpas
- Sub-mm precisie — een normaal meetlint volstaat, eerlijke leesfout rapporteren (±1-2 mm)
- Meerdere runs op meerdere rails

**Tijd:** 1-2u inclusief markers plaatsen, run uitvoeren, noteren.

---

### B3. Volgorde tijdens de run

Om alles in één sessie te doen:

1. **Vooraf** (15 min)
   - Plaats markers op de rail bij gekozen referentiepunten
   - Meet de positie van elke marker met meetlint vanaf het station
   - Start logging in de prototype (BT round-trip, encoder raw, encoder filtered)

2. **Stationaire baseline** (5 min)
   - Chair op één marker, niet bewegend
   - Log 10 s raw encoder + Kalman output
   - Dit levert B1.2 en B1.3 op

3. **Volledige run** (5-15 min afhankelijk van rail)
   - Drive van bottom naar top
   - Bij elke marker: noteer getoonde positie + tijdstempel (foto/screenshot is fijn)
   - Observeer: smoothness, snapping, oscillation
   - Tegelijkertijd loopt BT round-trip logging

4. **Return run** (5-15 min)
   - Drive top naar bottom
   - Idem
   - Geeft je effectief twee meetpunten per marker

5. **Afsluitend** (5 min)
   - Stop logging, bewaar de log files
   - Screenshot van werkende visualisatie

**Totale tijd op de hardware: ~1u.**

---

## Volgorde van uitvoering

| Stap | Wat | Wanneer | Tijd |
|---|---|---|---|
| 1 | A1: Code/firmware verificatie | Vandaag | 1u |
| 2 | A2 + A3: Verzonnen content schrappen + onzin-tests eruit, **tijdelijk** als placeholder in tabel | Vandaag | 45 min |
| 3 | **COMMIT** | Vandaag | 5 min |
| 4 | B1 + B2: Run op fysieke stairlift | Deze week | 1-2u |
| 5 | Verslag invullen met werkelijke meetdata | Direct na de run | 30 min |
| 6 | **COMMIT** | Direct na invullen | 5 min |
| 7 | Coherentie-check verslag (klopt conclusie nog?) | Daarna | 15 min |
| 8 | Final commit | | 5 min |

**Totaal: ~4-5u verspreid over één tot twee dagen.**

---

## Wat in het verslag staat na uitvoering

Validation table — één kolom werkelijke data, paar observaties:

| Metric | Run (single) | Pass/fail |
|---|---|---|
| Bluetooth round-trip time | [meet] ms avg | DV1(b): [pass/fail] |
| Encoder jitter raw (stationary) | [meet] pulses | baseline |
| Encoder jitter after Kalman | [meet] pulse | DV3(b): [pass/fail] |
| Position error at reference points | [meet] mm max | DV2(b): [pass/fail] |
| Render frame rate desktop | [meet] fps | observation |
| Visual smoothness | observational | observation |

Plus een paragraaf met je daadwerkelijke meetmethode (vervangt mijn verzonnen tape-paragraaf).

Conclusion en limitations al voorbereid in de structurele edits; vul daar de werkelijke getallen in.

---

## Wat NIET in het verslag hoeft

Definitieve lijst van wat je *niet* hoeft te doen:

- Drie aparte runs op drie rails
- Tablet validation
- Angle correction error meting
- Fault injection / robustness test
- Statistische analyse
- User study
- Per-bend gedetailleerde foutanalyse (bovenop wat je tijdens de run zou observeren)
- 100% Kalman vs 85/15 comparative run

Niets daarvan is essentieel voor de hoofdvraag.
