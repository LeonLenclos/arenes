from random import choices, choice, randint
from actions import *
from perso import *

class Hero():
	def __init__(self):

		self.race = choices([r for r,w in races], [w for r,w in races])[0]
		self.classe = choice([c for c in classes if c in self.race.classes])
		self.genre = choice([h, f])
		prenom = self.race.nom.generer(self.genre)
		titre = choice(list(self.classe.titres[self.genre]))
		self.nom = "{} {}".format(prenom, titre) 
		self.actions = creer_actions(self)
		self.jauges = {
			sante:randint(*self.race.sante),
			souffle:randint(*self.race.souffle),
			mental:randint(*self.race.mental),
		}

	def score(self):
		return int(sum(self.jauges.values())/2 + sum([a.score() for a in self.actions]))
	def repr(self):

		return "{nom} ({race} {classe}) [{score}]\n{jauges}\n\n{actions}".format(
			nom = self.nom.title(),
			race = self.race.denomination[self.genre],
			classe = self.classe.denomination[self.genre],
			score=self.score(),
			jauges= '\n'.join(['{} ({})'.format((k+' ')*v, v) for k, v in self.jauges.items()]),
			actions = '\n\n'.join(['{}. {}'.format(i+1,a.repr()) for i, a in enumerate(self.actions)]))

print("")

print(Hero().repr())
print("")