from random import choices, choice, randint
h,f, = 'mâle', 'femelle'

class Classe():
	def __init__(self, denomination, titres):
		self.denomination = denomination
		self.titres = titres

guerrier = Classe(
	denomination = {h:'guerrier', f:'guerrière'},
	titres={h:('le grand', 'le guerrier'), f:('la tempête', 'la chevalière')}
)
magicien = Classe(
	denomination = {h:'magicien', f:'magicienne'},
	titres={h:('de la confrérie', 'des plaines'), f:('flamme du déstin', 'des 7 vents')}
)
rodeur = Classe(
	denomination = {h:'rodeur', f:'rodeuse'},
	titres={h:('l\'obscur', 'le sombre'), f:('des bois', 'la lame')}
)

classes = [guerrier, magicien, rodeur]

class GenerateurDeNom():
	def __init__(self, n, syl=None, fin=None):
		self.n = n
		self.syl = syl
		self.fin = fin

	def generer(self, genre):
		n = randint(*self.n)
		if self.syl:
			nom = choices(self.syl, k=n)
		if self.fin:
			nom.append(choice(self.fin[genre]))
		return ''.join(nom)

class Race():
	def __init__(self, denomination, classes, nom, sante, souffle, mental):
		self.denomination = denomination
		self.classes = classes
		self.nom = nom
		self.sante = sante
		self.souffle = souffle
		self.mental = mental

		
humain = Race(
	denomination = {h:'humain', f:'humaine'},
	classes = [guerrier, magicien, rodeur],
	nom = GenerateurDeNom(
		n=(2,3),
		syl=('gar','fou','nor', 'lau', 'syl', 'té'),
		fin= {h:('rent', 'vain'), f:('nette', 'rie')}
	),
	sante=(10,13),
	souffle=(10,13),
	mental=(10,13),
)
ogre = Race(
	denomination = {h:'ogre', f:'ogresse'},
	classes = [guerrier, magicien],
	nom = GenerateurDeNom(
		n=(1,1),
		syl=('ku', 'ha', 'hu', 'haou'),
		fin= {h:('croc', 'cro'), f:('crie')}
	),
	sante=(10,13),
	souffle=(14,18),
	mental=(5,9),
)
geant = Race(
	denomination = {h:'géant', f:'géante'},
	classes = [guerrier],
	nom = GenerateurDeNom(
		n=(1,1),
		syl=('mo', 'fo', 'go', 'pi', 'ko'),
	),
	sante=(14,18),
	souffle=(10,13),
	mental=(5,9),
)
sansame = Race(
	denomination = {h:'sans-âme', f:'sans-âme'},
	classes = [rodeur, magicien],
	nom = GenerateurDeNom(
		n=(1,3),
		syl=('ci', 'cus', 'cien', 'rix', 'clus'),
		fin= {h:('rus', 'cruss'), f:('ris', 'criss')}
	),
	sante=(8,10),
	souffle=(10,12),
	mental=(14,18),
)
races = [(humain, 60),(ogre, 10),(geant, 5),(sansame, 5)]

