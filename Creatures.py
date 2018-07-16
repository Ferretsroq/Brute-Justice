import Characters
import skills

class Creature:
    def __init__(self,
                 name = '',
                 level=0,
                 hp=0,
                 armor=0,
                 inputSkills=[]):
        self.name = name
        self.level = level
        self.maxHP = hp
        self.hp = hp
        self.armor = armor
        self.skills = []
        for skill in inputSkills:
            if(skills.isSkill(skill[0])):
                self.skills.append(skill)
    def Attack(self, target, stat=Characters.Stat.Speed, defenseEffort=0):
        print('{} attacks {}.'.format(self.name, target.name))
        attackLevel = self.level
        for skill in self.skills:
            if(skill[0].name == 'Attack' and skill[0].stat == stat):
                attackLevel = skill[1]
        attackResult = target.Challenge(attackLevel, 
                                        skills=['{} Defense'.format(stat.name)], 
                                        stat=stat,
                                        effort=defenseEffort)
        if(not attackResult):
            target.intellect.reduce(target.speed.reduce(target.might.reduce(self.level)))
    def isDead(self):
        return self.hp <= 0