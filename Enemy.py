from tkinter import PhotoImage

#create an enemy object
class Enemy:   
    def __init__(self, canvasarg, x = 0, y = 0):
        self.__canvas = canvasarg
        self.__x = x
        self.__y = y
        self.__img = PhotoImage(file = 'New folder/SpikeBall.png')
        self.__height = self.__img.height()
        self.__width = self.__img.width()
        #create variable to check status of the enemy
        self.__placed = False
        self.__moveRight = True
        self.__move = True
    #initialize a function which places the enemy on the canvas    
    def placeEnemy(self, x = 0, y = 0):
        self.__x = x
        self.__y = y
        self.__enemy = self.__canvas.create_image(self.__x, self.__y, image = self.__img, anchor = 'nw')
    #initialize a function which removes the enemy from the canvas    
    def removeEnemy(self):
        print('f')
        self.__canvas.delete(self.__enemy)
    #create a function which moves the enemy    
    def move(self, x = 5):
        self.__timer = self.__canvas.after(100, self.move)
        
        if self.__move == True:
            if self.__moveRight == True:
                self.__x += x
                self.__canvas.coords(self.__enemy, self.__x, self.__y)
            elif self.__moveRight == False:
                self.__x -= x
                self.__canvas.coords(self.__enemy, self.__x, self.__y)
        elif self.__move == False:
            self.__canvas.after_cancel(self.__timer)
            
    def setMoveRight(self, moveRight):
        '''
        Sets the status of the enemy when moving to the right.
        PARAMETERS:
        -----------
        moveRight: bool
            The state of the enemy when moving right 
        '''
        self.__moveRight = moveRight
#         self.move()

    def setMove(self, move):
        '''
        Sets the status of the enemy.
        PARAMETERS:
        -----------
        move: bool
            The state of the enemy when moving. 
        '''
    
        self.__move = move
            
    def setX(self, x):
        '''
        Sets the x coordinate of the enemy.
        PARAMETERS:
        -----------
        x: int
            The x coordinate of the enemy 
        '''
        self.__x = x   
    
    def setY(self, y):
        '''
        Sets the y coordinate of the enemy.
        PARAMETERS:
        -----------
        y: int
            The y coordinate of the enemy 
        '''
        self.__y = y  
    def getenemy(self):
        '''
        Returns the canvas image of the enemy.
        RETURNS:
        --------
        image
            The canvas image of the enemy
        '''
        return self.__enemy
    
    def getX(self):
        '''
        Returns the x coordinate of the enemy.
        RETURNS:
        --------
        int
            The x coordinate of the enemy
        '''
        return self.__x
    
    def getY(self):
        '''
        Returns the y coordinate of the enemy.
        RETURNS:
        --------
        int
            The y coordinate of the enemy
        '''
        return self.__y
    
    def getHeight(self):
        '''
        Returns the height of the enemy.
        RETURNS:
        --------
        float
            The height of the enemy
        '''
        return self.__height
    
    def getWidth(self):
        '''
        Returns the width of the enemy.
        RETURNS:
        --------
        float
            The width of the enemy
        '''
        return self.__width