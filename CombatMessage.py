import discord
import asyncio


emojiCheck = '\u2705'
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
	def __init__(self, name='', enemies=[], player=''):
		self.name = name
		self.enemies = enemies
		self.numEnemies = len(enemies)
		self.embed = discord.Embed(title=":crossed_swords: **FIGHT** :crossed_swords:", description=player)
		self.embed.add_field(name="Character", value=self.name)
		for enemy in range(self.numEnemies):
			self.embed.add_field(name="Monster {}".format(enemy), value=str(self.enemies[enemy]))
		self.message = None
	async def send(self, channel):
		self.message = await channel.send(embed=self.embed)
		for enemy in range(self.numEnemies):
			await self.message.add_reaction(emojiNumbers[enemy])
		await self.message.add_reaction(emojiCheck)
