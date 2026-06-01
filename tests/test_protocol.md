# Stage Report – Test Protocol

Dit protocol hoort bij de instrumentatie op branch `feat/stage-report-logging`. Doel: echte meetwaarden verzamelen voor de validatietabel in het stageverslag (sectie 4.6 "Validation Results").

## 0. Waar komen de logs terecht?

`CalibLog` (autoload) schrijft naar `user://calibration_logs/calib_<timestamp>_<label>.log`.

- Desktop (Linux): `~/.local/share/godot/app_userdata/UP-Studio-gdscript/calibration_logs/`
- Android tablet: `/storage/emulated/0/Android/data/<package>/files/calibration_logs/`
  - Ophalen via: `adb pull /sdcard/Android/data/<package>/files/calibration_logs/ ./logs/`

Elke regel is gestructureerd: `YYYY-MM-DD HH:MM:SS.mmm [TAG] key=value ...`. Relevante tags:

| Tag         | Inhoud                                                   |
| ----------- | -------------------------------------------------------- |
| `[METRIC]`  | Losse meetwaarde (rail_length_mm, end_station_error_mm)  |
| `[LATENCY]` | BT round-trip per bericht (msg_id, elapsed_ms)           |
| `[FPS]`     | Render-framerate sample (1Hz)                            |
| `[JITTER]`  | Stationaire ruis (raw + Kalman)                          |
| `[ANGLE]`   | Hoekcorrectie bij horizontale bocht                      |
| `[BEND]`    | Positiefout bij bocht-overgang                           |
| `[COMPASS]` | Compass-reset + reden                                    |
| `[EVENT]`   | BT connect/disconnect, split-bend, latency-spikes (>150ms) |
| `[SUMMARY]` | Aggregaten geschreven aan het einde van de sessie        |

Aan het einde van elke run schrijft `CalibLog` een `[SUMMARY]`-blok met alle aggregaten (gemiddelden, min/max, counts). **Voor de verslag-tabel lees je gewoon de `[SUMMARY]`-regels.**

## 1. Welke metrics worden automatisch gelogd?

Per calibratierun schrijft de code het volgende weg zonder extra handelingen:

| Metric in verslag                          | Komt uit                                     |
| ------------------------------------------ | -------------------------------------------- |
| Rail length (mm)                           | `rail_info rail_length_mm=...`               |
| Total encoder range (pulses)               | `rail_info total_encoder_range=...`          |
| Position error at end station (mm)         | `end_station_error_mm=...` (in SUMMARY)      |
| Max position error at bend transition (mm) | `bend_error_mm_max_abs=...` (in SUMMARY)     |
| Angle correction error avg/max (°)         | `angle_correction_* max_abs_deg=...`         |
| Encoder jitter (raw, stationary)           | `raw_jitter_pulses_stddev=...`               |
| Encoder jitter (after Kalman)              | `kalman_jitter_pulses_stddev=...`            |
| Display update latency (BT) avg/min/max    | `bt_latency_ms_avg/min/max=...`              |
| Render frame rate avg/min/max              | `fps_avg=... min=... max=...`                |
| Latency spikes > 150 ms count              | `spikes_over_150ms=...`                      |
| Compass re-triggers count                  | `compass_resets=...`                         |
| BT disconnects count + reconnect time      | `bt_disconnects=...` + `bt_reconnect_ms=...` events |

## 2. Tests die je op het apparaat (tablet) moet uitvoeren

Voer **drie** volledige calibratieruns uit op **drie verschillende rail-configuraties**, zodat de verslag-tabel kolommen "Run 1 / Run 2 / Run 3" ingevuld kunnen worden. Bij voorkeur:

- **Run 1**: een middellange rail met ≥ 4 horizontale bochten
- **Run 2**: een korte rail (≤ 3.5 m) met weinig bochten
- **Run 3**: een lange rail (≥ 6 m) met 6+ bochten (stress-test)

### 2.1 Voorbereiding (elke run)

1. Zet de tablet in het montagekoffer, sluit ADB via USB aan of onthoud dat je de logfolder later met de bestandsmanager moet kopiëren.
2. Verwijder oude logbestanden (optioneel, maakt het makkelijker terug te vinden): `adb shell "rm -f /sdcard/Android/data/<pkg>/files/calibration_logs/*.log"`.
3. Start de app, ga door de stappen tot de calibratierun-stap.
4. Zorg dat de lift BT-verbonden is (traction + spindle waardes zijn zichtbaar in het UI).

### 2.2 Stationaire test (eerste ~10 seconden van elke run)

**Dit is belangrijk voor de jitter-metric.** De instrumentatie pakt automatisch de eerste 40 encoder-samples (≈ 10 s bij 250 ms polling) op zolang de lift niet beweegt, berekent de stddev en schrijft die weg als `raw_jitter_pulses_stddev`. Hetzelfde gebeurt voor de Kalman-gefilterde positie (`kalman_jitter_pulses_stddev`).

**Dus:** na het indrukken van "Start calibration" — **houd de joystick 10 seconden NIET ingedrukt**. Pas daarna begin je met rijden. Als je direct begint, valt het stationaire sample-venster te klein en wordt er geen jitter-metric weggeschreven.

### 2.3 Calibratierun zelf

1. Druk op "Start calibration".
2. Wacht 10 seconden (stationaire meting, zie 2.2).
3. Rijd de lift van onder naar boven (of van boven naar onder), met ingedrukte joystick.
4. Laat de firmware bij elke horizontale bocht automatisch stoppen (STOPPED_ON_STATION). De instrumentatie logt per bocht: target/measured/correction-hoek en bocht-overgangsfout.
5. Laat de run volledig uitlopen tot bij het eindstation (MOVE_TO_LAST → confirm).
6. Bij afronding schrijft `CalibLog` automatisch de SUMMARY en sluit het logbestand.

### 2.4 Stress- en randgevallen (eenmalig, niet per run)

Deze zijn **optioneel** maar geven extra logregels die in het verslag tussen de Run-kolommen (of in de "logged events" tekst) gebruikt kunnen worden:

| Scenario                     | Hoe uitvoeren                                                        | Wat verschijnt in log                |
| ---------------------------- | -------------------------------------------------------------------- | ------------------------------------ |
| BT-disconnect + auto-reconnect | Schakel even de BT-dongle uit tijdens de run (of loop 5 m weg)       | `[EVENT] bt_disconnect` + `bt_reconnect reconnect_ms=...` |
| Latency spike              | Zet de tablet onder zware CPU-load (open andere app + loop achtergrond) | `[EVENT] latency_spike msg_id=... elapsed_ms=...` |
| Manual compass re-trigger  | Druk op de compass-reset-knop in het UI mid-run                      | Verschijnt ook als `[COMPASS] reset reason=...` |
| Split-bend                 | Voer een rail uit met twee horizontale bochten van dezelfde richting < 250 mm uit elkaar | `[EVENT] split_bend_armed ...` |

## 3. Samen het verslag invullen

Na elke run heb je één `.log`-bestand. Trek de SUMMARY-regels eruit:

```bash
grep "\[SUMMARY\]" calib_20260417_143012_calibration_run.log
```

Geeft ongeveer:

```
[SUMMARY] duration_s=312.4
[SUMMARY] rail_length_mm=4820 total_encoder_range=16210
[SUMMARY] raw_jitter_pulses_stddev=2.140
[SUMMARY] kalman_jitter_pulses_stddev=0.087
[SUMMARY] bt_latency_ms_avg=38.2 min=21 max=174 samples=3420 spikes_over_150ms=2
[SUMMARY] fps_avg=57.3 min=51.0 max=60.0 samples=312
[SUMMARY] angle_correction_count=6 avg_abs_deg=0.41 max_abs_deg=0.92
[SUMMARY] bend_error_mm_max_abs=4.21 count=6
[SUMMARY] end_station_error_mm=2.81
[SUMMARY] compass_resets=11 bt_disconnects=0
```

Deze getallen plug je 1:1 in Tabel "Validation measurements" in `sections` (of direct in `main.tex` rond regel 1222–1238).

## 4. Aandachtspunten

- **Frame rate op desktop** (Run X, desktop-kolom) meet je door de calibratierun op de desktop-build te draaien — tegen een TCP-lift of demo-mock. Hergebruik hetzelfde protocol, alleen `platform=linux` verschijnt in de `[FPS]` regels.
- Als je de testrun NIET volledig wilt afmaken, stop via de app en de SUMMARY wordt alsnog geschreven (in `stop_calibration()`).
- Laat ADB logcat óók meelopen (`adb logcat -s godot`) als extra backup — alle `CalibLog` output gaat ook naar stdout.
- Het logbestand wordt na elke regel geflusht, dus bij een crash verlies je alleen de allerlaatste regel.
