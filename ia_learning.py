class IALearning:
    def __init__(self, actions, alpha, gamma, epsilon, epsilon_decay, ia_active):
        self.actions = actions # C'est une liste des actions possibles que l'IA peut entreprendre. Cela définit l'espace d'action pour l'agent.
        self.alpha = alpha # C'est le taux d'apprentissage. Il détermine dans quelle mesure les nouvelles informations vont remplacer les anciennes dans la Q-table. Un alpha plus élevé signifie que l'agent apprend plus rapidement, tandis qu'un alpha plus bas signifie qu'il apprend plus lentement.
        self.gamma = gamma # C'est le facteur de discount. Il représente l'importance des récompenses futures par rapport aux récompenses immédiates. Un gamma proche de 1 signifie que l'agent valorise fortement les récompenses futures, tandis qu'un gamma proche de 0 signifie qu'il privilégie les récompenses immédiates.
        self.epsilon = epsilon # C'est le taux d'exploration. Il détermine la probabilité que l'agent choisisse une action aléatoire (exploration) plutôt que celle qui semble la meilleure selon sa Q-table (exploitation). Un epsilon élevé favorise l'exploration, tandis qu'un epsilon plus bas favorise l'exploitation.
        self.epsilon_decay = epsilon_decay # C'est le facteur de diminution de l'epsilon. Il détermine à quelle vitesse le taux d'exploration diminue au fil du temps. Cela permet à l'agent d'explorer davantage au début de l'apprentissage et d'exploiter ses connaissances acquises plus tard.
        self.q_table = {} # C'est une table qui stocke les valeurs Q pour chaque état-action. Ces valeurs indiquent la qualité d'une action dans un état donné, permettant à l'agent de prendre des décisions éclairées.
        self.recompense = 0 # Cette variable sert à stocker la récompense reçue après une action. Cela permet de mettre à jour la Q-table en fonction de l'expérience de l'agent.
        self.recompences_cumulees = []  # C'est une liste qui suit les récompenses cumulées au fil du temps. Cela peut aider à évaluer la performance de l'agent pendant l'apprentissage.
        self.ia_active = ia_active

    def recupere_etat(self, vaisseau, surface):
        if self.ia_active:
            # État défini par position, vitesse horizontale et verticale, carburant, et si en zone d'atterrissage
            return (int(vaisseau.x), int(vaisseau.y), 
                    int(vaisseau.h_speed), int(vaisseau.v_speed),
                    int(vaisseau.angle), int(vaisseau.fuel),
                    surface.est_dans_la_zone(vaisseau))

    def choisir_action(self, etat):
        if self.ia_active:
            # Choisir une action basée sur l'état courant en utilisant epsilon
            if random.uniform(0, 1) < self.epsilon:
                return random.choice(self.actions)  # Exploration
            else:
                return self.meilleure_action(etat)  # Exploitation

    def meilleure_action(self, etat):
        if self.ia_active:
            # Trouver la meilleure action pour un état donné
            if etat not in self.q_table:
                self.q_table[etat] = np.zeros(len(self.actions))
            return self.actions[np.argmax(self.q_table[etat])]

    def update_q_table(self, etat, action, recompense, next_etat):
        if self.ia_active:
            # Mise à jour de la Q-table pour améliorer la prise de décision
            if etat not in self.q_table:
                self.q_table[etat] = np.zeros(len(self.actions))
            if next_etat not in self.q_table:
                self.q_table[next_etat] = np.zeros(len(self.actions))

            # Indice de l'action pour mise à jour
            action_index = self.actions.index(action)
            best_future_q = np.max(self.q_table[next_etat])
            
            # Equation de mise à jour Q-learning
            self.q_table[etat][action_index] += self.alpha * (recompense + self.gamma * best_future_q - self.q_table[etat][action_index])

    def recupere_recompense(self, a, v, s):
        if self.ia_active:

            #recompense = 100 - abs(v.v_speed) - abs(v.h_speed) 
            recompense = 0
            recompense += 1     if not  v.detruit   and not v.est_pose else -10
            recompense += 100   if not  v.detruit   and     v.est_pose else -1
            recompense += 50    if      v.detruit   and     v.est_pose else -50
            
            recompense += 5     if      v.peut_atterir()        else -1

            recompense += 5     if -30 <= abs(v.angle) <= 30    else -1
            recompense += 5     if abs(v.h_speed) < max_h_speed else -1
            recompense += 5     if abs(v.v_speed) < max_v_speed else -1
            recompense += 50    if s.est_dans_la_zone(v)        else -1

            recompense += 10    if s.se_rapproche_de_la_zone(v) else -10

            

            self.recompense = recompense
            return recompense

    def decay_epsilon(self):
        if self.ia_active:
            # Réduire l'exploration au fil du temps
            self.epsilon = max(0.01, self.epsilon * self.epsilon_decay)

    def ajout_recompense_cumulative(self, recompence):
        if self.ia_active:
            if len(self.recompences_cumulees) == 0:
                self.recompences_cumulees.append(recompence)
            else:
                self.recompences_cumulees.append(self.recompences_cumulees[-1] + recompence)

    def ia_appui(self, key):
        if self.ia_active:
            return key