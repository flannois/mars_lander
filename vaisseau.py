from data import *
import math

class Vaisseau:
    def init_vaisseau(self, info):
        
        self.x =            info['x']
        self.y =            info['y']
        self.h_speed =      info['h_speed']
        self.v_speed =      info['v_speed']
        self.fuel =         info['fuel']
        self.angle =        info['rotate']
        self.puissance =    info['power']
        self.detruit =      False
        self.est_pose =     False

    def en_dehors_de_la_zone(self):
        if not 0 < self.x < fenX or not 0 < self.y < fenY:
            return True
        else:
            return False

    def verif_si_HS(self):

        if self.en_dehors_de_la_zone():
            self.detruit = True
            return True
        else:
            return False

    def a_plus_dessence(self):
        if self.fuel <= 0:
            self.fuel = 0
            return True
        else:
            return False

    def actualisation(self):
        if self.fuel <= 0 or self.detruit or self.est_pose:
            self.puissance = 0
        
        if not self.detruit and not self.est_pose:
           
            self.fuel -= self.puissance
        
            # Calcul des vitesses
            self.v_speed += gravite

            # Blocage par angle max
            if not angle_vaisseau_max == 0:
                if self.angle < -angle_vaisseau_max:
                    self.angle = -angle_vaisseau_max
                elif self.angle > angle_vaisseau_max:
                    self.angle = angle_vaisseau_max

            # Conversion en radians
            angle_radians = math.radians(self.angle)

            # Calcul du sinus et du cosinus
            sin = math.sin(angle_radians)
            cos = math.cos(angle_radians)

            # Calcul trigo pour vitesse
            self.v_speed -= self.puissance * cos
            self.h_speed -= self.puissance * sin

            # Calcul des positions
            self.y += self.v_speed
            self.x += self.h_speed

    def peut_atterir(self):
        if self.angle == 0 and abs(self.v_speed) < max_v_speed and abs(self.h_speed) < max_h_speed:
            return True
        else:
            return False