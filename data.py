# Paramètres IA

# CHATGPT
#alpha=0.1
#gamma=0.9
#epsilon=1.0
#epsilon_decay=0.995


alpha = 0.1     # C'est le taux d'apprentissage. Il détermine dans quelle mesure les nouvelles informations vont remplacer les anciennes dans la Q-table. Un alpha plus élevé signifie que l'agent apprend plus rapidement, tandis qu'un alpha plus bas signifie qu'il apprend plus lentement.
gamma = 0.9     # C'est le facteur de discount. Il représente l'importance des récompenses futures par rapport aux récompenses immédiates. Un gamma proche de 1 signifie que l'agent valorise fortement les récompenses futures, tandis qu'un gamma proche de 0 signifie qu'il privilégie les récompenses immédiates.
epsilon = 0.8     # C'est le taux d'exploration. Il détermine la probabilité que l'agent choisisse une action aléatoire (exploration) plutôt que celle qui semble la meilleure selon sa Q-table (exploitation). Un epsilon élevé favorise l'exploration, tandis qu'un epsilon plus bas favorise l'exploitation.
epsilon_decay = 0.99991    # C'est le facteur de diminution de l'epsilon. Il détermine à quelle vitesse le taux d'exploration diminue au fil du temps. Cela permet à l'agent d'explorer davantage au début de l'apprentissage et d'exploiter ses connaissances acquises plus tard.

ia_active = True

if ia_active:
    affiche_espion = False
    img_par_sec = 10000
    gravite = 3.711
    gravite = 1
    angle_vaisseau_max = 90
else:
    affiche_espion = True
    img_par_sec = 5
    gravite = 0
    angle_vaisseau_max = 0 # 0 pour pas de limite


# Paramètre d'affichage
fenX = 7000
fenY = 3000
echelle = 5 # 1/echelle

degres_par_tour = 15

# Atterissage
max_v_speed = 40
max_h_speed = 20


# Couleurs
BLANC = (255, 255, 255)
BORDEAUX = (255, 100, 100)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
NOIR = (0, 0, 0)
GRIS = (127, 127, 127)
ORANGE = (255, 127, 0)
JAUNE = (255, 255, 0)
VERT = (0, 255, 0)

scenario0 = {
    "surface_mars"   : [(0,fenY - 200), (3000,fenY - 750), (4000,fenY - 750), (fenX,fenY - 200)],
    "vaisseau"  :{"x":2000,"y":fenY -2500,"h_speed":0,"v_speed":0,"fuel":1000,"rotate":0,"power":0}
}

scenario1 = {
    "surface_mars"   : [(0,fenY - 100), (1000,fenY - 500), (1500,fenY - 1500), (3000,fenY - 1000), (4000,fenY - 150), (5500,fenY - 150), (fenX,fenY - 800)],
    "vaisseau"  :{"x":2500,"y":fenY - 2700,"h_speed":0,"v_speed":0,"fuel":550,"rotate":0,"power":0}
}

scenario2 = {
    "surface_mars"   : [(0,fenY - 100), (1000,fenY - 500), (1500,fenY - 100), (3000,fenY - 100), (3500,fenY - 500), (3700,fenY - 200), (5000,fenY - 1500), (5800,fenY - 300), (6000,fenY - 1000), (fenX,fenY - 2000)],
    "vaisseau"  :{"x":6500,"y":fenY - 2800,"h_speed":-100,"v_speed":0,"fuel":600,"rotate":90,"power":0}
}

scenario3 = {
    "surface_mars"   : [(0,fenY - 100), (1000,fenY - 500), (1500,fenY - 1500), (3000,fenY - 1000), (4000,fenY - 150), (5500,fenY - 150), (fenX,fenY - 800)],
    "vaisseau"  :  {"x":6500,"y":fenY - 2800,"h_speed":-90,"v_speed":0,"fuel":750,"rotate":90,"power":0}
}

scenario4 = {
    "surface_mars"   : [(0,fenY - 1000), (300,fenY - 1500), (350,fenY - 1400), (500,fenY - 2000), (800,fenY - 1800), (1000,fenY - 2500), (1200,fenY - 2100), (1500,fenY - 2400), (2000,fenY - 1000), (2200,fenY -  500), (2500,fenY - 100), (2900,fenY - 800), (3000,fenY -  500), (3200,fenY -  1000), (3500,fenY -  2000), (3800,fenY -  800), (4000,fenY - 200), (5000,fenY - 200), (5500,fenY - 1500), (fenX,fenY - 2800)],
    "vaisseau"  :{"x":500,"y":fenY - 2700,"h_speed":100,"v_speed":0,"fuel":800,"rotate":-90,"power":0}
}

scenario5 = {
    "surface_mars"   : [(0,fenY - 1000), (300,fenY -  1500), (350,fenY -  1400), (500,fenY -  2100), (1500,fenY -  2100), (2000,fenY -  200), (2500,fenY -  500), (2900,fenY -  300), (3000,fenY -  200), (3200,fenY -  1000), (3500,fenY -  500), (3800,fenY -  800), (4000,fenY -  200), (4200,fenY -  800), (4800,fenY -  600), (5000,fenY -  1200), (5500,fenY -  900), (6000,fenY -  500), (6500,fenY -  300), (fenX,fenY -  500)],
    "vaisseau"  :  {"x":6500,"y":fenY - 2700,"h_speed":-50,"v_speed":0,"fuel":1000,"rotate":90,"power":0}
}


