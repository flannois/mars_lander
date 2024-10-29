from data import *
import pygame

import math

class Vaisseau:
    def init_vaisseau(self, info):
        
        self.x =            info['x']
        self.y =            fenY - info['y']
        self.h_speed =      info['h_speed']
        self.v_speed =      info['v_speed']
        self.fuel =         info['fuel']
        self.angle =        info['rotate']
        self.puissance =    info['power']
        self.detruit =      False

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
            return True
        else:
            return False

    def actualisation(self):
        if self.fuel <= 0:
            self.puissance = 0
        
        if not self.detruit:
            self.fuel -= self.puissance
        
            # Calcul des vitesses
            self.v_speed += gravite

            # Conversion en radians
            angle_radians = math.radians(self.angle)

            # Calcul du sinus et du cosinus
            sin = math.sin(angle_radians)
            cos= math.cos(angle_radians)

            # Calcul trigo pour vitesse
            self.v_speed -= self.puissance * cos
            self.h_speed -= self.puissance * sin

            # Calcul des positions
            self.y += self.v_speed
            self.x += self.h_speed

    def peut_atterir(self):
        if self.angle == 0 and abs(self.v_speed) < 40 and abs(self.h_speed) < 20:
           
            return True
        else:
            
            return False

    


class Surface:
    def __init__(self, mars_surface):
        self.mars_surface = mars_surface

    def calcul_zone_atterissage(self):
        surf = scenar['surface_mars']
        for i in range(len(surf) -1):
            p1X, p1Y = surf[i]
            p2X, p2Y = surf[i+1]
            if p1Y == p2Y:
                self.atterissage = ((p1X, p1Y),(p2X, p2Y))

        
   

class Affichage:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Mars Lander IA')
        
        # Initialisation de la fenêtre
        self.fenX = fenX // echelle
        self.fenY = fenY // echelle
        self.screen = pygame.display.set_mode((self.fenX, self.fenY))

        # Couleur de l'arrière-plan
        self.BLANC = (255, 255, 255)
        self.ROUGE = (255, 0, 0)

    # Fonction pour dessiner la surface de Mars
    def dessiner_surface(self, surface_mars):
        for i in range(len(surface_mars) - 1):
            x1, y1 = surface_mars[i]
            x1, y1 = x1 // echelle, y1 // echelle
            x2, y2 = surface_mars[i + 1]
            x2, y2 = x2 // echelle, y2 // echelle

            pygame.draw.line(self.screen, self.ROUGE, (x1, self.fenY - y1), (x2, self.fenY - y2), 2)

    def dessiner_vaisseau(self, vaisseau):
        
        if not vaisseau.detruit:
            
            img = f'images/vaisseau{vaisseau.puissance}.png'
        else:
            
            img = "images/detruit.png"
        
        image = pygame.image.load(img)
        image = pygame.transform.rotate(image, vaisseau.angle)  # Pour incliner l'image selon l'angle
        self.rect = image.get_rect(center=(vaisseau.x // echelle, vaisseau.y // echelle))
        self.screen.blit(image, self.rect)

    def effacer_tout(self):
        self.screen.fill(self.BLANC)

    def affiche_info(self, nom, valeur, pos):
        font = pygame.font.Font(None, 36)
        valeur = round(valeur, 3)
        text = f"{nom} : {valeur}"
        text_a_afficher = font.render(text, True, NOIR)
        self.screen.blit(text_a_afficher, pos)

    def traduction_angle(self, angle):
        calcul = angle % 360
        
        return calcul

    def ecrire_info(self, vaisseau):
        self.affiche_info("x",          vaisseau.x,             (10,0))
        self.affiche_info("y",          vaisseau.y,             (10,25))
        self.affiche_info("v_speed",    vaisseau.v_speed,       (10,50))
        self.affiche_info("h_speed",    vaisseau.h_speed,       (10,75))
        self.affiche_info("fuel",       vaisseau.fuel,          (10,100))
        self.affiche_info("angle",      self.traduction_angle(vaisseau.angle) , (10,125))
        self.affiche_info("puissance",  vaisseau.puissance,     (10,150))
        self.affiche_info("gravite",    gravite,                (10,175))
    

class Jeu:
    def actualisation(self, v, a, s):
        # VAISSEAU
        v.actualisation()
        v.verif_si_HS()

        # AFFICHAGE
        a.effacer_tout()
        a.ecrire_info(v)
        a.dessiner_vaisseau(v)
        a.dessiner_surface(s.mars_surface)
        
        pygame.display.flip()
        
        
    def touche_mars(self, a, v, s):
        points = []
        for i in range(len(s.mars_surface) - 1):
            pt1, pt2 = s.mars_surface[i]
            pt3, pt4 = s.mars_surface[i + 1]

            pt1 = pt1 // echelle
            pt2 = (fenY // echelle) - (pt2 // echelle)
            pt3 = pt3 // echelle
            pt4 = (fenY // echelle) - (pt4 // echelle)

            points.append(((pt1, pt2), (pt3, pt4)))

        crash = True if any(a.rect.clipline(*point) for point in points) else False
        if crash:
            v.detruit = True
           
    def fin_du_jeu(self, v):
        if v.detruit:
            v.v_speed = 0
            v.h_speed = 0

    def je_relance_le_jeu(self, v):
        v = None
        v = Vaisseau()
        v.init_vaisseau(scenar['vaisseau'])
        return v
    
scenar = scenario0

# Initialisation des objets
v = Vaisseau()
v.init_vaisseau(scenar['vaisseau'])
s = Surface(scenar['surface_mars'])
a = Affichage()
j = Jeu()

zone = s.calcul_zone_atterissage()

clock = pygame.time.Clock()

# Boucle Pygame
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        v = j.je_relance_le_jeu(v)
    
    if keys[pygame.K_LEFT]:
        v.angle += degres_par_tour
    if keys[pygame.K_RIGHT]:
        v.angle -= degres_par_tour
    if keys[pygame.K_1]:
        v.puissance = 0
    if keys[pygame.K_2]:
        v.puissance = 1
    if keys[pygame.K_3]:
        v.puissance = 2
    if keys[pygame.K_4]:
        v.puissance = 3
    if keys[pygame.K_5]:
        v.puissance = 4
    
    clock.tick(img_par_sec)
    
    
    
    j.actualisation(v, a, s)
    j.touche_mars(a, v, s)

    v.peut_atterir()

    j.fin_du_jeu(v)
    
    
   
