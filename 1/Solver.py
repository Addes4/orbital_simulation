# 6


import math
import matplotlib.pyplot as plt

# Enheter o konstanter
G = 4*math.pi**2   # AU^3 / (yr^2 * M_sun)

M_sun     = 1.0     # solens massa
M_earth   = 0.000003    # jordens massa i relation till solens
M_jupiter = 0.000954    # jupiteres massa i relation till solens

SOFT = 1e-7    # liten längd för att undvika singularitet r=0


# gravitation, acceleration på i från j
def acc_pair(xi, yi, xj, yj, mj, eps=SOFT):
    dx, dy = xj - xi, yj - yi  
    r2 = dx*dx + dy*dy 
    r  = math.sqrt(r2) + eps  
    invr3 = 1.0/(r2*r)     
    return G*mj*dx*invr3, G*mj*dy*invr3     # komponentvis acceleration

# Initiera sol, jord, jupiter med elliptiska banor + rörlig sol
def init_system(phase_j):
    # Orbitalelement, halvstoraxel a och excentricitet e
    aE, eE = 1.0000, 0.0167    # Jorden
    aJ, eJ = 5.2000, 0.0489    # Jupiter

    # vinkel på ellipsen
    fE = 0.0    # Jorden vid perihelion
    fJ = phase_j 

    # radier på ellipsen
    rE = aE*(1 - eE*eE) / (1 + eE*math.cos(fE))
    rJ = aJ*(1 - eJ*eJ) / (1 + eJ*math.cos(fJ))

    #positioner i xy-plan
    xE = rE
    yE = 0.0
    xJ = rJ*math.cos(fJ)
    yJ = rJ*math.sin(fJ)

    # tangent riktning
    vE = math.sqrt(G*M_sun*(2.0/rE - 1.0/aE))
    vxE, vyE = 0.0, vE

    vJ = math.sqrt(G*M_sun*(2.0/rJ - 1.0/aJ))
    tx, ty = -math.sin(fJ), math.cos(fJ)    # enhetstangent
    vxJ, vyJ = vJ*tx, vJ*ty

    # Solen får hastighet så att total rörelsemängd = 0
    xS, yS = 0.0, 0.0
    Px = M_earth*vxE + M_jupiter*vxJ
    Py = M_earth*vyE + M_jupiter*vyJ
    vxS, vyS = -Px/M_sun, -Py/M_sun

    return [xS, yS, xE, yE, xJ, yJ, vxS, vyS, vxE, vyE, vxJ, vyJ]


# Symplektiskt euler, upd hastighet o position
def simulate(DV_T, DV_R, PHASE_J, DT=1/5000, TEND=120.0, record_every=5):
    xS,yS,xE,yE,xJ,yJ, vxS,vyS,vxE,vyE,vxJ,vyJ = init_system(PHASE_J)

    # Skepp starta vid jorden (liten offset)
    xC, yC = xE + 1e-3, yE
    vxC, vyC = vxE, vyE
    
    vxC += DV_R
    vyC += DV_T

    N = int(TEND/DT)

    # Loggar för plott
    XS= []; YS= []; XE= []; YE= []; XJ= []; YJ= []; XC= []; YC= []
    rShip=[]; vShip=[]

    for n in range(N):
        # ackumulerad accelerationer på varje kropp
        aSx=aSy=0.0; aEx=aEy=0.0; aJx=aJy=0.0; aCx=aCy=0.0

        # Påverkan på solen från andra
        ax,ay = acc_pair(xS,yS, xE,yE, M_earth);   aSx+=ax; aSy+=ay
        ax,ay = acc_pair(xS,yS, xJ,yJ, M_jupiter); aSx+=ax; aSy+=ay

        # Påverkan på jorden av andra
        ax,ay = acc_pair(xE,yE, xS,yS, M_sun);     aEx+=ax; aEy+=ay
        ax,ay = acc_pair(xE,yE, xJ,yJ, M_jupiter); aEx+=ax; aEy+=ay

        # Påverkan på Jupiter av andra
        ax,ay = acc_pair(xJ,yJ, xS,yS, M_sun);     aJx+=ax; aJy+=ay
        ax,ay = acc_pair(xJ,yJ, xE,yE, M_earth);   aJx+=ax; aJy+=ay

        # Skepp påverkas av alla andra, men påverkar ingen pga masslös
        ax,ay = acc_pair(xC,yC, xS,yS, M_sun);     aCx+=ax; aCy+=ay
        ax,ay = acc_pair(xC,yC, xE,yE, M_earth);   aCx+=ax; aCy+=ay
        ax,ay = acc_pair(xC,yC, xJ,yJ, M_jupiter); aCx+=ax; aCy+=ay

        #uppdatera hastigheter
        vxS += DT*aSx; vyS += DT*aSy
        vxE += DT*aEx; vyE += DT*aEy
        vxJ += DT*aJx; vyJ += DT*aJy
        vxC += DT*aCx; vyC += DT*aCy

        # uppdatera positioner
        xS += DT*vxS; yS += DT*vyS
        xE += DT*vxE; yE += DT*vyE
        xJ += DT*vxJ; yJ += DT*vyJ
        xC += DT*vxC; yC += DT*vyC

        # Logg för figurer
        if n % record_every == 0:
            XS.append(xS); YS.append(yS)
            XE.append(xE); YE.append(yE)
            XJ.append(xJ); YJ.append(yJ)
            XC.append(xC); YC.append(yC)

            # heliocentrisk fart o radie (skepp relativt solen)
            vrx, vry = vxC - vxS, vyC - vyS
            vShip.append(math.hypot(vrx, vry))
            rShip.append(math.hypot(xC - xS, yC - yS))

    return XS,YS,XE,YE,XJ,YJ,XC,YC, rShip, vShip


# Körning
def main():
    PHASE_J = math.radians(110)     # jupiters fas
    DV_T = 2.2      # delta tangentiell
    DV_R = -0.55    # delta radiell
    DT = 1/5000
    TEND = 12.4 # simuleringstid

    XS,YS,XE,YE,XJ,YJ,XC,YC, rShip, vShip = simulate(DV_T, DV_R, PHASE_J, DT, TEND)

    # Figur 1
    plt.figure(figsize=(8,6)) 
    plt.plot(XS, YS, '-', lw=4.0, label='Sol')  # solens bana
    plt.plot(XE, YE, '-', lw=1.0, label='Jorden')  # jordens bana 
    plt.plot(XJ, YJ, '-', lw=1.0, label='Jupiter')  #  Jupiters bana 
    plt.plot(XC, YC, '-', lw=1.0, label='Skepp', color='tab:red')  # skeppets bana

    plt.gca().set_aspect('equal', adjustable='box')  # axlarna lika långa
    plt.grid(); plt.legend()  #  rutnät och förklaring
    plt.xlabel('x [AU]'); plt.ylabel('y [AU]')  # Axeletiketter o enheter
    plt.tight_layout()  # undvika klippning
    plt.show()  # Visa diagrammet

    # Figur 2
    v_esc = [math.sqrt(2*G*M_sun/r) for r in rShip]  # räkna flykthastighet för varje avstånd: v_esc = sqrt(2GM/r)
    plt.figure(figsize=(8,5))
    plt.plot(rShip, v_esc, color="green", label='Flykthastighet')  # flykthastigheten som funktion av avstånd
    plt.plot(rShip, vShip, color ="red", label='Skeppets hastighet')  # skeppets faktiska hastighet som funktion av avstånd
    plt.xlabel('Avstånd till solen, r [AU]')  # x-axel
    plt.ylabel('Hastighet [AU/yr]')  # y-axel
    plt.grid(); plt.legend()  # rutnät o förklaring
    plt.tight_layout()  # för att undvika klippning
    plt.show()

if __name__ == "__main__":
    main()
