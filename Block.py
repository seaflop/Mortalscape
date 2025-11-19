from tkinter import PhotoImage

#create a block object
class Block:
    def __init__(self, canvasarg, x = 0, y = 0):
        self.__canvas = canvasarg
        self.__x = x
        self.__y = y
        self.__img = PhotoImage(file = 'New folder/Brick.png')
        self.__height = self.__img.height()
        self.__width = self.__img.width()
        self.__placed = False
    #create a function which places the block on the canvas   
    def placeBlock(self, x = 0, y = 0):
        self.__x = x
        self.__y = y
        self.__block = self.__canvas.create_image(self.__x, self.__y, image = self.__img, anchor = 'nw')
    
    #create a function which removes the block from the canvas  
    def removeBlock(self):
        #print('f')
        self.__canvas.delete(self.__block)
     
    def setX(self, x):
        '''
        Sets the x coordinate of the block.
        PARAMETERS:
        -----------
        x: int
            The x coordinate of the block 
        '''
        self.__x = x   
    
    def setY(self, y):
        '''
        Sets the y coordinate of the block.
        PARAMETERS:
        -----------
        y: int
            The y coordinate of the block 
        '''
        self.__y = y  
    def getBlock(self):
        '''
        Returns the canvas image of the block.
        RETURNS:
        --------
        image
            The canvas image of the block
        '''
        return self.__block
    
    def getX(self):
        '''
        Returns the x coordinate of the block.
        RETURNS:
        --------
        int
            The x coordinate of the block
        '''
        return self.__x
    
    def getY(self):
        '''
        Returns the y coordinate of the block.
        RETURNS:
        --------
        int
            The y coordinate of the block
        '''
        return self.__y
    
    def getHeight(self):
        '''
        Returns the height of the block.
        RETURNS:
        --------
        float
            The height of the block
        '''
        return self.__height
    
    def getWidth(self):
        '''
        Returns the width of the block.
        RETURNS:
        --------
        float
            The width of the block
        '''
        return self.__width