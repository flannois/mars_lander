import pygame
from data import *
import math

class Affichage:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Mars Lander IA')
        
        # Initialisation de la fenêtre
        self.fenX = fenX // echelle
        self.fenY = fenY // echelle
        self.screen = pygame.display.set_mode((self.fenX, self.fenY))


    # Fonction pour dessiner la surface de Mars
    def dessiner_surface(self, surface_mars):
        for i in range(len(surface_mars) - 1):
            x1, y1 = surface_mars[i]
            x1, y1 = x1 // echelle, y1 // echelle
            x2, y2 = surface_mars[i + 1]
            x2, y2 = x2 // echelle, y2 // echelle

            pygame.draw.line(self.screen, ROUGE, (x1, y1), (x2, y2), 10)

    def dessiner_vaisseau(self, v, j):
        
        if not v.detruit:
            img = f'images/vaisseau{v.puissance}.png'
        else:
            img = "images/detruit.png"
        
        if v.est_pose:
            img = "images/vaisseauA.png"
        
        # Dessin vaisseau
        image = pygame.image.load(img)
        image = pygame.transform.rotate(image, v.angle)  # Pour incliner l'image selon l'angle
        self.rect = image.get_rect(center=(v.x // echelle, v.y // echelle))
        self.screen.blit(image, self.rect)

        # Dessin trainée
        centre_vaisseau = self.rect.center

        # Conversion en radians
        angle_radians = math.radians(v.angle)

        # Calcul du sinus et du cosinus
        sin = math.sin(angle_radians)
        cos = math.cos(angle_radians)

        v_bas_trainee = (centre_vaisseau[0] + sin * v.puissance * 30, centre_vaisseau[1] + cos * v.puissance * 30)

        match v.puissance:
            case 1:
                couleur = VERT
            case 2:
                couleur = JAUNE
            case 3:
                couleur = ORANGE
            case 4:
                couleur = ROUGE
            case _:
                couleur = GRIS
                    
        pygame.draw.line(self.screen, couleur, centre_vaisseau, v_bas_trainee, 5)


        

    def effacer_tout(self):
        self.screen.fill(BLANC)

    def affiche_info(self, nom, valeur, pos):
        font = pygame.font.Font(None, 36)
        valeur = round(valeur, 3)
        text = f"{nom} : {valeur}"
        text_a_afficher = font.render(text, True, NOIR)
        self.screen.blit(text_a_afficher, pos)

    def ecrire_info(self, v, ia, j):
        self.affiche_info("x",          v.x,        (10,0))
        self.affiche_info("y",          v.y,        (10,25))
        self.affiche_info("v_speed",    v.v_speed,  (10,50))
        self.affiche_info("h_speed",    v.h_speed,  (10,75))
        self.affiche_info("fuel",       v.fuel,     (10,100))
        self.affiche_info("angle",      v.angle ,   (10,125))
        self.affiche_info("puissance",  v.puissance,(10,150))
        self.affiche_info("gravite",    gravite,    (10,175))

        self.affiche_info("Img/sec",    img_par_sec,(500,0))

        if ia_active:

            self.affiche_info("Récompense",     ia.recompense,      (500,25))
            self.affiche_info("Cumul Recomp",   ia.recup_recompense(),(500,50))
            self.affiche_info("Q_TABLE",        len(ia.q_table),    (500,75))

            self.affiche_info("Tx ap",          ia.alpha,           (1000,0))
            self.affiche_info("Rec fut",        ia.gamma,           (1000,25))
            self.affiche_info("Tx exp",         ia.epsilon,         (1000,50))
            self.affiche_info("Tx ap",          ia.epsilon_decay,   (1000,75))
            
            self.affiche_info("Tentative",      j.tentative,        (1000,125))
            self.affiche_info("Atterissages",   j.att_reussi,       (1000,150))

            


        