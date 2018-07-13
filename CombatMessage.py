import discord
import asyncio
import Characters

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
		self.enemies = enemies
		self.numEnemies = len(enemies)
		self.embed = discord.Embed(title=":crossed_swords: **FIGHT** :crossed_swords:", description=player)
		self.embed.add_field(name="Character", value=self.name, inline=False)
		for enemy in range(self.numEnemies):
			self.embed.add_field(name="Monster {}".format(enemy), value=str(self.enemies[enemy]), inline=False)
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
		theron = Characters.Character("Theron", 25, 10, 5, 25,10,5,3,0,0,["Heavy Weapons", "Athletics", "Tracking", Characters.Weapon.Heavy])
		character = Characters.LoadCharacter("1Zni4ySL3zN_SR7DNs-3XQRrya4KZ3RY6C2VtRz6JC_k")
		content += "\n{}".format(str(character))
		embed = self.embed
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



