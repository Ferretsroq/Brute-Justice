from enum import Enum
import random
import skills
import BruteJusticeSpreadsheets

class Stat(Enum):
	"""Simple Enum for identifying stat pools"""
	Might = 0
	Speed = 1
	Intellect = 2

class Weapon(Enum):
	"""Simple Enum for identifying how much damage a weapon deals"""
	Light = 2
	Medium = 4
	Heavy = 6

class Pool:
	"""Class that holds methods relating to a character's pool"""
	def __init__(self, current=0, maximum=0, edge=0):
		"""Define the max of the pool, current value, and the character's edge"""
		self.max = maximum
		self.current = current
		self.edge = edge
	def __repr__(self):
		return "{}/{}".format(self.current, self.max)
	def reduce(self, amount):
		"""Reduce the pool by the specified amount. If there is not enough to redue,
		instead return the remainder to reduce from the next pool."""
		if(self.current > 0):
			difference = self.current - amount
			if(difference >= 0):
				self.current -= amount
				return 0
			else:
				self.current = 0
				return abs(difference)
		else:
			return amount
	def increase(self, amount):
		"""Increase the pool by the specified amount, capped to the maximum value."""
		if(self.current < self.max):
			self.current += amount
			self.current = min(self.current, self.max)
	def effort(self, num):
		"""Spend effort from the pool, taking edge into account"""
		spent = max(0, (num*3) - self.edge)
		if(spent <= self.current):
			self.reduce(spent)
			return True
		else:
			print("Not enough to spend {} effort.\nCurrent: {}\nRequired: {}".format(num, self.current, spent))
			return False

class Character:
	"""Holds information about a character."""
	def __init__(self, name='',
				 mightCurrent=0,
				 speedCurrent=0,
				 intellectCurrent=0, 
                 mightMax=0, 
                 speedMax=0, 
                 intellectMax=0, 
                 mightEdge=0, 
                 speedEdge=0, 
                 intellectEdge=0,
                 inputSkills = [],
                 weapon = Weapon.Light):
		"""Initialize the character pools, skills, and weapon damage"""
		self.name = name
		self.might = Pool(mightCurrent, mightMax, mightEdge)
		self.speed = Pool(speedCurrent, speedMax, speedEdge)
		self.intellect = Pool(intellectCurrent, intellectMax, intellectEdge)
		self.adventureSkills = []
		self.combatSkills = []
		self.craftingSkills = []
		self.numeneraSkills = []
		self.socialSkills = []
		for skill in inputSkills:
			if(skills.isSkill(skill)):
				if(skills.isAdventuringSkill(skill)):
					self.adventureSkills.append(skill)
				elif(skills.isCombatSkill(skill)):
					self.combatSkills.append(skill)
				elif(skills.isCraftingSkill(skill)):
					self.craftingSkills.append(skill)
				elif(skills.isNumeneraSkill(skill)):
					self.numeneraSkills.append(skill)
				elif(skills.isSocialSkill(skill)):
					self.socialSkills.append(skill)
		self.skills = self.adventureSkills + \
                      self.combatSkills + \
                      self.craftingSkills + \
                      self.numeneraSkills + \
                      self.socialSkills
		self.weapon = weapon
	def roll(self):
		"""Roll 1d20"""
		return random.randint(1,20)
	def Challenge(self, level=0, skills=[], stat=Stat.Might, effort=0, assets=0):
		"""Apply effort and relevant skills, then roll 1d20 to resolve a task"""
		skillCounter = 0
		for skill in skills:
			if skill in self.skills:
				skillCounter += 1
		if(self.Effort(stat, effort)):
			target = (level - skillCounter - effort - assets)*3
		else:
			target = (level - skillCounter - assets)*3
		print('Target number: {}'.format(target))
		if(target <= 0):
			return True
		else:
			roll = self.roll()
			print('{} rolled {}.'.format(self.name, roll))
			return roll >= target
	def Effort(self, stat=Stat.Might, num=1):
		"""Apply effort to the relevant pool"""
		if(stat == Stat.Might):
			return self.might.effort(num)
		elif(stat == Stat.Speed):
			return self.speed.effort(num)
		elif(stat == Stat.Intellect):
			return self.intellect.effort(num)
	def isDead(self):
		"""Report whether or not the character is dead"""
		return self.might.current==0 and \
			   self.speed.current == 0 and \
               self.intellect.current == 0
	def Attack(self, creature, stat=Stat.Speed, effort=0, assets=0):
		"""Special case of Challenge, to target a specific creature"""
		print('{} attacks {}.'.format(self.name, creature.name))
		result = self.Challenge(level=creature.level, skills=['{} Attack'.format(stat.name), '{} Weapons'.format(self.weapon.name)], effort=effort, assets=assets)
		if(result):
			creature.hp -= self.weapon.value
	def __repr__(self):
		adventuring = 'ADVENTURING SKILLS:\n' + '\n'.join(self.adventureSkills) + '\n'
		combat = '\nCOMBAT SKILLS:\n' + '\n'.join(self.combatSkills) + '\n'
		crafting = '\nCRAFTING SKILLS:\n' + '\n'.join(self.craftingSkills) + '\n'
		numenera = '\nNUMENERA SKILLS:\n' + '\n'.join(self.numeneraSkills) + '\n'
		social = '\nSOCIAL SKILLS:\n' + '\n'.join(self.socialSkills) + '\n'
		skills = '\n' + adventuring + combat + crafting + numenera + social
		return "Name: {}\nMight: {}\nSpeed: {}\nIntellect: {}\nSkills: {}".format(self.name, self.might, self.speed, self.intellect, skills)



def LoadCharacter(sheetID):
	data = BruteJusticeSpreadsheets.ReadSpreadsheet(['Info', 'Pools', 'Skills'], sheetID)
	info = data[0]
	pools = data[1]
	skillsData = data[2]
	name = info[0][1]
	descriptor = info[1][1]
	focus = info[2][1]
	mightCurrent = int(pools[0][1])
	speedCurrent = int(pools[1][1])
	intellectCurrent = int(pools[2][1])
	mightMax = int(pools[0][2])
	speedMax = int(pools[1][2])
	intellectMax = int(pools[2][2])
	mightEdge = int(pools[0][3])
	speedEdge = int(pools[1][3])
	intellectEdge = int(pools[2][3])
	skillsList = []
	for skill in skillsData:
		if skills.isSkill(skill[0]):
			skillsList.append(skill[0])
	return Character(name=name,
					 mightCurrent=mightCurrent,
					 speedCurrent=speedCurrent,
					 intellectCurrent=intellectCurrent,
					 mightMax=mightMax,
					 speedMax=speedMax,
					 intellectMax=intellectMax,
					 mightEdge=mightEdge,
					 speedEdge=speedEdge,
					 intellectEdge=intellectEdge,
					 inputSkills=skillsList)
