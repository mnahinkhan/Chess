#    15-112: Principles of Programming and Computer Science
#    Project: Chess Program
#    Name      : Muhammad Nahin Khan
#    AndrewID  : mnk1
#    File Created: 07/11/2016
#    Modification History:
#    Start             End
#    07/11 12:52       07/11 13:20
#    07/11 18:00       07/11 21:06
#    09/11 03:13       09/11 05:49
#    09/11 15:38       09/11 16:19
#    10/11 15:51       10/11 16:31
#    10/11 20:17       10/11 21:34
#    11/11 23:50       12/11 05:19
#    13/11 00:01       13/11 01:34
#    15/11 16:19       15/11 17:00
#    16/11 01:00       16/11 01:49
#
#
# This program is a chess game. 
#Note about coordinates:
#Normally, algebraic notation is used to specify a box on a chess board. In this
#program, coordinates will be index referecnes to the 2_D array that stores the
#state of the board. Thus, e4 in algebraic notation would be expressed as (4,4)
#in this program.
import pygame
from pygame.locals import *
def drawText(board):
    for i in range(len(board)):
        for k in range(len(board[i])):
            if board[i][k]==0:
                board[i][k] = 'Oo'
        print board[i]
    for i in range(len(board)):
        for k in range(len(board[i])):
            if board[i][k]=='Oo':
                board[i][k] = 0
    print "###############################################"
def getMouseClick():
    x = input("What's x value?: ")
    y = input("What's y value?: ")
    return [x,y]

def isOccupied(board,x,y):
    if board[y][x] == 0:
        #The square has nothing on it.
        
        return False
    return True
def isOccupiedby(board,x,y,color):
    if board[y][x]==0:
        #the square has nothing on it.
        return False
    if board[y][x][1] == color[0]:
        #The square has a piece of the color inputted.
        return True
    #The square has a piece of the opposite color.
    return False
def filterbyColor(board,listofTuples,color):
    #This function takes the board state, a list of coordinates, and a color as
    #input. It will return the same list, but without coordinates that are out
    #of bounds of the board and also without those occupied by the pieces of
    #the particular color passed to this function as an argument. In other words,
    #if 'white' is passed in, it will not return any white occupied square. 
    real_list = []
    for tupleq in listofTuples:
        x = tupleq[0]
        y = tupleq[1]
        if x>=0 and x<=7 and y>=0 and y<=7 and not isOccupiedby(board,x,y,color):
            #coordinates are on-board and no same-color piece is on the square.
            real_list.append(tupleq)
    return real_list
def isAttackedby(board,spec_x,spec_y,color,state_info=-1):
    #This function checks if the square specified by (x,y) coordinate is being
    #attacked by any of a specific colored set of pieces
    color = color[0]
    listofAttackedSquares = []
    for x in range(8):
        for y in range(8):
            if board[y][x]!=0 and board[y][x][1]==color:
                listofAttackedSquares.extend(
                    findPossibleSquares(board,x,y,state_info,True))
    return (spec_x,spec_y) in listofAttackedSquares             
def findPossibleSquares(board,x,y,state_info,AttackSearch=False):
    #This function takes as its input the current state of the chessboard, and
    #a particular x and y coordinate. It will return for the piece on that board
    #a list of possible coordinates it could move to.
    if len(board[y][x])!=2: #Unexpected, return empty list.
        return [] 
    piece = board[y][x][0] #Pawn, rook, etc.
    color = board[y][x][1] #w or b.
    #Have the complimentary color stored for convenience:
    enemy_color = opp(color)
    
    if state_info == -1:
        state_info = [0,[False,False],-1,0]
    
    listofTuples = [] #Holds list
    
    if piece == 'P': #The piece is a pawn.
        En_P_Target = state_info[2] #Possible en-passant target
        if color=='w': #The piece is white
            if not isOccupied(board,x,y-1) and not AttackSearch:
                #The piece immediately above is not occupied, append it.
                listofTuples.append((x,y-1))
                
                if y == 6 and not isOccupied(board,x,y-2):
                    #If pawn is at its initial position, it can move two squares.
                    listofTuples.append((x,y-2))
            
            if x!=0 and isOccupiedby(board,x-1,y-1,'black'):
                #The piece diagonally up and left of this pawn is a black piece.
                #Also, this is not an 'a' file pawn (left edge pawn)
                listofTuples.append((x-1,y-1))
            if x!=7 and isOccupiedby(board,x+1,y-1,'black'):
                #The piece diagonally up and right of this pawn is a black one.
                #Also, this is not an 'h' file pawn.
                listofTuples.append((x+1,y-1))
            if En_P_Target!=-1: #There is a possible en pasant target:
                if En_P_Target == (x-1,y-1) or En_P_Target == (x+1,y-1):
                    #We're at the correct location to potentially perform en
                    #passant:
                    listofTuples.append(En_P_Target)
            
        elif color=='b': #The piece is black, same as above but opposite side.
            if not isOccupied(board,x,y+1) and not AttackSearch:
                listofTuples.append((x,y+1))
                if y == 1 and not isOccupied(board,x,y+2):
                    listofTuples.append((x,y+2))
            if x!=0 and isOccupiedby(board,x-1,y+1,'white'):
                listofTuples.append((x-1,y+1))
            if x!=7 and isOccupiedby(board,x+1,y+1,'white'):
                listofTuples.append((x+1,y+1))
            if En_P_Target == (x-1,y+1) or En_P_Target == (x+1,y+1):
                listofTuples.append(En_P_Target)

    elif piece == 'R': #The piece is a rook.
        #Get all the horizontal squares:
        for i in [-1,1]:
            #i is -1 then +1. This allows for searching right and left.
            kx = x #This variable stores the x coordinate being looked at.
            while True: #loop till break.
                kx = kx + i #Searching left or right
                if kx<=7 and kx>=0: #Making sure we're still in board.
                    
                    if not isOccupied(board,kx,y):
                        #The square being looked at it empty. Our rook can move
                        #here.
                        listofTuples.append((kx,y))
                    else:
                        #The sqaure being looked at is occupied. If an enemy
                        #piece is occupying it, it can be captured so its a valid
                        #move. 
                        if isOccupiedby(board,kx,y,enemy_color):
                            listofTuples.append((kx,y))
                        #Regardless of the occupying piece color, the rook cannot
                        #jump over. No point continuing search beyond in this
                        #direction:
                        break
                        
                else: #We have exceeded the limits of the board
                    break
        #Now using the same method, get the vertical squares:
        for i in [-1,1]:
            ky = y
            while True:
                ky = ky + i 
                if ky<=7 and ky>=0: 
                    if not isOccupied(board,x,ky):
                        listofTuples.append((x,ky))
                    else:
                        if isOccupiedby(board,x,ky,enemy_color):
                            listofTuples.append((x,ky))
                        break
                else:
                    break
        
    elif piece == 'N': #The piece is a knight.
        #The knight can jump across a board. It can jump either two or one
        #squares in the x or y direction, but must jump the complimentary amount
        #in the other. In other words, if it jumps 2 sqaures in the x direction,
        #it must jump one square in the y direction and vice versa.
        for dx in [-2,-1,1,2]:
            if abs(dx)==1:
                sy = 2
            else:
                sy = 1
            for dy in [-sy,+sy]:
                listofTuples.append((x+dx,y+dy))
        #Filter the list of tuples so that only valid squares exist.
        listofTuples = filterbyColor(board,listofTuples,color)
    elif piece == 'B': # A bishop.
        #A bishop moves diagonally. This means a change in x is accompanied by a
        #change in y-coordiante when the piece moves. The changes are exactly the
        #same in magnitude and direction.
        for dx in [-1,1]: #Allow two directions in x.
            for dy in [-1,1]: #Similarly, up and down for y.
                kx = x #These varibales store the coordinates of the square being
                       #observed.
                ky = y
                while True: #loop till broken.
                    kx = kx + dx #change x
                    ky = ky + dy #change y
                    if kx<=7 and kx>=0 and ky<=7 and ky>=0:
                        #square is on the board
                        if not isOccupied(board,kx,ky):
                            #The square is empty, so our bishop can go there.
                            listofTuples.append((kx,ky))
                        else:
                            #The square is not empty. If it has a piece of the
                            #enemy,our bishop can capture it:
                            if isOccupiedby(board,kx,ky,enemy_color):
                                listofTuples.append((kx,ky))
                            #Bishops cannot jump over other pieces so terminate
                            #the search here:
                            break    
                    else:
                        #Square is not on board. Stop looking for more in this
                        #direction:
                        break
    
    elif piece == 'Q': #A queen
        #A queen's possible targets are the union of all targets that a rook and
        #a bishop could have made from the same location
        #Temporarily pretend there is a rook on the spot:
        board[y][x] = 'R' + color
        list_rook = findPossibleSquares(board,x,y,state_info,True)
        #Temporarily pretend there is a bishop:
        board[y][x] = 'B' + color
        list_bishop = findPossibleSquares(board,x,y,state_info,True)
        #Merge the lists:
        listofTuples = list_rook + list_bishop
        #Change the piece back to a queen:
        board[y][x] = 'Q' + color
    elif piece == 'K': # A king!
        #A king can make one step in any direction:
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                listofTuples.append((x+dx,y+dy))
        #Make sure the targets aren't our own piece or off-board:
        listofTuples = filterbyColor(board,listofTuples,color)
        if not AttackSearch:
            player = state_info[0]
            #Kings can potentially castle:
            castling_rights = state_info[1]
            right = castling_rights[player]
            #Kingside
            if (right and #White has right to castle
            not isOccupied(board,x+1,y) and #The square on its right is empty
            not isOccupied(board,x+2,y) and #The second square beyond is also empty
            not isAttackedby(board,x,y,enemy_color,state_info) and #The king isn't under atack
            not isAttackedby(board,x+1,y,enemy_color,state_info) and #Or the path through which
            not isAttackedby(board,x+2,y,enemy_color,state_info)):#it will move
                listofTuples.append((x+2,y))
            #Queenside
            if (right and #White has right to castle
            not isOccupied(board,x-1,y)and #The square on its left is empty
            not isOccupied(board,x-2,y)and #The second square beyond is also empty
            not isOccupied(board,x-3,y) and #And the one beyond.
            not isAttackedby(board,x,y,enemy_color,state_info) and #The king isn't under atack
            not isAttackedby(board,x-1,y,enemy_color,state_info) and #Or the path through which
            not isAttackedby(board,x-2,y,enemy_color,state_info)):#it will move
                listofTuples.append((x-2,y)) #Let castling be an option.

##            refinedlist = []
##            for tupleq in listofTuples:
##                px = tupleq[0]
##                py = tupleq[1]
##                if not isAttackedby(board,px,py,enemy_color,state_info):
##                    refinedlist.append(tupleq)
##            listofTuples = refinedlist

    #Make sure the king is not under attack as a result of this move:
    if not AttackSearch:
        new_list = []
        for tupleq in listofTuples:
            x2 = tupleq[0]
            y2 = tupleq[1]
            temp_board = [row[:] for row in board]
            #temp_state = [state_info[i] for i in range(len(state_info))]
            temp_board = makemove(temp_board,-1,x,y,
                             x2,y2)[0]
            if not isCheck(temp_board,color):
                new_list.append(tupleq)
        listofTuples = new_list
    return listofTuples
def opp(color):
    color = color[0]
    if color == 'w':
        oppcolor = 'b'
    else:
        oppcolor = 'w'
    return oppcolor
def isCheck(board,color):
    #This function takes a board as its input and checks if the King of the
    #specified color is under attack.
    color = color[0]
    enemy = opp(color)
    piece = 'K' + color
    x,y = lookfor(board,piece)[0]

    return isAttackedby(board,x,y,enemy)

def lookfor(board,piece):
    #This function looks for a speecified piece on the board and returns a list of all its
    #coordinates
    listofLocations = []
    for row in range(8):
        for col in range(8):
            if board[row][col] == piece:
                x = col
                y = row
                listofLocations.append((x,y))
    return listofLocations
def makemove(board,state_info,x,y,x2,y2):
    #This function makes a move on the board and
    #returns the resultant board and game state.
    #Get piece and color of the one being moved:
    if state_info == -1:
        state_info = [0,[False,False],-1,0]
    piece = board[y][x][0]
    color = board[y][x][1]
    #Get the individual game components:
    player = state_info[0]
    castling_rights = state_info[1]
    EnP_Target = state_info[2]
    half_move_clock = state_info[3]

    #Make the move:
    board[y2][x2] = board[y][x]
    board[y][x] = 0
    
    #Special piece requirements:
    #King:
    if piece == 'K':
        #Ensure that since a King is moved, the castling
        #rights are lost:
        castling_rights[player] = False
        #If castling occured:
        if abs(x2-x) == 2:
            if color=='w':
                l = 7
            else:
                l = 0
            
            if x2>x:
                    board[l][5] = 'R'+color
                    board[l][7] = 0
            else:
                    board[l][3] = 'R'+color
                    board[l][0] = 0
                    
    #Pawn:
    if piece == 'P':
        #If an en passant kill was made:
        if EnP_Target == (x2,y2):
            if color=='w':
                board[y2+1][x2] = 0
            else:
                board[y2-1][x2] = 0
        #If a pawn moved two steps, there is an en passant
        #target. Update the variable.
        if abs(y2-y)==2:
            EnP_Target = (x,(y+y2)/2)
        else:
            EnP_Target = -1
        #Promotion:
        if y2==0:
            board[y2][x2] = 'Qw'
        elif y2 == 7:
            board[y2][x2] = 'Qb'
    else:
        EnP_Target = -1

    #Update aspects of state_info:
    #Since a move has been made, the other player
    #should be the 'side to move'
    player = 1 - player
    #The half_move_clock should increase by 1.
    half_move_clock = half_move_clock + 1
    
    #Pack it back into one variable:       
    state_info = [ player, castling_rights,
                   EnP_Target, half_move_clock]
    
    return [board,state_info]
    

class Piece:
    def __init__(self,pieceinfo,chess_coord):
        #global pieces_image
        #global size_of_a_piece
        size = (square_width,square_height)
        color = pieceinfo[1]
        piece = pieceinfo[0]
        if piece=='K':
            left_x = 0
        else:
            if piece=='Q':
                index = 1
            elif piece=='B':
                index = 2
            elif piece == 'N':
                index = 3
            elif piece == 'R':
                index = 4
            elif piece == 'P':
                index = 5
            left_x = size[0]*index
        if color == 'w':
            left_y = 0
        else:
            left_y = size[1]
        
        self.pieceinfo = pieceinfo
        self.subsection = (left_x,left_y,size[0],size[1])
        self.chess_coord = chess_coord
        self.pos = (-1,-1)

    def getInfo(self):
        return [self.chess_coord, self.subsection,self.pos]
    def setpos(self,pos):
        self.pos = pos
    def getpos(self):
        return self.pos
    def setcoord(self,coord):
        self.chess_coord = coord
    def __repr__(self):
        #useful for debugging
        return self.pieceinfo+'('+str(chess_coord[0])+','+str(chess_coord[1])+')'
def chess_coord_to_pixels(chess_coord):
    #This function takes as input a chess coordinate such as (4,7) and
    #the size of the image of a chess piece. It returns the top left
    #corner pixel at which a piece of the given size should be placed
    #on the board for it to appear at the correct square.

    return (chess_coord[0]*square_width, chess_coord[1]*square_height)

def pixel_coord_to_chess(pixel_coord):
    return (pixel_coord[0]/square_width, pixel_coord[1]/square_height)
    
class Shades:
    def __init__(self,image,coord):
        self.image = image
        self.pos = coord
    def getInfo(self):
        return [self.image,self.pos]
def drawBoard():
    screen.blit(background,(0,0))
    if player==1:
        order = [listofWhitePieces,listofBlackPieces]
    else:
        order = [listofBlackPieces,listofWhitePieces]
    if isTransition:
        order = list(reversed(order))
    #Pieces
    for piece in order[0]:
        
        chess_coord,subsection,pos = piece.getInfo()
        pixel_coord = chess_coord_to_pixels(chess_coord)
        if pos==(-1,-1):
            screen.blit(pieces_image,pixel_coord,subsection)
        else:
            screen.blit(pieces_image,pos,subsection)
    #Shades
    for shade in listofShades:
        img,chess_coord = shade.getInfo()
        pixel_coord = chess_coord_to_pixels(chess_coord)
        screen.blit(img,pixel_coord)
    #Pieces
    for piece in order[1]:
        chess_coord,subsection,pos = piece.getInfo()
        pixel_coord = chess_coord_to_pixels(chess_coord)
        if pos==(-1,-1):
            screen.blit(pieces_image,pixel_coord,subsection)
        else:
            screen.blit(pieces_image,pos,subsection)
    
    

def getPiece(chess_coord):
    for piece in listofWhitePieces+listofBlackPieces:
        if piece.getInfo()[0] == chess_coord:
            return piece

def getPiece2(pieceinfo):
    l = []
    for piece in listofWhitePieces+listofBlackPieces:
        if piece.pieceinfo == pieceinfo:
            l.append(piece)
    return l

def createPieces(board):

    listofWhitePieces = []
    listofBlackPieces = []

    for i in range(len(board)):
        for k in range(len(board[i])):
            if board[i][k]!=0:
                p = Piece(board[i][k],(k,i))
                if board[i][k][1]=='w':
                    listofWhitePieces.append(p)
                else:
                    listofBlackPieces.append(p)
    return [listofWhitePieces,listofBlackPieces]

def createShades(listofTuples):
    global listofShades
    listofShades = []
    if isTransition:
        return
    for tupleq in listofTuples:
        if isOccupied(board,tupleq[0],tupleq[1]):
            img = circle_image_capture
        else:
            img = circle_image_green
        shade = Shades(img,tupleq)
        listofShades.append(shade)
    if isCheck(board,'white'):
        coord = lookfor(board,'Kw')[0]
        shade = Shades(circle_image_red,coord)
        listofShades.append(shade)
    if isCheck(board,'black'):
        coord = lookfor(board,'Kb')[0]
        shade = Shades(circle_image_red,coord)
        listofShades.append(shade)
        

#########MAIN FUNCTION####################################################
#Initialize the board:
board = [ ['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'], #8
          ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'], #7
          [  0,    0,    0,    0,    0,    0,    0,    0],  #6
          [  0,    0,    0,    0,    0,    0,    0,    0],  #5
          [  0,    0,    0,    0,    0,    0,    0,    0],  #4
          [  0,    0,    0,    0,    0,    0,    0,    0],  #3
          ['Pw', 'Pw', 'Pw',  'Pw', 'Pw', 'Pw', 'Pw', 'Pw'], #2
          ['Rw', 'Nw', 'Bw',  'Qw', 'Kw', 'Bw', 'Nw', 'Rw'] ]#1
          # a      b     c     d     e     f     g     h

#In chess some data must be stored that is not apparent in the board:
player = 0 #This is the player that makes the next move. 0 is white, 1 is black
castling_rights = [True, True] #This stores whether or not each of the players are permitted to castle. 
En_Passant_Target = -1 #This variable will store a coordinate if there is a square that can be
                       #en passant captured on. Otherwise it stores -1, indicating lack of en passant
                       #targets. 
half_move_clock = 0 #This variable stores the number of reversible moves that have been played so far.

state_info = [ player, castling_rights, En_Passant_Target,
                    half_move_clock] #This variable stores the above data in one variable.
#Make the GUI:
#Start pygame
pygame.init()
#Load the screen with any arbitrary size for now:
screen = pygame.display.set_mode((600,600))

#Load all the images:
#Load the background chess board image:
background = pygame.image.load('Media\\board.png').convert()
#Load an image with all the pieces on it:
pieces_image = pygame.image.load('Media\\Chess_Pieces_Sprite.png').convert_alpha()
circle_image_green = pygame.image.load('Media\\light_green_circle4.png').convert_alpha()
circle_image_capture = pygame.image.load('Media\\light_green_circle11.png').convert_alpha()
circle_image_red = pygame.image.load('Media\\light_red_circle12.png').convert_alpha()
greenbox_image = pygame.image.load('Media\\dark_green_box.png').convert_alpha()
#Getting sizes:
#Get background size:
size_of_bg = background.get_rect().size
#Get size of the individual squares
square_width = size_of_bg[0]/8
square_height = size_of_bg[1]/8


#Rescale the images so that each piece can fit in a square:
pieces_image = pygame.transform.scale(pieces_image,
                                      (square_width*6,square_height*2))
circle_image_green = pygame.transform.scale(circle_image_green,
                                      (square_width, square_height))
circle_image_capture = pygame.transform.scale(circle_image_capture,
                                      (square_width, square_height))
circle_image_red = pygame.transform.scale(circle_image_red,
                                      (square_width, square_height))
greenbox_image = pygame.transform.scale(greenbox_image,
                                      (square_width, square_height))
#Get final sizes:
#size_of_pcsImg = pieces_image.get_rect().size
#size_of_a_piece = (size_of_pcsImg[0]/6,size_of_pcsImg[1]/2)


#Make a window of the same size as the background, set its title, and
#load the background image onto it (the board):
screen = pygame.display.set_mode(size_of_bg)
pygame.display.set_caption('Chess')
screen.blit(background,(0,0))

#Generate a list of pieces that should be drawn on the board:
listofWhitePieces,listofBlackPieces = createPieces(board)
#(the list contains references to objects of the class Piece)
listofShades = []



clock = pygame.time.Clock() #Helps controlling fps of the game.
isDown = False #Variable that shows if the mouse is being held down
               #onto a piece 
isClicked = False
isTransition = False
movingPiece=0
#Draw the pieces onto the board:
drawBoard()
######INFINITE LOOP##########################################
#Allow loop to continue till game ends
gameEnded = False
while not gameEnded:
    #print isDown
    #Check for user inputs:
    #print isDown
    for event in pygame.event.get():
        if isTransition:
            #print 'continuing'
            continue
        if event.type==QUIT:
            #Window was closed.
            gameEnded = True
        if not isDown and event.type == MOUSEBUTTONDOWN:
            #Mouse was pressed down.
            #Get the oordinates of the mouse
            pos = pygame.mouse.get_pos()
            
            chess_coord = pixel_coord_to_chess(pos)
            x = chess_coord[0]
            y = chess_coord[1]
            print "I' here"
            if not isOccupiedby(board,x,y,'wb'[player]):
                print "But not here"
                continue
            dragPiece = getPiece(chess_coord)
            listofTuples = findPossibleSquares(board,x,y,state_info)
            createShades(listofTuples)
            if ((dragPiece.pieceinfo[0]=='K') and
                (isCheck(board,'white') or isCheck(board,'black'))):
                None
            else:
                listofShades.append(Shades(greenbox_image,(x,y)))
            isDown = True       
        if (isDown or isClicked) and event.type == MOUSEBUTTONUP:
            #Mouse was released.
            isDown = False
            #Snap the piece back to its coordinate position
            #if not isTransition or not dragPiece==movingPiece:
            dragPiece.setpos((-1,-1))
            
            pos = pygame.mouse.get_pos()
            chess_coord = pixel_coord_to_chess(pos)
            x2 = chess_coord[0]
            y2 = chess_coord[1]
            isTransition = False
            if (x,y)==(x2,y2): #NO dragging occured
                #print 'alpha'
                if not isClicked: #nothing had been clicked
                    isClicked = True
                    prevPos = (x,y) #Store it so next time we know the origin
                else: #Something had been clicked previously
                    x,y = prevPos
                    if (x,y)==(x2,y2): #User clicked on the same square again.
                        #So 
                        isClicked = False
                        createShades([])
                    else:
                        #User clicked elsewhere:
                        if isOccupiedby(board,x2,y2,'wb'[player]):
                            #User clicked on a square that is our own.
                            isClicked = True
                            prevPos = (x2,y2) #Store it
                        else:
                            isClicked = False
                            isTransition = True #Possibly

            if not (x2,y2) in listofTuples:
                isTransition = False
                #createShades([])
                print 'skipped'
                continue
            
            try:
                [board,state_info] = makemove(board,state_info,x,y,x2,y2)
            except:
                print "WTF!!!!!!!"
                print x,y
                print "^THOSE WERE X AND Y COORDINATES BTW"
                raise SystemExit,0
            player = state_info[0]
            dragPiece.setcoord((x2,y2))
            if not isTransition:
                listofWhitePieces,listofBlackPieces = createPieces(board)
            else:
                print 'In transition!!'
                movingPiece = dragPiece
                origin = chess_coord_to_pixels((x,y))
                destiny = chess_coord_to_pixels((x2,y2))
                movingPiece.setpos(origin)
                step = (destiny[0]-origin[0],destiny[1]-origin[1])
                print 'step  = ',step
            
            
            createShades([])
            #drawText(board)
    if isTransition and movingPiece!=0:
        p,q = movingPiece.getpos()
        dx2,dy2 = destiny
        #print p,dx2,'above'
        #print origin,destiny,step
        n= 30.0
        if abs(p-dx2)<=abs(step[0]/n) and abs(q-dy2)<=abs(step[1]/n):
##            print p,q,dx2,dy2,'middle'
            movingPiece.setpos((-1,-1))
            listofWhitePieces,listofBlackPieces = createPieces(board)
            isTransition = False
            createShades([])
        else:
##            print p,q,dx2,dy2,'below'
##            print abs(p-dx2)
##            print abs(step[0]/n)
##            print abs(q-dy2)
##            print abs(step[1]/n)
            movingPiece.setpos((p+step[0]/n,q+step[1]/n))

    if isDown:
        #Mouse is held down and a pie
        m,k = pygame.mouse.get_pos()
        
        dragPiece.setpos((m-square_width/2,k-square_height/2))
    #Update positions of all images:
    drawBoard()
    #Update the display:
    pygame.display.update()

    #Run at specific fps:
    clock.tick(60)

#Out of loop. Quit pygame:
pygame.quit()

