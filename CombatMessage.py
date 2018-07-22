import discord
import asyncio
import Characters
import Creatures
import BruteJusticeSpreadsheets

emojiCheck = '\u2705'
emojiQuestion = '\u2754'
emojiNumbers = ['0\u20e3',
				'1\u20e3',
				'2\u20e3',
				'3\u20e3',
				'4\u20e3',
				'5\u20e3',
				'6\u20e3',
				'7\u20e3',
				'8\u20e3',
				'9\u20e3']
class CombatMessage:
	"""Hold information about a combat message sent to Discord"""
	def __init__(self, name='', enemies=[], player=''):
		"""Initialize the fields for a message"""
		self.name = name
		self.combat = Combat()
		#self.enemies = enemies
		self.enemies = self.combat.creatures
		self.numEnemies = len(self.enemies)
		self.embed = discord.Embed(title=":crossed_swords: **FIGHT** :crossed_swords:", description=player)
		self.embed.add_field(name="Character", value=self.name, inline=False)
		self.character = Characters.LoadCharacter("1Zni4ySL3zN_SR7DNs-3XQRrya4KZ3RY6C2VtRz6JC_k")
		#self.creatures = []
		self.creatures = self.combat.creatures
		for enemy in range(self.numEnemies):
			#self.embed.add_field(name="Monster {}".format(enemy), value=str(self.enemies[enemy]), inline=False)
			self.embed.add_field(name="Monster {}".format(enemy), value=self.combat.creatures[enemy].name, inline=False)
			#self.creatures.append(Creatures.Creature(name=self.enemies[enemy], level=1, hp=3, armor=0))
		self.message = None
	async def send(self, channel):
		"""Send the message to the channel"""
		self.message = await channel.send(embed=self.embed)
		await self.SetReactions()
		#for enemy in range(self.numEnemies):
		#	await self.message.add_reaction(emojiNumbers[enemy])
		#await self.message.add_reaction(emojiCheck)
		#await self.message.add_reaction(emojiQuestion)
	async def Help(self):
		content = self.message.content
		content += "\nYou pressed question mark!"
		#theron = Characters.Character("Theron", 25, 10, 5, 25,10,5,3,0,0,["Heavy Weapons", "Athletics", "Tracking", Characters.Weapon.Heavy])
		#character = Characters.LoadCharacter("1Zni4ySL3zN_SR7DNs-3XQRrya4KZ3RY6C2VtRz6JC_k")
		content += "\n{}".format(str(self.character))
		embed = self.embed
		for enemy in range(self.numEnemies):
			monsterString = "{}\nLevel {}\n{}/{} hp".format(str(self.creatures[enemy].name), self.creatures[enemy].level, self.creatures[enemy].hp, self.creatures[enemy].maxHP)
			embed.set_field_at(index=enemy+1, name="Monster {}".format(enemy), value=monsterString, inline=False)
		await self.message.edit(embed=embed, content=content)
		await self.SetReactions()
		#await self.message.clear_reactions()
		#for enemy in range(self.numEnemies):
		#	await self.message.add_reaction(emojiNumbers[enemy])
		#await self.message.add_reaction(emojiCheck)
		#await self.message.add_reaction(emojiQuestion)
	async def SetReactions(self):
		await self.message.clear_reactions()
		for enemy in range(self.numEnemies):
			await self.message.add_reaction(emojiNumbers[enemy])
		await self.message.add_reaction(emojiCheck)
		await self.message.add_reaction(emojiQuestion)
	async def InitializeFields(self):
		self.embed.clear_fields()
		self.embed.add_field(name="Character", value=self.name, inline=False)
		for enemy in range(self.numEnemies):
			self.embed.add_field(name="Monster {}".format(enemy), value=self.combat.creatures[enemy].name, inline=False)
	async def ResolveTurn(self, target):
		self.character.Attack(self.creatures[target])
		for creature in self.creatures:
			if(not creature.isDead()):
				creature.Attack(self.character)
		self.combat.WriteToCreatureSheet()
		self.combat.WriteToCharacterSheet(self.character)
		if((False not in [creature.isDead() for creature in self.combat.creatures]) or self.character.isDead()):
			content = "Fight over!"
			await self.message.edit(content=content)



class Combat:
	def __init__(self, creatureSheetID="1YQKH6REpT5f8kDV0CNUK1OpC3M5jequvGZXudAOcv6I", playerSheetID="1Zni4ySL3zN_SR7DNs-3XQRrya4KZ3RY6C2VtRz6JC_k"):
		self.creatureSheetID = creatureSheetID
		self.playerSheetID = playerSheetID
		self.creatures = self.LoadCreaturesFromSheet()
	def LoadCreaturesFromSheet(self):
		data = BruteJusticeSpreadsheets.ReadSpreadsheet(['Name', 'Level', 'hp', 'Armor', 'Skills'], self.creatureSheetID)
		creatures = []
		for creature in range(len(data[0])):
			creatures.append(Creatures.Creature(name=data[0][creature][0], level=int(data[1][creature][0]), hp=int(data[2][creature][0]), armor=int(data[3][creature][0])))
		return creatures
	def WriteToCreatureSheet(self):
		BruteJusticeSpreadsheets.WriteToNamedRange(spreadsheetID=self.creatureSheetID, rangeName="hp", value=[[creature.hp] for creature in self.creatures])
	def WriteToCharacterSheet(self, character=None):
		if(character is not None):
			BruteJusticeSpreadsheets.WriteToNamedRange(spreadsheetID=self.playerSheetID, 
												   rangeName="Current", 
												   value=[[pool.current] for pool in [character.might, character.speed, character.intellect]])


