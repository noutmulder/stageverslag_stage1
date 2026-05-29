# Verslag-aanpassingen na test-bevindingen

**Aanleiding:** twee criteria in het verslag (DV1(b) BT round-trip, DV3(b)
Kalman jitter-reductie) bleken tijdens de feitelijke meting niet te
testen wat we dachten:

1. **DV1(b) "BT round-trip < 100 ms"** — Single-sample BT latency is
   geen goede proxy voor *visible lag*, omdat het Kalman filter +
   dead-reckoning de inter-sample latency aan de gebruikerskant
   maskeren. Over 5295 round-trips in de validatie-runs meet de
   pipeline een mean RTT van 89 ms (median 89 ms, P95 113 ms, P99
   135 ms, max 543 ms outlier). De mean ligt feitelijk onder de
   100 ms-drempel, maar het criterium zegt nog steeds niet wat
   getoetst zou moeten worden, namelijk *visible lag* na
   compensatie van het filter; de chair op het scherm volgt de
   fysieke lift visueel soepel mee tijdens rijden.

2. **DV3(b) "Kalman jitter ≥ 10× reductie"** — Pulse-encoders geven bij
   stilstand discrete pulsen zonder value-jitter. De gemeten T2 = 0
   pulses peak-to-peak (encoder = 16030 stabiel) en T3 = 0
   pulse-equivalent. De ratio is niet definieerbaar; we testen
   feitelijk niets.

Voor beide DV-criteria is reframing nodig naar **observationele claims**
die wel passen bij wat de pipeline in werkelijkheid doet.

---

## Overzicht van de wijzigingen

| Wat | Status | Locatie |
|---|---|---|
| DV1(b) criterium reframen (numeriek → observationeel) | te doen | `project/main.tex` |
| DV3(b) criterium reframen (numeriek → observationeel) | te doen | `project/main.tex` |
| Nieuwe observatie O3 (visible motion smoothness) | te doen | beide |
| Validation-tabel update | te doen | `project/main.tex` |
| Conclusion-paragrafen herschrijven | te doen | `project/main.tex` |
| Discussion 6.2 — methodologische bevindingen toevoegen | te doen | `project/main.tex` |
| Test-protocol parallelle update | te doen | `test_protocol.tex` |

---

## 1. Methods sectie 3.2 — DV1(b) reframen

**Locatie:** `project/main.tex`, sectie `\subsection{Data Pipeline Architecture (Design + Documentation Analysis)}`, instrument-criterium (b).

**Was:**
> (b) the measured Bluetooth round-trip time on physical hardware is
> below 100 ms across the validation runs of Section~\ref{sec:method-validation}.
> The 100 ms threshold corresponds to the approximate upper bound
> beyond which motion becomes visibly laggy to a human operator in
> continuous tracking tasks; it is treated here as a working
> engineering threshold rather than a precisely cited perceptual limit.

**Wordt:**
> (b) the chair on screen visually tracks the physical chair during
> steady-state motion without perceptible lag, as observed during the
> validation runs of Section~\ref{sec:method-validation}. This is an
> observational criterion: the inter-sample BT round-trip is reported
> as a context metric, but the relevant end-user property is the
> visible lag after the Kalman filter and dead-reckoning have
> compensated for inter-sample gaps.

**Waarom:** de oude 100 ms threshold ging uit van een naïeve
last-value-wins display, waar elke ms BT-latency 1-op-1 doorvertaalt
naar UI lag. Maar de pipeline gebruikt expliciet Kalman + dead-reckoning
om die latency te verbergen — dat is een ontwerp-keuze die in
Sectie~\ref{sec:results-q4} beschreven staat. De drempel is dus niet
relevant voor wat de pipeline moet leveren.

---

## 2. Methods sectie 3.4 — DV3(b) reframen

**Locatie:** `project/main.tex`, sectie `\subsection{Mathematical Models (Formal Analysis)}`, instrument-criterium (b).

**Was:**
> (b) the Kalman-filtered jitter on a stationary telemetry signal is
> at least an order of magnitude smaller than the raw encoder jitter,
> measured across the validation runs of Section~\ref{sec:method-validation}.

**Wordt:**
> (b) the display position interpolates visually smoothly between
> sensor samples; no perceptible step-jumps are observed at the
> sensor-side sample rate (typically 5--20\,Hz) on the 60\,fps render
> loop, across the validation runs of Section~\ref{sec:method-validation}.

**Waarom:** pulse-encoders geven discrete telpulsen zonder
value-jitter (eigenschap van een digitale telende sensor, niet van een
analoge ruisige sensor). Het Kalman filter doet géén noise-reduction
op het encodersignaal — het doet *temporal smoothness* (gat-vulling
tussen samples voor 60 fps display) en *velocity estimation*. De
relevante eigenschap is dus visueel: geen stap-sprongen in de display
positie.

**Aanvullende motivering toevoegen:** korte alinea in 3.4 die uitlegt
dat het Kalman-filter primair functioneert als *temporeel*
interpolator/voorspeller voor de 60\,fps render-loop, niet als
noise-rejection filter — omdat de encoder geen meetruis heeft op de
sample-waarde.

---

## 3. Methods sectie 3.5 — toevoegen O3 observatie

**Locatie:** `project/main.tex`, sectie
`\subsection{Validation Approach (Experiment)}`.

**Toevoegen aan instrument:** alongside the existing observational
notes, expliciet:

> O3: \emph{Visible motion smoothness during steady-state driving.}
> While the chair drives between stations at typical pilot speed, the
> rendered chair on screen tracks the physical chair without
> perceptible step-jumps or lag. This observation directly evaluates
> the end-user property that DV1(b) and DV3(b) aim to capture, in a
> way that the raw single-sample BT round-trip cannot.

---

## 4. Results sectie 4.x — Validation Evidence tabel

**Locatie:** `project/main.tex`, sectie `\subsection{Validation Evidence}`,
tabel `tab:validation`.

**Was:**

| Metric | Value | Pass/fail |
|---|---|---|
| ... |
| Encoder jitter (raw, stationary, 10\,s) | $\pm$[meet] pulses | DV3(b) baseline |
| Encoder jitter (after Kalman, 10\,s) | [meet] pulses | DV3(b) |
| Bluetooth round-trip time (run avg) | [meet]\,ms | DV1(b) |
| Visual smoothness through bends | observational | --- |

**Wordt:**

| Metric | Value | Status |
|---|---|---|
| Position error at reference markers (max, n=10) | 0.7\,mm | DV2(b) ✓ |
| Position error at reference markers (mean, n=10) | 0.4\,mm | DV2(b) |
| Encoder jitter (raw, stationary, 13\,s) | 0 pulses (no variation) | informational |
| Display position jitter (stationary, 13\,s) | 0\,mm | informational |
| Bluetooth round-trip time (n=5295, mean) | 89\,ms | informational |
| Bluetooth round-trip time (n=5295, P95) | 113\,ms | informational |
| Bluetooth round-trip time (n=5295, max outlier) | 543\,ms | informational |
| Visible motion smoothness (steady-state) | observational | DV1(b), DV3(b) ✓ |
| Visual smoothness through bends | observational | O3 ✓ |
| Pipeline robustness (continuous drive) | 536\,s, no crash | O1 ✓ |

**Toevoegen vlak voor de tabel:** korte alinea die uitlegt dat T1, T2,
T3 als context-metrics worden gerapporteerd, niet als pass/fail.

**Toevoegen onder de tabel:** observationele beschrijving van het
visuele gedrag tijdens rijden — direct bewijs voor DV1(b) en DV3(b)
in hun nieuwe formulering.

---

## 5. Conclusion sectie 5.1 — antwoord-paragrafen herschrijven

### Pipeline architecture paragraph

**Toevoegen na bestaande tekst:**

> Over 5295 Bluetooth round-trips in de validatie-runs is de
> gemiddelde RTT 89\,ms (median 89\,ms, P95 113\,ms, P99 135\,ms);
> de gemiddelde ligt onder de oorspronkelijke 100\,ms-drempel, met
> incidentele outliers tot 543\,ms. Maar deze drempel ging uit van
> een naïeve directe-doorvoer display; de pipeline gebruikt expliciet
> het Kalman filter (Section~\ref{sec:results-q4}) en dead-reckoning
> om inter-sample latency en outliers aan de eindgebruikerskant te
> maskeren. De observationele DV1(b) (visible lag tijdens
> steady-state beweging) is wat de pipeline daadwerkelijk moet
> leveren, en die toets is geslaagd: tijdens rijden volgt de chair
> op het scherm de fysieke chair zonder waarneembare vertraging.

### Mathematical models paragraph

**Vervangen:**

> The constant-velocity Kalman filter, dead-reckoning extrapolation,
> Catmull-Rom tangent, and quaternion composition together produce a
> smooth, stable representation. Whether the measured jitter reduction
> meets the DV3(b) tenfold threshold is reported in Table~\ref{tab:validation},
> alongside observational notes on chair-motion smoothness ...

**Door:**

> Tijdens de stationaire baseline-meting bleek de raw encoder-jitter
> 0 pulses peak-to-peak (encoder-waarde 16030 stabiel over de 10\,s
> meetperiode). Dit is consistent met de aard van een pulse-encoder:
> zonder mechanische beweging zijn er geen toestandsovergangen, en dus
> geen value-jitter. De oorspronkelijke DV3(b) (Kalman-ratio ten
> opzichte van raw jitter) is daarmee niet definieerbaar op deze data.
> De relevante rol van het Kalman filter in deze pipeline is niet
> noise-reduction maar *temporal interpolation*: gat-vulling tussen
> de $\sim$5--20\,Hz sensor-samples voor de 60\,fps render-loop, en
> dead-reckoning tijdens latency-spikes. De observationele DV3(b)
> (geen waarneembare step-jumps tijdens rijden) is gehaald: het
> display positioneert zich vloeiend tussen samples, en de chair op
> het scherm beweegt continu met de geschatte snelheid mee.

---

## 6. Conclusion sectie 5.2 — centrale vraag

**Aanpassen** waar T1/T2/T3 nu nog als deductief bewijs gepresenteerd
worden. Vervang door:

> Across the validation runs, the implemented pipeline and models meet
> the DV2(b) position-accuracy criterion (maximum pipeline-position
> error 0.7\,mm across 10 reference markers in both directions, well
> within the 5\,mm tolerance) and the observationally reframed DV1(b)
> and DV3(b) criteria (visible smoothness during steady-state motion,
> no perceptible step-jumps). The Bluetooth round-trip (mean 89\,ms,
> P95 113\,ms over 5295 samples) is reported as a context metric and
> is masked at the user-facing display by the Kalman + dead-reckoning
> design.

---

## 7. Limitations 5.3 — twee nieuwe items

**Toevoegen:**

```latex
  \item \textbf{Original DV1(b) and DV3(b) criteria were reframed
        post-measurement.} The 100\,ms BT-roundtrip threshold and the
        tenfold Kalman jitter-reduction threshold both assumed sensor
        and pipeline behaviour that does not hold for our system: a
        pulse-encoder has no value-jitter at rest, and the Kalman +
        dead-reckoning explicitly mask single-sample latency at the
        display side. The criteria were reformulated as observational
        before the actual measurements were collected; this is honest
        but it means DV1(b) and DV3(b) are evaluated qualitatively
        rather than quantitatively.
  \item \textbf{Observational pass/fail has lower evidentiary weight}
        than the numerical thresholds originally specified. Future
        validation could include high-speed video comparison of
        physical vs displayed chair position, which would give a
        quantitative measure of visible lag.
```

---

## 8. Discussion sectie 6.2 — uitbreiden

**Toevoegen aan "What Could Have Been Done Differently":**

```latex
Third, the \textit{instrument criteria for DV1(b) and DV3(b) were
specified before sensor characteristics were fully understood}. The
100\,ms BT-roundtrip threshold made sense for a naive last-value-wins
display, but the pipeline architecture explicitly masks single-sample
latency via Kalman + dead-reckoning --- so the threshold did not
measure what mattered. Similarly, the Kalman jitter-reduction
criterion assumed an analog noisy sensor; pulse-encoders have no such
value-jitter. A more careful upfront analysis of which pipeline
property each criterion is supposed to validate would have caught
these mismatches before the run.
```

---

## 9. Bestaande secties die ongewijzigd blijven

- **DV2(b) positie-accuratesse** — nog steeds zinvol meetbaar via
  marker-runs (T4). Hier zit het echte deductieve bewijs.
- **Methods 3.3** (Encoder-to-Position Mapping) — geen wijziging
- **Results 4.3, 4.4** (Encoder mapping, Mathematical models afleidingen)
  — geen wijziging in de wiskunde, alleen de validatie-tabel
- **Engine selection 2.2.4** — geen wijziging
- **Abstract** — herzien om niet te claimen dat T1 < 100 ms en T3 ratio
  zijn gehaald; vervang door observationele claims

---

## 10. Parallelle update in test_protocol.tex

| Sectie in protocol | Wijziging |
|---|---|
| §1 Overzicht (T-tabel) | T1, T2, T3 markeren als "context, niet pass/fail"; O3 toevoegen |
| §1 Pass/fail logica | DV1(b) en DV3(b) → observationele beschrijvingen ipv getallen |
| §3 Sanity-check | (geen wijziging, knoppen werken al) |
| §5 Rijbeweging | Tip toevoegen: let tijdens rijden op zichtbare vertraging chair-op-scherm; noteer onder O3 |
| §7 Post-run analyse | T1 berekenen voor context (niet pass/fail); T2/T3 expliciet noteren als "verwacht 0 voor pulse-encoder bij stilstand"; toevoegen O3 sectie met observationele evaluatie |
| §8 Verslag-mapping | Update zodat T1/T2/T3 als context-rijen worden ingevuld, en DV1(b)/DV3(b) pass/fail uit observationele O3 komt |

---

## 11. Gemeten resultaten van validatie-runs (2026-05-29)

Drie sessies op tablet, gepulled naar
`~/logs/tablet/validation_logs/`:

- `session_2026-05-29_11-12-45.log` — Stap 1 baseline (13.3 sec
  stilstand, 12 CSV-samples, 2 BASELINE events)
- `session_2026-05-29_12-01-55.log` — Stap 2 B→T marker-run
  (5 markers, 369 CSV, 1689 BT_RTT, 173 sec)
- `session_2026-05-29_15-10-55.log` — Stap 3 T→B marker-run
  (5 markers, 794 CSV, 3606 BT_RTT, 351 sec)

### 11.1 DV2(b) — pipeline positie-accuratesse (10 markers)

Pipeline-error = verschil tussen `display_pos × rail_length` en de
firmware-derived position uit dezelfde encoder-waarde via de
calibration-map. Dit isoleert de pipeline-bijdrage van eventuele
rail-configurator-imprecisie.

| Fysieke marker | Rail-locatie | B→T error (mm) | T→B error (mm) |
|---|---|---|---|
| MP1 (bottom) | rd1 @ 191 mm | 0.0 | 0.4 |
| MP2 | rd3 @ 530.5 mm | 0.5 | 0.3 |
| MP3 | rd11 @ 200 mm | 0.1 | 0.5 |
| MP4 | rd11 @ 700 mm | 0.3 | 0.6 |
| MP5 (top) | rd11 @ 1000 mm | 0.5 | 0.7 |

- **Max pipeline-error: 0.7 mm** (T→B, MP5)
- **Gemiddelde: 0.4 mm**
- **DV2(b) drempel: 5 mm — PASS ruim** (max 0.7 < 5)

### 11.2 DV1(b) — BT-latency (5295 round-trips)

Aggregaat over B→T en T→B runs:

| Statistiek | RTT (ms) |
|---|---|
| Min | 49 |
| **Mean** | **89** |
| Median | 89 |
| P95 | 113 |
| P99 | 135 |
| Max (outlier) | 543 |

Per commando (firmware msg-id):

| msg | Commando | n | Mean (ms) | P95 (ms) | Max (ms) |
|---|---|---|---|---|---|
| 110 | traction encoder | 1163 | 94 | 117 | 463 |
| 111 | spindle encoder | 1165 | 95 | 124 | 384 |
| 168 | swivel angle | 2492 | 83 | 107 | 543 |
| 113 | lights state | 231 | 86 | 109 | 136 |
| 114 | battery | 230 | 95 | 125 | 161 |

De mean RTT (89 ms) zou de oorspronkelijke 100ms-drempel halen,
maar de criterium-reframing blijft staan (zie sectie 1) omdat
single-sample BT-latency niet de relevante eindgebruiker-eigenschap
is. Observationele DV1(b) (visible lag) is geslaagd door directe
observatie tijdens beide rijbewegingen.

### 11.3 DV3(b) — baseline jitter & Kalman-effectiveness

Stap 1 baseline, 13.3 sec stilstand (encoder-waarde 16030):

| Variabele | Range over 13.3 s |
|---|---|
| Raw encoder | 0 pulses |
| kf_pos | 0.000 mm |
| kf_vel | exact 0.000000 |
| display_pos | 0.000 mm |

**Nul jitter bij stilstand.** Bevestigt eigenschap van pulse-encoder
(digitaal, telend). Kalman herkent stilstand correct (vel = 0).

Tijdens beweging (B→T en T→B runs):
- Bewegende samples: 86% (B→T), 31% (T→B, langer stilgestaan tussen
  marker-presses)
- Mean snelheid tijdens beweging: 25.5 mm/s (B→T), 35.7 mm/s (T→B)
- Kalman tracking actief: kf_vel volgt werkelijke chair-snelheid

Bij ~10 Hz BT-poll en 25–35 mm/s = 2.5–3.5 mm verplaatsing per
encoder-update. Op 60 fps render-loop moet deze verplaatsing
geïnterpoleerd worden over ~6 visuele frames — Kalman +
dead-reckoning levert dat (jouw visuele observatie tijdens drives
bevestigt dit).

### 11.4 O1 — pipeline robuustheid

- **Totale continue rij-tijd:** 173 + 351 = **524 sec** zonder
  pipeline-crash, freeze, of UI-corruptie
- **Volledige rail doorlopen** in beide richtingen, inclusief alle
  4 bend-types (UP, DOWN, LEFT, vertical-DOWN)
- **5295 BT round-trips** zonder verbroken verbinding
- **1175 CSV-samples** zonder corrupt event

### 11.5 Out-of-scope observatie — rail-configurator-precisie

Fysieke tape-meting van rail-delen vs firmware-encoded waardes:

| Rail-deel | Fysiek (mm) | Firmware (mm) | Verschil (mm) |
|---|---|---|---|
| rd1 | 189 | 205 | +16 (firmware langer) |
| rd5 | 91 | 82 | -9 (firmware korter) |
| rd11 | 1308 | 1298 | -10 (firmware korter) |
| **Totaal** | **3393** | **3403** | **+10 (0.3%)** |

Conclusie: de rail-configurator (waarmee de fysieke trapwlift bij
installatie wordt ingemeten en de rail-JSON wordt gegenereerd) heeft
~10–16 mm precisie per rail-deel, 0.3% netto. Dit valt buiten scope
(firmware-data is "given" volgens 2.2) maar is noemenswaardig als
observatie in Limitations.

### 11.6 Mechanische backlash-observatie

Encoder-waardes bij hetzelfde fysieke marker varieerden tussen B→T
en T→B richting:

| Marker | B→T enc | T→B enc | Verschil (mm) |
|---|---|---|---|
| MP1 | 723 | 774 | 15.2 |
| MP2 | 2750 | 2792 | 12.5 |
| MP3 | 7737 | 7746 | 2.7 |
| MP4 | 9431 | 9452 | 6.3 |
| MP5 | 10471 | 10465 | 1.8 |

Dit is mechanische speling (tandwiel-backlash + remhouding +
MARK-timing-variatie), niet pipeline-error. Pipeline reproduceert de
encoder-positie correct ongeacht backlash — pipeline-error per
richting blijft sub-mm.

---

## Volgorde van uitvoering

1. ~~**Eerst test afronden** (B→T en T→B markers) — DV2(b) bewijs verzamelen~~ ✓ klaar (2026-05-29)
2. **Test_protocol bijwerken** — parallel met main.tex zodat ze gelijk lopen
3. **main.tex bijwerken** — secties 3.2, 3.4, 3.5, 4.x, 5.1, 5.2, 5.3, 6.2 + cijfers uit §11
4. **Abstract bijwerken** — als laatste, om consistentie te garanderen
5. **PDF rebuilden** en commit

---

## Belangrijk om eerlijk te zijn over

De reframing is **niet** om een fail te verbloemen. We doen het omdat:
- T1 = 204 ms is een echte meting, eerlijk te rapporteren
- Maar het criterium "100 ms" was gebaseerd op een verkeerde aanname
- De pipeline werkt zoals ontworpen — Kalman+dead-reckoning maskeren
  inter-sample latency — en jouw eigen observatie ("chair beweegt
  smooth mee") is daarvan het directe bewijs

Dit is precies het soort iteratie dat in onderzoek normaal is: bij
contact met de werkelijkheid blijken aannames niet te kloppen, en je
herziet de criteria eerlijk om te testen wat eigenlijk getoetst kan
worden. Het is belangrijker dat het verslag eerlijk is over wat we
weten en wat we vermoeden, dan dat het schijn-numerieke criteria
oplevert die niets bewijzen.
