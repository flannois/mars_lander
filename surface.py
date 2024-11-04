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
        return True if self.atterissage[0][0] < v.x < self.atterissage[1][0] else False
        
    def est_a_gauche_de_la_zone(self, v):
        return True if v.x < self.atterissage[0][0] else False 
    
    def est_a_droite_de_la_zone(self, v):
        return True if v.x > self.atterissage[1][0] else False
    
    def est_en_haut_de_la_zone(self, v):
        return True if v.y < self.atterissage[0][1] else False

    def est_en_bas_de_la_zone(self, v):
        return True if v.y > self.atterissage[1][1] else False
        
    def va_a_gauche(self, v):
        return True if v.v_speed < 0 else False

    def va_a_droite(self, v):
        return True if v.v_speed > 0 else False
    
    def va_en_haut(self, v):
        return True if v.h_speed < 0 else False
    
    def va_en_bas(self, v):
        return True if v.h_speed > 0 else False
        

    def se_rapproche_de_la_zone(self, v):
        # en haut a gauche
        if self.est_en_haut_de_la_zone(v) and self.est_a_gauche_de_la_zone(v):
            if self.va_en_bas(v) and self.va_a_droite(v):
                return True 
                
        # en haut a droite
        elif self.est_en_haut_de_la_zone(v) and self.est_a_droite_de_la_zone(v):
            if self.va_en_bas(v) and self.va_a_gauche(v):  
                return True
            
        # en bas a gauche
        elif self.est_en_bas_de_la_zone(v) and self.est_a_gauche_de_la_zone(v):
            if self.va_en_haut(v) and self.va_a_droite(v):
                return True   
            
        # en bas a droite
        elif self.est_en_bas_de_la_zone(v) and self.est_a_droite_de_la_zone(v):
            if self.va_en_haut(v) and self.va_a_gauche(v):
                return True 
        
        # Atterit
        elif self.est_dans_la_zone(v) and self.va_en_bas(v):
            return True
            
        else:
            return False
                

