# Testrapport — Calibratierun validatiemetingen

**Datum:** 2026-04-17
**Apparaat:** Samsung Galaxy Tab A8 (SM-X230), Android
**APK:** `UP-Studio-staging.apk` (MD5 `8b67d3aad229166451df5098df88df62`), gebouwd uit branch `feat/stage-report-logging`
**Instrumentatie:** `CalibLog` autoload, output in `/data/data/com.example.upstudiogdscript/files/calibration_logs/`
**Log-bestanden:** drie `calib_*.log` in `~/stageverslag_periode_1_2_26/logs/`

## 1. Wat er getest is

Twee calibratieruns op twee verschillende stairlift-installaties. Een derde logbestand (12:10) is een run die voortijdig is afgebroken en niet in de analyse zit.

| Log | Tijd | Lift | Rail | Status |
| --- | --- | --- | ---: | --- |
| `calib_20260417_121016` | 12:10 | (lift 1) | — | afgebroken, geen SUMMARY |
| `calib_20260417_121319` | 12:13 | lift 1 | 3 365 mm / 9 parts | voltooid via stop |
| `calib_20260417_122106` | 12:21 | lift 2 | 5 437 mm / 15 parts | voltooid via stop |

Geen van beide runs is afgesloten met de officiële "confirm-end-station"-knop — de sessies zijn via `stop_calibration()` beëindigd voordat MOVE_TO_LAST bereikt werd.

## 2. Resultaten per run

### 2.1 Samenvatting

| Metric | Run 2 (lift 1) | Run 3 (lift 2) | Criterium verslag |
| --- | ---: | ---: | --- |
| Rail length | 3 365 mm | 5 437 mm | — |
| Encoder range | 11 312 pulses | 18 276 pulses | — |
| Rail parts | 9 | 15 | — |
| Duration | 174,6 s | 222,6 s | — |
| **FPS (tablet)** avg / min / max | 36,8 / 34 / 38 | 36,8 / 35 / 39 | ≥ 55 fps (**FAIL**) |
| BT latency avg | 84,4 ms | 80,4 ms | ≤ 100 ms (pass) |
| BT latency max | 191 ms | 193 ms | — |
| Latency spikes > 150 ms | 6 | 2 | — |
| **BT timeouts > 500 ms** | 58 | 86 | niet in verslag |
| Angle correction count | 2 | 4 | — |
| Angle correction avg abs | 0,82° | 0,34° | ≤ 1° (pass) |
| Angle correction max abs | 1,38° | 0,87° | ≤ 1° (run 2 **FAIL**) |
| Compass resets | 7 | 10 | — |
| BT disconnects | 0 | 0 | — |
| Raw encoder jitter (stationary) | 0,000 (11 samples) | 0,000 (37 samples) | — |
| Kalman jitter | **niet gelogd** | **niet gelogd** | — |
| End-station position error | **niet gelogd** | **niet gelogd** | ≤ 5 mm (niet gemeten) |

### 2.2 Detail — Run 2 (lift 1, 3 365 mm, 9 parts)

**Compass resets:**

```
12:13:21  first_bend_lookahead_from_bottom  enc=10730
12:13:31  midpoint_straight                 enc=9109
12:14:22  vertical_entry                    enc=6815
12:15:01  horizontal_exit                   enc=5674
12:15:03  vertical_entry                    enc=5521
12:15:30  midpoint_straight                 enc=3064
12:15:58  vertical_entry                    enc=1052
```

**Angle corrections (2 horizontale bochten, beide op part_idx=5):**

```
12:14:44  target=-45,00°  measured=-43,62°  correction=-1,38°
12:14:50  target=-45,00°  measured=-45,26°  correction= 0,26°
```

### 2.3 Detail — Run 3 (lift 2, 5 437 mm, 15 parts)

**Compass resets:** 10 (alle vier categorieën aanwezig: first-bend lookahead, vertical entry, horizontal exit, midpoint straight).

**Angle corrections (4 bochten, allen op part_idx=5 of 11):**

```
12:22:03  target=-45,00°  measured=-44,62°  correction=-0,38°
12:23:33  target=-45,00°  measured=-44,13°  correction=-0,87°
12:23:39  target=-45,00°  measured=-44,88°  correction=-0,12°
12:23:50  target=-45,00°  measured=-45,00°  correction= 0,00°
```

**BT timeout breakdown (msg_id → aantal):**

```
MSG 114 (system status)   42
MSG  97 (?)               16
MSG   7 (?)               11
MSG 110 (traction)         7
MSG 111 (spindle)          5
MSG  44 (pilot)            4
MSG 113 (footrest)         1
```

## 3. Hoofdbevindingen

### 3.1 Positief

- **Angle correction is zeer nauwkeurig.** Gemiddelde absolute fout < 1°, max 1,38° in run 2 (1 bocht over de 1°-grens), allemaal onder 0,9° in run 3. De verslag-claim "≤ 1° gemiddeld" houdt stand.
- **Compass-reset logica werkt.** Alle vier strategieën (first-bend lookahead, vertical entry, horizontal exit, midpoint straight) zijn in de praktijk gevuurd en op plausibele encoder-posities.
- **BT disconnects: 0.** De link blijft tijdens een run staan.

### 3.2 Rode vlaggen voor het verslag

- **FPS = 36,8 gem. op Galaxy Tab A8 — ver onder de 55 fps threshold.** Beide runs consistent. De verslagtekst in sectie 4.6 moet de tablet-FPS-cijfers bijstellen en de 55 fps-aanname heroverwegen, óf de render-pipeline optimaliseren.
- **BT poll-timeouts (>500 ms) komen 58×/86× per run voor.** Dit is nieuw — oorspronkelijk verslag noemt alleen latency-spikes >150 ms. De firmware reageert regelmatig helemaal niet binnen de POLL_TIMEOUT_MS. MSG 114 (system-status, laagfrequent) is het meest getroffen. Dit past in de "robustness"-claim van het verslag (pipeline herstelt zichzelf) maar moet concreet in de events-kolom.
- **Raw encoder jitter = 0 pulses bij stilstand.** De digitale encoder beweegt geen pulse als de motor uit is. Dat maakt de originele verslag-aanname van "±2-3 pulses jitter raw → <0,1 pulse na Kalman" onhoudbaar in deze vorm. **Aanbeveling**: herformuleren naar "jitter tijdens beweging" óf de KF-ruis karakteriseren tijdens langzame motion i.p.v. bij rest.

### 3.3 Data die ontbreekt

| Metric | Reden | Actie |
| --- | --- | --- |
| End-station position error | MOVE_TO_LAST niet bereikt (run afgebroken voor confirm) | extra run doen tot de app "near end station" zegt + confirm |
| Kalman jitter | IpcLiftController kreeg < 8 stationary samples voor beweging | minimaal 10 s stilstaan direct na Start + instrumentatie-fix (lagere flush-drempel) |
| Derde run | slechts 2 lift-installaties getest | extra run op derde rail voor "Run 3"-kolom verslagtabel |

## 4. Instrumentatie-bugs die gevonden zijn

### 4.1 `bend_error_mm` is geometrisch i.p.v. fysisch

`CalibLog.bend_error()` logt afstand tot dichtstbijzijnde segmentgrens bij STOPPED_ON_STATION, maar de firmware stopt **midden in** de horizontale bocht (tijdelijk station), niet aan de grenzen. Resultaat: `bend_error_mm ≈ 116 mm` in beide runs — exact halve horizontale-bocht-lengte. Dit is geen positiefout maar geometrie.

**Beslissing:** metric weghalen uit de logger. Voor het verslag gebruiken we `angle_correction max_abs_deg` als "bend-transition accuracy"-proxy.

### 4.2 Kalman-jitter flush-drempel

`_track_kalman_stationary_jitter` vereist ≥ 8 samples voor flush bij motion-detectie, maar onvoldoende in de praktijk omdat `IpcLiftController.on_encoder_received` de samples alleen opslaat nadat het filter geïnitialiseerd is. Fix: drempel verlagen naar 4, of starten vanaf de allereerste call.

### 4.3 End-station error afhankelijk van volledig afronden

De `end_station_error_mm` wordt alleen gelogd bij `near_end_station.emit()`. Geen issue voor volledig afgemaakte runs, maar voor dit rapport miste het omdat de user via stop-knop eindigde. Geen code-fix nodig, wel protocol-duidelijkheid.

## 5. Aanbevolen volgende stap

1. Twee kleine code-fixes:
   - `bend_error` metric verwijderen (of corrigeren naar encoder-vs-model-positie tijdens beweging i.p.v. op STOPPED_ON_STATION)
   - Kalman-jitter flush-drempel verlagen van 8 naar 4 samples
2. Derde calibratierun op een derde rail-installatie met:
   - 10 seconden stilstand direct na Start (voor Kalman-jitter)
   - Volledig doorlopen tot de app "near end station" toont
   - Confirm-knop indrukken aan het eindstation
3. Daarna: kolommen Run 1 / Run 2 / Run 3 in het verslag invullen met de werkelijke getallen uit bovenstaande tabel + de nieuwe run, en de FPS- en timeout-bevindingen in de events-tekst opnemen.

## 6. Bronbestanden

- Ruwe logs: `~/stageverslag_periode_1_2_26/logs/calib_20260417_12{1016,1319,2106}_calibration_run.log`
- Instrumentatie-code: `~/MergeIPC/GD-UP-Studio/` op branch `feat/stage-report-logging`
- Test-checklist: `~/stageverslag_periode_1_2_26/tests/test_checklist.pdf`
- Test-protocol: `~/stageverslag_periode_1_2_26/tests/test_protocol.md`
