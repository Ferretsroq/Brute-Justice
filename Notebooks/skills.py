from enum import Enum

class Skill:
    def __init__(self, name='', stat=0):
        self.name = name
        self.stat = Stat(stat)
    def __repr__(self):
        return "{}: {}".format(self.name, self.stat)

class Stat(Enum):
    Might = 0
    Speed = 1
    Intellect = 2


socialSkills = {'Rapport': Skill('Rapport', Stat.Intellect),
                             'Bluff': Skill('Bluff', Stat.Intellect)}
adventuringSkills = { 'Athletics': Skill('Athletics', Stat.Might),
                                   'Acrobatics': Skill('Acrobatics', Stat.Speed),
                                   'Perception': Skill('Perception', Stat.Intellect),
                                   'Nature': Skill('Healing', Stat.Intellect),
                                   'Stealth': Skill('Stealth', Stat.Speed),
                                   'Investigation': Skill('Investigation', Stat.Intellect),
                                   'Thievery': Skill('Thievery', Stat.Speed)}
numeneraSkills = {'Mechanical': Skill('Mechanical', Stat.Intellect),
                               'Biological': Skill('Biological', Stat.Intellect),
                               'Crystalline': Skill('Crystalline', Stat.Intellect),
                               'Energy': Skill('Energy', Stat.Intellect),
                               'Psychic': Skill('Psychic', Stat.Intellect),
                               'Temporal': Skill('Psychic', Stat.Intellect) }
craftingSkills = {'Weapons': Skill('Weapons', Stat.Intellect),
                               'Armor': Skill('Armor', Stat.Intellect),
                               'Devices': Skill('Devices', Stat.Intellect),
                               'Tools': Skill('Tools', Stat.Intellect),
                               'Consumables': Skill('Consumables', Stat.Intellect),
                               'Breeding': Skill('Breeding', Stat.Intellect),
                               'Animal Raising': Skill('Animal Raising', Stat.Intellect)}
combatSkills = {'Might Attack': Skill('Attack', Stat.Might),
                        'Speed Attack': Skill('Attack', Stat.Speed),
                        'Intellect Attack': Skill('Attack', Stat.Intellect),
                        'Might Defense': Skill('Defense', Stat.Might),
                        'Speed Defense': Skill('Defense', Stat.Speed),
                        'Intellect Defense': Skill('Defense', Stat.Intellect),
                        'Initiative': Skill('Initiative', Stat.Speed),
                        'Light Weapons': Skill('Light Weapons', Stat.Speed),
                        'Medium Weapons': Skill('Medium Weapons', Stat.Might),
                        'Heavy Weapons': Skill('Heavy Weapons', Stat.Might)}
skills = {**socialSkills, **adventuringSkills, **numeneraSkills, **craftingSkills, **combatSkills}
        
def isSkill(skill):
  return skill in skills
def isAdventuringSkill(skill):
  return skill in adventuringSkills
def isCombatSkill(skill):
  return skill in combatSkills
def isCraftingSkill(skill):
  return skill in craftingSkills
def isNumeneraSkill(skill):
  return skill in numeneraSkills
def isSocialSkill(skill):
  return skill in socialSkills