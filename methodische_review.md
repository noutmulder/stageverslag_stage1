# Methodische review van het stageverslag

**Datum:** 2026-05-28
**Scope:** secties 2 (Problem Statement), 3 (Methods), 4 (Results), 5 (Conclusion) van `project/main.tex`
**Doel:** per onderdeel beoordelen of (1) de onderzoeksclaim daadwerkelijk is getoetst, (2) de gebruikte toetsing valide is, en (3) het criterium zelf noodzakelijk is voor het beantwoorden van de bijbehorende onderzoeksvraag.

---

## Leessleutel

Voor elk *instrument-criterium* uit secties 3.2–3.5 stel ik drie vragen:

1. **Is het getoetst?** (volledig / gedeeltelijk / niet)
2. **Klopt de toetsing?** (meet je wat je denkt te meten? is de methode onafhankelijk?)
3. **Is dit criterium echt nodig?** (test het de onderzoeksvraag, of is het een ontwerpaanname / implementatiedetail dat er verkeerd is ingeslopen?)

Vraag 3 is even belangrijk als 1 en 2: een criterium dat niet getoetst is maar ook niet echt thuishoort, schrappen is beter dan extra metingen toevoegen.

---

## Samenvatting

**4 onderzoeksvragen, 13 instrument-criteria:**

| Status | Aantal |
|---|---|
| Volledig getoetst, valide | 4 |
| Gedeeltelijk of valideringsprobleem | 6 |
| Niet getoetst | 3 |

**De vier kritieke punten** (zie detail per DV):

1. **DV3(c)** — quaternion-singulariteitscheck staat als criterium in 3.4 maar wordt nergens gemeten. Hard gat.
2. **DV1(b)** — meetwaarde "BT round trip" matcht het criterium "end-to-end latency" niet. Mismatch.
3. **DV2(b)** — meetmethode voor "physical position" is niet beschreven; de 5 mm tolerantie is daardoor niet objectief verifieerbaar.
4. **Angle-correction error** wordt gemeten met dezelfde compass-tracker die de correctie berekent. Circulariteit.

---

## DV1 — Data Pipeline Architecture

> **Vraag:** *"What data pipeline architecture can transport live telemetry from the controller to a 3D rendering environment at sufficient throughput?"*
>
> **Methode (3.2):** Architectural design + documentation analysis.

### Criterium (a) — "Each layer has a single, well-defined responsibility"

**Getoetst?** Nee, want het is geen toetsbare hypothese. De 5-laagse architectuur in sectie 4.2 *demonstreert* deze eigenschap door beschrijving — maar er is geen meting die "single responsibility" kwantificeert.

**Klopt de toetsing?** Niet van toepassing — er is geen toetsing.

**Is dit criterium nodig?** **Twijfelachtig.** Dit is een *ontwerpprincipe*, geen *onderzoeksuitkomst*. Het hoort thuis als motivering in het "Why this approach"-veld, niet als instrument. Een instrument moet iets meten dat *na afloop* van het onderzoek aangetoond is.

**Suggestie:** verwijderen uit "Instrument (when done)" en verplaatsen naar "Why this approach". OF: meetbaar maken — bijvoorbeeld "geen cross-layer dependencies in de codebase, geverifieerd door static dependency graph".

---

### Criterium (b) — "Expected end-to-end latency from sensor read to display update is below 100 ms"

**Getoetst?** ⚠ Gedeeltelijk. In tabel `tab:validation` staat de rij *"Display update latency (BT round trip)"* met 35–42 ms, gemarkeerd als Pass (≤ 100 ms).

**Klopt de toetsing?** **Nee.** Het criterium specificeert *"end-to-end latency from sensor read to display update"*. Dat omvat:

```
[sensor] → BT transport → parser → poller → Kalman filter → render queue → [display]
```

De gemeten "BT round trip" is alleen het transport-segment. Parser, poller, Kalman, render queue zijn niet meegeteld. Op een 60 fps render loop (16.7 ms/frame) is alleen al de render queue plus 1 frame display lag ~30 ms extra. Realistische end-to-end is dus eerder 70–90 ms, mogelijk over de drempel bij latency spikes.

**Is dit criterium nodig?** Ja, latentie is centraal voor de "live" claim in de centrale vraag. Maar de meting moet matchen.

**Suggestie:** óf het criterium herformuleren naar "BT round trip < 100 ms" (eerlijk over wat je meet), óf de meting verbreden. Optie 2 vereist instrumentatie van elke laag — duur. Optie 1 is eerlijker maar dekt minder.

**Kritische vervolgvraag:** waar komt de 100 ms drempel überhaupt vandaan? De methode zegt "below the threshold at which the motion becomes visibly laggy to a human operator" — maar 100 ms staat zonder bron. Dit is een **onbewezen aanname**. Voor menselijke perceptie wordt vaak ~100–150 ms genoemd, maar dit is taakafhankelijk. Een literatuurverwijzing zou de drempel verankeren.

---

### Criterium (c) — "Poller sustains at least 20 Hz per telemetry axis under normal Bluetooth conditions"

**Getoetst?** **Nee.** De validatietabel heeft geen rij voor de behaalde polling rate. Er staat alleen impliciet "Display update latency (BT round trip): 35 ms avg" — daaruit kun je *afleiden* dat polling werkt, maar de 20 Hz claim wordt nergens direct gemeten.

**Klopt de toetsing?** Niet van toepassing.

**Is dit criterium nodig?** **Twijfelachtig in deze vorm.** De 20 Hz is een randvoorwaarde uit het probleem (sensors leveren met ~20 Hz). De vraag is niet of de *poller* dat haalt, maar of de pipeline het tempo van de sensor kan bijhouden. Dat is interessanter en al gedekt door criterium (b) als die goed gemeten wordt.

**Suggestie:** óf rij toevoegen "Achieved poll rate: traction X Hz, spindle Y Hz, swivel Z Hz", óf criterium schrappen omdat (b) het impliceert.

---

### Criterium (d) — "Byte-level corruption is detectable and recoverable without propagating to higher layers"

**Getoetst?** ⚠ Alleen observationeel. In [main.tex:1106-1107](project/main.tex#L1106-L1107) staat: *"no data corruption was detected by the parser checksum in any case"*. Dat is een vaststelling, geen test.

**Klopt de toetsing?** **Nee, dit is geen test.** Om "detectable AND recoverable" te bewijzen heb je *fault injection* nodig: opzettelijk corrupte bytes injecteren en kijken of (1) de parser ze afwijst en (2) de pipeline herstelt zonder corrupte data door te geven. Dat is hier niet gedaan.

**Is dit criterium nodig?** **Discussieerbaar.** Het zit eerder in het domein van *robuustheidstesten* dan van het onderzoek naar de pipeline-architectuur. De architectuur ondersteunt deze functionaliteit (checksum FSM is beschreven in 4.2) — maar dat de architectuur het kan, is wat anders dan dat het correct werkt onder fout-condities.

**Suggestie:** óf het criterium verzwakken naar "the architecture has a checksum mechanism at the parser layer, demonstrated by the FSM specification" (eerlijk over wat aangetoond is), óf het hele criterium schrappen als robuustheidstesten buiten scope vallen.

Bijkomende observatie: in [main.tex:1108-1110](project/main.tex#L1108-L1110) wordt wel een transient Bluetooth disconnect gemeld in Run 2 met auto-reconnect binnen 2 s. Dat is *transport-laag* recovery, niet *byte-level* corruption recovery. Het is een ander faalmodus.

---

### Criterium (e) — "Every message ID classified, with relevant subset identified with rationale and byte-level documentation"

**Getoetst?** ✓ Volledig. Tabel `tab:telemetry` in 4.2 noemt de 6 relevante van 145 berichten, en de prose in 4.2 documenteert de byte layout van MSG 110, MSG 111, MSG 168 etc.

**Klopt de toetsing?** Ja, formele documentatie-analyse is hier een valide methode (zoals 3.2 ook stelt).

**Is dit criterium nodig?** Ja — dit is het deel van DV2 dat oorspronkelijk DV1 was. Goed gedekt.

---

### DV1 — totaalbeoordeling

Van de vijf criteria is er één (e) goed, één (b) verkeerd gemeten, twee (c, d) niet getoetst, één (a) niet-toetsbaar. Dat is voor één DV een mager rapport. Aanbeveling:

- **Schrappen:** (a) — verplaatsen naar motivering.
- **Herformuleren:** (b) — meting matchen aan claim, OF claim aanpassen aan meting.
- **Meting toevoegen of schrappen:** (c) — als je het houdt, meet het; anders weg.
- **Verzwakken of schrappen:** (d) — eerlijk over wat aangetoond is.
- **Behouden:** (e).

Na deze opschoning zou DV1 nog 2–3 *valide* instrument-criteria hebben, allemaal getoetst. Dat is sterker dan 5 criteria waarvan 4 problemen hebben.

---

## DV2 — Encoder-to-Position Mapping

> **Vraag:** *"How can encoder pulse counts be mapped to a normalized position along a 3D rail with segment-dependent pulse costs?"*
>
> **Methode (3.3):** Formal mathematical analysis.

### Criterium (a) — "The mapping is defined for all segment types"

**Getoetst?** ✓ Volledig. Sectie 4.3 derives de mapping voor straight, vertical bend (up/down), en horizontal bend. Vergelijkingen 7–10 dekken alle types.

**Klopt de toetsing?** Ja — formele wiskundige derivatie is de juiste methode voor een deterministisch geometrisch probleem.

**Is dit criterium nodig?** Ja.

---

### Criterium (b) — "A calibration procedure aligns encoder values with 3D distances"

**Getoetst?** ⚠ Procedure beschreven, methode niet gespecificeerd.

In sectie 4.6 staat:

> *"Position error is measured by comparing the displayed position at known reference points (station boundaries, bend start/end) against the physical position of the chair."*

Maar **hoe wordt "physical position of the chair" gemeten?** Niets in 4.6 vertelt dit:
- Met een rolmaat langs de rail?
- Met een laser-afstandsmeter?
- Met visueel uitlijnen van markers?
- Door de chair op vooraf gemarkeerde punten te zetten (en hoe zijn die punten dan gemarkeerd)?

Zonder deze methode is de "5 mm tolerantie" niet objectief verifieerbaar. Een rolmaat heeft zelf ~1 mm leesfout, een laser <0.5 mm — afhankelijk van methode is de meetfout een significant deel van de 5 mm threshold.

**Klopt de toetsing?** Wordt onmogelijk te beoordelen zonder de meetmethode.

**Is dit criterium nodig?** Ja, maar het ontbreekt het cruciale stuk hoe de calibratie wordt uitgevoerd.

**Suggestie:** sectie 4.6 uitbreiden met een paragraaf "Measurement methodology" die specifies: instrument (rolmaat / laser / etc.), referentiepunten (hoe gemarkeerd), aantal metingen per punt, leesfout van het instrument.

---

### Criterium (c) — "Mapping error is below 5 mm on a reference rail"

**Getoetst?** ⚠ Ja, maar met een **ambiguïteit**.

In de validatietabel staan twee rijen die met "mapping error" te maken kunnen hebben:

| Metric | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Position error at end station | < 3 mm | < 2 mm | < 5 mm |
| Max position error at bend transition | 4.2 mm | 2.8 mm | 6.1 mm |

Welke is *de* mapping error van het criterium? Run 3 *passt* op end-station-error maar *faalt* op bend-transition-error.

**Klopt de toetsing?** Onduidelijk omdat het criterium ambigu is.

**Is dit criterium nodig?** Ja, maar het moet preciezer.

**Suggestie:** criterium herformuleren naar één van:
- "Mapping error < 5 mm at end station on rails up to 5 m" (zwakke claim, makkelijk te halen)
- "Mapping error < 5 mm at every reference point (stations + bend entries/exits) on rails up to 5 m" (sterke claim, Run 3 faalt)
- "Max mapping error < 5 mm bij elk reference point op rails ≤ 5 m, < 10 mm op langere rails" (zoals nu in 3.6(a) staat — *dit is al gespecificeerd in DV4's instrument, maar niet in DV2's*)

Merk op dat het instrument van DV4 in 3.6 (a) wél precies zegt: "positional error at every reference point is below 5 mm on rails up to 5 m and below 10 mm on longer rails". Dat is preciezer dan DV2(c). Op die manier gemeten faalt Run 3 dan toch (rail 6.45 m, ergo "longer rails", max bend error 6.1 mm < 10 mm → pass). Dit conflicteert met de tabel-uitkomst "Run 3 fail (> 5 mm criterion)".

**Conclusie:** DV2(c) en DV4(a) gebruiken verschillende drempels voor hetzelfde fenomeen. Inconsistent.

---

### Kritische vraag: wat meet "mapping error" eigenlijk?

De mapping omzet encoder-tellingen naar 3D positie. Een mapping error is dus: voorspelde 3D positie ≠ gemeten 3D positie. Maar fysiek zijn er meerdere foutbronnen:
1. Finite-precision van firmware pulse constants (al genoemd in 5.1).
2. Mechanische backlash (al genoemd in 5.1).
3. Arc-tracing approximatie (uitgesloten in 4.3 als <1 mm).
4. Calibration meetfout (onbekend, zie (b)).
5. Bend bend-radius variatie tussen fysieke rails.

De huidige "5 mm" claim onderscheidt niet welke bron de error veroorzaakt. Dat is in 5.1 honest erkend met "neither was instrumented separately". Maar dat betekent: **de mapping error is geen pure test van de mathematische mapping**; het is een test van mapping + mechanica + calibratie.

**Vraag:** is dat erg? Voor een toepassingsgerichte HBO-TI vraag waarschijnlijk niet — de gebruiker maakt het niet uit waar de error vandaan komt zolang de zichtbare positie correct is. Voor een zuivere "is de mapping wiskundig correct" claim wel — dan zou je een bench-test moeten doen met bekende encoder input en gemeten output op een rail-replica.

---

## DV3 — Mathematical Models for State Estimation

> **Vraag:** *"Which mathematical models for state estimation, interpolation, and rotation produce a stable live 3D representation from noisy telemetry?"*
>
> **Methode (3.4):** Formal mathematical analysis.

### Criterium (a) — "Every step of derivation in named equations traceable to cited sources"

**Getoetst?** ✓ Volledig. Sectie 4.4 heeft eq 11–21 met cites naar Kalman 1960, Welch & Bishop 1995, Catmull-Rom 1974, Kuipers 1999, Shoemake 1985, etc.

**Klopt de toetsing?** Ja.

**Is dit criterium nodig?** Ja — dit is wat een "formal analysis" betekent.

---

### Criterium (b) — "Predicted position at five fixed reference points deviates less than 5 mm from physically measured"

**Getoetst?** ⚠ Granulariteit-mismatch.

Het criterium specificeert **vijf reference points per run**: bottom station, elke bend entry, elke bend exit, top station. Run 1 (6 bends) heeft dus 1 + 6×2 + 1 = 14 reference points; Run 3 (8 bends) heeft 18.

De validatietabel rapporteert **alleen aggregaten**: end-station-error en max-bend-transition-error. De per-point afwijkingen zijn niet gerapporteerd.

**Klopt de toetsing?** Strikt genomen niet — het criterium eist per-point bewijs, de tabel geeft samenvattingen.

**Is dit criterium nodig?** Ja, want dit *is* hoe je een mathematisch model toetst — voorspelling vs werkelijkheid op meerdere punten. Maar de meting moet matchen.

**Suggestie:** óf per-point metingen toevoegen in een uitgebreide tabel of grafiek (sterk maar tijdsintensief), óf criterium herformuleren naar wat wel gerapporteerd is ("max position error at any reference point ≤ 5 mm, mean ≤ X mm"). Optie 2 is eerlijker over wat aangetoond is.

**Vraag:** is "5 reference points" de juiste set? Voor een 8-bend rail zijn er 18 zinvolle punten. Het criterium suggereert dat 5 voldoende is, maar dat is voor een rail met 1 bend (1 + 1×2 + 1 + 1 extra = 5). Voor langere rails klopt de specificatie niet. Heroverwegen.

---

### Criterium (c) — "Quaternion composition remains singularity-free across the full rail (no yaw or pitch discontinuity greater than 1° between consecutive frames)"

**Getoetst?** **Nee.** Hard gat. De validatietabel heeft geen rij voor inter-frame discontinuïteit. Dit criterium staat in 3.4 maar wordt nergens gemeten.

**Klopt de toetsing?** Niet van toepassing — er is geen meting.

**Is dit criterium nodig?** Goede vraag. **Argumenten voor:**
- Singulariteit was een van de drie motivaties in 2.1.4 voor quaternion-keuze (i.p.v. Euler).
- Als de quaternion wel zou falen, zou de chair zichtbaar "springen" en de visualisatie ondermijnen.

**Argumenten tegen:**
- Visuele inspectie tijdens de 3 calibration runs zou een grove sprong sowieso hebben opgemerkt; dat het *niet* genoemd is in de events ("no anomalies" voor Run 1 en 3, alleen kleine zaken voor Run 2) suggereert dat het stabiel was.
- Voor een formele mathematische derivatie ([Diebel 2006], [Kuipers 1999]) is singulariteitsvrijheid een eigenschap die volgt uit het quaternion-formalisme zelf. Het is geen empirische vraag of quaternions singulair worden; dat doen ze niet, per definitie. Wat wél empirisch kan falen is de *implementatie* (bv. normalisatie-drift), maar dat is een ander criterium.

**Suggestie:** kies één van:
1. **Schrappen** — singulariteitsvrijheid is theoretisch al gegarandeerd door quaternion-keuze; geen meting nodig.
2. **Herformuleren** naar "implementation maintains unit-norm quaternions across all rendered frames (max deviation < 1e-6)" — dat is wat je *kan* testen.
3. **Toevoegen aan validatietabel** als rij "Max inter-frame yaw discontinuity / pitch discontinuity" — alleen als je toch ergens meting wilt.

Mijn aanbeveling: **optie 1 of 2**. Optie 3 voegt rommel toe aan een rapport waar de claim toch al theoretisch verankerd is.

---

### Kritische vraag: testen we *het model* of *de implementatie*?

DV3 vraagt of wiskundige modellen een stabiele representatie produceren. In de validatie wordt dat indirect getoetst via positie-accuratesse (criterium b). Maar:
- Een correct model met buggy code geeft slechte positie-accuratesse → ten onrechte "model faalt".
- Een fout model met heroïsche post-hoc correctie kan goed scoren → ten onrechte "model klopt".

Met andere woorden: het experiment in 4.6 test de **gehele pipeline tegelijk**. Het isoleert niet of een fout in de Kalman, in de Catmull-Rom, in de quaternion, of in de encoder-mapping zit.

**Vraag:** is dat een probleem? Voor een HBO-TI artikel met implementatie-focus waarschijnlijk niet — als het werkt, werkt het. Voor een onderzoek dat claimt de modellen formeel te valideren wel — dan zou je elk model in isolatie moeten testen (bv. simulated input met bekende ruis, vergelijk Kalman-output met theoretische optimum).

Bestaande limitatie in 5.1 noemt dit gedeeltelijk ("tuning parameters determined empirically"). Maar het diepere punt — geen unit-tests per model — is niet genoemd.

---

## DV4 — Validation

> **Vraag:** *"How can the prototype be validated against practical scenarios, and what measurable criteria determine sufficient accuracy?"*
>
> **Methode (3.5):** Experiment with predefined pass/fail thresholds.

DV4 is een **meta-vraag**: het vraagt hoe je valideert, niet wat de pipeline doet. De "instrument (when done)" van 3.5 bevat dan ook geen criteria over de pipeline-werking maar over de **validation methodology** zelf.

### Criteria a–e in 3.5

(a) Positional error < 5 mm/10 mm. (b) Angle correction < 1°. (c) Kalman jitter 10× kleiner dan raw. (d) E2E latency < 100 ms. (e) Frame rate ≥ 55/50 fps.

Voor elk: getoetst in tabel, pass/fail gerapporteerd. ✓ Intern consistent.

**Maar:** deze criteria zijn deels duplicates van DV1–DV3's criteria, deels nieuwe. Concreet:

| 3.5 criterium | Equivalent in DV1–DV3 | Probleem |
|---|---|---|
| (a) positional error | DV2(c), DV3(b) | DV2(c) en 3.5(a) gebruiken verschillende thresholds |
| (b) angle correction | (niet eerder) | Nieuw — niet in DV3 criteria, hoort daar wel thuis |
| (c) Kalman jitter | DV3 deel | Niet in DV3 criteria, hoort daar wel thuis |
| (d) latency | DV1(b) | Zelfde mismatch (BT round trip vs end-to-end) |
| (e) frame rate | (niet eerder) | Nieuw — relateert aan DV1 maar staat daar niet |

**Vraag:** is dit een probleem? Ja, omdat:
1. **Duplicate criteria** (a, d) leiden tot inconsistentie als ze net iets anders gespecificeerd zijn.
2. **Nieuwe criteria** (b, c, e) horen logisch bij DV1 of DV3. Dat ze hier voor het eerst opduiken impliceert dat DV1 en DV3 hun eigen meetlatten missen.
3. **DV4 als losse vraag** voelt nu redundant — het is in essentie "we doen experimenten met de pass/fail criteria die we eigenlijk al in DV1–DV3 hadden moeten zetten".

**Suggestie radicaal:** DV4 schrappen, en de meetcriteria (a–e) verdelen over DV1, DV2, DV3 als hun respectievelijke "Instrument (when done)" criteria. Dan blijven er drie inhoudelijke DV's over, elk met goed gespecificeerde meetcriteria, en is sectie 4.6 een sub-onderdeel binnen elke DV-resultaten in plaats van een aparte vraag.

**Suggestie milder:** DV4 herformuleren als methodologische verantwoording binnen de Methods-sectie (een 3.0 "Validation strategy") in plaats van als zelfstandige DV.

**Tegenargument:** voor HBO-TI artikelformaat is een aparte validatievraag gebruikelijk. Schrappen zou kunnen afwijken van wat beoordelaars verwachten. Dit hangt af van wat de beoordelingsrubriek voorschrijft — als die expliciet een validatievraag eist, dan houden.

---

### Subcriterium 3.5(b) — "Angle correction error < 1° on average"

**Getoetst?** Ja — tabel rapporteert 0.3°/0.5°/0.4° avg.

**Klopt de toetsing?** **Nee — circulair.** De angle correction in 4.6 wordt berekend als:

```
δ = |θ_target/2| − |ψ_measured|
```

waar `ψ_measured` afkomstig is uit de compass tracker (gyroscoop-integratie). En de gerapporteerde "angle correction error" meet vermoedelijk hoe goed `δ` de werkelijke correctie benadert — maar dat wordt gedaan met... dezelfde compass tracker.

Dit is een **selfreferentiële meting**. Een onafhankelijke referentie zou nodig zijn — bijvoorbeeld een externe digitale waterpas of een laser-gebaseerde hoekmeter — om de werkelijke yaw vast te stellen.

**Suggestie:** in 4.6 specificeren hoe de "angle correction error" is bepaald. Als het inderdaad zelf-gemeten is, dat eerlijk noemen als limitatie in 5.3. Als er een externe referentie was, die noemen.

---

### Subcriterium 3.5(c) — "Kalman-filtered jitter at least 10× smaller than raw"

**Getoetst?** Ja — raw ±2-3 pulses, filtered <0.1 pulse, ratio >20×.

**Klopt de toetsing?** ⚠ Conditie niet gespecificeerd voor *filtered*.

Het criterium in 3.5 zegt niet onder welke conditie. De tabel zegt voor raw "(raw, stationary)". Voor filtered staat alleen "(after Kalman filter)" — niet of dat stationair of bewegend is.

Als beide stationair zijn meet je het filter-rust-gedrag, niet het filter-gedrag tijdens beweging. Een Kalman filter glad-strijken in rust is triviaal (omdat het tegen een constante predict-update). Tijdens beweging is het interessanter — daar moet het filter het noise dempen zonder de werkelijke signaalverandering te dempen.

**Suggestie:** specificeren onder welke conditie filtered jitter is gemeten. Als stationair, hetzelfde noemen. Als tijdens beweging, het residueel definiëren (filtered − verwachte trajectory).

---

### Cross-cutting: tablet frame rate confound (5.x)

In [main.tex:1130-1134](project/main.tex#L1130-L1134) staat al:

> *"On the tablet build, the shadow-quality setting was reduced automatically by the rendering layer to maintain frame rate under load; this is a configured behaviour, not a result of the validation runs, and is noted here only to identify a confounding factor in the tablet frame-rate numbers."*

Dat is een eerlijke disclaimer. Maar het maakt criterium 3.5(e) **deels nietig** voor tablet — de gemeten frame rate is niet de "ruwe" frame rate maar de frame rate-mét-automatische-degradatie. De 52 fps Run 3 fail zou met *vaste* shadow quality nog lager kunnen zijn. De pass voor Run 1 en 2 (55–60 fps) zegt mogelijk meer over de degradatie-logica dan over de pipeline.

**Vraag:** is dit erg? Voor de centrale vraag (kunnen we live 3D viz produceren?) niet — de auto-degradatie is onderdeel van het systeem. Voor een claim "de pipeline rendert intrinsiek op 55 fps" wel — dan moet de degradatie uit staan tijdens de test.

**Suggestie:** in 4.6 verduidelijken of de frame rate gemeten is mét of zonder automatische shadow-degradatie. Idealiter een extra rij in de tabel "Frame rate, shadow quality fixed at high" — als dat haalbaar is.

---

## Cross-cutting issues

### Steekproef N=3

Al genoemd in 5.3. Drie rails, drie configuraties. Niet generaliseerbaar.

**Kritische vraag:** is N=3 op zich genoeg voor een HBO-TI onderzoek? Voor *correctness-of-concept* (werkt het überhaupt?) ja. Voor *statistische generaliseerbaarheid* nee.

Het verslag claimt geen statistische generaliseerbaarheid, dus N=3 is acceptabel zolang je daar eerlijk over bent. De huidige formulering in 5.3 doet dat.

---

### Self-validation

Auteur definieert de criteria, voert de runs uit, scoort de pass/fail. **Geen onafhankelijke verificatie.**

Dit is normaal bij HBO-TI eindwerken en niet per se diskwalificerend. Maar in formele wetenschap zou je dit niet doen. Wat *wel* zou helpen:
- Pre-registreren van de criteria (technisch is dat gebeurd: ze staan in 3.x vóór de runs).
- Een tweede paar ogen op de meetuitkomsten (collega bij DeVi, stagebegeleider).
- Foto's / log-files openbaar maken als bewijs.

**Suggestie:** in 5.3 noemen dat self-validation een methodologische beperking is, eventueel met de mitigaties (pre-registratie van criteria) die wel zijn toegepast.

---

### Centrale vraag wordt niet volledig beantwoord

Centrale vraag: *"What data processing pipeline and mathematical models are required to transform live stairlift telemetry into a 3D visualization that enables **faster and more intuitive fault diagnosis compared to text-based error codes**?"*

Het vetgedrukte deel (laatste 15 woorden) wordt **nergens deductief getoetst**. Sectie 5.2 erkent dit: *"The broader claim ... is an inductive conclusion ... but not yet quantified through a controlled user study."*

**Vraag:** zou je de centrale vraag dan niet moeten herformuleren naar wat je *wel* kunt beantwoorden? Bijvoorbeeld:

> *"What data processing pipeline and mathematical models are required to transform live stairlift telemetry into a stable, accurate 3D visualization at >55 fps and <100 ms latency?"*

Die vraag is volledig deductief beantwoordbaar met de huidige validatie. De "intuïtieve / sneller dan tekstcodes" claim is dan niet meer onderdeel van de centrale vraag, maar wel onderdeel van de **motivatie** in de Introduction (wat het probleem is) en de **practical implications** (wat de bedoeling van het beroepsproduct is).

**Suggestie:** centrale vraag aanscherpen naar wat deductief getoetst kan worden, en de inductieve claim verplaatsen naar de motivatie / "practical relevance" paragraaf.

**Tegenargument:** misschien wil de stagebegeleider/beoordelaar juist die brede vraag. Check de rubriek of overleg.

---

### Engine selection (vooronderzoek, 2.2.4)

De MCA in tabel `tab:engine-mca` gebruikt ordinale scores (+/=/−). Geen schaal, geen meeteenheid. Voor C1 (configurabiliteit) en C2 (cross-platform export) is "+" plausibel (te checken in vendor docs); voor C3 (licence) is "+/=/−" bijna binair (licence is compatible of niet). Voor C4 (glTF import) idem.

**Vraag:** is een vier-engine MCA hier methodologisch sterk? Voor een vooronderzoek dat één keuze rechtvaardigt: ja. Voor een onderzoeksinstrument: nee — het schaalt en kwantificeert niets.

**Vraag:** hoort dit überhaupt thuis als vooronderzoek? Het is een *tooling choice* voor de implementatie van de renderer-laag (één van vijf lagen). Sommige stagebegeleiders zien dit als beroepsproduct-keuze, niet onderzoekkeuze. Het hangt opnieuw af van de rubriek.

**Suggestie:** check met begeleider of de engine-MCA hier past, of dat het beter naar appendix/beroepsproduct verhuist.

---

### Bend-transition error niet ontleed

In 5.1 wordt eerlijk gezegd:

> *"The more plausible dominant sources are the finite precision of the firmware pulse-cost constants and mechanical backlash at bend transitions; neither was instrumented separately during these calibration runs."*

Dit is een gat dat al onderkend is. De aanbeveling in 5.4 ("Bend-transition error decomposition") adresseert het. Geen nieuwe actie nodig — maar het is een belangrijk feit om in gedachten te houden.

---

## Wat zou je doen als je het opnieuw mocht doen?

Eerlijke checklist voor jezelf:

1. **Meetinstrumenten vooraf specificeren** — vooral hoe je *physical position* meet, en welke fout je daarvan accepteert. (Adresseert DV2(b), DV3(b), 3.5(a))
2. **Onafhankelijke referentie voor hoeken** — externe digitale waterpas of laser-hoekmeter. (Adresseert 3.5(b) circulariteit)
3. **Instrument-criteria per DV uitsluitend over die DV** — geen criteria die in DV4 horen ook in DV1–DV3 zetten. (Adresseert DV4-redundantie)
4. **Pre-registreren met begeleider** — vraag een vinkje op de criteria vóór de runs. (Adresseert self-validation)
5. **Unit-test per wiskundig model** — Kalman op simulated input met bekende ruis, voordat je het op echte data laat los. (Adresseert "test we model of implementatie")
6. **Frame rate met vaste settings** — degradatie-logica uit tijdens benchmark. (Adresseert tablet frame rate confound)
7. **Adversarial test voor byte corruption** — als criterium DV1(d) blijft, doe dan fault injection. (Adresseert DV1(d))

Dit is allemaal achteraf — voor het huidige verslag is de vraag: welke van deze kun je *nu nog* fixen, en welke moet je *eerlijk benoemen* als limitatie?

---

## Prioriteit-matrix

Wat eerst aanpakken, op volgorde van impact op rapport-kwaliteit:

| Prioriteit | Item | Type fix | Geschatte tijd |
|---|---|---|---|
| 🔴 Hoog | DV2(b) meetmethode "physical position" | Tekstaanvulling in 4.6 | 30 min |
| 🔴 Hoog | DV3(c) quaternion-singulariteit | Schrappen of herformuleren | 15 min |
| 🔴 Hoog | DV1(b) BT round trip vs end-to-end | Criterium of meting matchen | 20 min |
| 🟠 Middel | 3.5(b) circulariteit angle correction | Limitatie in 5.3 noemen | 15 min |
| 🟠 Middel | DV1(a) single responsibility | Verplaatsen naar motivering | 10 min |
| 🟠 Middel | DV2(c) ambiguïteit end station vs bend | Criterium preciezer | 10 min |
| 🟠 Middel | DV3(b) per-point granulariteit | Criterium aanpassen of metingen toevoegen | 15–60 min |
| 🟡 Laag | DV1(c) 20Hz poller niet gemeten | Rij toevoegen of criterium schrappen | 10 min |
| 🟡 Laag | DV1(d) byte corruption | Verzwakken naar wat aangetoond is | 10 min |
| 🟡 Laag | 3.5(c) Kalman jitter conditie | Tekst specificeren | 5 min |
| 🟡 Laag | DV4-redundantie criteria | Heroverwegen structuur | 30 min |
| 🟡 Laag | Self-validation als limitatie | Toevoegen aan 5.3 | 5 min |
| 🟢 Optioneel | Centrale vraag aanscherpen | Inductieve claim eruit | 20 min |
| 🟢 Optioneel | Frame rate confound expliciet | Tekst in 4.6 | 10 min |

Totaal voor alle hoog + middel items: ongeveer 2.5–3 uur werk.

---

## Slotopmerking

Het verslag heeft een **sterke kern**: DV2 (encoder mapping) en DV3 (math models) zijn formeel goed opgezet, met cites en derivaties. De validatie in 4.6 is qua *opzet* gestructureerd (pre-defined thresholds, eerlijk over fails). De grootste verbeteringen zitten in **alignment tussen criterium en meting** (mismatches in DV1(b), DV2(c), DV3(b)) en **eerlijkheid over wat niet gemeten is** (DV1(c), DV1(d), DV3(c)).

De **niet-gemeten** criteria zijn ironisch genoeg makkelijk op te lossen door **het criterium af te zwakken** naar wat je wel hebt aangetoond — niet door extra metingen toe te voegen. Voor een HBO-TI verslag is "eerlijk over wat aangetoond is" sterker dan "ambitieuze criteria die half getoetst zijn".
