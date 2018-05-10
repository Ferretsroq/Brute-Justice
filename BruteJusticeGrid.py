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
    ''' Defines an array in the shape of a hexagon
        lengthSquares is the length of the bounding square around the hexagon
        The middle row of the hexagon spans the entire length '''
    # Initialize the array
    dataArray = np.zeros((lengthSquares,lengthSquares))
    # Account for even and odd-numbered sizes
    dataArray[len(dataArray)//2] = 1
    dataArray[len(dataArray)//2-(1-len(dataArray)%2)] = 1
    # Assign the squares based on the shape of a hexagon
    for row in range(1,len(dataArray)//2-(1-len(dataArray)%2)):
        difference = (len(dataArray)//2-(1-len(dataArray)%2)) - row
        dataArray[row][int(np.ceil(difference/2)):-int(np.ceil(difference/2))] = [1]
    for row in range(len(dataArray)//2+(len(dataArray)%2), len(dataArray)-1):
        difference = row - len(dataArray)//2
        dataArray[row][int(np.ceil(difference/2)):-int(np.ceil(difference/2))] = 1
    return dataArray

def RectangleArray(widthSquares=12, heightSquares=6):
    ''' Defines an array in the shape of a rectangle
        widthSquares = the width of the array
        heightSquares = the height of the array'''
    dataArray = np.ones((heightSquares, widthSquares))
    return dataArray

def RectangleImage(widthSquares=12, heightSquares=6, backgroundColor=discordDarkGray, gridColor=discordGray, scaling=100):
    '''Defines the base image for a rectangle
       widthSquares = the width of the image, in grid squares
       heightSquares = the height of the image, in grid squares
       backgroundColor = the color of the image where there are no squares
       gridColor = the color of the image where there are squares
       scaling = the pixel size of the squares'''
    width = widthSquares*scaling
    height = heightSquares*scaling
    image = Image.new(mode='RGB', size=(width, height), color=gridColor)
    drawer = ImageDraw.Draw(image)
    drawer.polygon((0, 0, width-1, 0, width-1, height-1, 0, height-1), outline='black', fill=gridColor)
    return image

def HexagonImage(lengthSquares=12, backgroundColor=discordDarkGray, gridColor=discordGray, scaling=100):
    '''Defines the base image for a hexagon
       lengthSquares = the side length of the image, in grid squares
       backgroundColor = the color of the image where there are no squares
       gridColor = the color of the image where there are squares
       scaling = the pixel size of the squares'''
    image = Image.new(mode='RGB', size=(lengthSquares*scaling,lengthSquares*scaling), color=backgroundColor)
    drawer = ImageDraw.Draw(image)
    length=(lengthSquares*scaling)//2-1
    c60 = np.cos(np.pi/3)
    s60 = np.sin(np.pi/3)
    drawer.polygon((0,length,length*c60, length-(length*s60), length*(1+c60), length-(length*s60), 2*length, length, length*(1+c60), length+(length*s60), length*c60, length+(length*s60)), outline='black', fill=gridColor)
    return image

def GridFromArray(dataArray, image, color=discordDarkGray, scaling=100):
    ''' Draws a grid image based on the array coming in
        dataArray = the 2-D array defining a grid
        image = the base image to draw the grid on
        color = the color of the gridlines. Ideally this matches the backgroundColor of the image
        scaling = the pixel size of the squares'''
    # The drawer object handles drawing on an existing image
    drawer = ImageDraw.Draw(image)
    # I won't lie to you, I think this was demo code that's no longer being used
    mask = Image.new('L', (80,80), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0,80,80), fill=255)
    # Draw the squares of the array on the image
    # Step through each row of the array
    for row in range(len(dataArray)):
        # Step through each column of the array
        for column in range(len(dataArray[row])):
            # In case this number is a float or a string of a number, convert to int
            value = int(dataArray[row][column])
            # If something exists, draw a square
            if(icons[value] != 'blank'):
                # Draw the lines of the square
                # scaling defines the pixel length of a square's side
                drawer.line((column*scaling, row*scaling, column*scaling, ((row+1)*scaling)), fill=color, width=1)
                drawer.line((column*scaling, row*scaling, (column+1)*scaling, row*scaling), fill=color, width=1)
                drawer.line(((column+1)*scaling, row*scaling, (column+1)*scaling, ((row+1)*scaling)), fill=color, width=1)
                drawer.line((column*scaling, (row+1)*scaling, (column+1)*scaling, ((row+1)*scaling)), fill=color, width=1)
            # Need to fill in extra on the edges of the image
            if(column == len(dataArray[row])-1 and icons[value] != 'blank'):
                drawer.line(((column+1)*scaling-1, row*scaling, (column+1)*scaling-1, ((row+1)*scaling)), fill=color, width=1)
            if(row == len(dataArray)-1 and icons[value] != 'blank'):
                drawer.line((column*scaling, (row+1)*scaling-1, (column+1)*scaling, (row+1)*scaling-1), fill=color, width=1)
            # Draw a ring and token if something exists in the square
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
    ''' Take a grid image and label the sides with letters and numbers
        inputImage = image with a grid already drawn
        widthSquares = width of the image in squares
        heightSquares = height of the image in squares'''
    # Scale the font size to the size of the image
    scalingWidth = int(inputImage.width/widthSquares)
    scalingHeight = int(inputImage.height/heightSquares)
    fontSizeWidth = scalingWidth//2
    fontSizeHeight = scalingHeight//2

    fontWidth = ImageFont.truetype('consola.ttf', fontSizeWidth)
    fontHeight = ImageFont.truetype('consola.ttf', fontSizeHeight)
    # Keep everything uppercase because we aren't savages
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Rescale the image for the new characters
    outputImage = Image.new('RGBA', (inputImage.width+scalingWidth, inputImage.height+scalingHeight))
    gridDraw = ImageDraw.Draw(outputImage)
    outputImage.paste(inputImage, (fontSizeWidth, fontSizeHeight))
    # Fill in the appropriate letters and numbers for each row and column
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
    ''' Keeps the data of a grid in an object.'''
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

