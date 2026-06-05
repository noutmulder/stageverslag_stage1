# Bewaarde test — DV3 smoothness, continue rit op de 5,4 m-rail (2026-06-05)

**Logbestand:** `2026-06-05_ttrac_5428mm_dv3_continu.log` (bron: tablet Samsung SM-X230, serial R5GYA013CZZ;
session_2026-06-05_13-32-14, ~4 min).
**Rail:** dezelfde 5428,7 mm-rail als `2026-06-05_ttrac_5428mm_resultaat.md` (zie die voor rail-opbouw/QR).
**Doel:** DV3 (smoothness, velocity-gebaseerd) op de **doelhardware (tablet)** en een **lange rail** — de
06-02-DV3-pass was desktop. Aparte **continue** rit (geen markers/stops), zodat stops niet als pieken meetellen.

## Condities
- Frame-log: `[FRAME_LOG] START t=31006`, **13.596 `[FRAME]`-regels**, **0 markers** (geen stops).
- Gereden **B→T→B**; keerpunt op t=95,5 s, top **98,0% rail** (traject 1,9 → 98,0% ≈ vrijwel volledig).
- Render: **~53 fps** (frame-interval mediaan 19 ms), één eenmalige hapering van 153 ms (t=230,8 s) die
  de dead-reckoning vloeiend opving (gaf géén positiepiek).

## Resultaat (DV3-maat: pieken > 5× mediane |v| per as)
Per been geanalyseerd (keerpunt ±1,5 s uitgesneden), want over één B→T→B-venster drukt het keerpunt de
mediane snelheid en overdrijft het de relatieve pieken.

| Been | traction | spindle | swivel | %bewegend (traction) |
|---|---|---|---|---|
| **heen B→T** (94 s) | 2 (0,04%) | 1 (0,04%) | 3 (0,21%) | 95% |
| terug T→B (156 s) | 3 (0,06%) | 3 (0,12%) | 17 (1,21%) | 60% |
| (heel venster) | 6 (0,06%) | 9 (0,17%) | 22 (0,78%) | 73% |

**Leidend = de schone heen-rit (B→T):** traction **0,04%**, spindle 0,04%, swivel 0,21% pieken.
jerk p99 traction 0,009 (vergelijkbaar met 06-02: 0,007).

## Verdict
**Geen staircase.** De display volgt vloeiend op de doelhardware (tablet, ~53 fps) over vrijwel de hele
5,4 m-rail. De resterende pieken zijn **geïsoleerd en mild** (5–7,6× drempel; 6 stuks in 250 s, alle bij
normale frame-intervallen — geen frame-cadans-patroon zoals staircase dat zou geven), niet de letterlijke
nul van de desktop-rit (06-02: 0/0/1).

## Kanttekeningen
- **Letterlijk criterium niet gehaald.** `fase1_meetontwerp.md` stelt "0 pieken > 5× mediaan". De heen-rit
  haalt 2–3, geen 0. Inhoudelijk is er geen staircase, maar de letterlijke nul wordt niet gehaald.
  → Zie open punt over criterium-formulering (vooraf geregistreerd; niet zomaar post-hoc verzachten).
- **Terug-rit was minder continu** (60% bewegend = ~40% vrijwel stilstaand; 156 s vs. 94 s heen). Dat drukt
  de mediaan en blaast de relatieve pieken op — vooral swivel (kleine, ruisgevoelige steekproef: beweegt enkel
  bij de 2 horizontale bochten). Niet representatief voor de smoothness; de heen-rit is de schone meting.
- **~53 fps op de tablet** (vs. 60 fps desktop 06-02). Render-gezondheid op de doelhardware apart te benoemen.

## DV1 (meegelogd)
n=2293; mean 85 ms, P95 111 ms, P99 129 ms, max 673 ms (één uitschieter). Binnen drempel (P95<150/P99<250).
