#Authors: Haris Shah and Waleed Ghufran
#Date: Nov 12, 2020
#Program Name: MortalScape
#Course Code: ICS5U1
#Work Division: Waleed Ghufran: Created all graphics and the interface, created both toplevels, 
#               player movement, placement of blocks and coins. As well as close functions and life functions.
#               Haris Shah: Programmed Collision, buttons, classes, place spike function, clear function, 
#               reset function, keybinds, fall function and sounds.



from tkinter import Tk, Toplevel, Button, Label, Frame, Canvas, PhotoImage, messagebox, font, ttk
from src.player import Player
from src.block import Block
from src.enemy import Enemy
from src.coins import Coins
from src.finish_point import FinishPoint
import pygame

# Create a function that closes the program and destroys all windows
def close_mainMenu():
    
    pygame.mixer.Sound.play(soundEffects[0])
    
    ans = messagebox.askyesno('MORTALSCAPE', 'Are you sure you want to quit playing?')
    
    if ans == True:
        mainMenu.destroy()
        helpScreen.destroy()
        gameScreen.destroy()
        
        exit()
    else:
        return

# Create a function that withdraws the help menu and brings up the main menu    
def close_help():
    pygame.mixer.Sound.play(soundEffects[0])
    mainMenu.update()
    mainMenu.deiconify()
    
    helpScreen.withdraw()

# Create a function that withdraws the game screen, and brings up the main menu    
def close_game():
    global check, lives
    
    lives = int(cboLives.get())
    displayLives(lives)
    
    check = False
    checkCollision()
    resetAllButtons()
    gameBackground.bind('<Button-1>', dummy)
    gameScreen.bind('<KeyPress>', dummy)
    gameScreen.bind('<KeyRelease>', dummy)
    gameBackground.config(cursor = '')
    player.setLocation(0, gameBackground.winfo_reqheight())
    player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
    
    pygame.mixer.Sound.play(soundEffects[0])
    mainMenu.update()
    mainMenu.deiconify()
    
    gameScreen.withdraw()

# Create a function that withdraws the main menu and brings up the game screen    
def play():
    pygame.mixer.Sound.play(soundEffects[0])
    gameScreen.update()
    gameScreen.deiconify()
    
    mainMenu.withdraw()

# Create a function that withdraws the main menu and brings up the help menu    
def displayHelp():
    pygame.mixer.Sound.play(soundEffects[0])
    helpScreen.update()
    helpScreen.deiconify()
    
    mainMenu.withdraw()

# Create a function that resets all buttons to their original states    
def resetAllButtons():
    btnPlaceBlocks.config(image = PBImg, bg = 'black')
    btnPlaceEnemy.config(image = PSImg, bg = 'black')
    btnPlaceCoins.config(image = PCImg, bg = 'black')
    btnClear.config(image = CAImg, bg = 'black')
    btnPlayGame.config(image = PGImg, bg = 'black')

# Create a function that is called whenever the user wants to place blocks
def placeBlocks():
    global check, lives, score
    
    # Delete the welcome message
    try:
        gameBackground.delete(beginTxt)
    except:
        pass

    # Reset the score to 0
    score = 0
    gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
    
    # Play the button clicked sound effect
    pygame.mixer.Sound.play(soundEffects[0])
    
    # Reset the lives to the chosen value in the combobox and display the appropriate image
    lives = int(cboLives.get())
    displayLives(lives)
    
    # Stop checking for collision
    check = False
    checkCollision()
    # Reset all buttons to their original state
    resetAllButtons()
    # Configure the Place Blocks button to show that it is selected
    btnPlaceBlocks.config(image = PBGImg, bg = 'white')
    # If the player clicks anywhere on the screen, call the placeOneBlock function
    gameBackground.bind('<Button-1>', placeOneBlock)
    # Set window events to a dummy function
    gameScreen.bind('<KeyPress>', dummy)
    gameScreen.bind('<KeyRelease>', dummy)
    gameBackground.config(cursor = 'hand2')
    # Set the player's location to the bottom right side and set the image to face the right
    player.setLocation(0, gameBackground.winfo_reqheight())
    player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
    

def placeOneBlock(event):
    global indexBlocks, flag
    
    # Get the x and y coordinates of where the player clicked on the screen
    x = event.x
    y = event.y
    
    # Mod x and y by 32 to ensure the blocks place properly on the screen
    x = x - (x % 32)
    y = y - (y % 32)
    
    # Throw an error if the block is placed on the player or on the flag
    if x == 0 and y == 512:
        messagebox.showinfo('MORTALSCAPE', 'You cannot place a block where the player starts!')
        return
    elif x == 0 and y == 480:
        messagebox.showinfo('MORTALSCAPE', 'You cannot place a block where the player starts!')
        return
    elif x == 992 and y == 512:
        messagebox.showinfo('MORTALSCAPE', 'You cannot place a block at the finish point!')
        return
    elif x == 992 and y == 480:
        messagebox.showinfo('MORTALSCAPE', 'You cannot place a block at the finish point!')
        return
    else:
        pass
    
    # If the player has clicked where a coin already exists, throw an error
    for counter in range(len(coinsList)):
        if x == coinsList[counter].getX() and y == coinsList[counter].getY():
            messagebox.showinfo('MORTALSCAPE', 'You cannot place a block where a coin is already placed!')
            return
        else:
            pass
     
    # If the player has clicked where a spike already exists, throw an error   
    for counter in range(len(enemyList)):
        if x == enemyList[counter].getX() and y == enemyList[counter].getY():
            messagebox.showinfo('MORTALSCAPE', 'You cannot place a block where a spike is already placed!')
            return
        else:
            pass
    
    # If this is the only block placed on the screen, place the block increase the indexBlocks and play a sound effect
    # Ignore if it is not the first block being placed
    if indexBlocks == 0:
        blocksList.extend('0')
        blocksList[indexBlocks] = Block(gameBackground)
        blocksList[indexBlocks].placeBlock(x = x, y = y)
        indexBlocks += 1
        pygame.mixer.Sound.play(soundEffects[1])
        return indexBlocks
    else:
        pass
    
    # If the player has clicked where a block already exists, remove that block, reduce indexBlocks and play a sound effect
    for counter in range(len(blocksList)):
        if x == blocksList[counter].getX() and y == blocksList[counter].getY():
            blocksList[counter].removeBlock()
            del blocksList[counter]
            indexBlocks -= 1
            pygame.mixer.Sound.play(soundEffects[1])
            return indexBlocks
        else:
            pass
    
    # Place a block
    blocksList.extend('0')
    blocksList[indexBlocks] = Block(gameBackground)
    blocksList[indexBlocks].placeBlock(x = x, y = y)
    indexBlocks += 1
    
    # Play a sound effect
    pygame.mixer.Sound.play(soundEffects[1])
    
    return indexBlocks
    
def placeEnemy():
    global check, lives, score
    
    # Delete the welcome message
    try:
        gameBackground.delete(beginTxt)
    except:
        pass
    
    # Reset the score to 0
    score = 0
    gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
    
    # Play the button clicked sound effect
    pygame.mixer.Sound.play(soundEffects[0])
    
    # Reset the lives to the chosen value in the combobox and display the appropriate image
    lives = int(cboLives.get())
    displayLives(lives)
    
    # Stop checking for collision
    check = False
    checkCollision()
    # Reset all buttons to their original state
    resetAllButtons()
    # Configure the Place Spike button to show that it is selected
    btnPlaceEnemy.config(image = PSGImg, bg = 'white')
    # If the player clicks anywhere on the screen, call the placeOneEnemy function
    gameBackground.bind('<Button-1>', placeOneEnemy)
    # Set window events to a dummy function
    gameScreen.bind('<KeyPress>', dummy)
    gameScreen.bind('<KeyRelease>', dummy)
    gameBackground.config(cursor = 'hand2')
    # Set the player's location to the bottom right side and set the image to face the right
    player.setLocation(0, gameBackground.winfo_reqheight())
    player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
    
def placeOneEnemy(event):
    global indexEnemy
    
    # Get the x and y coordinates of where the player clicked on the screen
    x = event.x
    y = event.y
    
    # Mod x and y by 32 to ensure the spikes place properly on the screen
    x = x - (x % 32)
    y = y - (y % 32)
    
    # Throw an error if the spike is placed on the player or on the flag
    if x == 0 and y == 512:
        messagebox.showinfo('MORTALSCAPE', 'You cannot place spikes where the player spawns!')
        return
    elif x == 0 and y == 480:
        messagebox.showinfo('MORTALSCAPE', 'You cannot place spikes where the player spawns!')
        return
    elif x == 992 and y == 512:
        messagebox.showinfo('MORTALSCAPE', 'You cannot place spikes at the finish point!')
        return
    elif x == 992 and y == 480:
        messagebox.showinfo('MORTALSCAPE', 'You cannot place spikes at the finish point!')
        return
    
    # If the player has clicked where a block already exits, throw an error
    for counter in range(len(blocksList)):
        if x == blocksList[counter].getX() and y == blocksList[counter].getY():
            messagebox.showinfo('MORTALSCAPE', 'You cannot place a spike where a block is already placed!')
            return
        else:
            pass
     
    # If the player has clicked where a coin already exists, throw an error
    for counter in range(len(coinsList)):
        if x == coinsList[counter].getX() and y == coinsList[counter].getY():
            messagebox.showinfo('MORTALSCAPE', 'You cannot place a spike where a coin is already placed!')
            return
        else:
            pass
    # If this is the only spike placed on the screen, place the spike, increase indexEnemy and play a sound effect
    # Ignore if it is not the first spike being placed
    if indexEnemy == 0:
        enemyList.extend('0')
        enemyList[indexEnemy] = Enemy(gameBackground)
        enemyList[indexEnemy].placeEnemy(x = x, y = y)
        indexEnemy += 1
        pygame.mixer.Sound.play(soundEffects[4])
        return indexEnemy
    else:
        pass
    
    # If the player has clicked where a spike already exists, remove that spike, reduce indexEnemy and play a sound effect
    for counter in range(len(enemyList)):
        if x == enemyList[counter].getX() and y == enemyList[counter].getY():
            enemyList[counter].removeEnemy()
            del enemyList[counter]
            indexEnemy -= 1
            pygame.mixer.Sound.play(soundEffects[4])
            return indexEnemy
        else:
            pass
     
    # Place a spike
    enemyList.extend('0')
    enemyList[indexEnemy] = Enemy(gameBackground)
    enemyList[indexEnemy].placeEnemy(x = x, y = y)
    indexEnemy += 1
    
    # Play a sound effect
    pygame.mixer.Sound.play(soundEffects[4])
    
    return indexEnemy

def placeCoins():
    global check, lives, score
    
    # Delete the welcome message
    try:
        gameBackground.delete(beginTxt)
    except:
        pass
    
    # Reset the score to 0
    score = 0
    gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
    
    # Play the button clicked sound effect
    pygame.mixer.Sound.play(soundEffects[0])
    
    # Reset the lives to the chosen value in the combobox and display the appropriate image
    lives = int(cboLives.get())
    displayLives(lives)
    # Stop checking for collision
    check = False
    checkCollision()
    # Reset all buttons to their original state
    resetAllButtons()
    # Configure the Place Coins button to show that it is selected
    btnPlaceCoins.config(image = PCGImg, bg = 'white')
    # If the player clicks anywhere on the screen, call the placeOneCoin function
    gameBackground.bind('<Button-1>', placeOneCoin)
    # Set window events to a dummy function
    gameScreen.bind('<KeyPress>', dummy)
    gameScreen.bind('<KeyRelease>', dummy)
    gameBackground.config(cursor = 'hand2')
    # Set the player's location to the bottom right side and set the image to face the right
    player.setLocation(0, gameBackground.winfo_reqheight())
    player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
    
def placeOneCoin(event):
    global indexCoins
    
    # Get the x and y coordinates of where the player clicked on the screen
    x = event.x
    y = event.y
    
    # Mod x and y by 32 to ensure the spikes place properly on the screen
    x = x - (x % 32)
    y = y - (y % 32)
    
    # Throw an error if the coin is placed on the player or on the flag
    if x == 0 and y == 512:
        messagebox.showinfo('MORTALSCAPE', 'You cannot place coins where the player spawns!')
        return
    elif x == 0 and y == 480:
        messagebox.showinfo('MORTALSCAPE', 'You cannot place coins where the player spawns!')
        return
    elif x == 992 and y == 512:
        messagebox.showinfo('MORTALSCAPE', 'You cannot place coins at the finish point!')
        return
    elif x == 992 and y == 480:
        messagebox.showinfo('MORTALSCAPE', 'You cannot place coins at the finish point!')
        return
    
    # If the player has clicked where a block already exits, throw an error
    for counter in range(len(blocksList)):
        if x == blocksList[counter].getX() and y == blocksList[counter].getY():
            messagebox.showerror('MORTALSCAPE', 'You cannot place a coin where a block is already placed!')
            return
        else:
            pass
    
    # If the player has clicked where a spike already exists, throw an error
    for counter in range(len(enemyList)):
        if x == enemyList[counter].getX() and y == enemyList[counter].getY():
            messagebox.showinfo('MORTALSCAPE', 'You cannot place a coin where a spike is already placed!')
            return
        else:
            pass
    
    # If this is the only coin placed on the screen, place the coin, increase indexCoins and play a sound effect
    # Ignore if it is not the first coin being placed
    if indexCoins == 0:
        coinsList.extend('0')
        coinsList[indexCoins] = Coins(gameBackground)
        coinsList[indexCoins].placeCoin(x = x, y = y)
        indexCoins += 1
        pygame.mixer.Sound.play(soundEffects[6])
        return indexCoins
    else:
        pass
    
    # If the player has clicked where a coin already exists, remove that coin, reduce indexCoins and play a sound effect
    for counter in range(len(coinsList)):
        if x == coinsList[counter].getX() and y == coinsList[counter].getY():
            coinsList[counter].removeCoin()
            del coinsList[counter]
            indexCoins -= 1
            pygame.mixer.Sound.play(soundEffects[6])
            return indexCoins
        else:
            pass
    
    # Place a coin   
    coinsList.extend('0')
    coinsList[indexCoins] = Coins(gameBackground)
    coinsList[indexCoins].placeCoin(x = x, y = y)
    indexCoins += 1
    
    # Play a sound effect
    pygame.mixer.Sound.play(soundEffects[6])
    
    return indexCoins

# Create a function that is bound to a combobox that allows the player to select the amount of lives
def setLives(event):
    global lives
    
    chosenLives = int(cboLives.get())
    
    if chosenLives == 1:
        lives = 1
    elif chosenLives == 2:
        lives = 2
    elif chosenLives == 3:
        lives = 3
    
    displayLives(lives)
    return lives

# Based on the number of lives remaining, configure the images at the top
def displayLives(x):
    global lives, check
    
    if x == 1:
        liveslbl1.config(image = livesImg)
        liveslbl2.config(image = '')
        liveslbl3.config(image = '')
    elif x == 2:
        liveslbl1.config(image = livesImg)
        liveslbl2.config(image = livesImg)
        liveslbl3.config(image = '')
    elif x == 3:
        liveslbl1.config(image = livesImg)
        liveslbl2.config(image = livesImg)
        liveslbl3.config(image = livesImg)
    # If the lives reach 0, ask the user if they would like to continue playing.
    # If the player answers yes, reset the lives to the value in the combobox, configure the images, stop checking for collision, bind all 
    # window and canvas events to the dummy function, reset all buttons to their original states, and reset the player's location.
    # If the player answers no, return to the main menu.
    elif x == 0:
        liveslbl1.config(image = '')
        liveslbl2.config(image = '')
        liveslbl3.config(image = '')
        ans = messagebox.askyesno("MORTALSCAPE", "You have 0 lives remaining. \nWould you like to continue editing your level?")
        if ans == True:
            chosenLives = int(cboLives.get())
            if chosenLives == 1:
                liveslbl1.config(image = livesImg)
                liveslbl2.config(image = '')
                liveslbl3.config(image = '')
                lives = 1
            elif chosenLives == 2:
                liveslbl1.config(image = livesImg)
                liveslbl2.config(image = livesImg)
                liveslbl3.config(image = '')
                lives = 2
            elif chosenLives == 3:
                liveslbl1.config(image = livesImg)
                liveslbl2.config(image = livesImg)
                liveslbl3.config(image = livesImg)
                lives = 3
                
            resetAllButtons()
            
            check = False
            checkCollision()
            gameBackground.bind('<Button-1>', dummy)
            gameScreen.bind('<KeyPress>', dummy)
            gameScreen.bind('<KeyRelease>', dummy)
            gameBackground.config(cursor = '')
            
            return
        else:
            close_game()

# Create a function that removes all objects from the screen, resets the player's position to the start and resets all values and lists to their
# original states.
def clearAll():
    global indexBlocks, indexCoins, indexEnemy, blocksList, coinsList, enemyList, check, lives, score
    
    score = 0
    gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
    
    pygame.mixer.Sound.play(soundEffects[0])
    
    lives = int(cboLives.get())
    displayLives(lives)
    
    ans = messagebox.askyesno('MORTALSCAPE', 'Are you sure you want to remove all objects from the screen?')
    
    if ans == True:
        pass
    else:
        return
    
    check = False
    checkCollision()
    gameBackground.bind('<Button-1>', dummy)
    gameScreen.bind('<KeyPress>', dummy)
    gameScreen.bind('<KeyRelease>', dummy)
    gameBackground.config(cursor = '')
    
    resetAllButtons()
    
    player.setLocation(x = 0, y = gameBackground.winfo_reqheight())
    player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
    
    for counter in range(len(blocksList)):
        blocksList[counter].removeBlock()
        
    blocksList = []
    indexBlocks = 0
    
    for counter in range(len(coinsList)):
        coinsList[counter].removeCoin()
        
    coinsList = []
    indexCoins = 0
    
    for counter in range(len(enemyList)):
        enemyList[counter].removeEnemy()
        
    enemyList = []
    indexEnemy = 0
    
    return indexBlocks, indexCoins, indexEnemy, blocksList, coinsList, enemyList

# Create a function that starts playing the game, allows control for the player and starts checking for collision
def playGame():
    global fall, check
    
    # Delete the welcome message
    try:
        gameBackground.delete(beginTxt)
    except:
        pass
    
    pygame.mixer.Sound.play(soundEffects[0])
    
    check = True
    resetAllButtons()
    btnPlayGame.config(image = PGGImg, bg = 'white')
    gameBackground.bind('<Button-1>', dummy)
    gameScreen.bind('<KeyPress>', onkeypress)
    gameScreen.bind('<KeyRelease>', onkeyrelease)
    gameBackground.config(cursor = '')
    checkCollision()

# Create a dummy event function that can be bound to the window or canvas that will not in use at any particluar time    
def dummy(event):
    return

# Create a jump function that allows the player to jump
def playerJump():
    global seconds, fall, timer, playerIsJumped, jump

    timer = gameScreen.after(50, playerJump)
    
    if jump == True:
        if seconds == 11:
            jump = False
            playerIsJumped = False
            seconds = 0
            gameScreen.after_cancel(timer)
            fall = True
            playerFall()
        else:
            playerIsJumped = True
            player.setY(player.getY() - 10)
            fall = False
            playerFall()
            seconds += 1
    else:
        seconds = 0
        playerIsJumped = False
        gameScreen.after_cancel(timer)
        fall = True
        playerFall()

# Create a function that causes the player to fall every time it is called and as long as fall == True        
def playerFall():
    global fall, timerTwo
    
    timerTwo = gameScreen.after(500, playerFall)
    
    if fall == True:
        player.setY(player.getY() + 10)
    else:
        gameScreen.after_cancel(timerTwo)
        player.setY(player.getY())

# Create a function that allows for movement in the x-axis and jumping
def onkeypress(event):
    global movingLeft, movingRight, timerRight, timerLeft
    
    if event.char == 'd' or event.char == 'D' or event.keysym == 'Right':
        if movingRight == True:
            moveRight()
            player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
    elif event.char == 'a' or event.char == 'A' or event.keysym == 'Left':
        if movingLeft == True:
            moveLeft()
            player.setImage(PhotoImage(file = 'img/PlayerLeft.png'))
    elif event.keysym == 'space' or event.keysym == 'Up':
        playerJump()
        gameScreen.bind('<KeyPress>', onkeypress_withoutjump)
        pygame.mixer.Sound.play(soundEffects[2])

# Create a function that moves the player to the right by 20px
def moveRight():
    player.move(x = 20)

# Create a function that moves the player to the left by 20px    
def moveLeft():
    player.move(x = -20)

# Create a function that only allows for movement in the x-axis and disregards jumping
def onkeypress_withoutjump(event):
    global movingLeft, movingRight, timerRight, timerLeft
    
    if event.char == 'd' or event.char == 'D' or event.keysym == 'Right':
        if movingRight == True:
            moveRight()
            player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
    elif event.char == 'a' or event.char == 'A' or event.keysym == 'Left':
        if movingLeft == True:
            moveLeft()
            player.setImage(PhotoImage(file = 'img/PlayerLeft.png'))
        
def onkeyrelease(event):
    global movingLeft, movingRight, timerRight, timerLeft
    
    return

def checkCollision():
    global indexBlocks, fall, movingLeft, movingRight, jump, indexCoins, playerIsJumped, score, timer, check, lives, lives2, seconds
    
    # Loop this function every 25 ms.
    timerTwo = gameScreen.after(25, checkCollision)
    
    # As long as check is set to True, collision will keep being checked 
    if check == True:
        pass
    else:
        gameScreen.after_cancel(timerTwo)
        fall = False
        jump = False
        seconds = 0
        playerFall()
        return
     
    # Ensure the player does not go off the screen
    if player.getX() <= 0:
        player.setX(0)
        movingLeft = False
        movingRight = True
    elif player.getX() + player.getWidth() >= gameBackground.winfo_reqwidth():
        player.setX(gameBackground.winfo_reqwidth() - player.getWidth())
        movingLeft = True
        movingRight = False
    else:
        player.setX(player.getX())
        movingLeft = True
        movingRight = True
    if player.getY()  >= gameBackground.winfo_reqheight():
        player.setY(gameBackground.winfo_reqheight())
        fall = False
        jump = True
        playerIsJumped = False
        gameScreen.bind('<KeyPress>', onkeypress)
    elif player.getY() - player.getHeight() <= 0:
        player.setY(0 + player.getHeight())
        fall = True
        jump = False
        gameScreen.bind('<KeyPress>', onkeypress_withoutjump)
    else:
        gameScreen.bind('<KeyPress>', onkeypress_withoutjump)
        
    # Check for collision if a player is on top of a block
    # If collision is detected, immediately set the y-position of the player to the top of the block, stop the player from falling, and allow
    # them to jump again.
    for counter in range(len(blocksList)):
        if player.getY() + 2 >= blocksList[counter].getY() and player.getY() + 2 < blocksList[counter].getY() + blocksList[counter].getHeight():
            if player.getX() > blocksList[counter].getX() and player.getX() < blocksList[counter].getX() + blocksList[counter].getWidth():
                player.setY(blocksList[counter].getY())
                fall = False
                playerIsJumped = False
                jump = True
                gameScreen.bind('<KeyPress>', onkeypress)
                break
            elif player.getX() + player.getWidth() > blocksList[counter].getX() and player.getX() + player.getWidth() < blocksList[counter].getX() + blocksList[counter].getWidth():
                player.setY(blocksList[counter].getY())
                fall = False
                playerIsJumped = False
                jump = True
                gameScreen.bind('<KeyPress>', onkeypress)
                break
            elif player.getX() == blocksList[counter].getX() and player.getX() + player.getWidth() == blocksList[counter].getX() + blocksList[counter].getWidth():
                player.setY(blocksList[counter].getY())
                fall = False
                playerIsJumped = False
                jump = True
                gameScreen.bind('<KeyPress>', onkeypress)
                break
            else:
                if playerIsJumped == True:
                    fall = False
                    gameScreen.bind('<KeyPress>', onkeypress_withoutjump)
                else:
                    fall = True
                    gameScreen.bind('<KeyPress>', onkeypress_withoutjump)
                    
    # Check for collision if a player is underneath a block.
    # If a player is detected as being directly underneath a block, set their y-position to the bottom of the block and either cancel 
    # the player's jump or do not allow the player to jump again.
    for counter in range(len(blocksList)):
        if player.getY() - player.getHeight() + 2 <= blocksList[counter].getY() + blocksList[counter].getHeight() and player.getY() - player.getHeight() + 2 > blocksList[counter].getY() + blocksList[counter].getHeight() - 10:
            if not player.getY() - player.getHeight() + 2 == blocksList[counter].getY() or player.getY() - player.getHeight() + 2 == blocksList[counter].getY() + blocksList[counter].getHeight:
                if player.getX() + player.getWidth() > blocksList[counter].getX() and player.getX() + player.getWidth() < blocksList[counter].getX() + blocksList[counter].getWidth():
                    player.setY(blocksList[counter].getY() + blocksList[counter].getHeight() + player.getHeight())
                    jump = False 
                    gameScreen.bind('<KeyPress>', onkeypress_withoutjump)
                    break
                elif player.getX() < blocksList[counter].getX() + blocksList[counter].getWidth() and player.getX() > blocksList[counter].getX():
                    player.setY(blocksList[counter].getY() + blocksList[counter].getHeight() + player.getHeight())
    #                 player.setX(player.getX())
                    jump = False
                    gameScreen.bind('<KeyPress>', onkeypress_withoutjump)
                    break
                elif player.getX() == blocksList[counter].getX() and player.getX() + player.getWidth() == blocksList[counter].getX() + blocksList[counter].getWidth():
                    player.setY(blocksList[counter].getY() + blocksList[counter].getHeight() + player.getHeight())
    #                 player.setX(player.getX())
                    jump = False
                    gameScreen.bind('<KeyPress>', onkeypress_withoutjump)
                    break
                else:
                    gameScreen.bind('<KeyPress>', onkeypress)
                    pass
    
    # Check for collision with the player's right side and the block's left side
    # If collision is detected, set the player's x-position to the left side of the block and do not allow the player to move right
    for counter in range(len(blocksList)):
        if player.getX() + player.getWidth() >= blocksList[counter].getX() and player.getX() + player.getWidth() < blocksList[counter].getX() + blocksList[counter].getWidth():
            if player.getY() < blocksList[counter].getY() + blocksList[counter].getHeight() and player.getY() > blocksList[counter].getY() + 2:
                player.setX(blocksList[counter].getX() - player.getWidth())
                movingRight = False
                break
            elif player.getY() - player.getHeight() + 2 < blocksList[counter].getY() + blocksList[counter].getHeight() and player.getY() > blocksList[counter].getY() + 2:
                player.setX(blocksList[counter].getX() - player.getWidth())
                movingRight = False
                break
            else:
                pass
    # Check for collision with the player's left side and the block's right side.
    # If collision is detected, set the player's x-position to the right side of the block and do not allow the player to move left.
    for counter in range(len(blocksList)):
        if player.getX() <= blocksList[counter].getX() + blocksList[counter].getWidth() and player.getX() > blocksList[counter].getX():
            if player.getY() < blocksList[counter].getY() + blocksList[counter].getHeight() and player.getY() > blocksList[counter].getY() + 2:
                player.setX(blocksList[counter].getX() + blocksList[counter].getWidth())
                movingLeft = False
                break
            elif player.getY() - player.getHeight() + 2 < blocksList[counter].getY() + blocksList[counter].getHeight() and player.getY() > blocksList[counter].getY() + 2:
                player.setX(blocksList[counter].getX() + blocksList[counter].getWidth())
                movingLeft = False
                break
            else:
                pass
     
    # Check for collision between the spikes and the player.
    # If collision is detected, make a blood splatter image in place of the player, reduce the amount of lives, reduce the score, play a sound,
    # call the displayLives() function, display a messagebox showing the player that they lost a life and reset the player's position to the start.
    for counter in range(len(enemyList)):
        if player.getX() + player.getWidth() - 5 >= enemyList[counter].getX() + 5 and player.getX() + player.getWidth() - 5 < enemyList[counter].getX() + enemyList[counter].getWidth() - 5:
            if player.getY() - 5 >= enemyList[counter].getY() + 5 and player.getY() - 5 <= enemyList[counter].getY() + enemyList[counter].getHeight() - 5:
                if score > 0:
                    score -= 10
                    gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
                else:
                    pass
                pygame.mixer.Sound.play(soundEffects[3])
                blood = gameBackground.create_image(player.getX(), player.getY(), image = blood_img, anchor = 'sw')
                lives -= 1
                player.setLocation(0, gameBackground.winfo_reqheight())
                player.setImage(img = '')
                if lives > 0:
                    messagebox.showinfo('MORTALSCAPE', 'You died!\nYou have ' + str(lives) + ' lives remaining.')
                else:
                    pass
                displayLives(lives)
                gameBackground.delete(blood)
                player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
                break
            elif player.getY() - player.getHeight() + 5 >= enemyList[counter].getY() + 5 and player.getY() - player.getHeight() + 5 <= enemyList[counter].getY() + enemyList[counter].getHeight() - 5:
                if score > 0:
                    score -= 10
                    gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
                else:
                    pass
                pygame.mixer.Sound.play(soundEffects[3])
                blood = gameBackground.create_image(player.getX(), player.getY(), image = blood_img, anchor = 'sw')
                lives -= 1
                player.setLocation(0, gameBackground.winfo_reqheight())
                player.setImage(img = '')
                if lives > 0:
                    messagebox.showinfo('MORTALSCAPE', 'You died!\nYou have ' + str(lives) + ' lives remaining.')
                else:
                    pass
                displayLives(lives)
                gameBackground.delete(blood)
                player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
                break
            else:
                pass
        elif player.getX() + 5 <= enemyList[counter].getX() + enemyList[counter].getWidth() - 5 and player.getX() + 5 > enemyList[counter].getX() + 5:
            if player.getY() - 5 >= enemyList[counter].getY() + 5 and player.getY() - 5 <= enemyList[counter].getY() + enemyList[counter].getHeight() - 5:
                if score > 0:
                    score -= 10
                    gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
                else:
                    pass
                pygame.mixer.Sound.play(soundEffects[3])
                blood = gameBackground.create_image(player.getX(), player.getY(), image = blood_img, anchor = 'sw')
                lives -= 1
                player.setLocation(0, gameBackground.winfo_reqheight())
                player.setImage(img = '')
                if lives > 0:
                    messagebox.showinfo('MORTALSCAPE', 'You died!\nYou have ' + str(lives) + ' lives remaining.')
                else:
                    pass
                displayLives(lives)
                gameBackground.delete(blood)
                player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
                break
            elif player.getY() - player.getHeight() + 5 >= enemyList[counter].getY() + 5 and player.getY() - player.getHeight() + 5 <= enemyList[counter].getY() + enemyList[counter].getHeight() - 5:
                if score > 0:
                    score -= 10
                    gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
                else:
                    pass
                pygame.mixer.Sound.play(soundEffects[3])
                blood = gameBackground.create_image(player.getX(), player.getY(), image = blood_img, anchor = 'sw')
                lives -= 1
                player.setLocation(0, gameBackground.winfo_reqheight())
                player.setImage(img = '')
                if lives > 0:
                    messagebox.showinfo('MORTALSCAPE', 'You died!\nYou have ' + str(lives) + ' lives remaining.')
                else:
                    pass
                displayLives(lives)
                gameBackground.delete(blood)
                player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
                break
            else:
                pass
        elif player.getX() == enemyList[counter].getX() and player.getX() + player.getWidth() == enemyList[counter].getX() + enemyList[counter].getWidth():
            if player.getY() - 5 >= enemyList[counter].getY() + 5 and player.getY() - 5 <= enemyList[counter].getY() + enemyList[counter].getHeight() - 5:
                if score > 0:
                    score -= 10
                    gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
                else:
                    pass
                pygame.mixer.Sound.play(soundEffects[3])
                blood = gameBackground.create_image(player.getX(), player.getY(), image = blood_img, anchor = 'sw')
                lives -= 1
                player.setLocation(0, gameBackground.winfo_reqheight())
                player.setImage(img = '')
                if lives > 0:
                    messagebox.showinfo('MORTALSCAPE', 'You died!\nYou have ' + str(lives) + ' lives remaining.')
                else:
                    pass
                displayLives(lives)
                gameBackground.delete(blood)
                player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
                break
            elif player.getY() - player.getHeight() + 5 >= enemyList[counter].getY() + 5 and player.getY() - player.getHeight() + 5 <= enemyList[counter].getY() + enemyList[counter].getHeight() - 5:
                if score > 0:
                    score -= 10
                    gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
                else:
                    pass
                pygame.mixer.Sound.play(soundEffects[3])
                blood = gameBackground.create_image(player.getX(), player.getY(), image = blood_img, anchor = 'sw')
                lives -= 1
                player.setLocation(0, gameBackground.winfo_reqheight())
                player.setImage(img = '')
                if lives > 0:
                    messagebox.showinfo('MORTALSCAPE', 'You died!\nYou have ' + str(lives) + ' lives remaining.')
                else:
                    pass
                displayLives(lives)
                gameBackground.delete(blood)
                player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
                break
            else:
                pass
        else:
            pass
     
    # Check for collision with the coins
    # If collision is detected, play a sound, increase the score and remove the coin from the screen
    for counter in range(len(coinsList)):
        if player.getX() + player.getWidth() >= coinsList[counter].getX() and player.getX() + player.getWidth() < coinsList[counter].getX() + coinsList[counter].getWidth():
            if player.getY() >= coinsList[counter].getY() and player.getY() <= coinsList[counter].getY() + coinsList[counter].getHeight():
                pygame.mixer.Sound.play(soundEffects[5])
                coinsList[counter].removeCoin()
                del coinsList[counter]
                indexCoins -= 1
                score += 10
                gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
                break
            elif player.getY() - player.getHeight() >= coinsList[counter].getY() and player.getY() - player.getHeight() <= coinsList[counter].getY() + coinsList[counter].getHeight():
                pygame.mixer.Sound.play(soundEffects[5])
                coinsList[counter].removeCoin()
                del coinsList[counter]
                indexCoins -= 1
                score += 10
                gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
                break
            else:
                pass
        elif player.getX() <= coinsList[counter].getX() + coinsList[counter].getWidth() and player.getX() > coinsList[counter].getX():
            if player.getY() >= coinsList[counter].getY() and player.getY() <= coinsList[counter].getY() + coinsList[counter].getHeight():
                pygame.mixer.Sound.play(soundEffects[5])
                coinsList[counter].removeCoin()
                del coinsList[counter]
                indexCoins -= 1
                score += 10
                gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
                break
            elif player.getY() - player.getHeight() >= coinsList[counter].getY() and player.getY() - player.getHeight() <= coinsList[counter].getY() + coinsList[counter].getHeight():
                pygame.mixer.Sound.play(soundEffects[5])
                coinsList[counter].removeCoin()
                del coinsList[counter]
                indexCoins -= 1
                score += 10
                gameCanvas.itemconfig(displayScore, text = 'Score: ' + str(score))
                break
            else:
                pass
        else:
            pass
     
    # Check for collision with the finish point
    # If collision is detected, display a messagebox showing the player that they beat the level with their score and ask the user if they wish
    # to keep playing. If the player answers yes, reset the player's x-position to the start. If they answer no, take the player back to the 
    # main menu
    if player.getX() >= finish.getX() - finish.getWidth() and player.getX() <= finish.getX():
        if player.getY() >= finish.getY() - finish.getHeight() and player.getY() <= finish.getY():
            confetti1 = gameBackground.create_image(512,100, image = confettiImg)
            confetti2 = gameBackground.create_image(850,150, image = confettiImg)
            confetti3 = gameBackground.create_image(180,150, image = confettiImg)
            pygame.mixer.Sound.play(soundEffects[7])
            gameBackground.bind('<Button-1>', dummy)
            gameScreen.bind('<KeyPress>', dummy)
            gameScreen.bind('<KeyRelease>', dummy)
            player.setLocation(x = 0, y = gameBackground.winfo_reqheight())
            player.setImage(img = '')
            ans = messagebox.askyesno('MORTALSCAPE', 'You beat the level and finished with a score of ' + str(score) + '.\nWould you like to continue playing/editing your level?')
            if ans == True:
                score = 0
                gameBackground.itemconfig(displayScore, text = 'Score: ' + str(score))
                player.setImage(PhotoImage(file = 'img/PlayerRight.png'))
                lives = int(cboLives.get())
                displayLives(lives)
                resetAllButtons()
                gameBackground.delete(confetti1,confetti2,confetti3)
            
                check = False
                checkCollision()
                gameBackground.bind('<Button-1>', dummy)
                gameScreen.bind('<KeyPress>', dummy)
                gameScreen.bind('<KeyRelease>', dummy)
                gameBackground.config(cursor = '')
                gameBackground.delete(confetti1, confetti2,confetti3)

            else:
                score = 0
                gameBackground.itemconfig(displayScore, text = 'Score: ' + str(score))
                close_game()
    
    # Gravity 
    playerFall()


###################################################################################################################################################

# Set variables for all the window widths and heights
WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 768

# Create a list of audio files
audioFiles = ['sounds/Button Sound.wav', 'sounds/Plop.wav', 'sounds/Jump.wav', 'sounds/Death.wav', 'sounds/Spike.wav', 
    'sounds/CoinCollected.mp3', 'sounds/Ding.mp3', 'sounds/Yay.mp3']
# Create an empty list that will later be filled with sound objects
soundEffects = [0] * 8
# Initialize the pygame mixer
pygame.mixer.init()
# Initialize and store the list of Sound objects
for counter in range(len(audioFiles)):
    soundEffects[counter] = pygame.mixer.Sound(audioFiles[counter])
    soundEffects[counter].set_volume(0.30)

# Initialize and set properties for a Tk object
# This window will be the main window that the game will be played on
gameScreen = Tk()
gameScreen.title('MORTALSCAPE')
gameScreen.bind('<KeyPress>', dummy)
gameScreen.bind('<KeyRelease>', dummy)
gameScreen.protocol('WM_DELETE_WINDOW', close_mainMenu)
gameScreen.geometry("%dx%d+%d+%d" % (WINDOW_WIDTH, WINDOW_HEIGHT, gameScreen.winfo_screenwidth() // 2 - WINDOW_WIDTH // 2, 
    gameScreen.winfo_screenheight() // 2 - WINDOW_HEIGHT // 2))
gameScreen.resizable(False, False)
gameScreen.pack_propagate(False)
gameScreen.withdraw()

# Create various PhotoImages
confettiImg = PhotoImage(file = "img/Confetti.png")
gameNameImg = PhotoImage(file = "img/GameName.png")
ArrowImg = PhotoImage(file = "img/Home.png")
livesImg = PhotoImage(file = 'img/Heart.png')
background = PhotoImage(file = 'img/Background.png')
img_ground = PhotoImage(file = 'img/Ground.png')
blood_img = PhotoImage(file = 'img/Blood.png')
BeginImg = PhotoImage(file = "img/BeginImg.png")
gameTop = Frame(gameScreen, width = WINDOW_WIDTH, height = 64, bg = '#11C3ED')
gameTop.pack()
Homebtn = Button(gameScreen,  image = ArrowImg, bg = '#11C3ED',activebackground = '#11C3ED',  command = close_game)
Homebtn.place(x = 10, y = 10)

#create a title image to be displayed on the game screen
gameCanvas = Canvas(gameTop, width = 1024, height = 72, highlightthickness = 0)
gameCanvas.pack()
gameCanvas.create_image(0,0,image = gameNameImg, anchor = "nw")


#set players initial number of lives
lives = 3
#display hearts corresponding to the number of lives
liveslbl1 = Label(gameScreen, image = livesImg, bg = '#11C3ED')
liveslbl1.place(x = WINDOW_WIDTH - 55, y = 6)
liveslbl2 = Label(gameScreen, image = livesImg, bg = '#11C3ED')
liveslbl2.place(x = WINDOW_WIDTH - 105, y = 6)
liveslbl3 = Label(gameScreen, image = livesImg, bg = '#11C3ED')
liveslbl3.place(x = WINDOW_WIDTH - 155, y = 6)
#create all photoImage variables
PBImg = PhotoImage(file = "img/PBButton.png")
PBGImg = PhotoImage(file = 'img/PBGButton.png')
PSImg = PhotoImage(file = 'img/PSButton.png')
PSGImg = PhotoImage(file = 'img/PSGButton.png')
PCImg = PhotoImage(file = 'img/PCButton.png')
PCGImg = PhotoImage(file = 'img/PCGButton.png')
CAImg = PhotoImage(file = 'img/CAButton.png')
CAGImg = PhotoImage(file = 'img/CAGButton.png')
PGImg = PhotoImage(file = 'img/PGButton.png')
PGGImg = PhotoImage(file = 'img/PGGButton.png')
LivesLabelImg = PhotoImage(file = 'img/Lives.png')
PlayImg = PhotoImage(file = "img/PlayButton.png")
HelpImg = PhotoImage(file = "img/HelpButton.png")
ExitImg = PhotoImage(file = "img/ExitButton.png")
GuyImg = PhotoImage(file = "img/MenuPic.png")
helpMenuImg = PhotoImage(file = "img/HelpMenu.png")

# Create and pack a Canvas object that doubles as the playable area
gameBackground = Canvas(gameScreen, width = WINDOW_WIDTH, height = WINDOW_HEIGHT - 224, highlightthickness = 0)
gameBackground.bind('<Button-1>', dummy)
gameBackground.pack()
# Create a background image
gameBackground.create_image(0, 0, image = background, anchor = 'nw')
beginTxt = gameBackground.create_image(gameBackground.winfo_reqwidth()//2,gameBackground.winfo_reqheight()//2, image = BeginImg)

# Create various lists and variables that will all be manipulated as the program runs
movingRight = True
movingLeft = True
blocksList = []
coinsList = []
enemyList = []
enemyLocations = []
indexBlocks = 0
indexCoins = 0
indexEnemy = 0
seconds = 0
fall = True
jump = True
playerIsJumped = True
check = False
flag = False
score = 0

# Create fonts
notDaFont = font.Font(family = 'Arial Bold', size = 15)
notDaFont1 = font.Font(family = 'Fixedsys', size = 20)
notDaFont2 = font.Font(family = 'Fixedsys', size = 15)

# Display score at the top of the screen
displayScore = gameCanvas.create_text(200,35, text = 'Score: ' + str(score), font = notDaFont1)

# Create a Player object
player = Player(gameBackground, y = gameBackground.winfo_reqheight())

# Create a FinishPoint object
finish = FinishPoint(gameBackground)
finish.placeFinishPoint(x = gameBackground.winfo_reqwidth() - 10, y = gameBackground.winfo_reqheight())

# Create a frame at the bottom of the screen
gameBottom = Frame(gameScreen, width = WINDOW_WIDTH, height = 160)
gameBottom.pack_propagate(False)
gameBottom.pack()

# Create a Canvas object on gameBottom
gameGround = Canvas(gameBottom, width = WINDOW_WIDTH, height = 160, highlightthickness = 0)
gameGround.pack_propagate(False)
gameGround.pack()
# Create a ground image
gameGround.create_image(1024 // 2, 160 // 2, image = img_ground)

# Create, place, and set properties for buttons
btnPlaceBlocks = Button(gameScreen, image = PBImg, command = placeBlocks, borderwidth = 0, bg = "black", cursor = 'hand2')
btnPlaceBlocks.place(y = 670, x = 2)
btnPlaceEnemy = Button(gameScreen, image = PSImg, command = placeEnemy, borderwidth = 0, bg = "black", cursor = 'hand2')
btnPlaceEnemy.place(y = 670, x = 2 + btnPlaceBlocks.winfo_reqwidth() + 2)
btnPlaceCoins = Button(gameScreen, image = PCImg, command = placeCoins, borderwidth = 0, bg = "black", cursor = 'hand2')
btnPlaceCoins.place(y = 670, x = 2 + btnPlaceBlocks.winfo_reqwidth() + 2 + btnPlaceEnemy.winfo_reqwidth() + 2)
btnClear = Button(gameScreen, image = CAImg, command = clearAll, borderwidth = 0, bg = "black", cursor = 'hand2')
btnClear.place(y = 670, x = 2 + btnPlaceBlocks.winfo_reqwidth() + 2 + btnPlaceEnemy.winfo_reqwidth() + 2 + btnClear.winfo_reqwidth() + 2)
lblLives = Label(gameScreen, image = LivesLabelImg, borderwidth = 0, bg = 'black')
lblLives.place(y = 670, x = 2 + btnPlaceBlocks.winfo_reqwidth() + 2 + btnPlaceEnemy.winfo_reqwidth() + 2 + btnClear.winfo_reqwidth() + 2 + btnClear.winfo_reqwidth() + 2)
cboLives = ttk.Combobox(gameScreen, width = 2, state = 'readonly', values = ('1', '2', '3'), font = notDaFont)
cboLives.current(2)
cboLives.bind('<<ComboboxSelected>>', setLives)
cboLives.place(y = 678, x = 794)
btnPlayGame = Button(gameScreen, image = PGImg, command = playGame, borderwidth = 0, bg = "black", cursor = 'hand2')
btnPlayGame.place(y = 670, x = 849)



###################################################################################################################################################
#create a main menu top level
mainMenu = Toplevel(bg = '#11C3ED')
mainMenu.title('MORTALSCAPE (Main Menu)')
mainMenu.geometry("%dx%d+%d+%d" % (WINDOW_WIDTH, WINDOW_HEIGHT, mainMenu.winfo_screenwidth() // 2 - WINDOW_WIDTH // 2, 
    mainMenu.winfo_screenheight() // 2 - WINDOW_HEIGHT // 2))
mainMenu.resizable(False, False)
mainMenu.protocol('WM_DELETE_WINDOW', close_mainMenu)

#place the title on the main menu screen
MainName = PhotoImage(file = "img/Name.png")
canvas = Canvas(mainMenu, width = 900, height = 250, highlightthickness = 0)
canvas.pack()
canvas.create_image(0, 0, image = MainName, anchor = "nw")
btnPlay = Button(mainMenu, image = PlayImg, command = play, bg = "black", borderwidth = 0) 
btnPlay.pack(pady = 5)
btnHelp = Button(mainMenu,image = HelpImg, command = displayHelp, bg = "black", borderwidth = 0)
btnHelp.pack(pady = 5)
btnExit = Button(mainMenu, image = ExitImg, command = close_mainMenu, bg = "black", borderwidth = 0)
btnExit.pack(pady = 5)
GuyImglbl = Label(mainMenu, image = GuyImg, bg = '#11C3ED' )
GuyImglbl.pack(pady = 40)
     
###################################################################################################################################################
#create a toplevel to display the help menu
helpScreen = Toplevel(bg = '#11C3ED')
helpScreen.title('MORTALSCAPE (Help)')
helpScreen.geometry("%dx%d+%d+%d" % (WINDOW_WIDTH, WINDOW_HEIGHT, helpScreen.winfo_screenwidth() // 2 - WINDOW_WIDTH // 2, 
    helpScreen.winfo_screenheight() // 2 - WINDOW_HEIGHT // 2))
helpScreen.resizable(False, False)
helpScreen.protocol('WM_DELETE_WINDOW', close_help)
helpScreen.withdraw()
#canvas to hold the image
helpCanvas = Canvas(helpScreen, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, highlightthickness = 0 )
helpCanvas.pack()
helpCanvas.create_image(0,0,image = helpMenuImg, anchor = "nw")
#return to menu button
arrowBtn = Button(helpScreen, image = ArrowImg, command = close_help, bg = '#11C3ED')
arrowBtn.place(x = 10, y = 10)
returnMenulbl = Label(helpScreen, font = notDaFont2, text = "Return to Menu", bg = '#11C3ED')
returnMenulbl.place(x = 70, y = 25)
#output the window
gameScreen.mainloop()
