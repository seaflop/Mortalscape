from tkinter import PhotoImage
#create a finish point object
class FinishPoint:
    
    def __init__(self, canvasarg, x = 0, y = 0):
        self.__canvas = canvasarg
        self.__x = x
        self.__y = y
        self.__img = PhotoImage(file = 'New folder/FlagLeft.png')
        self.__height = self.__img.height()
        self.__width = self.__img.width()
        self.__placed = False
    
    #initialize a funtion which places the finish point   
    def placeFinishPoint(self, x = 0, y = 0):
        self.__x = x
        self.__y = y
        self.__finishPoint = self.__canvas.create_image(self.__x, self.__y, image = self.__img, anchor = 'se')
        
    def setX(self, x):
        '''
        Sets the x coordinate of the finish point.
        PARAMETERS:
        -----------
        x: int
            The x coordinate of the finish point 
        '''
        self.__x = x   
    
    def setY(self, y):
        '''
        Sets the y coordinate of the finish point.
        PARAMETERS:
        -----------
        y: int
            The y coordinate of the finish point 
        '''
        self.__y = y  
    def getX(self):
        '''
        Returns the x coordinate of the finish point.
        RETURNS:
        --------
        int
            The x coordinate of the finish point
        '''
        return self.__x
    
    def getY(self):
        '''
        Returns the y coordinate of the finish point.
        RETURNS:
        --------
        int
            The y coordinate of the finish point
        '''
        return self.__y
    
    def getHeight(self):
        '''
        Returns the height of the finish point.
        RETURNS:
        --------
        float
            The height of the finish point
        '''
        return self.__height
    
    def getWidth(self):
        '''
        Returns the width of the finish point.
        RETURNS:
        --------
        float
            The width of the finish point
        '''
        return self.__width