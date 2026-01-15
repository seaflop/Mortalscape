from tkinter import PhotoImage

#construct a player object
class Player:
    
    def __init__(self, canvasarg, x = 0, y = 0):
        self.__canvas = canvasarg
        self.__x = x
        self.__y = y
        self.__img = PhotoImage(file = './img/PlayerRight.png')
        self.__height = self.__img.height()
        self.__width = self.__img.width()
        self.__player = self.__canvas.create_image(self.__x, self.__y, image = self.__img, anchor = 'sw')
        self.__move = True
        self.__seconds = 0
        self.__fall = True
    #initialize a function which will move the player    
    def move(self, x = 1):
        if self.__move == True:
            self.__x += x
        
            self.__canvas.coords(self.__player, self.__x, self.__y)
        else:
            pass
    def setLocation(self, x, y):
        self.__x = x
        self.__y = y
        self.__canvas.coords(self.__player, self.__x, self.__y)
        
    def setImage(self, img):
        self.__img = img
        self.__canvas.itemconfig(self.__player, image = img)    
    
    def setX(self, x):
        '''
        Sets the x coordinate of the player.
        PARAMETERS:
        -----------
        x: int
            The x coordinate of the player 
        '''
        self.__x = x
        self.__canvas.coords(self.__player, self.__x, self.__y)
        
    def setY(self, y):
        '''
        Sets the y coordinate of the player.
        PARAMETERS:
        -----------
        y: int
            The y coordinate of the player 
        '''
        self.__y = y
        self.__canvas.coords(self.__player, self.__x, self.__y)
        
    def getX(self):
        '''
        Returns the x coordinate of the player.
        RETURNS:
        --------
        int
            The x coordinate of the player
        '''
        return self.__x
    
    def getY(self):
        '''
        Returns the y coordinate of the player.
        RETURNS:
        --------
        int
            The y coordinate of the player
        '''
        return self.__y
    
    def getHeight(self):
        '''
        Returns the height of the player.
        RETURNS:
        --------
        float
            The height of the player
        '''
        return self.__height
    
    def getWidth(self):
        '''
        Returns the width of the player.
        RETURNS:
        --------
        float
            The width of the player
        '''
        return self.__width
    def getImage(self):
        '''
        Returns the image of the player.
        RETURNS:
        --------
        PhotoImage
            The image of the player
        '''
        return self.__img