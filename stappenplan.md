# Stappenplan verbetering stageverslag

**Uitgangscijfer (docent-review tegen artikel-format v.2223):** 7,6 — goed.
**Doel:** 8,0–8,5 door de twee zwaarste deuken te dichten (generaliseerbaarheid + vooraf-geborgde meetcriteria) plus bureauwerk in de rigueur-dimensies.

**Volgorde-principe:** eerst bureauwerk + meetontwerp (Fase 0–1), dán pas de lift in (Fase 2). Anders meet je opnieuw en ontdek je achteraf dat je iets niet hebt gelogd.

Bron: `project/main.tex`. Regelnummers zijn indicatief (peilmoment review).

---

## Fase 0 — Bureauwerk, geen metingen nodig ✅ AFGEROND

Tilt vooral Methoden + Resultaten (samen 28% gewicht). Alle edits geverifieerd tegen de code; LaTeX compileert schoon (0 undefined refs/citations).

- [x] **0.1 Kalman-afleiding compleet maken.** Covariantie-update `P ← (I − KH)P` toegevoegd aan correctie-stap (`eq:kf-correct`). **Geverifieerd tegen code**: `ipc_lift_controller.gd:487–492` doet exact dit; verslag miste het juist. _Raakt: Resultaten._
- [x] **0.2 Q-matrix correct benoemen.** "white-noise-jerk" → "white-noise-acceleratie / constant-velocity". Code-comment regel 3 bevestigt "constant-velocity model". _Raakt: Resultaten._
- [x] **0.3 DV3 herformuleren.** "from noisy telemetry" → "sampled asynchronously and well below the display refresh rate". Lost tegenspraak met gap-filling-framing op. _Raakt: Vraagstelling._
- [x] **0.4 Transport-vooronderzoek bij RQ1.** Nieuwe subsectie `sec:prior-transport`: Bluetooth als geërfde hardware-constraint (HC-module + historische app-comms), wired/wifi kort uitgesloten, TCP = dev-substituut. _Raakt: Vooronderzoek._
- [x] **0.5 Bronnenhygiëne.** Bar-Shalom (canoniek, peer-reviewed) toegevoegd bij Q-matrix; elmenreich → `@techreport`; `merry2013encoder` → `merry2010encoder` (jaar consistent). _Raakt: Cross-cutting (bronnen)._
- [x] **0.6 Weesfiguur oplossen.** `fig:calibration-run` nu ge-`\ref`d in "Calibration run protocol". _Raakt: Resultaten._
- [x] **0.7 Configurator-discrepantie naar Results.** Per-deel getallen (rd1 +16 mm e.d.) nu als observatie in Validation Evidence; conclusie verwijst er alleen naar. _Raakt: Conclusie + Resultaten._
- [x] **0.8 Interpretatie-lekkage uit Results.** "load-bearing rather than cosmetic" (Results-q1) en de outlier-duiding (Logged events) verwijderd. _Raakt: Resultaten (objectiviteit)._
- [x] **0.9 Inleiding-relevantie minder hypothetisch.** "would/could" vervangen door concrete capability; diagnosetijd-claim blijft expliciet out-of-scope. _Raakt: Inleiding._
- [x] **0.10 Organisatorische aanbeveling toevoegen.** "Organisational embedding"-item toegevoegd aan Recommendations. _Raakt: Aanbevelingen._

---

## Fase 1 — Meetontwerp herzien (vóór de lift in)

Bepaalt of de tweede meetronde raak is. Pas hierna de method-secties aan.

- [ ] **1.1 DV1(b) kwantitatief + vooraf vastleggen.** RTT-**percentielgrens** (bv. P95 < X ms) i.p.v. alleen gemiddelde. _Raakt: Methoden (pre-registratie)._
- [ ] **1.2 DV3(b) kwantitatief + vooraf vastleggen.** Frame-level renderpositie+tijd → meetbare smoothness (bv. max stap tussen frames). _Raakt: Methoden._
- [ ] **1.3 Primaire foutmaat = display-vs-fysiek** (incl. configurator-bijdrage); display-vs-firmware-encoded als secundaire pipeline-isolatie. **Log beide.** _Raakt: Resultaten + DV2-meetdoel._
- [ ] **1.4 Logging-checklist hard maken:** per run automatisch frame-level renderpositie+timestamp, RTT per round-trip, ruwe encoder, gefilterde positie, **inter-sample gap**, **snelheidsprofiel**. (Laatste twee nodig voor stap 3.3.)
- [ ] **1.5 (Aanbevolen) externe hoekreferentie** (digitale gradenboog / laser) → compass-correctie niet langer self-referentieel.
- [ ] **1.6 (Aanbevolen) high-speed video** physiek-vs-display → kwantitatieve zichtbare lag.
- [ ] **1.7 (Aanbevolen) tweede waarnemer** scoort onafhankelijk pass/fail → ontkracht self-validation.

---

## Fase 2 — Meetcampagne op meerdere trapliften

Dichtt de zwaarste limitation (n=1 rail).

- [ ] **2.1 Rail-set kiezen op dekking, niet op aantal.** Variërend in lengte, aantal bochten, bochttypen (verticaal up/down + horizontaal links/rechts). Richtgetal **3–5 rails**; elk segmenttype op ≥2 rails.
- [ ] **2.2 Per traplift hetzelfde protocol:** stationaire baseline + B→T + T→B, met meer markers over álle segmenttypes, beide rijrichtingen.
- [ ] **2.3 Per rail de configuratie noteren** (lengte, bochten, types) voor per-rail/per-segmenttype-rapportage.

---

## Fase 3 — Analyse & herschrijven Resultaten/Conclusie

- [ ] **3.1 Aggregeren over rails:** fout (mean/SD/CI) totaal, per rijrichting, per segmenttype.
- [ ] **3.2 Grafieken maken** (geen losse tabelgetallen): positie-vs-tijd (smoothness), RTT-histogram, fout-per-rail/per-segmenttype.
- [ ] **3.3 Filter-tuning gronden** op gemeten gap-verdeling + snelheidsprofiel (σ_a, dead-reckoning-decay) → haalt "empirical tuning"-limitation weg.
- [ ] **3.4 Conclusie bijwerken:** antwoorden over meerdere rails; generaliseerbaarheid-limitation versmallen; interpretatie i.p.v. samenvatting.

---

## Fase 4 — Eindpolish

- [ ] **4.1** Elke figuur/tabel/vergelijking ge-`\ref`d.
- [ ] **4.2** Consistente terminologie + IEEE-nummerverwijzingen kloppen.
- [ ] **4.3** LaTeX compileert schoon; integrale eindlezing.

---

### Verwacht effect op het cijfer
- Fase 0 alleen (geen lift): ~7,8–8,0.
- + Fase 1–3 (meetontwerp goed + meerdere trapliften + grafieken + onderbouwde tuning): ~8,0–8,5.
