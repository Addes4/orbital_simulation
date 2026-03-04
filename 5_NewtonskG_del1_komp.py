# 5
# del 1
# Komplettering med plot för euler fram

import math
import matplotlib.pyplot as plt

G = 1.0

def euler_fram(h):
    t_star = 10.0 * math.pi        # fem varv (sluttid)
    N = int(t_star / h)         # antal steg
    t_star = N * h            # exakt multipel av h (sluttid)

    # begynnelsevärden
    x = 1.0
    y = 0.0
    vx = 0.0
    vy = 1.0

    for _ in range(N):
        r = math.sqrt(x*x + y*y)
        ax = -G * x / (r**3)
        ay = -G * y / (r**3)

        # Euler framåt
        x_new  = x  + h*vx
        y_new  = y  + h*vy
        vx_new = vx + h*ax
        vy_new = vy + h*ay

        x, y, vx, vy = x_new, y_new, vx_new, vy_new

    return x, y, t_star


#Beräknar absolut positionsfel
def error(h):
    x_num, y_num, t_star = euler_fram(h)

    # Exakt lösning vid t*
    x_ex = math.cos(t_star)
    y_ex = math.sin(t_star)

    return math.sqrt((x_num - x_ex)**2 + (y_num - y_ex)**2)


# --- Kör för fem steglängder ---
h0 = 1e-5       # startsteg, kan ändras
hs = [h0, h0/2, h0/4, h0/8, h0/16]

errors = []
for h in hs:
    err = error(h)
    errors.append(err)
    print(f"h={h:.6f}, fel={err:.6e}")

# --- Räkna ut lutningen ---
log_h = [math.log(h) for h in hs]
log_err = [math.log(e) for e in errors]
slope = (log_err[-1] - log_err[0]) / (log_h[-1] - log_h[0])
print(f"\nLutning: {slope:.4f}")

# --- Log–log plot ---
plt.loglog(hs, errors, "o-", label="Euler framåt")
plt.xlabel("Steglängd h")
plt.ylabel("Fel efter 5 varv")
plt.title("Log–log av fel vs steglängd (Euler framåt)")
plt.grid(True, which="both")
plt.legend()
plt.show()