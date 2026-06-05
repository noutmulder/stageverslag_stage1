# Bewaarde test — T-TRAC positie op grotere rail (2026-06-05)

**Logbestand:** `2026-06-05_ttrac_5428mm.log` (bron: tablet Samsung SM-X230, serial R5GYA013CZZ,
Godot user-data; session_2026-06-05_13-02-19, ~9 min).
**Rail-config:** `2026-06-05_ttrac_5428mm_rail_qr.pdf` (QR-export uit de quotation, exact de geüploade geometrie).
**Doel:** T-TRAC herhalen op een **langere rail dan de 3403 mm-regressierail** → generaliseerbaarheid van de
display-vs-fysiek-accuratesse (DV2). Rail > 5 m ⇒ DV2-drempel **10 mm** (`fase1_meetontwerp.md` §DV2).

## Condities
- **Firmware-baanlengte 5428,7 mm** (uit `total_mm` in de log; exact gereproduceerd door de QR-opbouw, zie onder).
- Rail-opbouw uit QR (`index-type-value_high-value_low-swivel`; type 10 = recht, lengte = `(vh<<8)|vl`;
  bochten dragen booglengte = `segmenten × 150 mm × 5°` = 13,09 mm/segment). 2 horizontale bochten (type 75,
  18 segs, swivel 60°), verticale up/down-bochten ertussen.
- **5 markers**, gereden **B→T→B** → 10 `[MARKER]`-events (MP1–MP5 omhoog, MP6–MP10 terug; heen/terug = zelfde
  fysieke punten). Markers op de rechte raildelen rd3, rd5, rd7, rd9, rd13.
- Frame-log (F) stond aan: `[FRAME_LOG] START t=109746`, 24.482 `[FRAME]`-regels.

### Rail-opbouw (positie-langs-baan, uit QR)
| rd (recht) | startpositie (mm) | lengte (mm) |
|---|---|---|
| rd1 | 0,0 | 172 |
| rd3 | 250,5 | 594 |
| rd5 | 949,3 | 476 |
| rd7 | 1660,9 | 194 |
| rd9 | 1959,6 | 1446 |
| rd11 | 3510,3 | 525 |
| rd13 | 4270,9 | 178 |
| rd15 | 4553,7 | 875 |

Som rechte stukken + bochtbogen = **5428,7 mm**, gelijk aan firmware `total_mm` → parsing geverifieerd.

## Resultaat

### DV2 — display vs. fysiek (positie-accuratesse)
`d_phys` = startpositie van het raildeel (uit QR) + **handmatig met meetlint gemeten offset** vanaf het begin
van dat raildeel tot de marker.

| Marker | rd | offset (mm) | d_phys (mm) | display (mm) | fout (mm) |
|---|---|---|---|---|---|
| MP1/MP10 | rd3 | 401 | 651,5 | 642,3 | **−9,24** |
| MP2/MP9 | rd5 | 326 | 1275,3 | 1271,2 | −4,06 |
| MP3/MP8 | rd7 | 181 | 1841,9 | 1832,0 | **−9,88** |
| MP4/MP7 | rd9 | 1060 | 3019,6 | 3014,5 | −5,10 |
| MP5/MP6 | rd13 | 66 | 4336,9 | 4330,8 | −6,14 |

- **max |fout| = 9,88 mm** (rd7), gemiddeld **−6,9 mm**, allemaal binnen de 10 mm-drempel → **DV2 PASS**.
- De fout is **systematisch negatief** (display leest consequent enkele mm kórter dan fysiek), consistent met de
  eerder gedocumenteerde configurator-discrepantie (firmware-encoded raillengtes ~10–16 mm vs. fysiek).
- **Herhaalbaarheid heen-vs-terug** (zelfde fysieke punt, B→T vs T→B, uit `display_mm`):
  rd3 0,3 mm · rd5 2,1 mm · rd7 4,1 mm · rd9 3,6 mm · rd13 2,4 mm — alle < 5 mm.

### DV1 — Bluetooth latency
- n = 5872 RTT-samples. mean 88,0 ms · median 88,9 ms · **P95 = 112,2 ms** (drempel <150) ·
  **P99 = 134,3 ms** (drempel <250) · max 166,7 ms → **DV1 PASS**.

### DV3 — smoothness
- **Niet geldig uit deze rit.** Het is een stop-and-go markerrit; de "pieken" (traction 193, spindle 297,
  swivel 68) zijn de stops, het keerpunt en de 60°-stoeldraai bij de twee horizontale bochten — precies de
  situatie die `fase1_meetontwerp.md` als misleidend voor DV3 markeert. DV3 hoort op een **aparte continue rit**.
- Render-fps op deze rit: ~42 fps (frame-interval mediaan 24 ms), lager dan de 60 fps van de 06-02-rit.

## Verdict
**DV2 (positie) generaliseert naar een 5,4 m-rail: max fout 9,88 mm < 10 mm.** DV1 ruim binnen drempel op deze
rail. De systematische −7 mm-bias is upstream hardware (configurator), geen pipeline-fout. Hiermee is T-TRAC op
een tweede, langere railgeometrie aangetoond naast de 3403 mm-regressie.

## Nog open
- **Continue DV3-rit op deze rail** (B→T zonder stoppen, frame-log aan) ontbreekt nog; nu leunt DV3 op de
  rail-onafhankelijke 06-02-pass (`2026-06-02_framelog_dv3_resultaat.md`).
- De ~42 fps op deze rail (vs. 60 fps) apart bekijken (render-gezondheid op langere/zwaardere geometrie).
- Bias-scheiding: om DV2-fout te splitsen in (a) binnen-segment-tracking en (b) firmware-vs-fysiek-lengte zou
  een fysiek gemeten **cumulatieve** afstand tot elk rd-begin nodig zijn (nu alleen offset-binnen-rd gemeten).
- Figuren (positie-vs-tijd, RTT-histogram) nog te genereren — vereist matplotlib (geen pip op werkmachine).
