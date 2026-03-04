
import math
import matplotlib.pyplot as plt

# Parametrar
G = 1.0     # gravitationskonstant
dt = 0.0001  # steglängd
T = 70     # sluttid
N = int(T / dt)

# BV
x = [1.0]   # pos
y = [0.0]   # pos
vx = [0.0]  # hastighet
vy = [1.0]  # hastighet

# Symplectic Euler
for n in range(N - 1):
    # nuvarande värden
    xn, yn = x[-1], y[-1]
    vxn, vyn = vx[-1], vy[-1]

    # beräkna acceleration
    r = math.sqrt(xn**2 + yn**2)
    ax = -G * xn / (r**3)
    ay = -G * yn / (r**3)

    # uppdatera hastighet först
    vxn_new = vxn + dt * ax
    vyn_new = vyn + dt * ay

    # uppdatera position med den NYA hastigheten
    xn_new = xn + dt * vxn_new
    yn_new = yn + dt * vyn_new

    # spara nya värden
    vx.append(vxn_new)
    vy.append(vyn_new)
    x.append(xn_new)
    y.append(yn_new)

# Plotta
plt.figure(figsize=(6,6))
plt.plot(x, y, lw=1)
plt.scatter(0, 0, color='orange', s=80, label='Solen')
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.show()
