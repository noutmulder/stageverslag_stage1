# Project-context / handover — stageverslag periode 1 & 2

> Dit bestand vat de stand van zaken samen zodat een nieuwe chat (of een andere machine)
> meteen begrijpt waar we staan. Laatste update: 2026-06-04.

## Wat dit project is
HBO-TI stageverslag bij **DeVi Comfort**. Onderzoeksartikel over een **live 3D-telemetrie-
visualisatie** ("ghost chair") voor **storingsdiagnose van trapliften**: ruwe puls-encoder-
telemetrie over Bluetooth → stabiele, accurate live 3D-weergave. Beoordeeld tegen het Inholland
**artikel-format v.2223**.

**Docent-review (onafhankelijk, neutraal) gaf 7,6 (goed); doel ~8.** De belangrijkste
verbeterpunten zijn uitgewerkt in `stappenplan.md`.

## Twee repo's
- **Verslag-repo (deze):** GitHub `noutmulder/stageverslag_stage1`, branch `main`.
  Bron van het artikel = **`project/main.tex`**.
- **Code-repo (beroepsproduct):** Godot-project **GD-UP-Studio**, branch `fix/live-telem`.
  Op deze machine: `/home/nmu/MergeIPC/GD-UP-Studio` (pad kan op een andere machine anders zijn).
  Relevante GDScript:
  - `assets/code/ipc/ipc_lift_controller.gd` — per-as Kalman (constant-velocity) + dead-reckoning
    + alle validatie-logging (`[CSV]`, `[FRAME]`, `[MARKER]`, baseline).
  - `assets/code/ipc/ipc_test_controls.gd` — test-UI (MARK, baseline, frame-log, kompas-nul).
  - `assets/code/ipc/ipc_encoder_mapper.gd` — encoder → genormaliseerde railpositie (piecewise).
  - `assets/code/ipc/test_logger.gd` — schrijft de sessielogs (autoload `TestLogger`).
  - `assets/code/ipc/net/lift/compass_tracker.gd` — gyro-yaw (alleen op tablet, niet desktop).

## Belangrijke bestanden in deze repo
- `project/main.tex` — het artikel.
- `testplan.md` / `testplan.tex` / `testplan.pdf` — veldklaar testplan (wat te meten, hoe).
- `fase1_meetontwerp.md` — pre-registratie meetontwerp: DV-criteria, methoden, drempels.
- `stappenplan.md` — verbeterplan. **Fase 0** (bureauwerk) ✅, **Fase 1** (meetontwerp) ✅ ontworpen,
  **Fase 2** (meetcampagne) loopt, **Fase 3** (verslag herschrijven met data) nog te doen.
- `analyse/analyse_logs.py` — `python3 analyse/analyse_logs.py <session.log> [outdir]` →
  figuren (positie-vs-tijd "Kalman vs meting", RTT-histogram) + samenvatting (DV1/DV3 + markertabel).
- `validatie_logs/` — **bewaarde testresultaten** (ruwe logs + `_resultaat.md` + figuren).
  ⚠️ **NIET aanraken/verwijderen.**
- Historische werknotities (behouden, niet leidend): `methodische_review.md`, `vooruitgang_nout.md`,
  `actiepunten.md`, `verbeterpunten.md`, `verslag_aanpassingen.md` (bevat 05-29 meetdata),
  `artikelstructuur_richtlijnen.md`.

## De validatiecriteria (pre-registered, zie fase1_meetontwerp.md)
- **DV1 (live/latency):** Bluetooth RTT P95 < 150 ms, P99 < 250 ms.
- **DV2 (accuraat/positie):** **display-vs-fysiek** < 5 mm (rail ≤ 5 m) / < 10 mm (langer).
  Secundair: display-vs-firmware (pipeline-isolatie).
- **DV3 (stabiel/smoothness):** snelheids-gebaseerd — **0 snelheidspieken > 5× mediaan** tijdens
  continue beweging (geen staircase). NIET de rauwe per-frame-stap gebruiken (schaalt met fps).
- **Hoeken:** spindel ~1–2°; **swivel ~±3,5°** (= inherente encoder↔fysiek-tolerantie, hardware).

## Status van de tests
| Test | Status | Resultaat |
|---|---|---|
| T-SPIN (spindel-zithoek) | ✅ PASS | max 1,05° vs waterpas (`validatie_logs/2026-06-04_tspin...`) |
| T-SWIV (swivel-draaihoek) | ✅ PASS | max 2,83° vs gyro, binnen ±3,5° (`..._tswiv...`) |
| T-TRAC (positie) | ✅ regressie op rail 3403 mm | pipeline-error 0,0 mm; gereproduceerd |
| DV1 (RTT) | ✅ | ~87 ms mean op tablet |
| DV3 (smoothness) | ✅ | continue rit 06-02: 0 pieken, 60 fps |
| **T-TRAC op grotere rail** | ⏳ **NOG TE DOEN** | generaliseerbaarheid-stap (meerdere rails) |

Spindel & swivel zijn **rail-onafhankelijk** (stoel-mapping) → één keer is genoeg, niet per rail.
**T-TRAC herhaal je wél per rail** (railgeometrie verschilt).

## Wat NU nog moet: T-TRAC op een grotere traplift
1. Verbind + **laad de rail**. **Nieuw logfile** (knop). Noteer rail-ID + config.
2. Markers over **alle segmenttypes**, met meetlint `d_phys` per marker.
   ⚠️ **Gebruik een dun streepje als referentie, niet brede tape** (tapebreedte ~15 mm = onzekerheid).
3. Rij **B→T en T→B**; bij elke marker uitsettelen → **MARK** (Spatie). MP-nummers lopen door →
   noteer **MP# ↔ marker** in logboek.
4. **Frame-log (F) aan** tijdens de rit → DV3-figuur op deze rail.
5. Rail > 5 m → drempel = **10 mm**.
6. Daarna: `adb pull …/validation_logs/` → `analyse/analyse_logs.py` → resultaat opslaan in
   `validatie_logs/` + committen.

## Belangrijke inzichten / valkuilen (hard geleerd)
- **Spindel: vergelijk waterpas met `spindle_kf` (lookup), NIET de gerenderde hoek.** De render toont
  bewust `0,85 × spindle_kf` op een vlak stuk (de `SPINDLE_GEOMETRY_WEIGHT = 0.15`-blend). Tegen de
  ghost meten geeft een schijn-fout van ~15%.
- **Swivel: tegengestelde tekenconventie** tussen kompas en encoder (oriëntatie-afhankelijk) +
  **gyro-drift** (~2–3° over een sweep). `compass_yaw` wordt automatisch in `[MARKER]` gelogd.
- **DV2 bij settled markers: `display_mm` == `fw_mm` (pipeline-error 0) is tautologisch.** De échte
  accuratesse = display vs **fysiek** (`d_phys`), die je handmatig met de tape meet.
- **Configurator-discrepantie:** firmware-encoded raillengtes wijken ~10–16 mm af van fysiek
  (rd1 +16/rd5 −9/rd11 −10 mm) — upstream hardware, geen pipeline-fout; apart als limitation gemeld.
- **DV3 op een stop-and-go marker-rit is misleidend** (stops/bochten tellen als "pieken"). Meet DV3
  op een **aparte continue rit**.
- **`meas_pos`-veld** is aan `[CSV]` toegevoegd zodat de positie-figuur de meting in dezelfde
  (piecewise) eenheid als de Kalman-lijn toont (lineair normaliseren wijkt af op bochten).

## Validatierail (vorige keer, "regressie")
3403 mm firmware-encoded, 11 raildelen, 1 horizontale bocht (90° links). Markers op rd1, rd3, rd11
(zie `verslag_aanpassingen.md` §11 voor de 05-29 data).

## Build/install workflow (deze machine)
```
cd /home/nmu/MergeIPC/GD-UP-Studio
/home/nmu/godot-web/Godot_v4.6.1-stable_linux.x86_64 --headless --path . \
  --export-debug "Android" export/apk/UP-Studio-dev0.0.8.apk
adb -s <serial> install -r export/apk/UP-Studio-dev0.0.8.apk
```
Test-tablets (Samsung SM-X230): serials wisselen (o.a. R5GYA013CZZ, R5GYC0XNEKH). Debug-APK is
adb-installeerbaar; bij signature-mismatch eerst `adb uninstall com.example.upstudio`.
Kompas/gyro werkt **alleen op de tablet** (desktop = "geen sensor").

## Werkafspraken
- Git-commits: zonder Co-Authored-By/zelf-attributie (voorkeur auteur).
- `verbeterpunten.md` niet gebruiken bij het beoordelen van het verslag (auteur wil onafhankelijke feedback).
- Bij codewijzigingen die gedrag beschrijven: altijd tegen de werkelijke GDScript verifiëren.
