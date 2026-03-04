# UPG5 & UPG6 – Newtonian Gravitation

---

## Task 5 – Newtonian Gravitation

### Description

Simulate a planet orbiting the Sun using Newton's law of gravitation. The equations of motion are derived in Cartesian coordinates (no polar coordinates). The task is divided into three parts:

1. **Part 1** – Sun fixed at the origin. Simulate a short and a long time using forward (explicit) Euler. Observe that the orbit drifts and energy is not conserved.
2. **Part 2** – Same setup, but switch to symplectic (semi-implicit) Euler. Show that energy is now conserved and the orbit remains stable over long times.
3. **Part 3** – Remove the assumption that the Sun is fixed. Let both the Sun and the planet move, with the Sun responding to the planet's gravity. Experiment with different relative masses.

### Physics

**Equation of motion** (Sun fixed at origin, planet at position $(x, y)$):

$$\ddot{x} = -\frac{G x}{r^3}, \qquad \ddot{y} = -\frac{G y}{r^3}, \qquad r = \sqrt{x^2 + y^2}$$

**Two-body system** (both bodies moving):

$$\ddot{\mathbf{r}}_i = G m_j \frac{\mathbf{r}_j - \mathbf{r}_i}{|\mathbf{r}_j - \mathbf{r}_i|^3}$$

**Units:** Parts 1–2 use scaled units with $G = 1$. Part 3 uses $G = 4\pi^2$ (AU, yr, $M_\odot$).

**Forward Euler** (Parts 1, 1-komp):
```
x_{n+1}  = x_n  + h * vx_n
vx_{n+1} = vx_n + h * ax_n
```

**Symplectic Euler** (Parts 2–3): velocity updated first, then position uses the new velocity:
```
vx_{n+1} = vx_n + h * ax_n
x_{n+1}  = x_n  + h * vx_{n+1}
```
This preserves a modified energy and keeps orbits stable indefinitely.

### Files

| File | Description |
|------|-------------|
| `5_NewtonskG_del1.py` | Forward Euler orbit simulation — short and long time, Sun fixed |
| `5_NewtonskG_del1_komp.py` | Convergence analysis for forward Euler: log-log plot of position error vs step size $h$ over 5 orbits (slope ≈ 1) |
| `5_NewtonskG_del2.py` | Symplectic Euler orbit — same setup as Part 1 but with stable long-time integration |
| `5_NewtonskG_del3.py` | Two-body simulation: both Sun and planet move, symplectic Euler, non-zero planet mass |
| `5_NewtonskG_del3_komp.py` | Convergence analysis for the two-body symplectic Euler: log-log plot (slope ≈ 2) |

### Usage

```bash
python 5_NewtonskG_del1.py        # Forward Euler orbit
python 5_NewtonskG_del1_komp.py   # Convergence: forward Euler
python 5_NewtonskG_del2.py        # Symplectic Euler orbit
python 5_NewtonskG_del3.py        # Two-body orbit (moving Sun)
python 5_NewtonskG_del3_komp.py   # Convergence: symplectic Euler two-body
```

Requires: `matplotlib`

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `G` | 1.0 (Parts 1–2) / $4\pi^2$ (Part 3) | Gravitational constant |
| `M_sun` | 1.0 | Solar mass |
| `M_planet` | 0.4 | Planet mass (Part 3) |
| `dt` | 0.001 – 0.0001 | Time step |
| `T` | 7 – 70 | Simulation end time |

### Results

- **Part 1:** Forward Euler causes the orbit to spiral outward — energy grows over time.
- **Part 2:** Symplectic Euler keeps the orbit closed and energy bounded, even over long simulations.
- **Part 3:** With a massive planet, the Sun visibly moves. Varying `M_planet` changes the character of the orbit.
- **Convergence plots:** Forward Euler shows slope ≈ 1 (first-order); symplectic Euler shows slope ≈ 2 in the two-body case.

---

## Task 6 – Newton Revisited: Gravitational Slingshot

### Description

Extend the simulation to a three-body system: Sun, Jupiter, and Earth. Add a massless spacecraft launched from near Earth with a delta-v too small to escape the solar system on its own. The goal is to design a flyby trajectory near Jupiter — a *gravitational slingshot* — that gives the spacecraft enough energy to escape.

### Physics

**Equations of motion:** Same Newtonian gravity applied to all pairs. The spacecraft is massless: it feels gravity from all bodies but exerts none.

**Units:** $G = 4\pi^2$, distances in AU, time in years, masses in $M_\odot$.

**Masses:**
- Sun: $M_\odot = 1.0$
- Jupiter: $M_J = 9.54 \times 10^{-4} \, M_\odot$
- Earth: $M_E = 3.0 \times 10^{-6} \, M_\odot$
- Spacecraft: massless

**Initial conditions:** Elliptical orbits from real orbital elements (semi-major axis $a$, eccentricity $e$). The Sun is given an initial velocity so that the total momentum is zero.

**Numerical method:** Symplectic Euler (same as Task 5, Part 2–3).

**Escape criterion:** The spacecraft has escaped when its heliocentric speed exceeds the local escape velocity:

$$v_\text{esc}(r) = \sqrt{\frac{2 G M_\odot}{r}}$$

### Files

| File | Description |
|------|-------------|
| `6_NewtonRe.py` | Main simulation: plots trajectories of Sun, Earth, Jupiter, and spacecraft; compares spacecraft speed to escape velocity vs. distance |
| `6_NewtonRe_komp2.py` | Energy analysis: prints initial and final total mechanical energy to verify conservation |
| `6_NewtonRe_komp1.py` | Plots total energy near Jupiter for step sizes $h, h/2, h/4, h/8, h/16$ — convergence analysis |
| `6_NewtonRe_komp3.py` | Plots spacecraft position near Jupiter for different step sizes — trajectory convergence |

### Usage

```bash
python 6_NewtonRe.py        # Main slingshot simulation
python 6_NewtonRe_komp2.py  # Energy conservation check
python 6_NewtonRe_komp1.py  # Energy near Jupiter (convergence)
python 6_NewtonRe_komp3.py  # Position near Jupiter (convergence)
```

Requires: `matplotlib`

### Key Parameters (main simulation)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `PHASE_J` | 110° | Jupiter's initial orbital angle |
| `DV_T` | 2.2 AU/yr | Tangential delta-v applied to spacecraft |
| `DV_R` | −0.55 AU/yr | Radial delta-v applied to spacecraft |
| `DT` | 1/5000 yr | Time step |
| `TEND` | 12.4 yr | Simulation duration |

### Results

- Figure 1 shows the trajectories in the xy-plane. The spacecraft starts near Earth, swings past Jupiter, and exits the solar system.
- Figure 2 confirms escape: the spacecraft's heliocentric speed exceeds the escape velocity at large distances.
- The energy analyses show that symplectic Euler conserves energy well, and the solution converges as the step size is halved.
