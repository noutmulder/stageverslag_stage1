# Test-uitvoeringsplan

Concrete voorbereiding voor de fysieke validatie-run. Geen theorie meer — alleen actie. Drie delen:

- **§1** wat je gaat meten (3 metingen + 2 observaties, gekoppeld aan DV1–DV3)
- **§2** wat je nodig hebt (fysiek + code-instrumentatie)
- **§3** de run zelf, stap-voor-stap
- **§4** post-run dataverwerking
- **§5** verslag invullen

Eindresultaat: een complete tabel met cijfers in plaats van `[meet]` placeholders.

---

## §1 — Wat je meet

| # | Meting | Voor | Hoe verkregen |
|---|---|---|---|
| M1 | Bluetooth round-trip time (run-gemiddelde) | DV1(b) | Uit logfile, applicatielaag |
| M2 | Raw encoder jitter (stationair, 10 s) | DV3(b) baseline | Uit logfile, stationaire periode |
| M3 | Kalman-filtered jitter (stationair, 10 s) | DV3(b) | Uit logfile, zelfde periode |
| M4 | Positie-error bij referentiepunten | DV2(b) | Vergelijking display vs meetlint |
| O1 | Visuele smoothness | observation | Tijdens de run kijken + screenshot |
| O2 | Anomalieën (BT drops, glitches, etc.) | observation | Tijdens de run noteren + logfile |

Drie metingen die direct het criterium toetsen, twee observaties die context geven.

---

## §2 — Wat je nodig hebt

### Fysiek

- **Eén stairlift** waarvan je de rail kunt bereiken voor markeringen. Eén rail, één run is genoeg.
- **Meetlint** (rolmaat). Een goedkope met mm-graduatie volstaat. Leesfout ±1 mm.
- **Tape** (papier of schilders) voor minimaal 4 markers op de rail.
- **Een laptop of tablet** waarop de app draait met USB/Bluetooth verbinding naar de lift.
- **Een telefoon** om foto's te maken van het scherm op markerpunten (of screenshots in de app als dat werkt).
- **Pen + papier** om handmatig per marker fysieke positie + tijdstempel te noteren.

### Code-instrumentatie

De huidige code logt al een aantal dingen naar Godot console maar **niet alles wat je nodig hebt**. Twee aanpassingen zijn nuttig vóór de run:

#### A. Logfile maken in plaats van alleen console-output

Eenvoudigste optie: run de app vanaf de terminal en stuur stdout naar een file.

```bash
cd ~/MergeIPC/GD-UP-Studio
godot --path . > ~/run_log_$(date +%Y%m%d_%H%M).txt 2>&1
```

Of in Godot zelf: via `OS.execute()` of een logger-autoload. Maar terminal redirect is simpeler.

#### B. Per-frame telemetry-log toevoegen

De huidige `ipc_lift_controller.gd` print elke 2 s een samenvatting (regel 267-270). Voor jitter-analyse heb je per-frame data nodig tijdens de stationaire baseline. Voeg deze regel toe aan `_process()` of `on_encoder_received()`:

```gdscript
# Tijdelijk voor validatierun: per-meting log voor jitter-analyse
print("[CSV] %d,%d,%.6f,%.6f,%.6f" % [
    Time.get_ticks_msec(), last_encoder_value,
    _kf_pos, _kf_vel, _display_pos
])
```

Dat geeft je CSV-achtige regels:
```
[CSV] timestamp_ms, raw_encoder, kf_position, kf_velocity, display_position
```

Na de run kun je deze regels uit de logfile grep'en:
```bash
grep "\[CSV\]" run_log.txt > validation_data.csv
```

#### C. BT round-trip log

In `lift_client.gd` rond regel 124-141 (de `send_and_receive` functie) is `elapsed_ms` berekend maar niet gelogd. Voeg deze print toe na de while-loop:

```gdscript
if _pending_result != null:
    print("[BT_RTT] msg_id=%d rtt_ms=%.1f" % [msg_id, elapsed_ms])
```

Dat geeft je een lijst RTT-metingen per request. Run-gemiddelde bereken je na de tijd.

#### D. Markeer reference points handmatig

Tijdens de run druk je een toets op je toetsenbord op het moment dat de chair een marker passeert. In `_process()` van main_visualizer of een input-handler:

```gdscript
if Input.is_action_just_pressed("ui_select"):  # of bv. spatiebalk
    print("[MARKER] t=%d encoder=%d kf_pos=%.5f display_pos=%.5f" % [
        Time.get_ticks_msec(),
        IpcLiftController.last_encoder_value,
        _ipc_lift._kf_pos,
        _ipc_lift._display_pos
    ])
```

Of nog simpler: gebruik een knop in de UI die je al hebt.

---

### Snel-instrumentatie zonder code-aanpassing

Als je geen code wilt aanpassen: gebruik wat er al is. De bestaande prints geven:
- `[IpcTelemetry] avg=X.X Hz, vel=X, encoder=X, pos=X` (elke 2 s) → ruwe encoder + filter state
- `[LiftClient] TX/RX X bytes` → BT activiteit (geen timing)

Niet ideaal — je krijgt geen RTT-meting zonder code-toevoeging — maar voor visuele smoothness en de positie-vergelijking is dit genoeg.

---

## §3 — De run zelf

### Stap 0 — De dag vóór de run

- [ ] Beslis welke lift je gebruikt
- [ ] Plan minstens 4 referentiepunten op de rail:
  - Bottom station (bv. 200 mm vanaf onderkant)
  - Een punt midden op rechte rail (~midden)
  - Eén bend entry of exit
  - Top station (~ 200 mm vanaf bovenkant)
- [ ] Bereid de code-instrumentatie voor (§2, optioneel maar aanbevolen)
- [ ] Druk dit document af of zet het op je telefoon

### Stap 1 — Op locatie, vóór de run (~15 min)

- [ ] Lift uitschakelen, app testen op TCP/demo eerst
- [ ] Plak markers op de rail bij gekozen referentiepunten
- [ ] Meet met meetlint de positie van elke marker vanaf de bottom station; noteer:

```
Marker M1 (bottom): _______ mm
Marker M2 (......): _______ mm
Marker M3 (......): _______ mm
Marker M4 (top):    _______ mm
```

- [ ] Start de app: `godot --path . > run_log.txt 2>&1` (of jouw equivalent)
- [ ] Connect Bluetooth, verifieer dat data binnenkomt

### Stap 2 — Stationaire baseline (5 min)

Doel: 10-seconden meting met chair NIET bewegend, voor M2 en M3.

- [ ] Plaats chair op M1 (bottom)
- [ ] Wacht tot logfile constant draait (~5 s pauze)
- [ ] Markeer in de log: typ een teken op stdin OF noteer de exacte klok-tijd
- [ ] Wacht 10 seconden, chair blijft stil
- [ ] Markeer einde

### Stap 3 — Bottom-naar-top run (5–15 min, afhankelijk van rail)

- [ ] Druk de joystick of joystick-knop in om de chair te starten
- [ ] Bij elke marker:
  - Stop de chair (of laat doorrijden indien lift dat niet toestaat)
  - Maak een foto/screenshot van het scherm waarop de getoonde positie zichtbaar is
  - Druk je marker-knop (zie §2.D) OF noteer in een aparte file/papier: marker-nummer + klok-tijd + getoonde positie
- [ ] Observeer terwijl het rijdt: smooth motion? Jumps? Oscillation?

### Stap 4 — Top-naar-bottom return (5–15 min)

- [ ] Idem als stap 3, maar omgekeerd
- [ ] Je krijgt nu 2 metingen per marker → middelen

### Stap 5 — Afsluitend (~5 min)

- [ ] Stop de app netjes (Ctrl+C in terminal, niet kill -9)
- [ ] Bewaar `run_log.txt`
- [ ] Bewaar foto's/screenshots
- [ ] Schrijf binnen 10 min na de run je observaties op (smooth/niet smooth, glitches, BT drops, etc.) — anders vergeet je het

**Totale tijd op de lift: 30–45 min**

---

## §4 — Post-run dataverwerking

### M1 — BT round-trip

Als je instrumentatie §2.C hebt gedaan:
```bash
grep "\[BT_RTT\]" run_log.txt | awk -F"rtt_ms=" '{print $2}' | awk '{sum+=$1; n++} END {print "avg:", sum/n, "ms ("n" samples)"}'
```

Zonder instrumentatie: niet direct meetbaar. Optie: schat uit polling rate. Als sample rate ~20 Hz dan is RTT ≤ 50 ms.

### M2 + M3 — Encoder jitter

Als je instrumentatie §2.B hebt gedaan:
```bash
grep "\[CSV\]" run_log.txt > validation.csv
# Open in spreadsheet, filter op stationaire periode (10s window)
# Bereken voor raw encoder kolom: max - min (= peak-to-peak jitter)
# Bereken voor display_pos kolom: max - min, omgerekend naar pulse-equivalent
# Ratio = raw_jitter / kalman_jitter
```

Of in Python:
```python
import csv
rows = [r for r in csv.reader(open("validation.csv")) if r[0].startswith("[CSV]")]
# Filter rows met timestamp in stationaire window (handmatig)
encoders = [int(r[1]) for r in stationary_window]
display_pos = [float(r[4]) for r in stationary_window]
raw_jitter = max(encoders) - min(encoders)
kf_jitter = max(display_pos) - min(display_pos)
print(f"raw: ±{raw_jitter/2} pulses, kalman: {kf_jitter*4500:.3f} pulse-equivalent")
# (factor 4500 ≈ total encoder range; pas aan je rail aan)
```

### M4 — Positie error per marker

Voor elke marker:
1. Fysieke positie M_i (van je meetlint).
2. Getoonde positie uit screenshot/log: `display_pos × rail_length_mm`.
3. Error_i = |fysiek - getoond| in mm.

Maak een mini-tabel:
```
Marker | Fysiek (mm) | Display (mm) | Error (mm)
M1     | 200         | 198          | 2
M2     | 1500        | 1503         | 3
M3     | 2800        | 2792         | 8
M4     | 4800        | 4796         | 4
```

Rapporteer: max error en (optioneel) avg error.

### O1 + O2 — Observaties

Schrijf eerlijk op wat je zag:
- "Chair tracked rail smoothly throughout the run"
- "One brief stutter at the second bend (~3 second pause)"
- "BT remained connected throughout"
- etc.

---

## §5 — Verslag invullen

Open `project/main.tex`, ga naar Table~\ref{tab:validation} (rond regel 1100), vervang `[meet]` placeholders:

| Metric | Value | Pass/fail |
|---|---|---|
| Rail length | **[vul in]** mm | --- |
| Number of horizontal bends | **[vul in]** | --- |
| Position error at end station | **[vul in M4 voor M1 of M4]** mm | DV2(b): pass/fail |
| Max position error at reference points | **[vul in max M4]** mm | DV2(b): pass/fail |
| Encoder jitter (raw, stationary, 10 s) | ±**[vul in M2]** pulses | DV3(b) baseline |
| Encoder jitter (after Kalman, 10 s) | **[vul in M3]** pulses | DV3(b): pass/fail |
| Bluetooth round-trip time (run avg) | **[vul in M1]** ms | DV1(b): pass/fail |
| Visual smoothness through bends | observational: **[O1]** | --- |

Pass/fail logica:
- DV1(b): pass als M1 ≤ 100 ms
- DV2(b): pass als max M4 ≤ 5 mm (rail ≤ 5 m) of ≤ 10 mm (rail > 5 m)
- DV3(b): pass als (M2 / M3) ≥ 10

Ga ook naar de "Logged events" paragraaf (regel ~1126) en vul de werkelijke observaties O2 in. Voorbeeld:

```latex
\textbf{Logged events.} During the run, [no anomalies were observed / 
a brief pause at bend 2 was observed / Bluetooth maintained connection 
throughout / etc.].
```

Build de PDF:
```bash
cd project && latexmk -pdf main.tex
```

Commit:
```bash
git add project/main.tex project/main.aux project/main.fdb_latexmk \
        project/main.fls project/main.log project/main.pdf
git commit -m "validate: fill measurement results from physical run"
```

---

## Belangrijke kanttekeningen

1. **N=1 is OK** — je rapporteert eerlijk dat het een single run is. Niet pretenderen dat het meer is.
2. **Schrijf alles op tijdens de run**, niet erna. Geheugen is onbetrouwbaar.
3. **Bij failure: rapporteer eerlijk** — als M4 max = 12 mm en de threshold is 10 mm, dan failt DV2(b) en dat ga je expliciet noemen in de conclusie. Eerlijkheid is meer waard dan een gefabriceerde pass.
4. **Geen tweede run om resultaten te "verbeteren"** — als je een tweede run doet, rapporteer beide en discuss waarom je een tweede deed.
5. **Bewaar de raw logs** in een aparte directory `logs/` (al aanwezig in de repo, niet committen vanwege size). Dan kun je later terug naar de data.

---

## Wat te doen NA de run

1. Verslag invullen (§5) — 30 min
2. Commit de gevulde versie — 5 min
3. Optioneel: coherentie-check (lees end-to-end of de conclusies nu logisch volgen uit de meetdata) — 15 min
4. Optioneel: vraag een collega om met verse ogen door het verslag te gaan — geen onafhankelijke validatie, maar wel een check op begrijpelijkheid

---

## Als de run mislukt of niet kan plaatsvinden

Plan B: gebruik **demo mode** in de app (`demo_lift_transport.gd` zit in de code) om in elk geval iets functioneels te laten zien. De position-accuracy meting werkt dan niet, maar je kunt wel:
- Visuele smoothness observeren
- Jitter laten zien (synthetic encoder met noise)
- BT vervangen door TCP simuleren

Dan rapporteer je: "Validation was performed in demo mode with simulated telemetry; physical-hardware validation is a recommendation for future work." Niet ideaal, maar eerlijk en verdedigbaar.
