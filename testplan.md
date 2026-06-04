# Testplan — uitvoering validatiecampagne

Puur wat je doet. Waarom + pass-drempels: zie `fase1_meetontwerp.md`.
Knoppen in de Live-tab: **Spatie = MARK**, **B = baseline**, **F = frame-log**, **S = summary**.
Elke MARK-druk logt nu álle assen tegelijk (positie + spindel + swivel + firmware + mm).

---

## 0. Eenmalig vooraf (thuis/op kantoor)
- [ ] Build + installeer de app met de nieuwe logging.
- [ ] Desktop-rooktest: druk MARK → controleer dat de logregel `[MARKER] ... display_mm=.. fw_mm=.. spindle_kf=.. swivel_kf=..` bevat. Druk F → `[FRAME_LOG] START`, daarna `[FRAME]`-regels, weer F → `STOP`.
- [ ] Instrumenten klaar: meetlint (1 mm), plakkers/tape voor markers, **digitale waterpas** (spindel), logboek/pen. Optioneel: gradenboog-template (swivel), telefoon op **240 fps** (lag-video).
- [ ] Kies één **carriage-referentiepunt** + dunne pointer (gebruik dit voor álle markers, beide richtingen).
- [ ] Vul de rail-set in (`fase1_meetontwerp.md` §3): welke trapliften, lengte, bochttypen.

---

## Per traplift — vaste volgorde

### 1. Setup
- [ ] Koppel app aan de lift (Bluetooth), **laad de rail in** (anders is de encoder→positie niet gecalibreerd).
- [ ] Knop **"Nieuw logfile"**. Schrijf in logboek: **rail-ID + configuratie**.
- [ ] Plaats markers verspreid over **alle segmenttypes**. Meet per marker met het lint de **cumulatieve afstand vanaf het onderstation** → noteer **marker-ID ↔ `d_phys` (mm)**.

### 2. Baseline (stationair) — 0-jitter check
- [ ] Chair stil. Druk **B**, wacht **≥ 15 s**, druk **B**.

### 3. T-TRAC — positie (markers)
- [ ] Rijd in **jog/lage snelheid** richting B→T. Pointer exact op marker → druk **Spatie**.
- [ ] Noteer in logboek: **MP-nummer ↔ marker-ID** (de `d_phys` heb je al).
- [ ] Doe alle markers B→T, dan alle markers **T→B** (zelfde referentiepunt).

### 4. T-SPIN — zithoek (digitale waterpas), op een **vlak railstuk**
- [ ] Rijd naar een vlak stuk. Leg de waterpas op het zit-referentievlak.
- [ ] Zet de spindel met de **fysieke knoppen** op **0°**, laat **uitsettelen** → lees de waterpas → druk **Spatie**.
- [ ] Noteer: **MP-nummer ↔ "SPIN 0° op" + waterpas-waarde**.
- [ ] Herhaal **15°, 30°, 45°, 60°, 75°** (oplopend), dan **75→0** (aflopend). Eén MARK per stand, telkens waterpas noteren.
- [ ] *(optioneel lag):* film waterpas + tablet op 240 fps, geef teststart op de tablet aan, commandeer één sprong.

### 5. T-SWIV — zitdraaiing (kompas + tablet)
- [ ] Tablet plat op de zitting. **Nul de kompas/gyro** vlak vóór de meting.
- [ ] Draai met de **fysieke knoppen** naar stand 1, laat **uitsettelen** → lees de gyro-/kompaswaarde → druk **Spatie**.
- [ ] Noteer: **MP-nummer ↔ "SWIV stand1" + gyro-waarde**.
- [ ] Meerdere standen, **beide draairichtingen**. **Nul de gyro opnieuw vóór elke meting** en meet **kort** (drift).
- [ ] *(optioneel):* lees ook de gradenboog-template af en noteer ernaast.

### 6. DV3 + DV1 — tijdens één rit
- [ ] Druk **F** (frame-log AAN). Rijd **één volledige rustige rit B→T**. Druk **F** (UIT).
- [ ] RTT wordt automatisch gelogd (`[BT_RTT]`) — niets extra te doen.

### 7. Afsluiten
- [ ] Druk **S** (summary). Daarna **"Nieuw logfile"** voor de volgende lift.

---

## Na de campagne
- [ ] Logs ophalen: `adb pull /storage/emulated/0/Android/data/com.example.upstudio/files/validation_logs/ ~/logs/tablet/`
- [ ] Lever het **logboek** in naast de logs: (a) marker-ID ↔ `d_phys`, (b) MP-nummer ↔ test/stand/referentie-waarde.
- [ ] Analyse-script draaien → foutentabellen (T-TRAC/T-SPIN/T-SWIV), smoothness (DV3), RTT-percentielen (DV1), grafieken.

---

## Wat elke logregel is (voor de analyse)
| Regel | Test | Sleutelvelden |
|---|---|---|
| `[MARKER]` | T-TRAC / T-SPIN / T-SWIV | `display_mm`, `fw_mm` (positie); `spindle_kf` (= lookup, vergelijk met waterpas); `swivel_kf` (vergelijk met gyro) |
| `[FRAME]` | DV3 | `display_pos` per frame |
| `[BT_RTT]` | DV1 | `rtt_ms` per round-trip |
| `[BASELINE_START/END]` | 0-jitter | `encoder` constant? |

> Vergelijk bij T-SPIN de waterpas met **`spindle_kf`** (de lookup-uitkomst), niet met de gerenderde
> hoek — die bevat de 85/15-blend. Bij T-SWIV vergelijk de gyro met **`swivel_kf`**.
