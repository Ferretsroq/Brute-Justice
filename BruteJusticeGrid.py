import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

discordBlue = '#7289da'
discordWhite = '#ffffff'
discordGray = '#99aab5'
discordDarkGray = '#2c2f33'
discordBlack = '#23272a'
discordBackground = '#36393e'
enemyRing = '#990000'
playerRing = '#000099'
allyRing = '#aaaa00'

icons = {}
icons[0] = 'blank'
icons[1] = 'square'
icons[2] = 'Xelophehod'
icons[3] = 'Subotai'
icons[4] = 'Chahil'
icons[5] = 'Goblin'

enemies = ['Xelophehod', 'Goblin']
players = ['Subotai']
allies = ['Chahil']

def HexagonArray(lengthSquares=12):
    dataArray = np.zeros((lengthSquares,lengthSquares))
    dataArray[len(dataArray)//2] = 1
    dataArray[len(dataArray)//2-(1-len(dataArray)%2)] = 1
    for row in range(1,len(dataArray)//2-(1-len(dataArray)%2)):
        difference = (len(dataArray)//2-(1-len(dataArray)%2)) - row
        dataArray[row][int(np.ceil(difference/2)):-int(np.ceil(difference/2))] = [1]
    for row in range(len(dataArray)//2+(len(dataArray)%2), len(dataArray)-1):
        difference = row - len(dataArray)//2
        dataArray[row][int(np.ceil(difference/2)):-int(np.ceil(difference/2))] = 1
    return dataArray

def RectangleArray(widthSquares=12, heightSquares=6):
    dataArray = np.ones((heightSquares, widthSquares))
    return dataArray

def RectangleImage(widthSquares=12, heightSquares=6, backgroundColor=discordDarkGray, gridColor=discordGray, scaling=100):
    width = widthSquares*scaling
    height = heightSquares*scaling
    image = Image.new(mode='RGB', size=(width, height), color=gridColor)
    drawer = ImageDraw.Draw(image)
    drawer.polygon((0, 0, width-1, 0, width-1, height-1, 0, height-1), outline='black', fill=gridColor)
    return image

def HexagonImage(lengthSquares=12, backgroundColor=discordDarkGray, gridColor=discordGray, scaling=100):
    image = Image.new(mode='RGB', size=(lengthSquares*scaling,lengthSquares*scaling), color=backgroundColor)
    drawer = ImageDraw.Draw(image)
    length=(lengthSquares*scaling)//2-1
    c60 = np.cos(np.pi/3)
    s60 = np.sin(np.pi/3)
    drawer.polygon((0,length,length*c60, length-(length*s60), length*(1+c60), length-(length*s60), 2*length, length, length*(1+c60), length+(length*s60), length*c60, length+(length*s60)), outline='black', fill=gridColor)
    return image

def GridFromArray(dataArray, image, color=discordDarkGray, scaling=100):
    drawer = ImageDraw.Draw(image)
    mask = Image.new('L', (80,80), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0,80,80), fill=255)
    for row in range(len(dataArray)):
        for column in range(len(dataArray[row])):
            value = int(dataArray[row][column])
            if(icons[value] != 'blank'):
                drawer.line((column*scaling, row*scaling, column*scaling, ((row+1)*scaling)), fill=color, width=1)
                drawer.line((column*scaling, row*scaling, (column+1)*scaling, row*scaling), fill=color, width=1)
                drawer.line(((column+1)*scaling, row*scaling, (column+1)*scaling, ((row+1)*scaling)), fill=color, width=1)
                drawer.line((column*scaling, (row+1)*scaling, (column+1)*scaling, ((row+1)*scaling)), fill=color, width=1)
            if(column == len(dataArray[row])-1 and icons[value] != 'blank'):
                drawer.line(((column+1)*scaling-1, row*scaling, (column+1)*scaling-1, ((row+1)*scaling)), fill=color, width=1)
            if(row == len(dataArray)-1 and icons[value] != 'blank'):
                drawer.line((column*scaling, (row+1)*scaling-1, (column+1)*scaling, (row+1)*scaling-1), fill=color, width=1)
            if(value > 1 and value in icons):
                #drawer.ellipse((column*scaling+1, row*scaling+1, (column+1)*scaling-1, (row+1)*scaling-1), fill='black')
                ringColor = 'gray'
                if(icons[value] in enemies):
                    ringColor = enemyRing
                elif(icons[value] in players):
                    ringColor = playerRing
                elif(icons[value] in allies):
                    ringColor = allyRing
                drawer.ellipse((column*scaling+3, row*scaling+1, (column+1)*scaling-1, (row+1)*scaling-3), fill=ringColor)
                #drawer.ellipse((column*scaling+8, row*scaling+8, (column+1)*scaling-8, (row+1)*scaling-8), fill='black')
                image.paste(Image.open('./Images/NPCs/{}.png'.format(icons[value])).resize((scaling-20,scaling-20)), (column*scaling+10, row*scaling+10, (column+1)*scaling-10, (row+1)*scaling-10), mask)
                
    return image

def LabelGrid(inputImage, widthSquares=12, heightSquares=12):
    scalingWidth = int(inputImage.width/widthSquares)
    scalingHeight = int(inputImage.height/heightSquares)
    fontSizeWidth = scalingWidth//2
    fontSizeHeight = scalingHeight//2

    fontWidth = ImageFont.truetype('consola.ttf', fontSizeWidth)
    fontHeight = ImageFont.truetype('consola.ttf', fontSizeHeight)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    outputImage = Image.new('RGBA', (inputImage.width+scalingWidth, inputImage.height+scalingHeight))
    gridDraw = ImageDraw.Draw(outputImage)
    outputImage.paste(inputImage, (fontSizeWidth, fontSizeHeight))
    for square in range(widthSquares):
        gridDraw.text((square*scalingWidth+(scalingWidth/2)-(fontSizeWidth/2+1)+fontSizeWidth, -1), '{}'.format(alphabet[square]), fill='black', font=fontWidth)
        gridDraw.text((square*scalingWidth+(scalingWidth/2)-(fontSizeWidth/2-1)+fontSizeWidth, 1), '{}'.format(alphabet[square]), fill='black', font=fontWidth)
        gridDraw.text((square*scalingWidth+(scalingWidth/2)-(fontSizeWidth/2+1)+fontSizeWidth, 1), '{}'.format(alphabet[square]), fill='black', font=fontWidth)
        gridDraw.text((square*scalingWidth+(scalingWidth/2)-(fontSizeWidth/2-1)+fontSizeWidth, -1), '{}'.format(alphabet[square]), fill='black', font=fontWidth)

        gridDraw.text((square*scalingWidth+(scalingWidth/2)-(fontSizeWidth/2)+fontSizeWidth, 0), '{}'.format(alphabet[square]), fill='white', font=fontWidth)
        
        gridDraw.text((square*scalingWidth+(scalingWidth/2)-(fontSizeWidth/2+1)+fontSizeWidth, inputImage.height+scalingHeight/2-1), '{}'.format(alphabet[square]), fill='black', font=fontWidth)
        gridDraw.text((square*scalingWidth+(scalingWidth/2)-(fontSizeWidth/2-1)+fontSizeWidth, inputImage.height+scalingHeight/2+1), '{}'.format(alphabet[square]), fill='black', font=fontWidth)
        gridDraw.text((square*scalingWidth+(scalingWidth/2)-(fontSizeWidth/2+1)+fontSizeWidth, inputImage.height+scalingHeight/2+1), '{}'.format(alphabet[square]), fill='black', font=fontWidth)
        gridDraw.text((square*scalingWidth+(scalingWidth/2)-(fontSizeWidth/2-1)+fontSizeWidth, inputImage.height+scalingHeight/2-1), '{}'.format(alphabet[square]), fill='black', font=fontWidth)

        gridDraw.text((square*scalingWidth+(scalingWidth/2)-(fontSizeWidth/2)+fontSizeWidth, inputImage.height+scalingHeight/2), '{}'.format(alphabet[square]), fill='white', font=fontWidth)
    for square in range(heightSquares):
        gridDraw.text((-1, square*scalingHeight+(scalingHeight/2)-(fontSizeHeight/2+1)+fontSizeHeight), '{}'.format(square+1), fill='black', font=fontHeight)
        gridDraw.text((1, square*scalingHeight+(scalingHeight/2)-(fontSizeHeight/2-1)+fontSizeHeight), '{}'.format(square+1), fill='black', font=fontHeight)
        gridDraw.text((1, square*scalingHeight+(scalingHeight/2)-(fontSizeHeight/2+1)+fontSizeHeight), '{}'.format(square+1), fill='black', font=fontHeight)
        gridDraw.text((-1, square*scalingHeight+(scalingHeight/2)-(fontSizeHeight/2-1)+fontSizeHeight), '{}'.format(square+1), fill='black', font=fontHeight)
    
        gridDraw.text((0, square*scalingHeight+(scalingHeight/2)-(fontSizeHeight/2)+fontSizeHeight), '{}'.format(square+1), fill='white', font=fontHeight)
        
        gridDraw.text((inputImage.width+scalingWidth/2-1, square*scalingHeight+(scalingHeight/2)-(fontSizeHeight/2+1)+fontSizeHeight), '{}'.format(square+1), fill='black', font=fontHeight)
        gridDraw.text((inputImage.width+scalingWidth/2+1, square*scalingHeight+(scalingHeight/2)-(fontSizeHeight/2-1)+fontSizeHeight), '{}'.format(square+1), fill='black', font=fontHeight)
        gridDraw.text((inputImage.width+scalingWidth/2+1, square*scalingHeight+(scalingHeight/2)-(fontSizeHeight/2+1)+fontSizeHeight), '{}'.format(square+1), fill='black', font=fontHeight)
        gridDraw.text((inputImage.width+scalingWidth/2-1, square*scalingHeight+(scalingHeight/2)-(fontSizeHeight/2-1)+fontSizeHeight), '{}'.format(square+1), fill='black', font=fontHeight)
    
        gridDraw.text((inputImage.width+scalingWidth/2, square*scalingHeight+(scalingHeight/2)-(fontSizeHeight/2)+fontSizeHeight), '{}'.format(square+1), fill='white', font=fontHeight)
    return outputImage

class Grid:
    def __init__(self, shape='rectangle', width=12, height=12, scaling=100, backgroundColor=discordDarkGray, gridColor=discordGray):
        self.shape = shape
        self.width = width
        self.height = height
        self.scaling = scaling
        self.backgroundColor = backgroundColor
        self.gridColor = gridColor
        if(self.shape == 'rectangle'):
            self.data = RectangleArray(self.width, self.height)
            self.image = LabelGrid(GridFromArray(self.data, RectangleImage(self.width, self.height, self.backgroundColor, self.gridColor, self.scaling), scaling=self.scaling), self.width, self.height)
        elif(self.shape == 'hexagon'):
            self.data = HexagonArray(self.width)
            self.image = LabelGrid(GridFromArray(self.data, HexagonImage(self.width, self.backgroundColor, self.gridColor, self.scaling), scaling=self.scaling), self.width, self.height)
        else:
            self.data = np.zeros((height,width))
            self.image = LabelGrid(GridFromArray(self.data, RectangleImage(self.width, self.height, self.backgroundColor, self.gridColor, self.scaling), scaling=self.scaling), self.width, self.height)
    def __repr__(self):
        return self.data

