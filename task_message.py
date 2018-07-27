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
