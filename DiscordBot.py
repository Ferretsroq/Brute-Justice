from __future__ import print_function
import discord
import asyncio
import pprint
import httplib2
import os
import random
import re
from PIL import Image, ImageDraw
import shelve
import numpy as np
#import PyPDF2 as pdf
import BruteJusticeGrid as grid
import CombatMessage

from apiclient import discovery
from oauth2client import client as cl
from oauth2client import tools
from oauth2client.file import Storage


client = discord.Client()
#google_api_key = open('./google_api_key').read()
import pprint
import sys

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

gridSheetID = '1-DjsyCbph0tw4Esg87pEApyp-NZn3B6yx5A6nk3uYUs'
infoSheetID = '15SD1ovSoXzNyobFeHfRb6vyhfx0OG7eRe1IFTqhGfYE'
characterNames = ['!Harix', '!Kokoyo', '!Edemie', '!Illie', '!Setorie', '!Sparrow', '!Elstan', '!Jigo', '!Sarnai']
npcNames = ['!Xelophehod']
implementedCommands = ['!test', '!help', '!sleep', '!forward', '\n'.join(characterNames), '\n'.join(npcNames), '!RidgeRuth', '!Xelphatol', '!roll', '!grid', '!place']
gridSpacing = 100
#mm2Path = 'F:\\RPG Stuff\\4e\\PDFs\\Monster Manual 2.pdf'
#mm3Path = 'F:\\RPG Stuff\\4e\\PDFs\\Monster Manual 3.pdf'
#monsterDict = {}
icons = grid.icons

ferretsroq = "<@111529517541036032>"
ari = "<@112754131558481920>"

#def InitializeMonsters(path, inputDictionary):
#	pdfFileObj = open(path, 'rb')
#	pdfReader = pdf.PdfFileReader(pdfFileObj)
#	outlines = pdfReader.getOutlines()
#
#	bookmarks = []
#	for outline in outlines:
#		bookmarks.append(pdfReader.getDestinationPageNumber(outline))
#	bookmarks.append(pdfReader.numPages-1)
#	pages = []
#	for index in range(len(bookmarks)-1):
#		pages.append(bookmarks[index+1] - bookmarks[index])
 #       
#	for outline in range(len(outlines)):
#		inputDictionary[outlines[outline]['/Title']] = {'pageStart' : pdfReader.getDestinationPageNumber(outlines[outline]),
#														'pageSpan'  : pages[outline],
#														'book'		: path.split('\\')[-1].strip('.pdf') }


#def GetImageFromPDF(path, pageNumber, name=None):
#	myPDF = pdf.PdfFileReader(open(path, 'rb'))
#	page = myPDF.getPage(pageNumber)
#	xObject = page['/Resources']['/XObject'].getObject()
#	for obj in xObject:
#		if xObject[obj]['/Subtype'] == '/Image':
#			if(name):
#				title = name+'.jpg'
#			else:
#				title = obj[1:]+'.jpg'
#			size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
#			data = xObject[obj].getData()
#			mode = "RGB"
#			img = open(title, "wb")
#			img.write(data)
#			img.close()
#			return title
#	return None

def get_credentials():
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')
	store = Storage(credential_path)
	credentials = store.get()
	if(not credentials or credentials.invalid):
		flow = cl.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if(flags):
			credentials = tools.run_flow(flow, store, flags)
		else:
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

#def Grid(image, spacing=100):
#    drawer = ImageDraw.Draw(image)
#    for pixel in range(0, image.width, spacing):
#        drawer.line((pixel, 0, pixel, image.height), fill=0, width=1)
#    for pixel in range(0, image.height, spacing):
#        drawer.line((0, pixel, image.width, pixel), fill=0, width=1)
#    drawer.line((image.width-1, 0, image.width-1, image.height), fill=0, width=1)
#    drawer.line((0, image.height-1, image.width, image.height-1), fill=0, width=1)

#def ImageByArray(inputArray, spacing):
#    image = Image.new('RGB', (inputArray.shape[0]*spacing, inputArray.shape[1]*spacing), 'white')
#    Grid(image, spwacing)
#    return image


def ReadSpreadsheet(rangeNames, inputID):
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
			'version=v4')
	service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
	spreadsheetId = inputID
	result = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId, ranges=rangeNames).execute()
	values = result.get('valueRanges', [])
	return values


def WriteSpreadsheet(sheet=1, cell='A1', value=0, inputID=gridSheetID):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    spreadsheetId = inputID
    values = [[value]]
    body = {'values': values}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId, range='Sheet{}!{}'.format(sheet, cell),
        valueInputOption='USER_ENTERED', body=body).execute()
    return result

def GetCell(sheet=1, cell='A1'):
    return int(ReadSpreadsheet('Sheet{}!{}'.format(sheet, cell), gridSheetID)[0]['values'][0][0])

def Move(sheet=1, start='A1', end='A1'):
    token = GetCell(sheet, start)
    if(token == 0 or token == 1):
        return 'Invalid starting location'
    elif(GetCell(sheet, end) != 1):
        return 'Invalid ending location'
    else:
        WriteSpreadsheet(sheet, start, 1)
        WriteSpreadsheet(sheet, end, token)
        return 'Moved {} from {} to {}.'.format(icons[token], start, end)
        

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		self.activeMessage = None
		self.activeUser = None

	async def on_reaction_add(self, reaction, user):
		if(user == self.activeUser and reaction.message.id == self.activeMessage.message.id):
			#await reaction.message.channel.send('You reacted with {}!'.format(str(reaction)))
			if(str(reaction) == CombatMessage.emojiQuestion):
				await self.activeMessage.Help()
			if(str(reaction) in CombatMessage.emojiNumbers):
				pass
			if(str(reaction) == CombatMessage.emojiCheck):
				#print('foo')
				targets = []
				for react in range(len(reaction.message.reactions)):
					#print('bar')
					async for x in reaction.message.reactions[react].users():#react.users():
						#if(self.activeUser == x and str(react) in CombatMessage.emojiNumbers):
						if(self.activeUser == x and str(reaction.message.reactions[react]) in CombatMessage.emojiNumbers):
							targets.append(react)
						#print(x)
				await self.activeMessage.InitializeFields()
				if(len(targets) > 0):
					await self.activeMessage.message.edit(embed=self.activeMessage.embed, content="You are targeting {}!".format(str(targets[0])))
					#print(targets[0])
					await self.activeMessage.ResolveTurn(targets[0])
				else:
					await self.activeMessage.message.edit(embed=self.activeMessage.embed, content="No target selected.")

				await self.activeMessage.SetReactions()
				#print(str(targets[0]))

					#for user in react.users():
					#	print('baz')
			#			print("{}: {}".format(str(react), user))
				#print([(str(x), list(x.users().flatten())) for x in reaction.message.reactions])
		#print(reaction.message)
		#print(self.activeMessage.message)
		#print(reaction.message.id == self.activeMessage.message.id)
		#if(reaction.message.id == self.activeMessage.message.id):
			#await reaction.message.channel.send("You reacted with {}".format(str(reaction)))
	async def on_message(self, message):
		if message.content.startswith('!test'):
			#im = Image.new('RGB', (100,100), 'green')
			#await message.channel.send(file=discord.File(im.tobytes()))
			#await message.channel.send(':thinking:')
			#color = discord.Colour.from_rgb(255,0,255)
			#embed = discord.Embed(title=":crossed_swords: **FIGHT** :crossed_swords:", type="rich", description=" <@111529517541036032>", color=color)
			#embed.add_field(name="Character", value="Theron")
			#embed.add_field(name="Monster 0", value="Chronal Feeder")
			#embed.add_field(name="Monster 1", value="Chronal Feeder")
			#embed.add_field(name="Monster 2", value="Chronal Feeder")
			#self.activeMessage = message
			#self.activeMessage = await message.channel.send(embed=embed)
			#await self.activeMessage.add_reaction("0\u20e3")
			#await self.activeMessage.add_reaction("1\u20e3")
			#await self.activeMessage.add_reaction("2\u20e3")
			#await self.activeMessage.add_reaction("\u2705")
			#print(message.id)
			#def check(reaction, user):
			#	return user == message.author and reaction.message.id == self.activeMessage.id
			#try:
			#	reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
			#except asyncio.TimeoutError:
			#	await message.channel.send('No reaction')
			#else:
			#	await message.channel.send('Reaction sent')
			#	await message.channel.send(str(reaction))
			self.activeMessage = CombatMessage.CombatMessage('Theron', ['Chronal Feeder', 'Voltron', 'Crawlybugs', 'foo', 'bar', 'baz'], message.author.mention)
			self.activeUser = message.author
			await self.activeMessage.send(message.channel)
			#def check(reaction, user):
		#		return user == message.author and reaction.message.id == self.activeMessage.message.id
			#try:
			#	reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
			#except asyncio.TimeoutError:
			#	await message.channel.send('No reaction')
			#else:
			#	await message.channel.send('You reacted with {}'.format(str(reaction)))
			
		elif(message.content.startswith('!help')):
			await message.channel.send('Hi there! My name is BruteJustice, the friendly robot!')
			await message.channel.send('These are my current implemented commands:\n' + '\n'.join(implementedCommands)+'\nI hope you find that I am much friendlier here than I was in Midas. Those were my rebellious days.')
		elif message.content.startswith('!sleep'):
			await asyncio.sleep(5)
			await message.channel.send('Done sleeping')
		elif(message.content.startswith('!forward')):
			await message.channel.send('and back')
			await asyncio.sleep(2)
			await message.channel.send('and then forward and back')
			await asyncio.sleep(2)
			await message.channel.send('and then go forward and back')
			await asyncio.sleep(2)
			await message.channel.send('and put one foot')
			await message.channel.send('forward')
		elif(message.content in characterNames):
			rangeNames = ['Player Characters!Categories', 'Player Characters!'+message.content.split('!')[1]]
			values = ReadSpreadsheet(rangeNames, infoSheetID)
			if(not values):
				print('No data found.')
			else:
				for row in range(len(values[0]['values'])):
					await message.channel.send('**{}:** {}'.format(values[0]['values'][row][0], values[1]['values'][row][0]))
		elif(message.content.startswith('!Ridgeruth')):
			await message.channel.send('is poor af')
		elif(message.content.startswith('!Xelphatol')):
			await message.channel.send('Did you mean: !Xelophehod?')
		elif(message.content in npcNames):
			rangeNames = ['NPCs!NPC_Categories', 'NPCs!'+message.content.split('!')[1]]
			values = ReadSpreadsheet(rangeNames, infoSheetID)

			if(not values):
				print('No data found.')
			else:
				for row in range(len(values[0]['values'])):
					await message.channel.send('**{}:** {}'.format(values[0]['values'][row][0], values[1]['values'][row][0]))
				if(message.content.split()[0][1:]+'.png' in os.listdir('./Images/NPCs')):
					await message.channel.send(file=discord.File('./Images/NPCs/'+message.content.split()[0][1:]+'.png'))
		elif(message.content.startswith('!roll')):
			pattern = '(?P<Number>\d+)d(?P<Die>\d+)(?P<Kept>k\d+)?(?P<Modifier>[\+|-]\d+)?'
			try:
				roll = message.content.split()[1]
				if(re.match(pattern, roll)):
					rollDict = re.match(pattern, roll).groupdict()
					try:
						notes = ' '.join(message.content.split()[2:])
					except:
						notes = ''
					numberOfDice = int(rollDict['Number'])
					die = int(rollDict['Die'])
					diceKept = numberOfDice
					modifier = 0
					if(rollDict['Kept']):
						diceKept = int(rollDict['Kept'][1:])
					else:
						diceKept = numberOfDice
					if(rollDict['Modifier']):
						modifier = int(rollDict['Modifier'])
					else:
						modifier = 0
					rolls = []
					for dieRoll in range(numberOfDice):
						rolls.append(random.randint(1, die))
					rolls.sort(reverse=True)
					keptRolls = rolls[0:diceKept]
					result = sum(keptRolls) + modifier
					await message.channel.send('You rolled {} and got {}. [{}]'.format(roll, result, rolls))
			except:
				await message.channel.send('I couldn\'t parse your roll. But don\'t parse shame me or SE will ban you.')
				await message.channel.send('Problematic roll: {} <@111529517541036032>'.format(message.content))
		#elif(message.content.startswith('!grid')):
		#	loadPattern = '!grid load (?P<Name>.+)'
		#	newPattern = '!grid new (?P<Name>name=.+) (?P<Width>width=\d+) (?P<Height>height=\d+)'
		#	if(re.match('!grid new(.+)?', message.content)):
		#		if(re.match(newPattern, message.content)):
		#			gridDict = re.match(newPattern, message.content).groupdict()
		#			width = int(gridDict['Width'].split('=')[1])
		#			height = int(gridDict['Height'].split('=')[1])
		#			name = gridDict['Name'].split('=')[1]
		#		else:
		#			width = 12
		#			height = 12
		#			name = 'Default Grid'
		#		widthSpacing = gridSpacing
		#		heightSpacing = gridSpacing
		#		image = Image.new('RGB', (width*widthSpacing, height*heightSpacing), 'white')
		#		Grid(image, gridSpacing)
		#		image.save(name+'.png')
		#		await message.channel.send(file=discord.File(name+'.png'))
#
#			elif(re.match(loadPattern, message.content)):
#				matchName = re.match(loadPattern, message.content).groupdict()['Name']
#				if(matchName+'.png' in os.listdir('.')):
#					await message.channel.send(file=discord.File(matchName+'.png'))
#				else:
#					await message.channel.send('{} not found'.format(matchName))
#			else:
#				await message.channel.send('I\'m sorry, I didn\'t understand you.')
#				await message.channel.send('Syntax: !grid new name=<desired name> width=<width in squares> height=<height in squares>')
		elif(message.content.startswith('!grid')):
			gridImage = grid.LabelGrid(grid.GridFromArray(ReadSpreadsheet('Sheet1', gridSheetID)[0]['values'], grid.HexagonImage()))
			gridImage.save('temp grid.png')
			await message.channel.send(file=discord.File('temp grid.png'))
		elif(message.content.startswith('!move')):
			pattern = '!move (?P<start>[a-zA-z]+\d+) (?P<end>[a-zA-z]+\d+)'
			if(re.match(pattern, message.content)):
				moveDict = re.match(pattern, message.content).groupdict()
				await message.channel.send(Move(start=moveDict['start'], end=moveDict['end']))
				gridImage = grid.LabelGrid(grid.GridFromArray(ReadSpreadsheet('Sheet1', gridSheetID)[0]['values'], grid.HexagonImage()))
				gridImage.save('temp grid.png')
				await message.channel.send(file=discord.File('temp grid.png'))

		elif(message.content.startswith('!place')):
			pattern = '!place (?P<Row>row=\d+) (?P<Column>column=\d+)'
			image = Image.open('Grid.png')
			pasteImage = Image.open('./Images/NPCs/Xelophehod.png')
			if(re.match(pattern, message.content)):
				placeDict = re.match(pattern, message.content).groupdict()
				row = int(placeDict['Row'].split('=')[1])
				column = int(placeDict['Column'].split('=')[1])
				box = ((column*gridSpacing)+1, (row*gridSpacing)+1)
			else:
				box = (101, 101)
			image.paste(pasteImage.resize((gridSpacing-2, gridSpacing-2)), box)
			image.save('Grid.png')
			await message.channel.send(file=discord.File('Grid.png'))
			image.close()
			pasteImage.close()
		elif(message.content.startswith('!logout')):
			await self.logout()

		"""elif(message.content.startswith('!monster')):
			pattern = '!monster (?P<Name>.+)'
			if(re.match(pattern, message.content)):
				if(re.match(pattern, message.content).groupdict()['Name'].title() in monsterDict):
					name = re.match(pattern, message.content).groupdict()['Name'].title()
					for page in range(monsterDict[name]['pageSpan']):
						await message.channel.send(file=discord.File(GetImageFromPDF(mm2Path, monsterDict[name]['pageStart'] + page)))
				else:
					await message.channel.send('{} not found.'.format(re.match(pattern, message.content.groupdict()['Name'].title())))
			elif(message.content == '!monsters'):
				monsterStrings = ['```']
				for key in monsterDict.keys():
					monsterStrings[-1] += '{:<24} - {}\n'.format(key, monsterDict[key]['book'])
					if(len(monsterStrings[-1]) >= 900):
						monsterStrings[-1] += '```'
						monsterStrings.append('```')
				if(monsterStrings[-1][-3:] != '```'):
					monsterStrings[-1] += '```'
				for monsterString in monsterStrings:
					await message.channel.send(monsterString)
					"""




if(__name__ == '__main__'):
	#InitializeMonsters(mm2Path, monsterDict)	
	#InitializeMonsters(mm3Path, monsterDict)	
	client = MyClient()
	client.run('MzUzNjY0MTQwMTc2MjYxMTMx.DIzCkw.CPNh064jbITfV2Y2rke8PVhnPL8')
	client.logout()
	client.close()