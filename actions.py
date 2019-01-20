from random import choice, randint, choices, random, shuffle

from perso import *
sante, souffle, mental = '♥', '᯾', '◉'

class Action():
	def __init__(self, nom, cout=None, condition=None, attaque=None, defense=None, regeneration=None, apprentissage=None, effet=None):
		self.nom = nom
		self.cout = cout
		self.conditions = condition
		self.attaque = attaque
		self.defense = defense
		self.regeneration = regeneration
		self.apprentissage = apprentissage
		self.effet = effet
	def score(self):
		sc = 2
		if self.attaque:
			sc += sum(self.attaque.values())
		if self.defense:
			sc += sum(self.defense.values())
		if self.regeneration:
			sc += sum(self.regeneration.values())
		if self.cout:
			sc -= sum(self.cout.values())
		if self.conditions:
			sc -=2
		if self.effet:
			sc +=2
		return sc
	def repr(self):
		def repr_jauge(d):
			if d is None : return None
			representation = ''
			for k, v in d.items():
				if v > 0:
					representation += v*(k+' ')
			if representation != '' : return representation

		representation = []
		representation.append(self.nom.upper() + ' [{}]'.format(self.score()))
		if self.apprentissage : representation.append('Apprentissage : ' + self.apprentissage)
		if self.conditions : representation.append('Condition : ' + self.conditions)
		if repr_jauge(self.cout): representation.append('Coût : ' + repr_jauge(self.cout))
		if repr_jauge(self.attaque): representation.append('Attaque : ' + repr_jauge(self.attaque))
		if repr_jauge(self.defense): representation.append('Defense : ' + repr_jauge(self.defense))
		if repr_jauge(self.regeneration): representation.append('Regénération : ' + repr_jauge(self.regeneration))
		if self.effet : representation.append('Effet : ' + self.effet)
		
		return '\n'.join(representation)

brutes = [ogre, geant]

def creer_actions(perso):

	actions = []
	# Calcul du nombre d'action
	nb_action = randint(9,12)
	if perso.race in brutes:
		nb_action = randint(8,10)
	if perso.classe is magicien:
		nb_action = randint(10,12)

	########## TRIVIALES

	# frappe

	cout = choices([0, 1, 2], [10, 3, 1])[0]
	attaque = 1
	if perso.race in brutes :
		cout = 0
		attaque = randint(1,3)

	frappe = Action(
		nom = 'frappe',
		cout = {souffle:cout},
		attaque = {sante:attaque}
	)

	if random() < 0.99: actions.append(frappe)

	# repli

	cout = 0
	if perso.race in brutes :
		cout = choices([0, 1, 2], [10, 3, 1])[0]
	repli = Action(
		nom='repli',
		cout = {mental:cout},
		effet = "Le héro retourne sur le banc à la fin du tour, ses prochaines actions sont annulées."
	)

	if random() < 0.99: actions.append(repli)

	# abandon

	cout = 0
	if perso.race in brutes :
		cout = choices([0, 1, 2], [20, 3, 1])[0]
	abandon = Action(
		nom='abandon',
		cout = {mental:cout},
		effet = "Le héro quitte le combat immédiatement. Les actions de l'adversaire sont annulées"
	)

	if random() < 0.99: actions.append(abandon)
	
	# esquive
	
	cout = 0
	if perso.race not in brutes :
		cout = choices([0, 1], [5, 1])[0]

	esquive = Action(
		nom='esquive',
		condition=choice(['1/2 chances de réussir', '']),
		cout = {souffle:cout},
		defense = {sante:1}
	)

	if random() < 0.99: actions.append(esquive)
	
	# respiration

	regen = choices([1, 2, 3], [20, 3, 1])[0]

	respiration = Action(
		nom='respiration',
		regeneration = {souffle:regen}
	)

	if random() < 0.99: actions.append(respiration)
	
	########## SPECIALES


	actions_possibles = []
	set_actions_possibles = []

	#### SETS

	# potions
	set_actions_possibles.append([
		Action(
			condition='Ne peut être utilisé que 5 fois : □ □ □ □ □',
			nom='potion de vie',
			regeneration={sante:5},
		),
		Action(
			condition='Ne peut être utilisé que 5 fois : □ □ □ □ □',
			nom="potion d'endurence",
			effet="les prochaines actions du tour ne coûtent pas d'᯾",
		),
		Action(
			condition='Ne peut être utilisé que 5 fois : □ □ □ □ □',
			nom="potion de force",
			effet='la prochaine action a son attaque multipliée par deux.',
		),
	])

	# insecte
	set_actions_possibles.append([
		# + variation sur les insecte
		Action(
			nom="nuée d'insecte",
			cout={souffle:randint(2,3)},
			attaque={sante:randint(1,2),mental:randint(1,2)},
			defense={sante:randint(1,2),mental:randint(1,2)},
		),
		Action(
			apprentissage="Avoir lancé trois nuées d'insectes : □ □ □",
			nom="fléau d'insecte",
			cout={souffle:randint(4,5)},
			attaque={sante:randint(3,4),mental:randint(3,4)},
			defense={sante:randint(1,2),mental:randint(1,2)},
		),
	])

	# fourbe
	set_actions_possibles.append([
		# + variation sur les insecte
		Action(
			nom="cracher au visage",
			cout={souffle:randint(0,1)},
			attaque={mental:1}
		),
		Action(
			nom="insulter",
			cout={mental:2},
			attaque={mental:2},
			defense={mental:1},
		),
	])

	# guerisseur
	set_actions_possibles.append([
		Action(
			nom="soin primaire",
			cout={souffle:randint(0,1)},
			regeneration={sante:1}
		),
		Action(
			nom="soin total",
			cout={souffle:3},
			regeneration={sante:2},
			effet="tous les héros de l'équipe ont regeneration ♥ ♥",
			defense={sante:1}
		),
		Action(
			nom="sauvetage",
			cout={souffle:3},
			regeneration={sante:1},
			effet="une des jauges d'un des héros de l'équipe est remplie de {}".format(randint(6,8)),
			defense={mental:1}
		),
	])


	#### CLASSE

	# guerrier
	if perso.classe is guerrier or random() > 0.99:
		
		actions_possibles.append(Action(
			nom='parade',
			cout={souffle:2},
			defense={sante:1, mental:1},
			attaque={souffle:1}
		))
		actions_possibles.append(Action(
			nom="coup d'épée",
			cout={souffle:1},
			defense={sante:1},
			attaque={sante:randint(1,2)}
		))
		actions_possibles.append(Action(
			nom='riposte',
			cout={souffle:1},
			attaque={sante:randint(1,3)},
			defense={sante:1},
			effet="ne coûte rien si l'action précédente du tour était une parade"
		))

	# rodeurs
	if perso.classe is rodeur or random() > 0.99:
		
		actions_possibles.append(Action(
			nom='camoufflage',
			cout={souffle:2},
			defense={sante:1, mental:1},
			attaque={souffle:1}
		))
		actions_possibles.append(Action(
			apprentissage="s'être déjà replié : □",
			nom="faux repli",
			effet="sur la prochaine action de l'adversaire, la défense est annulée",
			cout={souffle:1},
			attaque={mental:randint(0,1)}
		))
		actions_possibles.append(Action(
			nom='coup dans le dos',
			cout={souffle:2},
			attaque={sante:randint(2,3)},
		))

	# magicien
	if perso.classe is magicien or random() > 0.99:
		
		actions_possibles.append(Action(
			nom='éblouir',
			cout={souffle:2},
			defense={sante:2, mental:1},
			attaque={sante:1}
		))
		actions_possibles.append(Action(
			apprentissage="Avoir déjà fait la même action que son adversaire : □",
			nom="miroir",
			effet="reproduit les effets, l'attaque et la défense du coup adverse",
			cout={souffle:1},
		))
		actions_possibles.append(Action(
			nom='maudire',
			cout={souffle:randint(1,2)},
			attaque={mental:2},
		))
		actions_possibles.append(Action(
			nom='bénir',
			cout={souffle:randint(1,2)},
			effet="un des héro de l'équpe gagne ♥ ᯾ ᯾ ◉ ◉ ◉"
		))

	#### RACE

	# ogres
	if perso.race is ogre or random() > 0.99:
		
		actions_possibles.append(Action(
			nom='haleine qui pue',
			cout={souffle:2},
			attaque={sante:1,souffle:1}
		))
		actions_possibles.append(Action(
			nom='bouh !',
			cout={souffle:1},
			defense={mental:1},
			attaque={mental:1}
		))
		actions_possibles.append(Action(
			nom='morsure',
			attaque={sante:1}
		))

	# sans-âme
	if perso.race is sansame or random() > 0.99:
		
		puissance = randint(1,3)
		actions_possibles.append(Action(
			nom='cri strident',
			cout={souffle:puissance},
			attaque={mental:puissance}
		))
		puissance = randint(1,2)
		actions_possibles.append(Action(
			nom='sacrifice',
			cout={sante:puissance},
			regeneration={souffle:puissance+1}
		))
		actions_possibles.append(Action(
			nom='hurlement',
			apprentissage='avoir été eu sa jauge de ♥ dans le seuil critique : □',
			cout={souffle:3, sante:1},
			attaque={sante:3},
			defense={mental:3}
		))
		# actions_possibles.append(Action(
		# 	nom='tenebres',
		# 	attaque={sante:1}
		# ))

	# geant
	if perso.race is geant or random() > 0.99:
		actions_possibles.append(Action(
			nom='piétiner',
			cout={souffle:1},
			attaque={sante:2}
		))

	shuffle(actions_possibles)
	shuffle(set_actions_possibles)
	if random()>0.6:
		set_actions = set_actions_possibles.pop()
		for i in range(0, randint(0,len(set_actions))):
			actions.append(set_actions[i])

	while len(actions) < nb_action and len(actions_possibles)>0:
		actions.append(actions_possibles.pop())

	return actions