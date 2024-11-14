from socket import * 
import pickle
import pygame #pygame library
import random #random library
from datetime import datetime #from datetime library import datetime module
pygame.init()

#Variables for Server 
serverName = "45.33.36.89"
serverPort = 22324 #Server port
server = socket(AF_INET, SOCK_STREAM) #Create an INET, STREAMing socket

#Variables for screen size and font size
screen = pygame.display.set_mode((800,900))#screen size
text1 =pygame.font.SysFont("Type1",115) #size 145
text11 =pygame.font.SysFont("Type1",70) #size 145
text2 =pygame.font.SysFont("Type1",50) #size small
text3 =pygame.font.SysFont("Type1",125) #logo size
text4 =pygame.font.SysFont("Type1",75) #Game Over Font

playerInfo = [] #2D array of players read in from Math_Slayers.txt note pad
#Pre set 2D array of player names and scores as a form of backup to rewrite the text file if there was an error reading
backUpPlayerInfo = [["Creeper","26"],["Ash","46"],["Hulk","47"],["Goku","52"],["Thor","80"],["Ruben","111"],["Pikachu","115"],["Omega","160"],["Thanos","200"],["Alex","431"]]

#Error Checking, try and catch statements

try: #try to read from the text file into the 2D Array
  file = open("Math_Slayers.txt","r+") #open Math_Slayers.txt for reading and writing
  #read in player names and scores from Math_Slayers.txt into the 2D Dynamic Array
  for eachLine in file: #loop control variable (eachLine) is each line of the text file, consisting of "player,score"
    removeTrailingSpace = eachLine.strip() #Removes any leading and trailing character spaces in the text file
    #Splitting the string of "player,score" by the comma into 2 separate elements: player and score and appending it to the same row of the array
    playerInfo.append(removeTrailingSpace.split(","))
  #Selection Sort: sort the list from fastest to slowest 
  for eachPlayer in range(0,len(playerInfo),1): #loop control variable is eachPlayer 
    fastestSelect = eachPlayer #current minimum placeholder variable
    for eachPlayerName in range(eachPlayer+1,len(playerInfo),1): #algorithm to find the current minimum number 
      if int(playerInfo[eachPlayerName][1]) < int(playerInfo[fastestSelect][1]):
        fastestSelect = eachPlayerName 
    placeHolder = playerInfo[eachPlayer]
    playerInfo[eachPlayer] = playerInfo[fastestSelect] #moving the current minimum number to the sorted partition
    playerInfo[fastestSelect] = placeHolder
  textFileError = True #Once textFileError is True, the program will draw the Home Interface
except: 
  textFileError = False
  #if there is an error with reading from the text file the program will enter a while loop to display the TextFile Reset Interface
  #and reset the data of the text file to the original 10 player names and their scores 

#images constants
shooter = pygame.image.load("shooter.PNG")
enemy = pygame.image.load("enemy.PNG")
monster = pygame.image.load("monster.PNG")
monsterFlame = pygame.image.load("monsterFlame.png")
alien = pygame.image.load("alien.png")
flame = pygame.image.load("flame.png")
tank1 = pygame.image.load("tank1.png")
tank2 = pygame.image.load("tank2.png")
tank3 = pygame.image.load("tank3.png")
tank4 = pygame.image.load("tank4.png")
tank5 = pygame.image.load("tank5.png")
car1 = pygame.image.load("car1.png")
car2 = pygame.image.load("car2.png")
car3 = pygame.image.load("car3.png")
car4 = pygame.image.load("car4.png")
car5 = pygame.image.load("car5.png")
muzzleFlash = pygame.image.load("muzzleFlash.png")
eTank1 = pygame.image.load("eTank1.png")
eTank2 = pygame.image.load("eTank2.png")
eTank3 = pygame.image.load("eTank3.png")
eTank4 = pygame.image.load("eTank4.png")
eTank5 = pygame.image.load("eTank5.png")
eCar1 = pygame.image.load("eCar1.png")
eCar2 = pygame.image.load("eCar2.png")
eCar3 = pygame.image.load("eCar3.png")
eCar4 = pygame.image.load("eCar4.png")
eCar5 = pygame.image.load("eCar5.png")
enemyMuzzleFlash = pygame.image.load("enemyMuzzleFlash.png")
explosion1 = pygame.image.load("explosion1.png")
explosion2 = pygame.image.load("explosion2.png")
explosion3 = pygame.image.load("explosion3.png")
explosion4 = pygame.image.load("explosion4.png")
explosion5 = pygame.image.load("explosion5.png")
explosion6 = pygame.image.load("explosion6.png")
alienExplosion1 = pygame.image.load("ae1.png")
alienExplosion2 = pygame.image.load("ae2.png")
alienExplosion3 = pygame.image.load("ae3.png")
alienExplosion4 = pygame.image.load("ae4.png")
alienExplosion5 = pygame.image.load("ae5.png")
#variables
fastestGameScore = playerInfo[0] #The fastest player + speed 
searchBarCounter = 0 
searchBarAsker = True
mouseClick = ""
counter = 0
currentMode = 0 #0 = Home screen , 1 = Game Screen
selectedPlayer = 0 #selected player index
selectedListPlayer = playerInfo[selectedPlayer] #selected player 
searchBar = ""
searchBar_placeHolder = ""
searchBar2 = ""
currentTime = 0
shooterLeft = False
shooterRight = False
shooterAnswer = ""
mathCounter = 1
mathAnswer = 1
mathCounter = random.randrange(1,5,1)
number1 = random.randrange(1,11,1)
number2 = random.randrange(1,10,1)
mathAnswerDisplay = ""
tankList = []
enemyBulletList = []
eBLCounter= 0
currentTime = 5
timeSaverChecker = True
#list to send [shooterX,[bulletListXCoordinate]]
dataSend = [338,[],True]
#data to receive 
dataReceive =[(800-338-62),[]]

#Functions and Class
def DrawErrorScreen(): #Function for drawing the TextFile Reset Interface
  pygame.draw.rect(screen,(255,0,0),(100,100,600,700)) #Draw red rectangular box at coordinates (100,100) with 600 width and 700 length
  gameText = text2.render(("Resetting TextFile in: " +str(currentTime)), True, "white")
  screen.blit(gameText,(110,110)) #Displaying the text at coordinates (110,110)
  
#function to draw the table in home interface
def DrawGrid():
    #logo box 
    pygame.draw.rect(screen,(255,164,0),(50,30, 700,90)) #orange    
    #Search + Sort bar
    pygame.draw.rect(screen,(255,164,0),(50,150, 525,58)) #orange border search bar
    pygame.draw.rect(screen,(0,0,0),(55,155, 515,48))#black interior search bar
    pygame.draw.rect(screen,(255,164,0),(575,150,175,58))#orange border sort bar 57,255,20
    pygame.draw.rect(screen,(0,0,0),(575,155,170,48))#black interior sort bar
    #Table
    for i in range (1,12,1):
        pygame.draw.rect(screen,(255,164,0),(50,155+48*i, 175,58))#orange border Rank
        pygame.draw.rect(screen,(0,0,0),(55,155+48*i+5, 165,48))#black interior Rank
        pygame.draw.rect(screen,(255,164,0),(225,155+48*i,350,58))#orange border Player
        pygame.draw.rect(screen,(0,0,0),(225,155+48*i+5,345,48))#black interior Player
        pygame.draw.rect(screen,(255,164,0),(575,155+48*i,175,58))#orange border Time
        pygame.draw.rect(screen,(0,0,0),(575,155+48*i+5,170,48))#black interior Time
    #Offline Play button
    pygame.draw.rect(screen,(255,164,0),(50,775,350,80))#orange box Play Button
    
    #Multiplayer Play button
    pygame.draw.rect(screen,(0,255,255),(400,775,350,80))#cyan box Play Button

#function to draw the grid on the offline game interface
def DrawGameGrid():
  #Time/Score (Top portion of the screen)
  pygame.draw.rect(screen,(255,164,0),(0,0, 800,50)) #orange border top bar
  pygame.draw.rect(screen,(0,0,0),(5,5, 790,40))#black interior top bar
  #Math Equations (Upper-Low portion of the screen)
  pygame.draw.rect(screen,(255,164,0),(0,735, 800,50)) #orange border bottom bar
  pygame.draw.rect(screen,(0,0,0),(5,740, 790,40))#black interior bottom bar
  #Lives Left (Lower portion of the screen)
  pygame.draw.rect(screen,(255,164,0),(0,780, 800,120)) #orange border bottom bar 
  pygame.draw.rect(screen,(0,0,0),(5,785, 790,110))#black interior bottom bar

#function to draw the grid on the multiplayer game interface
def DrawMultiplayerGameGrid():
  #Time/Score (Top portion of the screen)
  pygame.draw.rect(screen,(255,164,0),(0,0, 800,120)) #orange border top bar
  pygame.draw.rect(screen,(0,0,0),(5,5, 790,110))#black interior top bar
  #Math Equations (Upper-Low portion of the screen)
  pygame.draw.rect(screen,(255,164,0),(0,735, 800,50)) #orange border bottom bar
  pygame.draw.rect(screen,(0,0,0),(5,740, 790,40))#black interior bottom bar
  #Lives Left (Lower portion of the screen)
  pygame.draw.rect(screen,(255,164,0),(0,780, 800,120)) #orange border bottom bar
  pygame.draw.rect(screen,(0,0,0),(5,785, 790,110))#black interior bottom bar    

#Offline game interface text displaying function
def GameText():
  global currentTime
  gameText = text2.render("TIME:",True,"white")#white text TIME
  screen.blit(gameText,(15,10))
  gameText = text2.render(str(currentTime),True,"white")#white text Rank
  screen.blit(gameText,(120,10))
  gameText = text2.render("FASTEST TIME:",True,"white")#white text Rank
  screen.blit(gameText,(460,10))
  gameText = text2.render(str(fastestGameScore[1]),True,"white")#white text Rank
  screen.blit(gameText,(730,10))
  gameText = text2.render("LIVES LEFT:",True,"white")#white text Rank
  screen.blit(gameText,(15,790))
  for i in range(0,livesLeft,1):
    screen.blit(shooter,(225+75*i,790))
    
#Multiplayer game interface text displaying function
def MultiplayerGameText():
  gameText = text2.render("ENEMY LIFE:",True,"white")#white text Rank
  screen.blit(gameText,(351,10))
  for i in range(0,enemyLivesLeft,1):
      screen.blit(enemy,(578+75*i,10))
  gameText = text2.render("LIVES LEFT:",True,"white")#white text Rank
  screen.blit(gameText,(15,790))
  for i in range(0,livesLeft,1):
    screen.blit(shooter,(225+75*i,790))

#Function for math equation generator
def MathText(): #Declaring the MathText function that generates math equations
  global mathCounter, mathAnswer, number1, number2 #Declaring the variables as global
  placeHolder = 0
  if mathCounter == 1: #addition question
    mathAnswer = number1 + number2 #answer equals the sum of the two random integers
    #what will be displayed in equation section of game interface with white text
    gameText = text2.render((str(number1)+" + "+str(number2)+" = " + mathAnswerDisplay),True,"white")
    screen.blit(gameText,(250,745)) #displays the math equation in the game interface in the coordinates (250, 745)
  elif mathCounter == 2: #subtraction question
    if number2 > number1: #complex selection, check if no1>no2 so there are no negatives
      placeHolder = number1
      number1 = number2
      number2 = placeHolder #swap values of no1 and no2 to ensure the answer is positive
    mathAnswer = number1 - number2 #answer equals the difference of no1 and no2
    gameText = text2.render((str(number1)+" - "+str(number2)+" = " + mathAnswerDisplay),True,"white")
    screen.blit(gameText,(250,745))
  elif mathCounter == 3: #multiplication question
    mathAnswer = number1 * number2 #answer equals the product of no1 and no2 
    gameText = text2.render((str(number1)+" x "+str(number2)+" = " + mathAnswerDisplay),True,"white")
    screen.blit(gameText,(250,745))
  elif mathCounter == 4: #division question
    while number1 % number2 != 0:
      #if the remainder of the division question is not 0, then two new values will be assigned to the two variables,
      #this will repeat until 2 numbers with a remainder of 0 is found
      number1 = random.randrange(1,11,) #number1 equals random number generated by random module from 1 to 10
      number2 = random.randrange(1,11,1) #number2 equals random number generated by random module from 1 to 10
    mathAnswer = int(number1 / number2)
    gameText = text2.render((str(number1)+" / "+str(number2)+" = " + mathAnswerDisplay),True,"white")
    screen.blit(gameText,(250,745))
      
#Function for displaying the shooter
def Shooter():
  global shooterX
  screen.blit(shooter,(shooterX,630))

#Function for displaying the enemy
def Enemy():
  global enemyX
  screen.blit(enemy,(enemyX,125))

#Class of the bullet
class ShooterBullet(): 
  def __init__(self,x,y):#constructor method
    self.x = x 
    self.y = y 
  def PrintBullet(self): #Function to display the bullet in the Game Interface
    pygame.draw.rect(screen,(255,255,0),(self.x,self.y, 5,10)) #shape:rectangle, color: yellow
  def BulletMovement(self): #Function for bullet's direction and speed 
    self.y += -15 #Bullet y coordinates decreases by 15 pixels everytime it is called, moving up the screen

#Class of the EnemyBullet
class EnemyBullet(): 
  def __init__(self,x,y):
    self.x = x
    self.y = y
  def PrintEnemyBullet(self):
    pygame.draw.rect(screen,(255,255,0),(self.x,self.y, 5,10)) #neon border search bar
  def EnemyBulletMovement(self):
    self.y += 15

#function for displaying the monster and the monster's movement pattern
def Monster():
  global monsterX
  screen.blit(monster,(monsterX, 80)) #Displaying the monster
  pygame.draw.rect(screen,(255,0,0),(monsterX-50,58,250,20)) #Displaying the Monster's red health bar
  pygame.draw.rect(screen,(57,255,20),(monsterX-50,58,monsterHP*25,20)) #displaying the Monster health bar
  if monsterDirection == "right": #Monster movement pattern
    monsterX += 4
  if monsterDirection == "left":
    monsterX += -4

#Class of the Flame 
class Flame(): #Parent Class
  def __init__(self,x,y): #Consturctor method
    self.x = x
    self.y = y
  def PrintFlame(self): #function for displaying the flame
    screen.blit(flame,(self.x,self.y))
  def FlameMovement(self): #function for the flame's movement pattern
    self.y += 10 #Flame y coordinates increases by 10 pixels every time it is called

#Class for the MonsterFlame
class MonsterFlame(Flame): #Inheritance, Child Class
  def PrintMonsterFlame(self): #Function for printing the MonsterFlame
    screen.blit(monsterFlame,(self.x,self.y))

#Class for the Alien
class Alien(): 
  def __init__(self,x,y): #Constructor method
    self.x = x
    self.y = y
  def PrintAlien(self): #Function for displaying the Alien in the Game Interface
    screen.blit(alien,(self.x,self.y)) #alien is the png of the Alien object
  def AlienMovement(self): #Function for the Alien's movement pattern
    global alienDirection 
    if alienDirection == "right": #if alienDirection is right, Alien moves right
      self.x += 4
    if alienDirection == "left": #if alienDirection is left, Alien moves left
      self.x += -4

#Function for displaying tank1
def PrintTank1():
  global tank1Animation #Tank1 Exploding animation
  if tank1HP == 5: #The PNG of the tank to display when at a certain HP
    screen.blit(tank1,(20,520))
  elif tank1HP == 4:
    screen.blit(tank2,(20,520))
  elif tank1HP == 3:
    screen.blit(tank3,(20,520))
  elif tank1HP == 2:
     screen.blit(tank4,(20,520))
  elif tank1HP == 1:
    screen.blit(tank5,(20,520))
  elif tank1HP<=0:
    if 0 <= tank1Animation < 3:
      screen.blit(explosion1,(20,490))#Tank1 Exploding animation
      tank1Animation += 1
    elif 3 <= tank1Animation < 6: 
      screen.blit(explosion2,(20,490))
      tank1Animation += 1
    elif 6 <= tank1Animation < 9: 
      screen.blit(explosion3,(20,490))
      tank1Animation += 1
    elif 9 <= tank1Animation < 12:
      screen.blit(explosion4,(20,490))
      tank1Animation += 1
    elif 12 <= tank1Animation < 15:
      screen.blit(explosion5,(20,490))
      tank1Animation += 1
    elif 15 <= tank1Animation < 18:
      screen.blit(explosion6,(20,490))
      tank1Animation += 1
    else:
      pass

#Function for displaying Tank2
def PrintTank2():
  global tank2Animation
  if tank2HP == 5: #The PNG of the tank to display when at a certain HP
    screen.blit(tank1,(588,520))
  elif tank2HP == 4:
    screen.blit(tank2,(588,520))
  elif tank2HP == 3:
    screen.blit(tank3,(588,520))
  elif tank2HP == 2:
    screen.blit(tank4,(588,520))
  elif tank2HP == 1:
    screen.blit(tank5,(588,520))
  elif tank2HP<=0:
    if 0 <= tank2Animation < 3:
      screen.blit(explosion1,(588,490))#Tank1 Exploding animation
      tank2Animation += 1
    elif 3 <= tank2Animation < 6: 
      screen.blit(explosion2,(588,490))
      tank2Animation += 1
    elif 6 <= tank2Animation < 9: 
      screen.blit(explosion3,(588,490))
      tank2Animation += 1
    elif 9 <= tank2Animation < 12:
      screen.blit(explosion4,(588,490))
      tank2Animation += 1
    elif 12 <= tank2Animation < 15:
      screen.blit(explosion5,(588,490))
      tank2Animation += 1
    elif 15 <= tank2Animation < 18:
      screen.blit(explosion6,(588,490))
      tank2Animation += 1
    else:
      pass

#Function for displaying Tank2  
def PrintCar1():
  global car1Animation
  if car1HP == 5: #The PNG of the tank to display when at a certain HP
    screen.blit(car1,(292,520))
  elif car1HP == 4:
    screen.blit(car2,(292,520))
  elif car1HP == 3:
    screen.blit(car3,(292,520))
  elif car1HP == 2:
    screen.blit(car4,(292,520))
  elif car1HP == 1:
    screen.blit(car5,(292,510))
  elif car1HP<=0:
    if 0 <= car1Animation < 3:
      screen.blit(explosion1,(292,490))#Tank1 Exploding animation
      car1Animation += 1
    elif 3 <= car1Animation < 6: 
      screen.blit(explosion2,(292,490))
      car1Animation += 1
    elif 6 <= car1Animation < 9: 
      screen.blit(explosion3,(292,490))
      car1Animation += 1
    elif 9 <= car1Animation < 12:
      screen.blit(explosion4,(292,490))
      car1Animation += 1
    elif 12 <= car1Animation < 15:
      screen.blit(explosion5,(292,490))
      car1Animation += 1
    elif 15 <= car1Animation < 18:
      screen.blit(explosion6,(292,490))
      car1Animation += 1
    else:
      pass
    
#Function for displaying the vehicles in multiplayer game mode
def PrintTank11():
    if tank1HP == 5:
      screen.blit(tank1,(20,520))
    elif tank1HP == 4:
      screen.blit(tank2,(20,520))
    elif tank1HP == 3:
      screen.blit(tank3,(20,520))
    elif tank1HP == 2:
      screen.blit(tank4,(20,520))
    elif tank1HP == 1:
      screen.blit(tank5,(20,520))
    elif tank1HP<=0:
      pass

def PrintCar11():
    if car1HP == 5:
      screen.blit(car1,(230,520))
    elif car1HP == 4:
      screen.blit(car2,(230,520))
    elif car1HP == 3:
      screen.blit(car3,(230,520))
    elif car1HP == 2:
      screen.blit(car4,(230,520))
    elif car1HP == 1:
      screen.blit(car5,(230,510))
    elif car1HP<=0:
      pass
    
def PrinteTank1():
    if eTank1HP == 5:
      screen.blit(eTank1,(800-20-197,260))
    elif eTank1HP == 4:
      screen.blit(eTank2,(800-20-193,260))
    elif eTank1HP == 3:
      screen.blit(eTank3,(800-20-194,260))
    elif eTank1HP == 2:
      screen.blit(eTank4,(800-20-196,260))
    elif eTank1HP == 1:
      screen.blit(eTank5,(800-20-182,260))
    elif eTank1HP<=0:
      pass
 
def PrinteCar1():
    if eCar1HP == 5:
      screen.blit(eCar1,(800-230-188,260))
    elif eCar1HP == 4:
      screen.blit(eCar2,(800-230-185,260))
    elif eCar1HP == 3:
      screen.blit(eCar3,(800-230-187,260))
    elif eCar1HP == 2:
      screen.blit(eCar4,(800-230-195,260))
    elif eCar1HP == 1:
      screen.blit(eCar5,(800-230-193,260))
    elif eCar1HP<=0:
      pass

#Function for displaying the text in the ranking table of the home interface
def Text():
  #Rank Text + Ranking
  rankText = text2.render("RANK",True,"white")#white text Rank
  screen.blit(rankText,(85,215))
  for i in range(1,10,1):
    rankText = text2.render(str(i),True,"white") #white text ranking 1-9
    screen.blit(rankText,(125,215+48*i))
  rankText = text2.render("10",True,"white") #white text ranking 10
  screen.blit(rankText,(116,695))  
  #Player Text
  playerText = text2.render("PLAYER",True,"white") #white text Player
  screen.blit(playerText,(325,215))
  #Time Text
  timeText = text2.render("TIME",True,"white") #what text time
  screen.blit(timeText,(620,215)) 
  #Offline Play Button Text
  playText = text1.render("OFFLINE",True,"white") #white text Play button
  screen.blit(playText,(55,780))
  #Multiplyaer Play Button Text
  playText = text11.render("MULTIPLAYER",True,"white") #white text Play button
  screen.blit(playText,(408,792))
  #Logo Text
  timeText = text3.render("MATH SLAYERS",True,"white") #what text time
  screen.blit(timeText,(65,40)) 
  #Sort Button Text
  if counter == 0:
    playText = text2.render("Fast>Slow",True,"white") #white text Sort Fastest to Slowest
    screen.blit(playText,(575,165))
  if counter == 1:
    playText = text2.render("Slow>Fast",True,"white") #white text Sort Slowest to Fastest
    screen.blit(playText,(575,165))
  if counter == 2:
    playText = text2.render("Fastest",True,"white") #white text Sort Single Fastest
    screen.blit(playText,(600,165))
  if counter == 3:
    playText = text2.render("Slowest",True,"white") #white text Sort Single Slowest
    screen.blit(playText,(595,165))
  #Updated Player Name + Info
  for i in range(0,10,1):
    playText = text2.render(playerInfo[i][0],True,"white") #white text player's name
    screen.blit(playText,(235,263+48*i))
    playText = text2.render(playerInfo[i][1],True,"white") #white text player's time
    screen.blit(playText,(585,263+48*i))

#Function for calculating the current sorting mode index of the home interface
def MouseClick():
  global mouseClick,counter
  if mouseClick == "sortBox":
    if counter == 3:
      counter = 0
    else:
      counter +=1
#function for highlighting the player's row in the ranking table of the home interface for selecting players
def SelectedPlayer():
  global selectedPlayer, counter
  if counter == 0 or counter == 2 or counter ==3:
    pygame.draw.rect(screen,(57,255,20),(55,251+48*selectedPlayer+5, 165,43))#green highlighted interior Rank
    pygame.draw.rect(screen,(57,255,20),(225,251+48*selectedPlayer+5,345,43))#green highlighted interior Player
    pygame.draw.rect(screen,(57,255,20),(575,251+48*selectedPlayer+5,170,43))#green highlighted interior Time
  else:
    pygame.draw.rect(screen,(57,255,20),(55,683-48*selectedPlayer+5, 165,43))#green highlighted interior Rank
    pygame.draw.rect(screen,(57,255,20),(225,683-48*selectedPlayer+5,345,43))#green highlighted interior Player
    pygame.draw.rect(screen,(57,255,20),(575,683-48*selectedPlayer+5,170,43))#green highlighted interior Time

#function for highlighting the player's row in the ranking table of the home interface for locating players
def SearchBarHighlighter():
  global searchBarCounter, counter
  if counter == 0 or counter == 2 or counter ==3:
    pygame.draw.rect(screen,(240,230,140),(55,251+48*searchBarCounter+5, 165,43))#yellow highlighted interior Rank
    pygame.draw.rect(screen,(240,230,140),(225,251+48*searchBarCounter+5,345,43))#yellow highlighted interior Player
    pygame.draw.rect(screen,(240,230,140),(575,251+48*searchBarCounter+5,170,43))#yellow highlighted interior Time
  else:
    pygame.draw.rect(screen,(240,230,140),(55,683-48*searchBarCounter+5, 165,43))#yellow highlighted interior Rank
    pygame.draw.rect(screen,(240,230,140),(225,683-48*searchBarCounter+5,345,43))#yellow highlighted interior Player
    pygame.draw.rect(screen,(240,230,140),(575,683-48*searchBarCounter+5,170,43))#yellow highlighted interior Time
  
#Function for displaying the texts of the search bar
def SearchBar():
  global searchBar2
  playText = text2.render(searchBar2,True,"white") #white text Sort Fastest to Slowest
  screen.blit(playText,(65,165))

#function for the sorting algorithms
def SingleFastestScore():
  pygame.draw.rect(screen,(0,0,0),(55,299+5,690,432))#neon border Player
      
def SingleSlowestScore():
  pygame.draw.rect(screen,(0,0,0),(55,251+5,690,432-5))#neon border Player

def FastestToSlowest():
  #Fastest to slowest Selection sort
  for i in range(0,len(playerInfo),1):
    fastestSelect = i
    for j in range(i+1,len(playerInfo),1):
      if int(playerInfo[j][1]) < int(playerInfo[fastestSelect][1]):
        fastestSelect = j
    placeHolder = playerInfo[i]
    playerInfo[i] = playerInfo[fastestSelect]
    playerInfo[fastestSelect] = placeHolder
    
def SlowestToFastest():
  #Slowest to fastest bubble sort
  for i in range(0,len(playerInfo)-1,1):
    for j in range(1,len(playerInfo),1):
      if int(playerInfo[j-1][1]) < int(playerInfo[j][1]): 
        placeHolder = playerInfo[j-1]
        playerInfo[j-1] =playerInfo[j]
        playerInfo[j] = placeHolder

#Execution of Code
timeSaverChecker = True #used to save the exact time entering the TextFile Reset Interface to create the countdown 
#Writing new data into text file
while textFileError == False: #while there is an error reading from the text file
  screen.fill("black")
  DrawErrorScreen() #Using Pygame library draw the TextFile Reset Interface
  if timeSaverChecker == True:
    #This will only be done once in the Textfile Reset Interface, saving the exact time the client enters the TextFile Reset Interface
    #in order to create a countdown of 5 seconds
    timeSaver = datetime.now()
  currentTimeX = datetime.now() #constantly getting the current time
  currentTime = 5-(currentTimeX - timeSaver).seconds
  #subtracting the time entering the Interface from the current time to calculate the duration spent in the interface, and then
  #subtracting it from 5 to create a countdown of 5 seconds
  timeSaverChecker = False
  if (currentTime<=0): #Once the countdown timer of 5 seconds has completed
    file = open("Math_Slayers.txt","r+") #open file for reading and writing 
    file.truncate(0) #deletes all content in the text file
    spaceChecker = False #initially False to prevent spaces in the first line
    file.seek(0) #set the reference point of the file handle to the beginning of the file
    #Complex selection (nested loop) for writing into file
    for eachBackUpPlayer in backUpPlayerInfo: #eachBackUpPlayer is equal to an array of player name and score
      if spaceChecker == True:
        file.writelines("\n")#new line in text file
      commaCheck = True
      for individualElement in eachBackUpPlayer:
        file.writelines(individualElement) #writes the player info into text file
        if commaCheck == True: #Checks to see when to add a comma
          file.writelines(",") #After writing player name in the text file, a comma is written after it
          commaCheck = False
      spaceChecker = True
    file.close()       
    textFileError = True #After rewritting the text file, the user will return to the home interface
  for eachEvent in pygame.event.get(): #Pygame module get events from the queue
    pygame.display.update() #make the display surface, appear on the screen
    
playerInfo = []
file = open("Math_Slayers.txt","r+") #open Math_Slayers.txt for reading and writing
#read in player names and scores from ShMath_Slayers.txt into the 2D Dynamic Array
for eachLine in file: #loop control variable (eachLine) is each line of the text file, consisting of "player,score"
  removeTrailingSpace = eachLine.strip() #Removes any leading and trailing character spaces in the text file
  #Splitting the string of "player,score" by the comma into 2 separate elements: player and score and appending it to the same row of the array
  playerInfo.append(removeTrailingSpace.split(","))
#Selection Sort: sort the list from fastest to slowest 
for eachPlayer in range(0,len(playerInfo),1): #loop control variable is eachPlayer 
  fastestSelect = eachPlayer #current minimum placeholder variable
  for eachPlayerName in range(eachPlayer+1,len(playerInfo),1): #algorithm to find the current minimum number 
    if int(playerInfo[eachPlayerName][1]) < int(playerInfo[fastestSelect][1]):
      fastestSelect = eachPlayerName 
  placeHolder = playerInfo[eachPlayer]
  playerInfo[eachPlayer] = playerInfo[fastestSelect] #moving the current minimum number to the sorted partition
  playerInfo[fastestSelect] = placeHolder
  textFileError = True #Once textFileError is True, the program will draw the Home Interface

screen.fill("black")
#While loop to keep the game continuous
while textFileError == True:
    if currentMode == 0: #Home screen
      DrawGrid() #Drawing home screen table
      if searchBarAsker == False and searchBar != "": 
        SearchBarHighlighter()
      SelectedPlayer()
      Text()
      SearchBar()
      #Check for keys pressed
      for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
          mouseX,mouseY = pygame.mouse.get_pos()
          if 575<=mouseX<=743 and 153<=mouseY<=199:
            #mouseClicked sort box
            mouseClick = "sortBox"
            MouseClick()
          if 50<=mouseX<=400 and 775<=mouseY<=851:
            #mouseClicked Play button
            mouseClick = "playButton"
            countDown = 0
            shooterLeft = False
            shooterRight = False
            bulletList = []
            alienList = []
            flameList=[]
            monsterFlameList = []
            additionArray = [] #for addition question
            shooterX = 338 #shooter starting x-coordinates
            monsterX = 325 #monster starting x-coordinates
            monsterDirection  = "right" #monster's initial starting direction
            alienDirection  = "left" #alien's initial starting direction
            monsterHP =  10 #the number of hitpoints the monster starts with
            currentMode = 1 
            timeReset = datetime.now() #Keeps track of the time the game started to calculate the countdown timer
            livesLeft = 3 #The number of hitpoints the shooter starts with
            tank1Animation = 0 #An index to keep track of what png to print for tank1's exploding animation
            tank2Animation = 0 #An index to keep track of what png to print for tank2's exploding animation
            car1Animation = 0 #An index to keep track of what png to print for car1's exploding animation
            alienAnimation = 0 #An index to keep track of what png to print for alien's exploding animation
            booleanCountDown = True
            tank1HP = 5 #The number of hitpoints tank1 starts with 
            tank2HP = 5 #The number of hitpoints tank1 starts with
            car1HP = 5 #The number of hitpoints tank1 starts with
            alienSpawnerChecker = 0
            currentAlienTime = 1000 #alien time counter
          #multiplayer play button pressed
          if 400<mouseX<=750 and 775<=mouseY<=851:
            server.connect((serverName, serverPort)) #Connect to the server port
            symbol = server.recv(1024).decode()
            #Draw Waiting Room Interface
            screen.fill("black")
            pygame.draw.rect(screen,(0,255,255),(195,430, 443,50))#Aqua colored rectangular box
            gameText = text2.render("Waiting For Enemy Player",True,"white")#white text 
            screen.blit(gameText,(202,440))
            #Initializing variable with default values before game begins
            #list to send [shooterX,[bulletListXCoordinate]]
            dataSend = [338,[],True]
            #data to receive 
            dataReceive =[(800-338-62),[]]#Data recieved from Server
            enemyBulletList = [] #Local list of enemy bullets
            eBLCounter= 0 #Local enemy bullet list counter to calculate index of a new bullet
            bulletList = [] #local list of ShooterBullets
            countDown = 0 #Calculating duration of screen flash
            shooterLeft = False #Direction the player moves
            shooterRight = False #Direction the player moves
            shooterX = 338 #Player's starting coordinates
            livesLeft = 3 #Player's starting lives
            enemyLivesLeft = 3 #Enemy's starting lives
            booleanCountDown = True #If statement condition to see when to keep track of current time
            gameOverCountDown = 0 #To calculate the stopwatch in Lose Condition Interface
            gameOverTimer = 0 #If Statement condition for calculating the stopwatch in Lose Condition Interface
            tank1HP = 5 #The number of hitpoints tank1 starts with 
            car1HP = 5 #The number of hitpoints tank1 starts with
            eTank1HP = 5 #The number of hitpoints tank1 starts with 
            eCar1HP = 5 #The number of hitpoints tank1 starts with
            currentMode = 2 #Immediately draws Multiplayer Game Interface
            
          #What happens when the mouse clicks on the rows in the ranking table
          #When sorted to fastest to slowest scores 
          if counter == 0: 
            if 55<=mouseX<=742 and 256<=mouseY<=294:
              #row rank 1
              selectedPlayer = 0
              selectedListPlayer = playerInfo[selectedPlayer]
            if 55<=mouseX<=742 and 304<=mouseY<=344:
              #row rank 2
              selectedPlayer = 1
              selectedListPlayer = playerInfo[selectedPlayer]
            if 55<=mouseX<=742 and 352<=mouseY<=392:
              #row rank 3
              selectedPlayer = 2
              selectedListPlayer = playerInfo[selectedPlayer]
            if 55<=mouseX<=742 and 401<=mouseY<=439:
              #row rank 4
              selectedPlayer = 3
              selectedListPlayer = playerInfo[selectedPlayer]
            if 55<=mouseX<=742 and 448<=mouseY<=488:
              #row rank 5
              selectedPlayer = 4
              selectedListPlayer = playerInfo[selectedPlayer]
            if 55<=mouseX<=742 and 495<=mouseY<=534:
              #row rank 6
              selectedPlayer = 5
              selectedListPlayer = playerInfo[selectedPlayer]
            if 55<=mouseX<=742 and 544<=mouseY<=582:
              #row rank 7
              selectedPlayer = 6
              selectedListPlayer = playerInfo[selectedPlayer]
            if 55<=mouseX<=742 and 592<=mouseY<=632:
              #row rank 8
              selectedPlayer = 7
              selectedListPlayer = playerInfo[selectedPlayer]
            if 55<=mouseX<=742 and 640<=mouseY<=680:
              #row rank 9
              selectedPlayer = 8
              selectedListPlayer = playerInfo[selectedPlayer]
            if 55<=mouseX<=742 and 687<=mouseY<=729:
              #row rank 10
              selectedPlayer = 9
              selectedListPlayer = playerInfo[selectedPlayer]
          #When sorted to Single Fastest score
          elif counter == 2:
            if 55<=mouseX<=742 and 256<=mouseY<=294:
              #row rank 1
              selectedPlayer = 0
              selectedListPlayer = playerInfo[selectedPlayer]
          #When sorted to Single Slowest score
          elif counter == 3:
            if 55<=mouseX<=742 and 687<=mouseY<=729:
              #row rank 10
              selectedPlayer = 9
              selectedListPlayer = playerInfo[selectedPlayer]
          #When sorted to Slowest to Fastest scores
          else:
            if 55<=mouseX<=742 and 256<=mouseY<=294:
              #row rank 1
              selectedPlayer = 9
              selectedListPlayer = playerInfo[0]
            if 55<=mouseX<=742 and 304<=mouseY<=344:
              #row rank 2
              selectedPlayer = 8
              selectedListPlayer = playerInfo[1]
            if 55<=mouseX<=742 and 352<=mouseY<=392:
              #row rank 3
              selectedPlayer = 7
              selectedListPlayer = playerInfo[2]
            if 55<=mouseX<=742 and 401<=mouseY<=439:
              #row rank 4
              selectedPlayer = 6
              selectedListPlayer = playerInfo[3]
            if 55<=mouseX<=742 and 448<=mouseY<=488:
              #row rank 5
              selectedPlayer = 5
              selectedListPlayer = playerInfo[4]
            if 55<=mouseX<=742 and 495<=mouseY<=534:
              #row rank 6
              selectedPlayer = 4
              selectedListPlayer = playerInfo[5]
            if 55<=mouseX<=742 and 544<=mouseY<=582:
              #row rank 7
              selectedPlayer = 3
              selectedListPlayer = playerInfo[6]
            if 55<=mouseX<=742 and 592<=mouseY<=632:
              #row rank 8
              selectedPlayer = 2
              selectedListPlayer = playerInfo[7]
            if 55<=mouseX<=742 and 640<=mouseY<=680:
              #row rank 9
              selectedPlayer = 1
              selectedListPlayer = playerInfo[8]
            if 55<=mouseX<=742 and 687<=mouseY<=729:
              #row rank 10
              selectedPlayer = 0
              selectedListPlayer = playerInfo[9]

        #What happens when alhpabet characters are pressed on the keyboard
        if e.type == pygame.KEYDOWN:
          if e.key == pygame.K_a: 
            searchBar2 += "a" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_b:
            searchBar2 += "b" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_c:
            searchBar2 += "c" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_d:
            searchBar2 += "d" #String Concatenation, adds characters to be displayed on the search bar        
          if e.key == pygame.K_e:
            searchBar2 += "e" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_f:
            searchBar2 += "f" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_g:
            searchBar2 += "g" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_h:
            searchBar2 += "h" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_i:
            searchBar2 += "i" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_j:
            searchBar2 += "j" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_k:
            searchBar2 += "k" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_l:
            searchBar2 += "l" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_m:
            searchBar2 += "m" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_n:
            searchBar2 += "n" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_o:
            searchBar2 += "o" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_p:
            searchBar2 += "p" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_q:
            searchBar2 += "q" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_r:
            searchBar2 += "r" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_s:
            searchBar2 += "s" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_t:
            searchBar2 += "t" #String Concatenation, adds characters to be displayed on the search bar         
          if e.key == pygame.K_u:
            searchBar2 += "u" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_v:
            searchBar2 += "v" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_w:
            searchBar2 += "w" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_x:
            searchBar2 += "x" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_y:
            searchBar2 += "y" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_z:
            searchBar2 += "z" #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_SPACE:
            searchBar2 += " " #String Concatenation, adds characters to be displayed on the search bar
          if e.key == pygame.K_BACKSPACE:
            for i in range(0,len(searchBar2)-1,1): #String manipulation, for deleting characters when backspace is pressed
              searchBar_placeHolder+= searchBar2[i]            
            searchBar2 = searchBar_placeHolder
            searchBar_placeHolder = ""
          if e.key == pygame.K_RETURN:
            searchBar = searchBar2
            
      #The order of the 4 sorting systems 
      if counter == 0:
        FastestToSlowest()
      elif counter == 1:
        SlowestToFastest()
      elif counter ==2:
        FastestToSlowest()
        SingleFastestScore()
      elif counter == 3:
        FastestToSlowest()
        SingleSlowestScore()  
      if counter == 1:
        for i in range (9,-1,1):
          if searchBar == playerInfo[i][0].lower():
            searchBarCounter = i
            searchBarAsker = False
      else:
        for i in range (0,10,1):
          if searchBar == playerInfo[i][0].lower():
            searchBarCounter = i
            searchBarAsker = False
      
    elif currentMode == 1: #Game Screen
      #Determine when the screen flashes red
      if countDown == 0:
        screen.fill("black")
      elif countDown > 0:
        if countDown %2 == 0:
          screen.fill("red")
        else:
          screen.fill("black")
          
      DrawGameGrid()
      GameText()
      Shooter()
      if monsterHP > 0:
        Monster()
        monsterFireRate = random.randrange(1,25,1) #The monster's rate of fire

      #calculation for the countdown timer
      if booleanCountDown == True:
         currentTimeX = datetime.now()
         currentTime = (currentTimeX - timeReset).seconds
         
      #During the first 8 seconds of gameplay, display 6 aliens in the Game Section 
      if currentTime == 8 and alienSpawnerChecker == 0:
        #Setting the amount of aliens
        for eachAlienSpawner in range(0,6,1): #number of aliens appended is 6
        #Appending aliens with x coordinates different from each other to the dynamic array,
        #to have all aliens spaced out in the same row
          alienList.append(Alien(225+70*eachAlienSpawner,280))
        alienSpawnerChecker = 1 #indicate that 1 set of aliens have already been appended
        
      #Used to save the exact time the first set of 6 aliens were eliminated to create a timer of 8 seconds
      if len(alienList) == 0 and alienSpawnerChecker == 1:
        currentAlienTime = currentTime #save the current time the first set of 6 aliens were eliminated
        alienSpawnerChecker = 2
        
      #After 8 seconds of the initial 6 aliens being eliminated, display a new set of 6 aliens in front of the monster
      if (currentTime - currentAlienTime) >= 8 and alienSpawnerChecker == 2: 
        for eachAlienSpawner in range(0,6,1): #number of aliens appended is 6
          alienList.append(Alien(225+70*eachAlienSpawner,280)) 
        alienSpawnerChecker = 3 #ensure that the program doesn't enter the if statements above again
            
      MathText()
      for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
          mouseX,mouseY = pygame.mouse.get_pos()
          print(mouseX,",",mouseY)
        if e.type == pygame.KEYDOWN:
          if e.key == pygame.K_RIGHT:
            shooterRight = True
          if e.key == pygame.K_LEFT:
            shooterLeft = True
          if e.key == pygame.K_0:
            mathAnswerDisplay += "0"
          if e.key == pygame.K_1:
            mathAnswerDisplay += "1"
          if e.key == pygame.K_2:
            mathAnswerDisplay += "2"
          if e.key == pygame.K_3:
            mathAnswerDisplay += "3"
          if e.key == pygame.K_4:
            mathAnswerDisplay += "4"
          if e.key == pygame.K_5:
            mathAnswerDisplay += "5"
          if e.key == pygame.K_6:
            mathAnswerDisplay += "6"
          if e.key == pygame.K_7:
            mathAnswerDisplay += "7"
          if e.key == pygame.K_8:
            mathAnswerDisplay += "8"
          if e.key == pygame.K_9:
            mathAnswerDisplay += "9"
          if e.key == pygame.K_BACKSPACE:
            mathAnswerDisplay = mathAnswerDisplay[0:-1:1]
        elif e.type == pygame.KEYUP:
          if e.key == pygame.K_RIGHT:
            shooterRight = False
          if e.key == pygame.K_LEFT:
            shooterLeft = False
      if shooterLeft == True and shooterX>10:
        shooterX += -11
      if shooterRight == True and shooterX + 62 <795 :
        shooterX += 11
      if len(mathAnswerDisplay) == len(str(mathAnswer)):
        shooterAnswer = ""
        if int(mathAnswerDisplay) == mathAnswer:
          shooterAnswer = "correct"
          bulletList.append(ShooterBullet(shooterX+40,625-20))
          screen.blit(muzzleFlash,(shooterX+33,595))
        if int(mathAnswerDisplay) != mathAnswer:
          shooterAnswer = "wrong"
          countDown += 10

        #Generate new random Integers
        number1 = random.randrange(1,11,1)
        number2 = random.randrange(1,10,1)
        mathCounter = random.randrange(1,5,1)
        mathAnswerDisplay = ""
      pygame.time.delay(50)
      PrintTank1()
      PrintTank2()
      PrintCar1()
        
      if countDown > 0:
        countDown += -0.25 #Duration of the flahsing red screen effect
        
      for eachBullet in bulletList:
        eachBullet.PrintBullet()
        eachBullet.BulletMovement()
        if eachBullet.y < 50:
          bulletList.remove(eachBullet)
        if (23<=eachBullet.x<= 172 and (eachBullet.y) < 595 and tank1HP > 0\
          or 23<=eachBullet.x+5<= 172 and (eachBullet.y) < 595 and tank1HP > 0):
          bulletList.remove(eachBullet)
          tank1HP += -1
        if (592<=eachBullet.x<= 742 and (eachBullet.y) < 595 and tank2HP > 0\
          or 592<=eachBullet.x+5<= 742 and (eachBullet.y) < 595 and tank2HP > 0):
          bulletList.remove(eachBullet)
          tank2HP += -1
        if (291<=eachBullet.x<= 476 and (eachBullet.y) < 595 and car1HP > 0\
          or 291<=eachBullet.x+5<= 476 and (eachBullet.y) < 595 and car1HP > 0):
          bulletList.remove(eachBullet)
          car1HP += -1
        elif (monsterX<=eachBullet.x<= monsterX+142 and (eachBullet.y) < 270 and monsterHP > 0\
          or monsterX<=eachBullet.x+5<= monsterX+142 and (eachBullet.y) < 270 and monsterHP > 0):
          bulletList.remove(eachBullet)
          monsterHP += -1

      if monsterX > 599:
        monsterDirection = "left"
      if monsterX-50 < 1:
        monsterDirection = "right"
      
      if monsterFireRate == 1:
        monsterFlameList.append(MonsterFlame(monsterX+33,243))
      #Monster Flame Movement Pattern
      for eachMonsterFlame in monsterFlameList:
        eachMonsterFlame.PrintMonsterFlame() 
        eachMonsterFlame.FlameMovement()
        if eachMonsterFlame.y+85 > 735:
          monsterFlameList.remove(eachMonsterFlame)
        elif (shooterX<=eachMonsterFlame.x<= (shooterX+62) and (eachMonsterFlame.y+85) > 670\
          or shooterX<=eachMonsterFlame.x+59<= (shooterX+62) and (eachMonsterFlame.y+85) > 670):
          monsterFlameList.remove(eachMonsterFlame)
          livesLeft += -1
          countDown += 10
        elif (23<=eachMonsterFlame.x<= 172 and (eachMonsterFlame.y+85) > 520 and tank1HP > 0\
          or 23<=eachMonsterFlame.x+70<= 172 and (eachMonsterFlame.y+85) > 520 and tank1HP > 0):
          monsterFlameList.remove(eachMonsterFlame)
          tank1HP += -1
        elif (592<=eachMonsterFlame.x<= 742 and (eachMonsterFlame.y+85) > 520 and tank2HP > 0\
          or 592<=eachMonsterFlame.x+70<= 742 and (eachMonsterFlame.y+85) > 520 and tank2HP > 0):
          monsterFlameList.remove(eachMonsterFlame)
          tank2HP += -1
        elif (291<=eachMonsterFlame.x<= 476 and (eachMonsterFlame.y+85) > 520 and car1HP > 0\
          or 291<=eachMonsterFlame.x+70<= 476 and (eachMonsterFlame.y+85) > 520 and car1HP > 0):
          monsterFlameList.remove(eachMonsterFlame)
          car1HP += -1

      #Algorithm for alien movement pattern
      for eachAlien in alienList: #loop control variable is eachAlien, loop through each element in alienList
        eachAlien.PrintAlien() #call each individual Alien’s PrintAlien function
        if eachAlien.x > 746: #if alien reaches the right border of the screen
          for eachAlienYCoordinates in alienList:#all aliens move 20 pixels down and change direction to left
            eachAlienYCoordinates.y += 20
          alienDirection = "left"
        elif eachAlien.x < 6: #if alien reaches the left border of the screen
          for eachAlienYCoordinates in alienList: #all aliens move 20 pixels down and change direction to right
            eachAlienYCoordinates.y += 20
          alienDirection = "right"
        fireRate = random.randrange(1,len(alienList)*20,1) #Firerate of each alien, 1 to length of alien list times 20
        if fireRate == 1 and eachAlien.y+120 < 679: #1 in 20 * lenght of alien list probability of 1 alien firing a Flame down the screen
          flameList.append(Flame((eachAlien.x+47),eachAlien.y+120))#create flame object with x coordinate center of individual alien 
        eachAlien.AlienMovement() #Call each Alien's alienMovement() function
        #code for the interaction between the bullet and alien 
        for eachBullet in bulletList: #if alien comes in contact with bullet, both are removed from their respective lists
          if eachAlien.x<=eachBullet.x<=eachAlien.x+33 and eachAlien.y<=eachBullet.y<=eachAlien.y+100 :
            bulletList.remove(eachBullet)
            alienList.remove(eachAlien)    
        #if alien comes in contact with a vehicle shield, the respective vehicle's hit points decrease by 1
        if (22<=eachAlien.x<= 175 and (eachAlien.y+120) > 525\
          or 22<=eachAlien.x+ 47<= 175 and (eachAlien.y+120) > 525):
          tank1HP += -1
        if (292<=eachAlien.x<= 476 and (eachAlien.y+120) > 525\
          or 292<=eachAlien.x+ 47<= 476 and (eachAlien.y+120) > 525):
          car1HP += -1
        if (592<=eachAlien.x<= 742 and (eachAlien.y+120) > 525\
          or 592<=eachAlien.x+ 47<= 742 and (eachAlien.y+120) > 525):
          tank2HP += -1
        #When alien touches the player, the player immediately loses and the game ends
        if (shooterX<=eachAlien.x<= shooterX+62 and (eachAlien.y+120) > 670\
          or shooterX<=eachAlien.x+ 47<= shooterX+62 and (eachAlien.y+120) > 670):
            livesLeft = 0

      #Alien flame movement pattern
      for eachFlame in flameList:
        eachFlame.PrintFlame() 
        eachFlame.FlameMovement()
        if eachFlame.y +100 > 735:
          flameList.remove(eachFlame)
        elif (shooterX<=eachFlame.x<= (shooterX+62) and (eachFlame.y+100) > 670\
          or shooterX<=eachFlame.x+59<= (shooterX+62) and (eachFlame.y+100) > 670):
          flameList.remove(eachFlame)
          livesLeft += -1
          countDown += 10
        elif (23<=eachFlame.x<= 172 and (eachFlame.y+100) > 520 and tank1HP > 0\
          or 23<=eachFlame.x+59<= 172 and (eachFlame.y+100) > 520 and tank1HP > 0):
          flameList.remove(eachFlame)
          tank1HP += -1
        elif (592<=eachFlame.x<= 742 and (eachFlame.y+100) > 520 and tank2HP > 0\
          or 592<=eachFlame.x+59<= 742 and (eachFlame.y+100) > 520 and tank2HP > 0):
          flameList.remove(eachFlame)
          tank2HP += -1
        elif (291<=eachFlame.x<= 476 and (eachFlame.y+100) > 520 and car1HP > 0\
          or 291<=eachFlame.x+59<= 476 and (eachFlame.y+100) > 520 and car1HP > 0):
          flameList.remove(eachFlame)
          car1HP += -1

       #Alien spawn explosion animation for first set of aliens
      if 8 <= currentTime <=9 and 0<= alienAnimation < 2: #interval of alienAnimation is the speed of the animation
        for i in range(0,6,1): #Amount of colums  0,6,1
          screen.blit(alienExplosion1,(180+70*i,260))#object
        alienAnimation += 1
      if 8 <= currentTime <=9 and 2<= alienAnimation < 4:
        for i in range(0,6,1): #Amount of colums  0,6,1
          screen.blit(alienExplosion2,(180+70*i,260))#object
        alienAnimation += 1
      if 8 <= currentTime <=9 and 4<= alienAnimation < 6:
        for i in range(0,6,1): #Amount of colums  0,6,1
          screen.blit(alienExplosion3,(180+70*i,260))#object
        alienAnimation += 1
      if 8 <= currentTime <=9 and 6<= alienAnimation < 8:
        for i in range(0,6,1): #Amount of colums  0,6,1
          screen.blit(alienExplosion4,(180+70*i,260))#object
        alienAnimation += 1
      if 8 <= currentTime <=9 and 8<= alienAnimation < 10:
        for i in range(0,6,1): #Amount of colums  0,6,1
          screen.blit(alienExplosion5,(180+70*i,260))#object
        alienAnimation += 1
      if alienAnimation == 10:
        alienAnimation = 20

      #Alien spawn explosion animation for second set of aliens
      if (currentTime - currentAlienTime) >= 8 and 20 <= alienAnimation < 22:
        for i in range(0,6,1): #Amount of colums  0,6,1
          screen.blit(alienExplosion1,(180+70*i,260))#object
        alienAnimation += 1
      if (currentTime - currentAlienTime) >= 8 and 22 <= alienAnimation < 24:
        for i in range(0,6,1): #Amount of colums  0,6,1
          screen.blit(alienExplosion2,(180+70*i,260))#object
        alienAnimation += 1
      if (currentTime - currentAlienTime) >= 8 and 24 <= alienAnimation < 26:
        for i in range(0,6,1): #Amount of colums  0,6,1
          screen.blit(alienExplosion3,(180+70*i,260))#object
        alienAnimation += 1
      if (currentTime - currentAlienTime) >= 8 and 26 <= alienAnimation < 28:
        for i in range(0,6,1): #Amount of colums  0,6,1
          screen.blit(alienExplosion4,(180+70*i,260))#object
        alienAnimation += 1
      if (currentTime - currentAlienTime) >= 8 and 28 <= alienAnimation < 30:
        for i in range(0,6,1): #Amount of colums  0,6,1
          screen.blit(alienExplosion5,(180+70*i,260))#object
        alienAnimation += 1
      if alienAnimation == 30:
        alienAnimation = 40     

      if livesLeft <=0: #if all three lives are gone, player loses, lose condition screen 
        booleanCountDown = False
        gameOverCountDown = (datetime.now() - currentTimeX).seconds
        screen.fill("black")
        pygame.draw.rect(screen,(255,0,0),(200,250, 400,400))#black interior search bar
        gameText = text4.render("GAME OVER",True,"Black")#white text TIME
        screen.blit(gameText,(220,260))
        gameText = text2.render(("PLAYER: "+ selectedListPlayer[0]),True,"Black")#white text TIME
        screen.blit(gameText,(220,340))
        gameText = text2.render("YOU LOST NO SCORE",True,"Black")#white text TIME
        screen.blit(gameText,(220,420))
        gameText = text2.render(("FASTEST TIME: " + selectedListPlayer[1]),True,"Black")#white text TIME
        screen.blit(gameText,(220,500))
        gameText = text2.render("RETURNING IN: " + str(5-gameOverCountDown),True,"Black")#white text TIME
        screen.blit(gameText,(220,580))
        if (5-gameOverCountDown) <= 0: #game over countdown to return to home screen
          currentMode = 0

      #If player eliminates all displayed aliens and monster, win condition screen
      if livesLeft> 0 and len(alienList) == 0 and monsterHP <= 0:
        booleanCountDown = False
        #This stops the program from assigning the variable currenTimeX a new current time the moment the
        #player beats the game. Therefore saving the exact time of when the player beat the game
        gameOverCountDown = (datetime.now() - currentTimeX).seconds
        #Subtracting the exact time of when the player beat the game from the current time,
        #this creates a stopwatch of when the player beat the game
        screen.fill("black")
        pygame.draw.rect(screen,(57,255,20),(200,250, 400,400))#black interior search bar
        gameText = text2.render("CONGRAGULATIONS",True,"Black")#white text TIME
        screen.blit(gameText,(220,280))
        gameText = text2.render(("PLAYER: "+ selectedListPlayer[0]),True,"Black")#white text TIME
        screen.blit(gameText,(220,340))
        gameText = text2.render("TIME: " + str(currentTime),True,"Black")#white text TIME
        screen.blit(gameText,(220,420))
        gameText = text2.render(("FASTEST TIME: " + selectedListPlayer[1]),True,"Black")#white text TIME
        screen.blit(gameText,(220,500))
        gameText = text2.render("RETURNING IN: " + str(5-gameOverCountDown),True,"Black")#white text TIME
        screen.blit(gameText,(220,580))
      
        if (5-gameOverCountDown) <= 0: #by subtracting it from 5 it creates a countdown timer of 5 seconds
          if int(selectedListPlayer[1]) > currentTime:
            #if the player’s previous fastest score is slower than their current score then their new score will be updated 
            selectedListPlayer[1] = str(currentTime) #selectedListPlayer is current selected player, element at index 1 is score
            FastestToSlowest() #sorts the list to fastest to slowest to sort the scores in order in the text file
            counter = 0 #Changes the filter button title in the Home Interface back to Fast>Slow
            playerInfo[selectedPlayer] = selectedListPlayer #Curret player data in the 2D Array is updated with the new score
            file = open("Math_Slayers.txt","r+") #open file “Math_Slayers.txt” for reading and writing
            file.truncate(0) #Set file size to 0, deletes everything in the file
            spaceChecker = False
            file.seek(0) #Set the reference point of the file handle to the beginning of the file
            
            #Algorithm to rewrite contents of the text file with new player names and scores
            for eachPlayerInPlayerInfo in playerInfo: #eachPlayerInPlayerInfo is equal to an array of player name and score
              if spaceChecker == True:
                file.writelines("\n")#write a new line in text file
              commaCheck = True
              for individualElement in eachPlayerInPlayerInfo: 
                file.writelines(individualElement) #writes the player info into text file
                if commaCheck == True: #Checks to see when to add a comma
                  file.writelines(",") #after writing player name in the text file, a comma is written after it 
                  commaCheck = False
              spaceChecker = True
            file.close()  
          currentMode = 0 #Retuns to Home Interface
          
    elif currentMode == 2: #Multiplayer Game Interface
      #recieving data from server
      dataReceiveByte = server.recv(2048)#receive byte-stream data from server, buffer size is 2048 bytes
      dataReceive = pickle.loads(dataReceiveByte) #convert byte-stream data into string
      enemyX = dataReceive[0] #first element in the list is the x coordinates of the enemy player
      #Checking if there is a new enemyBullet object: if the array of enemy player bullets received is larger
      #than the array of enemy player bullets stored locally on the computer, then there is new data
      if(len(dataReceive[1])>len(enemyBulletList)): #algorithm for adding a new enemy bullet
        eBLCounter = len(dataReceive[1])-len(enemyBulletList) #calculate how many new bullets there are
        for i in range(0,eBLCounter,1):
        #calculates the number to add to the index of the second row in order to calculate the
        #exact position of the new bullet in the 2D array 
          enemyBulletList.append(EnemyBullet(dataReceive[1][len(enemyBulletList)+i], 232))

      #Algorithm for flashing red screen
      if countDown == 0:
        screen.fill("black")
      elif countDown > 0:
        if countDown %2 == 0:
          screen.fill("red")
        else:
          screen.fill("black")
      DrawMultiplayerGameGrid()
      MultiplayerGameText()
      Shooter()
      Enemy()
      #Count Down Timer 
      if booleanCountDown == True:
        currentTime += 0.55
        
      #Keyboard Inputs
      MathText()
      for e in pygame.event.get():
        #Mouse Testing coordinates
        if e.type == pygame.MOUSEBUTTONDOWN:
          mouseX,mouseY = pygame.mouse.get_pos()
          print(mouseX,",",mouseY)
        if e.type == pygame.KEYDOWN:
          #Arrow Keys
          if e.key == pygame.K_RIGHT:
            shooterRight = True
          if e.key == pygame.K_LEFT:
            shooterLeft = True
          #Numbers for Math shooting mechanism
          if e.key == pygame.K_0:
            mathAnswerDisplay += "0"
          if e.key == pygame.K_1:
            mathAnswerDisplay += "1"
          if e.key == pygame.K_2:
            mathAnswerDisplay += "2"
          if e.key == pygame.K_3:
            mathAnswerDisplay += "3"
          if e.key == pygame.K_4:
            mathAnswerDisplay += "4"
          if e.key == pygame.K_5:
            mathAnswerDisplay += "5"
          if e.key == pygame.K_6:
            mathAnswerDisplay += "6"
          if e.key == pygame.K_7:
            mathAnswerDisplay += "7"
          if e.key == pygame.K_8:
            mathAnswerDisplay += "8"
          if e.key == pygame.K_9:
            mathAnswerDisplay += "9"
          #Delete key to delete math text
          if e.key == pygame.K_BACKSPACE:
            mathAnswerDisplay = mathAnswerDisplay[0:-1:1]
        #Releasing arrow keys
        elif e.type == pygame.KEYUP:
          if e.key == pygame.K_RIGHT:
            shooterRight = False
          if e.key == pygame.K_LEFT:
            shooterLeft = False

      #Shooter Movement
      if shooterLeft == True and shooterX>10:
        shooterX += -25
      if shooterRight == True and shooterX + 62 <795 :
        shooterX += 25
      dataSend[0] = shooterX
      #The case where the digit inputed equals to digit of answer
      if len(mathAnswerDisplay) == len(str(mathAnswer)):
        shooterAnswer = ""
        #The case where the math is correct
        if int(mathAnswerDisplay) == mathAnswer:
          shooterAnswer = "correct"
          #Firing a bullet
          bulletList.append(ShooterBullet(shooterX+40,625-20))
          dataSend[1].append(shooterX+40)
          screen.blit(muzzleFlash,(shooterX+33,595))
        #The case where the math is wrong
        if int(mathAnswerDisplay) != mathAnswer:
          shooterAnswer = "wrong"
          countDown += 10 #Screen Flash
        #Picking new numbers for new math equation
        number1 = random.randrange(1,11,1)
        number2 = random.randrange(1,10,1)
        mathCounter = random.randrange(1,5,1)
        mathAnswerDisplay = ""
      pygame.time.delay(0)
      PrintTank11()
      PrintCar11()
      PrinteTank1()
      PrinteCar1()
      #Flashing Red Srceen duration
      if countDown > 0:
        countDown += -0.25
        
      #Bullet Movement         
      bulletListCounter = 0 #used to calculate the index of the bulletList to be popped 
      for eachBullet in bulletList: #loop control variable is eachBullet, loop through each element in bulletList
        eachBullet.PrintBullet() #Call each individual bullet’s PrintBullet() function
        eachBullet.BulletMovement()#Call each individual bullet’s BulletMovement() function
        if eachBullet.y < 120: #if each bullet touches the top borders of the Game section, the bullet disappears
          bulletList.remove(eachBullet)
          dataSend[1].pop(bulletListCounter) #Remove the bullet at index bulletListCounter
          bulletListCounter += -1 #subtract 1 from the counter as there is now 1 less bullet
        #Bullet interaction with vehicle shields
        if (20<=eachBullet.x<= 172 and (eachBullet.y) < 595 and tank1HP > 0\
          or 20<=eachBullet.x+5<= 172 and (eachBullet.y) < 595 and tank1HP > 0):
          #For the vehicle shields closer to the player, data have to be sent first, if not, because the vehicle is
          #so close to the player, and due to latency, the bullet will immediately be removed locally without the the server
          #getting any information of its creation
          dataSendByteStream = pickle.dumps(dataSend)#Convert 2D array into byte stream for socket
          server.send(dataSendByteStream) #send data to server
          bulletList.remove(eachBullet)
          dataSend[1].pop(bulletListCounter) #Remove the bullet at index bulletListCounter
          bulletListCounter += -1 #subtract 1 from the counter as there is now 1 less bullet
          tank1HP += -1 #Subtract 1 hit point from player's tank shield
        if (230<=eachBullet.x<= 419 and (eachBullet.y) < 595 and car1HP > 0\
          or 230<=eachBullet.x+5<= 419 and (eachBullet.y) < 595 and car1HP > 0):
          dataSendByteStream = pickle.dumps(dataSend)#Convert 2D array into byte stream for socket
          server.send(dataSendByteStream) #send data to server
          bulletList.remove(eachBullet)
          dataSend[1].pop(bulletListCounter) #Remove the bullet at index bulletListCounter
          bulletListCounter += -1 #subtract 1 from the counter as there is now 1 less bullet
          car1HP += -1 #Subtract 1 hit point from player's car shield
        if (800-172<=eachBullet.x<= 800-20 and (eachBullet.y) < 335 and eTank1HP > 0\
          or 800-172<=eachBullet.x+5<= 800-20 and (eachBullet.y) < 335 and eTank1HP > 0):
          bulletList.remove(eachBullet)
          dataSend[1].pop(bulletListCounter)#Remove the bullet at index bulletListCounter
          bulletListCounter += -1 #subtract 1 from the counter as there is now 1 less bullet
          eTank1HP += -1 #Subtract 1 hit point from enemy's tank shield
        if (800-419<=eachBullet.x<= 800-230 and (eachBullet.y) < 335 and eCar1HP > 0\
          or 800-419 <=eachBullet.x+5<= 800-230 and (eachBullet.y) < 335 and eCar1HP > 0):
          bulletList.remove(eachBullet)
          dataSend[1].pop(bulletListCounter)#Remove the bullet at index bulletListCounter
          bulletListCounter += -1 #subtract 1 from the counter as there is now 1 less bullet
          eCar1HP += -1 #Subtract 1 hit point from enemy's car shield 
        #Shoot enemy
        if (enemyX<=eachBullet.x<= enemyX+62 and (eachBullet.y) < 225\
          or enemyX<=eachBullet.x+5<= enemyX+62 and (eachBullet.y) < 225):
          bulletList.remove(eachBullet)
          dataSend[1].pop(bulletListCounter) #Remove the bullet at index bulletListCounter
          bulletListCounter += -1 #subtract 1 from the counter as there is now 1 less bullet
          enemyLivesLeft += -1 #subtract 1 life from the enemy player
        bulletListCounter += 1 #After every iteration counter increments by 1 to move onto the next bullet 
        counter+=1

       #Enemy Bullet Movement
      for eachEnemyBullet in enemyBulletList:
        eachEnemyBullet.PrintEnemyBullet()
        eachEnemyBullet.EnemyBulletMovement()
        if 225<eachEnemyBullet.y<300:
          screen.blit(enemyMuzzleFlash,(enemyX+7,222))
        if eachEnemyBullet.y > 730:
          enemyBulletList.remove(eachEnemyBullet)
        #Bullet hit car/tank 
        if (20<=eachEnemyBullet.x<= 172 and (eachEnemyBullet.y) > 520 and tank1HP > 0\
          or 20<=eachEnemyBullet.x+5<= 172 and (eachEnemyBullet.y) > 520 and tank1HP > 0):
          enemyBulletList.remove(eachEnemyBullet)
          tank1HP += -1
        if (230<=eachEnemyBullet.x<= 419 and (eachEnemyBullet.y) > 520 and car1HP > 0\
          or 230<=eachEnemyBullet.x+5<= 419 and (eachEnemyBullet.y) > 520 and car1HP > 0):
          enemyBulletList.remove(eachEnemyBullet)
          car1HP += -1
        if (800-172<=eachEnemyBullet.x<= 800-20 and (eachEnemyBullet.y) > 260 and eTank1HP > 0\
          or 800-172<=eachEnemyBullet.x+5<= 800-20 and (eachEnemyBullet.y) > 260 and eTank1HP > 0):
          enemyBulletList.remove(eachEnemyBullet)
          eTank1HP += -1
        if (800-419<=eachEnemyBullet.x<= 800-230 and (eachEnemyBullet.y) > 260 and eCar1HP > 0\
          or 800-419 <=eachEnemyBullet.x+5<= 800-230 and (eachEnemyBullet.y) > 260 and eCar1HP > 0):
          enemyBulletList.remove(eachEnemyBullet)
          eCar1HP += -1
        #Shoot enemy
        if (shooterX<=eachEnemyBullet.x<= shooterX+62 and (eachEnemyBullet.y) > 630\
          or shooterX<=eachEnemyBullet.x+5<= shooterX+62 and (eachEnemyBullet.y) > 630):
          enemyBulletList.remove(eachEnemyBullet)
          livesLeft += -1
      if livesLeft <=0:
        if gameOverTimer == 0:
          currentTimeX = datetime.now()
          gameOverTimer = 1
        gameOverCountDown = (datetime.now()-currentTimeX).seconds
        booleanCountDown = False
        screen.fill("black")
        pygame.draw.rect(screen,(255,0,0),(200,250, 400,400))#black interior search bar
        gameText = text4.render("GAME OVER",True,"Black")#white text TIME
        screen.blit(gameText,(220,260))
        gameText = text2.render(("RETURNING IN: " + str(5-gameOverCountDown)),True,"Black")#white text TIME
        screen.blit(gameText,(220,580))
        if 5-gameOverCountDown <= 0:
          dataSend[2] = 0
          currentMode = 0

      if livesLeft> 0 and enemyLivesLeft <= 0:
        if gameOverTimer == 0:
          currentTimeX = datetime.now()
          gameOverTimer = 1
        gameOverCountDown = (datetime.now()-currentTimeX).seconds
        booleanCountDown = False
        screen.fill("black")
        pygame.draw.rect(screen,(57,255,20),(200,250, 400,400))#black interior search bar
        gameText = text2.render("CONGRAGULATIONS",True,"Black")#white text TIME
        screen.blit(gameText,(220,280))
        gameText = text2.render(("RETURNING IN: " +  str(5-gameOverCountDown)),True,"Black")#white text TIME
        screen.blit(gameText,(220,580))
        if 5-gameOverCountDown <= 0:
          dataSend[2] = 0
          currentMode = 0
      
      counter+=1
      dataSendByteStream = pickle.dumps(dataSend)#Pickle.dump turns list into byte stream for socket
      server.send(dataSendByteStream)
    pygame.display.update()

