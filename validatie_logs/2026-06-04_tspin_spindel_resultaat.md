# Bewaarde test — T-SPIN spindel-accuratesse (2026-06-04)

**Logbestand:** `2026-06-04_tspin_spindel.log` (tablet, session_2026-06-04_15-46-45).
**Doel:** valideren dat de getoonde spindel-zithoek (`spindle_kf`, uit de 751-punts lookup)
overeenkomt met de werkelijke fysieke kanteling. Code vooraf "volgens ontwerp" gefixt na
eerdere mislukte pogingen.

## Condities
- Statisch, op een **vlak railstuk** (rail-pitch ≈ 0).
- Referentie: **digitale waterpas** op een vlak, meedraaiend vlak van de zitting.
- Spindel-bereik 0–75°, stappen van 15°. MP3 en MP4 zijn beide 30° (dubbele MARK; één telt).
- Vergeleken met **`spindle_kf`** (lookup-uitkomst), **niet** de gerenderde hoek (zie blend hieronder).

## Resultaat
| Commando | `spindle_kf` | Waterpas (fysiek) | \|verschil\| |
|---|---|---|---|
| 0°  | 0,00  | 0,00  | 0,00 |
| 15° | 15,10 | 15,50 | 0,40 |
| 30° | 30,00 | 30,55 | 0,55 |
| 45° | 45,70 | 45,50 | 0,20 |
| 60° | 60,20 | 60,31 | 0,11 |
| 75° (max) | 75,00 | 76,05 | 1,05 |

- **Max verschil: 1,05°** (bij 75°, de mechanische eindstand).
- **Gemiddeld: ~0,4°.**
- **Drempel ~1–2° → PASS.** De encoder→hoek-mapping klopt over het hele bereik; alleen aan de
  eindstand loopt het ~1° op.

## Ontwerp-bevestiging (geometry-blend)
`spindle_disp` (gerenderde ghost-hoek) = 12,8 / 25,5 / 38,8 / 51,2 / 63,75° = **exact 0,85 ×
`spindle_kf`**. Op een vlak stuk (geometry-pitch ≈ 0) toont de ghost dus bewust 85% van de
spindelhoek (de `SPINDLE_GEOMETRY_WEIGHT = 0.15`-blend). Daarom is gevalideerd tegen `spindle_kf`
(de lookup), niet tegen de gerenderde hoek — anders zou de blend als schijn-fout van ~15%
verschijnen.

## Status
T-SPIN gevalideerd, binnen ~1°. Rail-onafhankelijk (stoel-mapping) → niet per rail herhalen.
