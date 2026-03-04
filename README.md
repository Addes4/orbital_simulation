# UPG6 – Newton Revisited: Gravitational Slingshot

## Task

Simulate a planetary system with the Sun, Jupiter, and Earth, along with a spacecraft near Earth. The spacecraft's initial delta-v is too small to escape the solar system on its own. The goal is to design a trajectory near Jupiter that acts as a *gravitational slingshot*, giving the spacecraft enough energy to escape.

## Physics

**Equations of motion:** Newton's law of gravitation in Cartesian coordinates. For each pair of bodies $i$ and $j$:

$$\ddot{\mathbf{r}}_i = G m_j \frac{\mathbf{r}_j - \mathbf{r}_i}{|\mathbf{r}_j - \mathbf{r}_i|^3}$$

**Units:** Astronomical units (AU), years (yr), solar masses ($M_\odot$). In these units:

$$G = 4\pi^2 \quad [\text{AU}^3 / (\text{yr}^2 \cdot M_\odot)]$$

**Masses:**
- Sun: $M_\odot = 1.0$
- Jupiter: $M_J = 9.54 \times 10^{-4} \, M_\odot$
- Earth: $M_E = 3.0 \times 10^{-6} \, M_\odot$
- Spacecraft: massless (feels gravity but exerts none)

**Initial conditions:** Elliptical orbits with realistic orbital elements ($a$, $e$). The Sun is given an initial velocity so that the total momentum of the system is zero.

**Numerical method:** Symplectic (semi-implicit) Euler, which conserves energy over long timescales:
```
v_{n+1} = v_n + dt * a(r_n)
r_{n+1} = r_n + dt * v_{n+1}
```

**Escape criterion:** The spacecraft has escaped the solar system when its heliocentric speed exceeds the local escape velocity:

$$v_\text{esc}(r) = \sqrt{\frac{2GM_\odot}{r}}$$

## Files

| File | Description |
|------|-------------|
| `6_NewtonRe.py` | Main simulation: plots the trajectories of the Sun, Earth, Jupiter, and spacecraft, and compares the spacecraft's speed to the escape velocity as a function of distance |
| `6_NewtonRe_komp2.py` | Supplement: computes and prints the total mechanical energy (initial vs. final) to verify energy conservation |
| `6_NewtonRe_komp1.py` | Supplement: plots the total energy near Jupiter for step sizes $h, h/2, h/4, h/8, h/16$ — convergence analysis |
| `6_NewtonRe_komp3.py` | Supplement: plots the spacecraft's position near Jupiter for different step sizes — shows how the trajectory converges |

## Usage

```bash
python 6_NewtonRe.py        # Main simulation with slingshot trajectory
python 6_NewtonRe_komp2.py  # Energy analysis
python 6_NewtonRe_komp1.py  # Energy near Jupiter (convergence)
python 6_NewtonRe_komp3.py  # Position near Jupiter (convergence)
```

Requires: `matplotlib`

## Parameters (main simulation)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `PHASE_J` | 110° | Jupiter's initial orbital angle |
| `DV_T` | 2.2 AU/yr | Tangential delta-v applied to spacecraft |
| `DV_R` | −0.55 AU/yr | Radial delta-v applied to spacecraft |
| `DT` | 1/5000 yr | Time step |
| `TEND` | 12.4 yr | Simulation duration |

## Results

- Figure 1 shows the trajectories in the xy-plane. The spacecraft starts near Earth, swings past Jupiter, and exits the solar system.
- Figure 2 confirms escape: the spacecraft's heliocentric speed exceeds the escape velocity at large distances.
- The energy analyses show that the symplectic Euler method conserves energy well, and that the trajectory converges as the step size is halved.
