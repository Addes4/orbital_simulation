# UPG6 – Newton Revisited: Gravitational Slingshot

## Uppgift

Simulera ett planetsystem med solen, Jupiter och jorden, samt ett rymdskepp nära jorden. Skeppets initiala delta-v är så litet att det inte kan lämna solsystemet på egen hand. Målet är att designa en bana nära Jupiter som fungerar som en *gravitational slingshot* – så att skeppet ändå kan lämna solsystemet.

## Fysik

**Ekvationer:** Newtons gravitationslag i kartesiska koordinater. För varje par av kroppar $i$ och $j$:

$$\ddot{\mathbf{r}}_i = G m_j \frac{\mathbf{r}_j - \mathbf{r}_i}{|\mathbf{r}_j - \mathbf{r}_i|^3}$$

**Enheter:** Astronomiska enheter (AU), år (yr), solmassor ($M_\odot$). Med dessa enheter ges:

$$G = 4\pi^2 \quad [\text{AU}^3 / (\text{yr}^2 \cdot M_\odot)]$$

**Massor:**
- Solen: $M_\odot = 1.0$
- Jupiter: $M_J = 9.54 \times 10^{-4} \, M_\odot$
- Jorden: $M_E = 3.0 \times 10^{-6} \, M_\odot$
- Rymdskepp: masslöst (påverkas av men påverkar inte andra kroppar)

**Initialvillkor:** Elliptiska banor med realistiska orbitalelement ($a$, $e$). Solen ges en initial hastighet så att systemets totala rörelsemängd är noll.

**Numerisk metod:** Symplektisk (semi-implicit) Euler för att bevara energin långsiktigt:
```
v_{n+1} = v_n + dt * a(r_n)
r_{n+1} = r_n + dt * v_{n+1}
```

**Flykt från solsystemet:** Skeppet har lämnat solsystemet när dess heliocentriska hastighet överstiger flykthastigheten vid aktuellt avstånd:

$$v_\text{esc}(r) = \sqrt{\frac{2GM_\odot}{r}}$$

## Filer

| Fil | Beskrivning |
|-----|-------------|
| `6_NewtonRe.py` | Huvudsimulering: plottar banorna för sol, jord, Jupiter och skepp, samt skeppets hastighet mot flykthastigheten som funktion av avstånd |
| `6_NewtonRe_komp2.py` | Komplement: beräknar och plottar den mekaniska energin för systemet (initial vs slutlig) – verifierar energibevarande |
| `6_NewtonRe_komp1.py` | Komplement: plottar total energi nära Jupiter för olika steglängder $h, h/2, h/4, h/8, h/16$ – konvergensanalys |
| `6_NewtonRe_komp3.py` | Komplement: plottar skeppets position nära Jupiter för olika steglängder – visar hur banan konvergerar |

## Körning

```bash
python 6_NewtonRe.py        # Huvudsimulering med slingshot-bana
python 6_NewtonRe_komp2.py  # Energianalys
python 6_NewtonRe_komp1.py  # Energi nära Jupiter (konvergens)
python 6_NewtonRe_komp3.py  # Position nära Jupiter (konvergens)
```

Kräver: `matplotlib`

## Parametrar (huvudsimulering)

| Parameter | Värde | Förklaring |
|-----------|-------|------------|
| `PHASE_J` | 110° | Jupiters startvinkel |
| `DV_T` | 2.2 AU/yr | Tangentiellt delta-v för skeppet |
| `DV_R` | −0.55 AU/yr | Radiellt delta-v för skeppet |
| `DT` | 1/5000 yr | Tidssteg |
| `TEND` | 12.4 yr | Simuleringstid |

## Resultat

- Figur 1 visar banorna i xy-planet. Skeppet startar nära jorden, svänger förbi Jupiter och lämnar solsystemet.
- Figur 2 bekräftar att skeppet lämnar solsystemet: dess heliocentriska hastighet överstiger flykthastigheten vid stora avstånd.
- Energianalyserna visar att den symplektiska Euler-metoden bevarar energin väl, och att lösningen konvergerar vid halvering av steglängden.
