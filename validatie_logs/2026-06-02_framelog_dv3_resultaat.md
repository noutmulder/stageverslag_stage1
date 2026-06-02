# Bewaarde test — frame-log / DV3 smoothness (2026-06-02)

**Logbestand:** `2026-06-02_framelog_dv3_3assen.log` (bron: desktop, Godot user-data; session_2026-06-02_13-26-39).
**Doel:** verifiëren dat de nieuwe `[FRAME]`-logging werkt en de dead-reckoning op alle drie de assen
vloeiend interpoleert (DV3, velocity-gebaseerd criterium uit `fase1_meetontwerp.md` §1/§7.C).

## Condities
- Eén frame-log venster: `[FRAME_LOG] START t=40708` → `STOP t=86608` (≈ 45,9 s, 2754 frames).
- Volledige beweging met alle drie de assen actief.
- Platform: desktop. (Tablet-fps nog apart te checken.)

## Resultaat
- **Render:** 60,0 fps; frame-interval mediaan 17 ms, max 20 ms.
- **Bereik:** traction 7,0 → 91,2 % rail (84,2 %); spindle 0,0 → 70,7°; swivel −61,6 → +2,2°.
- **DV3-smoothness (velocity-maat: pieken > 5× mediane |v|):**

| As | bewegend | pieken > 5× mediaan | jerk p99 | oordeel |
|---|---|---|---|---|
| traction | 94 % | 0 (0,00 %) | 0,007 | vloeiend, geen staircase |
| spindle | 46 % | 0 (0,00 %) | 3,58 | vloeiend |
| swivel | 29 % | 1 (0,13 %) | 6,91 | vloeiend (1 piek = verwaarloosbaar) |

## Verdict
DV3-mechanisme + dead-reckoning werken op alle drie de assen. Geen staircase. Eenmalige eerdere
~52 fps-dip (vorige sessie) niet gereproduceerd — hier vast 60 fps.

## Nog open
- MARK (`[MARKER]`) nog niet getest in deze sessie.
- fps op de Android-tablet apart verifiëren (render-gezondheid, los van smoothness).
