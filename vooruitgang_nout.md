# Vooruitgang Nout Mulder - Stage DeVi Comfort

**Periode:** 9 maart 2026 - 14 april 2026 (~5 weken)
**Repository:** GD-UP-Studio (Godot 4 applicatie)
**Totaal commits:** ~206 (waarvan ~130 uniek)
**Netto code:** +36.341 regels (42.039 toegevoegd / 5.698 verwijderd)
**IPC-module alleen:** 10.251 regels code over 41 bestanden - volledig door Nout gebouwd

---

## Inhoudsopgave

1. [Overzicht per onderzoeksvraag](#1-overzicht-per-onderzoeksvraag)
2. [Categorie A: IPC / Live Telemetry Systeem](#categorie-a-ipc--live-telemetry-systeem)
3. [Categorie B: 3D Virtual Ghost / Visualisatie](#categorie-b-3d-virtual-ghost--visualisatie)
4. [Categorie C: Calibratierun / Positiebepaling / Piloting](#categorie-c-calibratierun--positiebepaling--piloting)
5. [Categorie D: Laadstationsysteem](#categorie-d-laadstationsysteem)
6. [Categorie E: UI / Glass Shader Design System](#categorie-e-ui--glass-shader-design-system)
7. [Categorie F: 3D Textures / Materials / Rendering](#categorie-f-3d-textures--materials--rendering)
8. [Categorie G: Onderdelen-tooltips / 3D Rail Preview](#categorie-g-onderdelen-tooltips--3d-rail-preview)
9. [Categorie H: Tablet / Android / Mobiele Optimalisatie](#categorie-h-tablet--android--mobiele-optimalisatie)
10. [Categorie I: Datamodel / Infrastructuur](#categorie-i-datamodel--infrastructuur)
11. [Categorie J: Installatieflow / Stappenplan UI](#categorie-j-installatieflow--stappenplan-ui)
12. [Categorie K: Bend Support / Rail Editing](#categorie-k-bend-support--rail-editing)
13. [Wiskundige onderbouwing van de live telemetry pipeline](#wiskundige-onderbouwing)
14. [Volledige dataflow-diagram](#volledige-dataflow)

---

## 1. Overzicht per onderzoeksvraag

### Onderzoeksvraag 1: Welke storingen en waarschuwingen zijn het meest relevant om te visualiseren?

| Wat is gebouwd | Bestanden | Commits |
|---|---|---|
| Telemetry poller die fout-/statusdata van de lift parsed | `telemetry_poller.gd`, `lift_protocol_parser.gd` | Meerdere IPC-commits |
| Infrastructuur waar foutmodellen op aansluiten | `lift_errors_warnings.gd`, `lift_error_resolutions.gd` (dir door Nout aangemaakt) | - |
| Chair status polling (armsteunen, gordel, voetsteun) | `telemetry_poller.gd` slow loop | `e2246e7` |

### Onderzoeksvraag 2: Welke technische inputs zijn nodig voor een betrouwbare 3D-representatie?

| Wat is gebouwd | Bestanden | Commits |
|---|---|---|
| Encoder-naar-positie mapping (piecewise geinterpoleerd) | `ipc_encoder_mapper.gd` | `f17de3d`, `dbe05f6` |
| Spindle encoder → hoek via firmware lookup-table | `ipc_spindle_lookup.gd` | `f17de3d` |
| Traction encoder parsing (32-bit big-endian) | `telemetry_poller.gd` | Meerdere |
| Spindle encoder parsing (16-bit) | `telemetry_poller.gd` | Meerdere |
| Swivel encoder → hoek (`(enc - 0x7FFF) / 18`) | `telemetry_poller.gd` | Meerdere |
| Compass/gyroscoop integratie voor yaw | `compass_tracker.gd` | `e475584` |
| Split-bend detectie uit sensordata | `split_bend_detector.gd` | `e475584` |
| Calibratierun: volledige piloting met snelheidsbeheer | `calibration_run_service.gd` | `e475584`, `0a8e3ad` |

### Onderzoeksvraag 3: Hoe wordt de verwachte positie bepaald en hoe wordt het verschil berekend?

| Wat is gebouwd | Bestanden | Commits |
|---|---|---|
| Rail opbouw uit IPC JSON met arc-tracing geometrie | `ipc_rail_builder.gd` | `f17de3d` |
| Kalman Filters (constant-velocity model) voor traction, spindle, swivel | `ipc_lift_controller.gd` | `f17de3d` |
| Dead-reckoning extrapolatie tussen metingen | `ipc_lift_controller.gd` | `f17de3d` |
| Piecewise encoder mapping met calibratie tegen 3D-afstanden | `ipc_encoder_mapper.gd` | `dbe05f6` |
| Spindle geometrie-blending (85% Kalman + 15% verwachte hoek) | `ipc_lift_controller.gd` | `f17de3d` |
| Rail block converter (inverse: 3D → firmware blokken) | `rail_block_converter.gd` | `75694f4` |

### Onderzoeksvraag 4: Welke visualisatievormen maken afwijkingen het best begrijpelijk?

| Wat is gebouwd | Bestanden | Commits |
|---|---|---|
| Virtual ghost chair (3D model dat meebeweegt via telemetry) | `ipc_ghost_chair.gd` (617 regels) | `f17de3d` |
| Ghost stair renderer (semi-transparante trappen) | `ghost_stair_renderer.gd` (623 regels) | `f17de3d` |
| Custom ghost shader | `ghost_stair.gdshader` | `f17de3d` |
| Dither clip effect | `dither_clip_controller.gd` + shader | `0a8e3ad` |
| Cel-shading (Wind Waker stijl) voor onderdelen-tooltips | `cel_shade.gdshader` | `5f12597` |
| Rail annotaties over 3D-model | `rail_annotation_manager.gd` | `b6349d1` |
| Liquid glass UI design system (volledig) | `glass_effect.gd`, `glass_style.gd`, shaders | `458edfc` + 30 commits |
| Stair texturen: hout-UV mapping per trede | Meerdere texture commits | `634f2d0`, `d40e869` |

### Onderzoeksvraag 5: Hoe kan het prototype gevalideerd worden met praktijkscenario's?

| Wat is gebouwd | Bestanden | Commits |
|---|---|---|
| Calibratierun systeem (rijdt echte lift + vergelijkt posities) | `calibration_run_service.gd` (838 regels) | `e475584` |
| Override controller (handmatige traction/spindle/swivel/footrest) | `override_controller.gd` | `fd01166` |
| Horizontaliseer-service (live waterpas polling) | `horizontalize_service.gd` | `ba6d0e6` |
| Test-data CSV's | Diverse meetbestanden | `6afa800` |
| Volledig stappenplan (20+ stappen) als validatieworkflow | Meerdere stappenplan-bestanden | Categorie J commits |

### NIEUW - Onderzoeksvraag 6 (voorstel): Welke wiskundige modellen zijn nodig om live telemetry om te zetten naar een betrouwbare 3D-representatie?

| Wat is gebouwd | Wiskundig concept | Bestanden |
|---|---|---|
| Kalman Filter (2D constant-velocity) | Procesruis: Q = σ²·[[dt³/3, dt²/2],[dt²/2, dt]] | `ipc_lift_controller.gd` |
| Catmull-Rom spline interpolatie | CR(p0,p1,p2,p3,t) = 0.5(2p1 + (-p0+p2)t + ...) | `ipc_ghost_chair.gd` |
| Quaternion transformaties | local_quat = parent⁻¹ · world_quat · parent | `ipc_ghost_chair.gd` |
| Arc-tracing (trapezoidale benadering) | pos += avg(d_voor, d_na) · (radius · hoek) | `ipc_rail_builder.gd` |
| Piecewise encoder mapping | Lineaire interpolatie per raildeel | `ipc_encoder_mapper.gd` |
| Binary search lookup-table inversie | 751 entries, 0.1° resolutie, 0-75° | `ipc_spindle_lookup.gd` |
| Chiraliteitsdetectie (2D cross-product) | Σ(dir_in × dir_out) bepaalt links/rechts | `ipc_ghost_chair.gd` |
| Exponential smoothing | x = lerp(x, target, 1 - e^(-rate·dt)) | `ipc_lift_controller.gd`, `ipc_ghost_chair.gd` |
| Gyroscoop integratie | yaw += gyro.z · (180/π) · dt | `compass_tracker.gd` |
| Split-bend compensatie | Patroondetectie + richtingsafhankelijke hoekaftrek | `split_bend_detector.gd` |

---

## Categorie A: IPC / Live Telemetry Systeem

**Onderzoeksvragen: Q2 (technische inputs), Q3 (positiebepaling), Q6 (wiskunde)**

Het volledige IPC-communicatiesysteem is from scratch gebouwd door Nout. Dit omvat Bluetooth-transport, TCP-sockets, telemetry-polling, protocol-parsing en de live datapipeline.

### Commits

| Datum | Hash | Bericht |
|---|---|---|
| 2026-03-09 | `f17de3d` | IPC live mode: room walls, follow camera, ghost stairs, UI improvements |
| 2026-03-10 | `082cc74` | Design mode grid radius fade + BT permission fix |
| 2026-03-12 | `66bd064` | Linux BT Classic verbinding + stappenplan lift-connectie + UI verbeteringen |
| 2026-03-12 | `34e49ff` | Voeg Ubuntu BT setup script toe voor rfcomm binding |
| 2026-03-12 | `d601c87` | Lift verbinding UI: liquid glass 3D-tracking panel + auto rfcomm |
| 2026-03-13 | `75694f4` | Rail block converter: gebruik rail_nodes_3d ipv segments_3d |
| 2026-03-13 | `8db7773` | Fix BT rail readback + post-upload verification overlay |
| 2026-03-13 | `5d1ed4c` | WiFi stap + database verzending + verbindingsfixes |
| 2026-03-19 | `33b5752` | Klantgegevens BLE service, links/rechts lift, rail-fallback en input-fixes |

### Sleutelbestanden (alle door Nout aangemaakt)

| Bestand | Regels | Functie |
|---|---|---|
| `source/ipc/net/lift/bluetooth_lift_transport.gd` | - | Bluetooth transport layer |
| `source/ipc/net/lift/tcp_lift_transport.gd` | - | TCP transport layer |
| `source/ipc/net/lift/lift_client.gd` | - | High-level communicatieclient met retry/timeout |
| `source/ipc/net/lift/lift_connection_manager.gd` | - | Verbindingsbeheer |
| `source/ipc/net/lift/lift_message.gd` | - | Binair draadprotocol (168+ command IDs) |
| `source/ipc/net/lift/lift_protocol_parser.gd` | - | 6-state FSM byte parser |
| `source/ipc/net/lift/telemetry_poller.gd` | - | 3 concurrente polling loops |
| `source/ipc/net/lift/app_to_bus_client.gd` | - | APP_TO_BUS multiplexing |
| `source/ipc/net/lift/rail_manager.gd` | - | Rail data management |
| `source/ipc/net/lift/linux_bt_bridge.py` | - | Linux BT Classic bridge script |
| `source/ipc/net/ipc_client_session.gd` | - | IPC sessiebeheer |
| `source/ipc/net/ipc_protocol.gd` | - | IPC protocol definitie |
| `source/ipc/net/ipc_socket_server.gd` | - | TCP socket server |
| `source/ipc/net/lift/wifi/` | - | Volledig WiFi-subsysteem (5 bestanden) |

### Technische details

**Draadprotocol (app → lift):**
```
[0x0A] [MessageNumber] [ReadWriteId=0x00] [CommandId] [Length(0-40)] [Data(0-40 bytes)] [Checksum]
```
Checksum: `(START_BYTE + msg_nr + rw_id + cmd_id + length + Σdata) & 0xFF`

**Protocol parser:** 6-state FSM: `WAIT_START → MSG_NR → CMD_ID → LENGTH → DATA → CHECKSUM`. Resync bij ongeldige lengte (>40) of checksum-mismatch.

**Polling architectuur (3 concurrente coroutine-loops):**
- **Fast loop (~20Hz):** Afwisselend traction (MSG 110) en spindle (MSG 111) per frame tick
- **Swivel loop (~20Hz):** APP_TO_BUS (MSG 168) targeting CHAIR chip, 50ms interval
- **Slow loop (0.5Hz):** Chair status (MSG 114 system + MSG 113 footrest) elke 2 seconden

**Data parsing:**
- Traction encoder: 32-bit big-endian uit `data[1..4]`
- Spindle encoder: 16-bit uit `data[1..2]`, hoek uit `data[7]`
- Swivel hoek: 16-bit `(data[3]<<8)|data[4]`, dan `(encoder - 0x7FFF) / 18` → graden
- Chair status bits: `data[14]` bit 0=arm_links, bit 1=arm_rechts, bit 2=gordel

---

## Categorie B: 3D Virtual Ghost / Visualisatie

**Onderzoeksvragen: Q1 (relevante storingen), Q3 (verwacht vs gemeten), Q4 (visualisatievormen), Q6 (wiskunde)**

De "ghost chair" — de 3D-representatie van de traplift die in real-time meebeweegt op basis van telemetrydata.

### Commits

| Datum | Hash | Bericht |
|---|---|---|
| 2026-03-09 | `f17de3d` | IPC live mode: room walls, follow camera, ghost stairs, UI (6534 regels toegevoegd - fundament) |
| 2026-03-10 | `571f56e` | Installatie mode: kamer met doos, tooltip met rail/lift keuze |
| 2026-03-10 | `8bdcb4b` | Merge install mode into bouw tab + start-rail met IpcGhostChair |
| 2026-04-13 | `b6349d1` | feat: Stappenplan rail annotations, ghost removal, and fixes |

### Sleutelbestanden

| Bestand | Regels | Functie |
|---|---|---|
| `source/ipc/ipc_ghost_chair.gd` | 617 | De virtual ghost zelf |
| `source/ipc/ghost_stair_renderer.gd` | 623 | Ghost stair visualisatie |
| `source/ipc/ipc_lift_controller.gd` | 550 | Vertaalt telemetry naar ghost-positie |
| `source/ipc/ipc_encoder_mapper.gd` | 110 | Encoder → railpositie mapping |
| `source/ipc/ipc_spindle_lookup.gd` | 112 | Spindle positie lookup |
| `source/ipc/ipc_rail_builder.gd` | 268 | Bouwt 3D rail uit IPC-data |
| `source/ipc/stair_ipc_bridge.gd` | 217 | Bridge stairdata naar IPC |
| `source/ipc/rail_annotation_manager.gd` | 263 | Rail annotaties |
| `shaders/ghost_stair.gdshader` | 50 | Custom ghost shader |
| `source/ipc/dither_clip_controller.gd` | - | Dither clip effect |
| `source/ipc/model/traplift.gd` | - | Traplift datamodel |
| `source/ipc/model/traplift_rail.gd` | - | Rail datamodel |
| `source/ipc/model/traplift_stoel.gd` | - | Stoel datamodel |

---

## Categorie C: Calibratierun / Positiebepaling / Piloting

**Onderzoeksvragen: Q2, Q3, Q5, Q6**

Het calibratierun-systeem: de echte traplift wordt aangestuurd via Bluetooth terwijl de positie in real-time wordt vergeleken met de verwachte positie.

### Commits

| Datum | Hash | Bericht |
|---|---|---|
| 2026-03-17 | `1ebe666` | Stappenplan: lift-naar-boven stap + rail upload fixes |
| 2026-03-17 | `0285178` | Stappenplan: IPC rail alignment + instructiepaneel |
| 2026-03-17 | `fd01166` | OverrideController + drive-onto-rail stap |
| 2026-03-17 | `4bb68b3` | Fix lift-flip, voetenplank, herhaalanimaties |
| 2026-03-17 | `e6a92af` | Laadstation-stap zet locatie op top via BT |
| 2026-03-17 | `ba6d0e6` | Horizontaliseer-stap met live HORIZON_GAUGE polling |
| 2026-03-19 | `e016d55` | "Use current rail from lift" dev-optie |
| 2026-03-19 | `e475584` | **Calibratierun: volledige piloting, compass, split-bend en live telemetry** (1874 regels) |
| 2026-03-20 | `0a8e3ad` | Dither clip, override-fix, betrouwbare BT start |
| 2026-03-20 | `58e4654` | Annotaties zichtbaar tijdens calibratierun |
| 2026-03-24 | `dbe05f6` | Fix encoder mapping, station offsets, charger plaatsing |
| 2026-03-24 | `cab93d5` | Fix charger flip IPC standalone |
| 2026-03-26 | `cc2df70` | Fix traptextuur bij calibratierun |
| 2026-03-26 | `e2246e7` | Chair status polling + laadstations in dither clip |

### Sleutelbestanden

| Bestand | Regels | Functie |
|---|---|---|
| `source/ipc/net/lift/calibration_run_service.gd` | 838 | Volledige calibratierun state machine |
| `source/ipc/net/lift/compass_tracker.gd` | 153 | Gyroscoop-integratie voor yaw |
| `source/ipc/net/lift/split_bend_detector.gd` | 182 | Detecteert split-bends in rail |
| `source/ipc/net/lift/override_controller.gd` | 125 | Handmatige traction/spindle/swivel/footrest override |
| `source/ipc/net/lift/horizontalize_service.gd` | - | Live waterpas polling |

### Calibratierun technische details

- **Polling interval:** 250ms per tick
- **Per tick gepolled:** lock state, traction, pilot state (keep-alive), spindle, lift location
- **Elke 4e tick:** errors
- **Elke 8e tick:** chair status
- **Hoek correctie bij bochten:** `correctie = |target_half| - |gemeten_hoek|`
- **Hoek encoding firmware:** `scaled = round(hoek_graden × 8.0)`, als negatief: `scaled += 65536`
- **Snelheidsbeheer:** Normaal = 50, bocht = 20 (ook korte rechte stukken <250mm)
- **Eindstation detectie:** Binnen 118 pulsen (~35mm)

---

## Categorie D: Laadstationsysteem

**Onderzoeksvragen: Q2 (technische inputs), Q5 (validatie)**

### Commits

| Datum | Hash | Bericht |
|---|---|---|
| 2026-03-23 | `48bdd84` | Station installatie-stappen: OOP model, camera, afstand-invoer |
| 2026-03-23 | `0d2fefe` | Fix dubbele laadcontacten |
| 2026-03-24 | `3869600` | Station stappen splitsen: aparte installatie- en afstand-stap |
| 2026-03-24 | `3d749d2` | Station offsets uploaden en teruglezen bij rail upload |
| 2026-03-24 | `3e2f801` | Laadcontacten fly-off en fly-in animatie |
| 2026-03-24 | `a7ba198` | Fix charger fly-in: herbouw na readback |
| 2026-03-24 | `cecf905` | Chargers herbouwen op IPC readback rail |
| 2026-03-24 | `1e3bc7e` | Fix laadstation verkeerde kant: XOR rotation |
| 2026-03-24 | `d9bc721` | Fix charger offset: gebruik IPC rail |
| 2026-03-24 | `7380255` | Fix charger afstand na readback |
| 2026-03-24 | `1a3f85c` | Lift naar laadstation: echte station offset |
| 2026-03-24 | `ec6576a` | Laadstations bij 'Use current rail from lift' |

---

## Categorie E: UI / Glass Shader Design System

**Onderzoeksvraag: Q4 (visualisatievormen)**

Complete UI-overhaul met "liquid glass" / "matte glass" design systeem. Meer dan 30 commits op 2026-04-08.

### Belangrijkste commits

| Datum | Hash | Bericht |
|---|---|---|
| 2026-04-08 | `458edfc` | Liquid glass UI overhaul: unified shaders, consistent styling |
| 2026-04-08 | `95eef29` | Extract glass parameters into GlassStyle theme resource |
| 2026-04-08 | `6144e88` | Matte glass style voor leesbare content |
| 2026-04-08 | `92e5c5c` | Alle buttons, dropdowns, inputs als matte glass squircles |
| 2026-04-08 | `be07dce` | Panel snapping + auto-positioning |
| 2026-04-09 | `0df50fa` | Matte glass noise: fijner grain, rounded corner shader mask |
| 2026-04-13 | `eeb9c13` | Artist-friendly glass shader met live-updating parameters |

### Sleutelbestanden

- `source/dashboard/glass_effect.gd`
- `source/dashboard/glass.gdshader`
- `source/theme/glass_style.gd`
- `source/theme/glass_dark.tres`
- `source/shaders/liquid_glass.gdshader`

---

## Categorie F: 3D Textures / Materials / Rendering

**Onderzoeksvraag: Q4**

### Commits (allemaal 2026-04-09)

| Hash | Bericht |
|---|---|
| `b998762` | Fix stair textures: reduce UV tiling, warmer tint |
| `634f2d0` | Per-tread UV mapping: wood grain volgt langste kant |
| `d40e869` | Stringer (trapboom) matched tread texture |
| `c715778` | Remove floor gloss |
| `2c4d890` | Railing texture: proper UV mapping langs rail |

---

## Categorie G: Onderdelen-tooltips / 3D Rail Preview

**Onderzoeksvraag: Q4**

### Commits

| Datum | Hash | Bericht |
|---|---|---|
| 2026-03-23 | `4f8befa` | Onderdelen-tooltip met 3D rail preview |
| 2026-03-23 | `5f12597` | Wind Waker cel-shading, 2D labels, bounding sphere |
| 2026-03-23 | `387ac16` | Rail tooltip: donkerder metallic look |
| 2026-04-09 | `07cde51` | Parts tooltip: fixed-size square met labels |

---

## Categorie H: Tablet / Android / Mobiele Optimalisatie

**Onderzoeksvraag: Q4 (cross-platform)**

### Commits

| Datum | Hash | Bericht |
|---|---|---|
| 2026-03-24 | `a59a21c` | Herstel manifest met BT permissions Android 12+ |
| 2026-03-26 | `b1a363d` | Reduceer shadow lights van 3 naar 1 voor tablet |
| 2026-03-26 | `f6daceb` | Tablet optimalisatie: brightness slider, fill lights zonder shadows |
| 2026-04-09 | `1d2f212` | Mobile perf: disable shadows, flat glass, persist quality |
| 2026-04-13 | `f820b70` | fix: Tablet wall rendering |
| 2026-04-14 | `df21fa5` | feat: tablet UI auto-detection and scaling |

---

## Categorie I: Datamodel / Infrastructuur

**Onderzoeksvraag: Q2**

| Datum | Hash | Bericht |
|---|---|---|
| 2026-04-08 | `c2cddb5` | Add lift_serial en lift_mac_address aan ProjectData |
| 2026-04-08 | `264e4ff` | Add lift_mac_address aan MaintenanceData en ServiceCallData |
| 2026-03-24 | `6a1b1eb` | Vertaalsysteem met NL/EN language files |
| 2026-03-19 | `6afa800` | Testdata CSVs en meetbestanden |
| 2026-03-10 | `d5f11df` | DEV_MODE + camera debug overlay |

---

## Categorie J: Installatieflow / Stappenplan UI

**Onderzoeksvraag: Q5**

| Datum | Hash | Bericht |
|---|---|---|
| 2026-04-08 | `787e79a` | Rail visibility toggles en part_info offset |
| 2026-04-09 | `7e54e8a` | Fix start-rail, installation flow camera, parts tooltip |
| 2026-03-26 | `7b4807c` | Fix stoelzijde linker lift |
| 2026-03-26 | `02c91f1` | Fix drive-onto-rail panel positionering |
| 2026-04-14 | `0cfafd5` | fix: installation flow camera position |
| 2026-04-14 | `10a4c33` | fix: hide annotation on start-rail step |

---

## Categorie K: Bend Support / Rail Editing

**Meest recente werk (2026-04-14)**

| Hash | Bericht |
|---|---|
| `3ea4b66` | chore: add always-on support bend zone logging |
| `4f29777` | fix: bend support placement |
| `7e0e889` | fix: bend support -- groove recalculation |
| `2e46e57` | fix: bend support selection and node tracking |
| `5db12b6` | fix: bend support spacing and edit restrictions |

---

## Wiskundige onderbouwing

Dit is de kern van de (voorgestelde) nieuwe onderzoeksvraag: de wiskunde achter het live telemetry systeem.

### 1. Kalman Filter (Constant-Velocity Model)

Toegepast op 3 onafhankelijke assen: traction, spindle en swivel.

**Toestandsvector:** `x = [positie, snelheid]ᵀ`

**Predict stap:**
```
pos += vel × dt
P[0,0] += 2·dt·P[0,1] + dt²·P[1,1] + σ²_accel · dt³/3
P[0,1] += dt·P[1,1] + σ²_accel · dt²/2
P[1,1] += σ²_accel · dt
```

Procesruismatrix (white-noise-jerk model):
```
Q = σ²_accel · [[dt³/3, dt²/2], [dt²/2, dt]]
```

**Correct stap:**
```
y = meting - pos                    (innovatie)
S = P[0,0] + σ²_meas               (innovatie-covariantie)
K[0] = P[0,0] / S                  (Kalman gain positie)
K[1] = P[0,1] / S                  (Kalman gain snelheid)
pos += K[0] · y
vel += K[1] · y
```

**Tuning parameters:**

| Parameter | Traction | Spindle | Swivel |
|---|---|---|---|
| σ_accel | 0.03 | 8.0 | 10.0 |
| σ_meas | 0.0002 | 0.2 | 0.5 |
| display_smoothing | 8.0 | 12.0 | 12.0 |
| max_vel | 1.2× max_speed_norm | 30°/s | 40°/s |

### 2. Dead-Reckoning Extrapolatie

Tussen metingen door:
```
target = kf_pos + vel × verstreken_tijd
```
Met snelheidsverval na 0.8s:
```
vel *= e^(-5.0 · (verstreken_tijd - 0.8))
```

### 3. Display Smoothing (Exponentieel Filter)

Frame-rate onafhankelijk eerste-orde laagdoorlaatfilter:
```
display_pos = lerp(display_pos, target, 1 - e^(-smoothing × dt))
```

### 4. Catmull-Rom Spline Interpolatie

**Positie (standaard kubisch):**
```
CR(p0,p1,p2,p3,t) = 0.5 · (2p1 + (-p0+p2)t + (2p0-5p1+4p2-p3)t² + (-p0+3p1-3p2+p3)t³)
```

**Tangent (eerste afgeleide):**
```
CR'(p0,p1,p2,p3,t) = 0.5 · ((-p0+p2) + (4p0-10p1+8p2-2p3)t + (-3p0+9p1-9p2+3p3)t²)
```

Ontwerpkeuze: positie gebruikt lineaire interpolatie (volgt railsegmenten), tangent gebruikt Catmull-Rom (vloeiende rotatie).

### 5. Quaternion Transformaties

World-to-local conversie voor pitch en spindle:
```
local_quat = parent_quat⁻¹ · world_quat · parent_quat
```

**Unit pitch:**
```
pitch_hoek = atan2(dir.y, length(dir.xz))
world_pitch_as = UP × dir_flat (genormaliseerd)
unit_pivot.quaternion = parent_quat⁻¹ · Quaternion(as, -pitch) · parent_quat
```

**Spindle compensatie:**
```
seat_world_hoek = -pitch_hoek + spindle_rad
spindle_pivot.quaternion = parent_quat⁻¹ · Quaternion(as, seat_world_hoek) · parent_quat
```

### 6. Arc-Tracing Geometrie (Rail Opbouw)

**Richting uit yaw/pitch (Godot Y-up):**
```
direction(yaw, pitch) = Vector3(-sin(yaw)·cos(pitch), sin(pitch), -cos(yaw)·cos(pitch))
```

**Booglengte per segment:**
```
arc_len = radius × stap_rad = 0.150 × deg_to_rad(5.0) ≈ 0.01309 m
```

**Trapezoidale benadering:**
```
pos += ((d_voor + d_na) × 0.5).normalized() × arc_len
```

### 7. Piecewise Encoder Mapping

**Firmware constanten:**
- `PULSES_PER_MM = 3.361352398` (rechte stukken)
- `UP_CURVE_PULSES_PER_SEG = 37.54666` (bocht omhoog)
- `DOWN_CURVE_PULSES_PER_SEG = 50.45333` (bocht omlaag)
- `HORIZ_PULSES_PER_SEG = 44.0` (horizontale bocht)
- `FIRMWARE_START_ENC = 100` (initieel offset)

Twee modes:
1. **Fallback (lineair):** `genormaliseerd = (encoder - min) / totaal_bereik`
2. **Piecewise-gekalibreerd:** Na `calibrate_with_points()` bouwt een map van `{enc, dist}` paren per railgrens. Lineaire interpolatie per segment.

### 8. Spindle Lookup-Table Inversie

Firmware `Curve.h` tabel: 751 entries, index `i` = `i/10.0` graden, waarde = encoder pulsen.

Binary search (11 iteraties, 2¹¹ = 2048 > 751):
```
encoder = max(0, raw - BASE_OFFSET)    // BASE_OFFSET = 10000
hoek = binary_search_index / 10.0      // graden
```

### 9. Chiraliteitsdetectie

Cumulatief 2D cross-product van opeenvolgende richtvectoren:
```
cumulative_cross = Σ(dir_in.x · dir_out.y - dir_in.y · dir_out.x)
is_links_draaiend = cumulative_cross ≥ 0
stoel_rotatie = 90° (links) of 270° (rechts)
```

### 10. Gyroscoop-Integratie (Compass Tracker)

```
accumulated_yaw += gyro.z × (180/π) × dt
relatieve_hoek = normalize(accumulated_yaw - baseline_yaw)
```
Normalisatie naar [-180, 180]: `deg = fmod(deg + 180, 360) - 180`

---

## Volledige Dataflow

```
╔══════════════════════════════════════════════════════════════╗
║                   EXTERNE BRON                               ║
║  Android app / TCP client / Raspberry Pi                     ║
╚══════════════════════════╦═══════════════════════════════════╝
                           ║
              ┌────────────╨────────────┐
              │    StairIpcBridge        │
              │  (TCP server, poll I/O)  │
              └────┬──────┬──────┬──────┘
                   │      │      │
        rail_json  │      │      │  encoder / spindle / swivel
                   ▼      │      ▼
     ┌─────────────────┐  │  ┌──────────────────────┐
     │  IpcRailBuilder  │  │  │  IpcLiftController   │
     │  (arc-tracing)   │  │  │  (3× Kalman Filter)  │
     └──┬──────┬──────┬─┘  │  └──────────┬───────────┘
        │      │      │    │             │
        ▼      ▼      ▼    │             │ positie + hoeken
   GhostStair  Encoder  Ghost           │
   Renderer    Mapper   Chair ◄──────────┘
                 │       │
                 │       ├── Catmull-Rom tangent → yaw/pitch
                 │       ├── Quaternion → unit tilt
                 │       ├── Spindle compensatie → stoel hoek
                 │       └── Chiraliteit → links/rechts
                 │
                 └── Piecewise interpolatie → genormaliseerde positie
```

**Alternatief pad (directe Bluetooth):**
```
LiftClient (BT/TCP transport)
    → LiftProtocolParser (6-state FSM)
        → TelemetryPoller (3 coroutine loops)
            → IpcLiftController (zelfde pipeline)
```

---

## Tijdlijn Samenvatting

| Week | Periode | Focus |
|---|---|---|
| 1 | 9-13 maart | IPC fundament: BT transport, protocol, ghost chair, ghost stairs, live mode |
| 2 | 17-19 maart | Stappenplan integratie, calibratierun systeem, compass, piloting |
| 3 | 20-24 maart | Laadstations, encoder fixes, onderdelen-tooltips, testdata |
| 4 | 26 maart | Tablet optimalisatie, Android BT fixes, stoelzijde correcties |
| 5 | 8-9 april | Liquid glass UI overhaul (30+ commits), textuur-verbeteringen |
| 6 | 13-14 april | Tablet rendering, bend support, annotaties, flow fixes |
