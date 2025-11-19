from tkinter import PhotoImage

#initialize a Coin object
class Coins:
    def __init__(self, canvasarg, x = 0, y = 0):
        self.__canvas = canvasarg
        self.__x = x
        self.__y = y
        self.__img = PhotoImage(file = 'New folder/Coin.png')
        self.__height = self.__img.height()
        self.__width = self.__img.width()
        self.__placed = False
    #initialize a function which places the coin on the canvas   
    def placeCoin(self, x = 0, y = 0):
        self.__x = x
        self.__y = y
        self.__coin = self.__canvas.create_image(self.__x, self.__y, image = self.__img, anchor = 'nw')
    #initialize a function which removes the coin from the canvas   
    def removeCoin(self):
        #print('f')
        self.__canvas.delete(self.__coin)
        
    def setX(self, x):
        '''
        Sets the x coordinate of the coin.
        PARAMETERS:
        -----------
        x: int
            The x coordinate of the coin 
        '''
        self.__x = x   
    
    def setY(self, y):
        '''
        Sets the y coordinate of the coin.
        PARAMETERS:
        -----------
        y: int
            The y coordinate of the coin 
        '''
        self.__y = y  
    def getcoin(self):
        '''
        Returns the canvas image of the coin.
        RETURNS:
        --------
        image
            The canvas image of the coin
        '''
        return self.__coin
    
    def getX(self):
        '''
        Returns the x coordinate of the coin.
        RETURNS:
        --------
        int
            The x coordinate of the coin
        '''
        return self.__x
    
    def getY(self):
        '''
        Returns the y coordinate of the coin.
        RETURNS:
        --------
        int
            The y coordinate of the coin
        '''
        return self.__y
    
    def getHeight(self):
        '''
        Returns the height of the coin.
        RETURNS:
        --------
        float
            The height of the coin
        '''
        return self.__height
    
    def getWidth(self):
        '''
        Returns the width of the coin.
        RETURNS:
        --------
        float
            The width of the coin
        '''
        return self.__width