import Characters
import skills
import random

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
            if(skills.isSkill(skill)):
                self.skills.append(skill)
    def Attack(self, target, stat=Characters.Stat.Speed, defenseEffort=0):
        print('{} attacks {}.'.format(self.name, target.name))
        attackLevel = self.level
        for skill in self.skills:
            if(skill == '{} Attack'.format(stat.name)):
                attackLevel += 1
        attackResult = target.Challenge(attackLevel, 
                                        skills=['{} Defense'.format(stat.name)], 
                                        stat=stat,
                                        effort=defenseEffort)
        if(not attackResult):
            #target.intellect.reduce(target.speed.reduce(target.might.reduce(self.level)))
            target.TakeDamage(self.level)
    def isDead(self):
        return self.hp <= 0
    def roll(self):
        """Roll 1d20"""
        return random.randint(1,20)
    def Challenge(self, level=0, skills=[], stat=None, effort=None):
        """Similar to Character.Challenge, but creatures have no effort nor stats, then roll 1d20 to resolve a task"""
        skillCounter = 0
        for skill in skills:
            if skill in self.skills:
                skillCounter += 1
        
        target = (level - skillCounter)*3
        print('Target number: {}'.format(target))
        if(target <= 0):
            return True
        else:
            roll = self.roll()
            print('{} rolled {}.'.format(self.name, roll))
            return roll >= target
    def TakeDamage(self, damage):
        self.hp -= damage