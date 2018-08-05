import discord
import asyncio

class TaskMessage:
	#def __init__(self, triggerMessage):
	#	self.embed = discord.Embed(content=triggerMessage.content)
	#	self.message = None
	#	await InitializeMessage(triggerMessage)
	#async def InitializeMessage(self, triggerMessage):
	#	self.message = await triggerMessage.channel.send(embed=self.embed)
	@classmethod
	async def create(cls, triggerMessage):
		self = TaskMessage()
		print(triggerMessage.content)
		self.embed = discord.Embed(description=triggerMessage.content)
		self.message = await triggerMessage.channel.send(embed=self.embed)
		return self

class Scene:
	def __init__(self):
		self.embed = discord.Embed()
		self.description = ''
		self.title = ''
		self.fields = []
		self.message = None
	async def send(self, channel):
		self.message = await channel.send(embed=self.embed)