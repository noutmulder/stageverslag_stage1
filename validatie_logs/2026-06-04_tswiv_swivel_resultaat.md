# Bewaarde test — T-SWIV swivel-accuratesse (2026-06-04)

**Logbestand:** `2026-06-04_tswiv_swivel.log` (tablet, session_2026-06-04_16-15-05).
**Doel:** valideren dat de getoonde draaihoek (`swivel_kf`, uit MSG 168) overeenkomt met de
werkelijke rotatie, gemeten met de tablet-kompas/gyro.

## Condities
- Statisch, **zitting horizontaal** (spindel 0°), **tablet plat op de zitting**.
- Referentie: tablet-kompas (gyro-integratie), genuld aan het begin van de sweep.
- Swivel-bereik ~±60°, stappen van 15°. `compass_yaw` automatisch mee-gelogd in `[MARKER]`.

## Resultaat
⚠️ Compass en swivel-encoder hebben een **tegengestelde tekenconventie** (afhankelijk van de
tablet-oriëntatie); hieronder is de compass tekengecorrigeerd.

| MP | `swivel_kf` | compass (gecorr.) | \|verschil\| |
|---|---|---|---|
| 1 (start) | 0,00 | −0,53 | 0,53 |
| 2 | 60,00 | 57,46 | 2,54 |
| 3 | 30,00 | 27,17 | 2,83 |
| 4 | 15,00 | 13,21 | 1,79 |
| 5 | 0,00 | −2,59 | 2,59 |
| 6 | −15,00 | −17,06 | 2,06 |
| 7 | −45,00 | −46,12 | 1,12 |
| 8 | −60,00 | −60,56 | 0,56 |

- **Max verschil: 2,83°; gemiddeld: ~1,7°.**
- **Encoder↔fysiek-tolerantie ~±3,5° → PASS.** Magnitudes lopen 1-op-1 mee (60↔57, 30↔27,
  15↔13); geen grove afwijking (toont geen 50° bij 60°).

## Context / kanttekeningen
- **Gyro-drift:** bij MP5 staat de swivel weer op 0° maar de compass leest 2,6° → ~2,6°
  opgebouwde drift over de sweep (consumenten-gyro). Een deel van de 2–3° spread is dus de
  **referentie**, niet de lift; de werkelijke mapping-fout is kleiner. Voor een driftvrije
  controle zou een fysieke gradenboog-template kunnen dienen (optioneel).
- **Geen blend op swivel:** `swivel_disp` ≈ `swivel_kf` (59,96 vs 60,00) — anders dan de spindel
  (0,85-blend) wordt de swivel ongeblend gerenderd.
- **Tekenconventie:** vermelden bij rapportage; absolute waarden komen overeen.

## Status
T-SWIV gevalideerd, binnen tolerantie. Rail-onafhankelijk (stoel-mapping) → niet per rail herhalen.
