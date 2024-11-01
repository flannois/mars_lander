from data import *

class Surface:
    def __init__(self, mars_surface):
        self.mars_surface = mars_surface

    def calcul_zone_atterissage(self, scenar):
        surf = scenar['surface_mars']
        for i in range(len(surf) -1):
            p1X, p1Y = surf[i]
            p2X, p2Y = surf[i+1]
            if p1Y == p2Y:
                self.atterissage = ((p1X, p1Y),(p2X, p2Y))
        return self.atterissage

    def est_dans_la_zone(self,v):
        zoneAtterissageGauche, zoneAtterissageDroite = self.atterissage
        if zoneAtterissageGauche[0] < v.x < zoneAtterissageDroite[0]:
            return True
        else:
            return False

    def se_rapproche_de_la_zone(self, v, scenar):
        #ICI JE TRAVAILLE

        vaisseau_va_a_gauche = False
        vaisseau_va_a_droite = False
        vaisseau_va_en_bas = False
        vaisseau_va_en_haut = False

        if v.h_speed > 0:
            vaisseau_va_a_droite = True
        elif v.h_speed < 0:
            vaisseau_va_a_gauche = True

        if v.v_speed < 0:
            vaisseau_va_en_haut = True
        elif v.v_speed > 0:
            vaisseau_va_en_bas = True

        attG, attD = self.calcul_zone_atterissage(scenar)

        if vaisseau_va_en_bas and vaisseau_va_a_droite and v.x < attG[0] and v.y < attG[1]:
            ter = 1