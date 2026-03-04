# 5
# del 3
# Planetbana med symplektisk euler + rörandes sol
# Komplettering med log-log plot med lutning 2


import math
import matplotlib.pyplot as plt

# Parametrar
PI = math.pi
G = 4 * PI * PI  # gravitationskonstant

# Massor
M_sun = 1.0      # solens massa
M_planet = 0.4   # planetens massa

# Simuleringsparametrar
DT = 1.0 / 1000.0  # steglängd
TEND = 10.0        # total simuleringstid
EPS = 1e-3         # softening längd

def acc_pair(xi, yi, xj, yj, mj, eps=EPS):
    """Acceleration på kropp i från kropp j med massa mj."""
    dx, dy = xj - xi, yj - yi
    r2 = dx*dx + dy*dy
    r = math.sqrt(r2) + eps
    invr3 = 1.0 / (r2 * r)
    return G * mj * dx * invr3, G * mj * dy * invr3

def symplectic_euler_two_body(h: float):
    """
    Kör Symplectic Euler för tvåkroppssystem upp till fem varv och returnerar (xP, yP, t_star).
    """
    # Sluttid: fem varv (uppskattad period för elliptisk bana)
    t_star = 5 * 2 * math.pi  # fem varv
    N = int(t_star / h)
    t_star = N * h  # justera till exakt multipel av h

    # BV
    xS, yS = 0.0, 0.0           # solens pos
    xP, yP = 1.0, 0.0           # planetens pos
    vxS, vyS = 0.0, 0.0         # solens hastighet
    vxP, vyP = 0.0, 0.0         # planetens hastighet
    
    r = math.sqrt((xP - xS)**2 + (yP - yS)**2)
    v_circ = math.sqrt(G * M_sun / r)
    
    # Initiala hastigheter för elliptisk bana
    vxP = 0.15
    vyP = v_circ * 0.7
    vxS = 0.05
    vyS = 0.02

    for _ in range(N):
        # Beräkna accelerationer
        aSx, aSy = acc_pair(xS, yS, xP, yP, M_planet)
        aPx, aPy = acc_pair(xP, yP, xS, yS, M_sun)
        
        # Symplectic Euler: uppdatera hastigheter först
        vxS += h * aSx
        vyS += h * aSy
        vxP += h * aPx
        vyP += h * aPy
        
        # Uppdatera positioner med nya hastigheter
        xS += h * vxS
        yS += h * vyS
        xP += h * vxP
        yP += h * vyP

    return xP, yP, t_star

def simulate():
    """Integrera solen-planet system med symplektisk euler."""
    
    # BV
    xS, yS = 0.0, 0.0           # solens pos
    xP, yP = 1.0, 0.0           # planetens pos
    vxS, vyS = 0.0, 0.0         # solens hastighet
    vxP, vyP = 0.0, 0.0         # planetens hastighet
    
    r = math.sqrt((xP - xS)**2 + (yP - yS)**2) # avstånd
    v_circ = math.sqrt(G * M_sun / r) # den has som krävs för en cirkulär bana
    

    vxP = 0.15  # radial hastighet
    vyP = v_circ * 0.7  # reducerad tangentiell hastighet -> elliptisk
    
    # initial drift
    vxS = 0.05  # solens initial drift hastighet
    vyS = 0.02
    
    # antal steg
    N = int(TEND / DT)
    
    # arrays för att lagra bana data
    XS, YS = [], []  # solens bana
    XP, YP = [], []  # planetens bana
    
    for n in range(N):
        # beräkna accelerationer
        # solens acceleration från planet
        aSx, aSy = acc_pair(xS, yS, xP, yP, M_planet)
        
        # planetens acceleration från solen
        aPx, aPy = acc_pair(xP, yP, xS, yS, M_sun)
        
        # Symplectic Euler uppdatera hastigheter först
        vxS += DT * aSx
        vyS += DT * aSy
        vxP += DT * aPx
        vyP += DT * aPy
        
        # uppdatera positioner med nya hastigheter
        xS += DT * vxS
        yS += DT * vyS
        xP += DT * vxP
        yP += DT * vyP
        
        # lagra bana data var 10:e steg
        if n % 10 == 0:
            XS.append(xS)
            YS.append(yS)
            XP.append(xP)
            YP.append(yP)
    
    return XS, YS, XP, YP

def error_two_body(h):
    """Beräknar fel i planetens position vid fem varv."""
    xP_num, yP_num, t_star = symplectic_euler_two_body(h)
    
    # Referensposition med mycket liten steglängd
    h_ref = 1e-6
    xP_ref, yP_ref, _ = symplectic_euler_two_body(h_ref)
    
    return math.sqrt((xP_num - xP_ref)**2 + (yP_num - yP_ref)**2)

if __name__ == "__main__":
    # Log-log plot av fel för olika steglängder
    
    h0 = 1e-3
    hs = [h0, h0/2, h0/4, h0/8, h0/16]
    errors = []
    
    for h in hs:
        err = error_two_body(h)
        errors.append(err)
        print(f"h={h:.6f}, fel={err:.6e}")
    
    # Räkna ut lutningen
    log_h = [math.log(h) for h in hs]
    log_err = [math.log(e) for e in errors]
    slope = (log_err[-1] - log_err[0]) / (log_h[-1] - log_h[0])
    print(f"\nLutning: {slope:.4f}")
    
    # Log-log plot
    plt.figure(figsize=(8, 6))
    plt.loglog(hs, errors, "o-", label="Symplectic Euler (tvåkroppar)")
    plt.xlabel("Steglängd h")
    plt.ylabel("Fel efter 5 varv")
    plt.title("Log–log av fel vs steglängd (tvåkroppssystem)")
    plt.grid(True, which="both")
    plt.legend()
    plt.show()
    
    # Kör även original simulering för jämförelse
    print("\nKör original simulering...")
    XS, YS, XP, YP = simulate()
    
    # Plotta banor
    plt.figure(figsize=(6, 6))
    plt.plot(XS, YS, lw=1, color='orange', label='Sun')
    plt.plot(XP, YP, lw=1, label='Planet')
    plt.xlabel("x [AU]")
    plt.ylabel("y [AU]")
    plt.axis("equal")
    plt.grid(True)
    plt.legend()
    plt.show()
