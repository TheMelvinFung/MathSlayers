#Server
from socket import *
import pickle

print("Starting PVP Server asd")
shooterX = 338 #shooter starting coordinates
enemyX = (800-338-62) #enemy starting coordinates
enemyLivesLeft = 3
tank1HP = 5
car1HP = 5
eTank1HP = 5
eCar1HP = 5
#list to send [shooterX,[bulletListXCoordinate]]
dataRecieved1 = [338,[],True]
dataSend1Enemey = [338,[],True]
#list to send [shooterX,[bulletListXCoordinate]]
dataRecieved2 = [338,[],True]
dataSend2Enemey = [338,[],True]

livesLeft = 3 #shooter total lives

# Socket setup
serverSocket = socket(AF_INET, SOCK_STREAM) #create an INET, STREAMing socket
serverSocket.bind(('', 22321)) #bind the socket to the tuple containing public host on port 22321
serverSocket.listen(2) #Queue 2 client connect requests: maximum 2 clients for the game

Connected = False  #Identifies whether the client has connected to the server
Connected2 = False
while True:
    if Connected2 == False: #If client1 hasn't connected to the server
        # Accept connection from player1
        player1, addr1 = serverSocket.accept() #accept a connection
        print("Player 1 has joined") #Allows server to test for for connection (extensibility)
        player1.send("1".encode()) #Will be sent to client1 to notify connection
        Connected2 = True
    if Connected == False: #If client2 hasn't connected to the server
        # Accept connection from player2
        player2, addr2 = serverSocket.accept() #accept a connection
        print("Player 2 has joined") #Allows server to test for for connection (extensibility)
        player2.send("2".encode()) #Will be sent to client2 to notify connection
        Connected = True
        
    #Multiplayer Game Start
    while Connected == True and Connected2 == True: 
        #send enemy info to player 1
        #Player's x-coordinates sent to opponent is subtracted from width of screen and
        #the width of the player avatar's png to reverse the image 
        dataSend1Enemey[0] = 800-62-dataRecieved2[0] #DataRecieved2 is the data recieved from client 2
        dataSend1Enemey[1] = dataRecieved2[1]
        #Algorithm to reverse the coordinates of each enemy bullet by subtracting
        #each bullet's x coordinates from the width of the screen and bullet
        for eachBullet in range(0,len(dataSend1Enemey[1]),1):
            dataSend1Enemey[1][eachBullet] = 800-5-dataRecieved2[1][eachBullet]
        dataSend1ByteStream = pickle.dumps(dataSend1Enemey) #Convert 2D array into byte stream for socket
        player1.send(dataSend1ByteStream) #send data to client 1
        
        
        #send enemy info to player 2
        #Player's x-coordinates sent to opponent is subtracted from width of screen and
        #the width of the player avatar's png to reverse the image 
        dataSend2Enemey[0] = 800-62-dataRecieved1[0] #DataRecieved1 is the data recieved from client 1
        dataSend2Enemey[1] = dataRecieved1[1]
        #Algorithm to reverse the coordinates of each enemy bullet by subtracting
        #each bullet's x coordinates from the width of the screen and bullet
        for eachBullet in range(0,len(dataSend2Enemey[1]),1):
            dataSend2Enemey[1][eachBullet] = 800-5-dataRecieved1[1][eachBullet]
        dataSend2ByteStream = pickle.dumps(dataSend2Enemey) #Convert 2D array into byte stream for socket
        player2.send(dataSend2ByteStream) #send data to client 2
        
        dataReceive1 = player1.recv(2048)
        dataReceive2 = player2.recv(2048)       
        dataRecieved1 = pickle.loads(dataReceive1)
        dataRecieved2 = pickle.loads(dataReceive2)
        if dataUpdate1[2] == 0 or dataUpdate2[2] == 0:
            Connected = False
            Connected2 = False
        print("1",Connected)
        print("2",Connected2)

  
    
