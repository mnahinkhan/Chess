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
#    16/11 12:50       16/11 13:31
#    17/11 21:20       17/11 22:21
#    18/11 00:15       18/11 01:15
#    18/11 19:01       19/11 20:20
#    21/11 00:56       21/11 02:01
#    21/11 19:36       21/11 20:30
#    22/11 18:10       22/11 20:02
#    23/11 01:00       23/11 02:30
#    23/11 18:05       23/11 20:03
#    25/11 04:10       25/11 04:50
#    25/11 13:00       25/11 14:35
#    25/11 18:35       25/11 19:25
#    26/11 08:04       26/11 08:31
#

#Ensure that Pygame is installed

#GUI inspired by:
#https://en.lichess.org/

#Chess board image was taken from lichess website as well.
#The images for the pieces came from:
#https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Chess_Pieces_Sprite.svg/2000px-Chess_Pieces_Sprite.svg.png

#AI ideas from:
#https://chessprogramming.wikispaces.com/

# An online lecture that helped me understand alpha-beta pruning:
# Winston, P. [MIT OpenCourseWare]. (2010) 6. Search: Games, Minimax,
# and Alpha-Beta. [Video File]. Retrieved from https://www.youtube.com/watch?v=STjW3eH0Cik

#Special thanks to professor Saquib for being so amazing.

# This program is a chess game. The user may play against a friend or the
# computer.
#
# The game state is mainly stored as a 2D list of strings, and most of the
# processing is thus done on a list of strings.
#
# The GUI takes the current state and displays it on the screen. The GUI allows
# drag and drop movement of pieces as well as click-click movement.
#
# The AI that plays against the human evaluates all possible moves made by either
# player up to a certain level of depth. The AI evaluates each position by giving
# it a score. The higher the value of the score, the more favourable a position
# is for white and the lower the value of the score, the more favourable the
# position is for black. Knowing that white will try to get the score to be higher
# and black will try and get the score to be lower, the AI assumes best play from
# either side as it traverses up the search tree and chooses the best move to be
# played. A problem that may arise is the number of postions that need to be
# evaulated. Even at 3 levels of depth, thousands of positions have to be
# evaluatd.
# Several methods are used in this program to reduce positions that are searched:
# 1. Alpha-beta pruning: As a result of  evaluating a position it can be found
# that a portion of the search tree can be ignored as no further evaluations can
# guarantee better results. This can happen because white and black area against
# one another. White plays what is best for it and black plays what is best for it,
# so it would make sense for white to ignore any portion of the tree where black
# has a clear upperhand that it can choose to play.
# 2. Transposition table: Often, two different pathways in a search tree can result
# in the same board being evaluated. Instead of evaluating the same board several
# times, the program stores a table of values in a dictionary where the keys are
# the positions. This way, repeated positions can have their evaluations looked up
# fairly quickly, as the board state is hashed.
# 3. Opening Book - The opening book is again a dictionary that stores board
# positions often seen in the beginning few moves in chess. Appropraite moves that
# can be played at such positions is stored in the dictionary. A random move is
# selected and played from the list of suggested moves wihtout searching if the AI
# finds itself confronting a such a board postion. Note that this opening book was
# recorded by myself and so it does not have many positions stored in it.

#Note about coordinates:
#Normally, algebraic notation is used to specify a box on a chess board. In this
#program, coordinates will be index referecnes to the 2_D array that stores the
#state of the board. Thus, e4 in algebraic notation would be expressed as (4,4)
#in this program.

#Import dependencies:
import pygame #Game library
from pygame.locals import * #For useful variables
import copy #Library used to make exact copies of lists.
import pickle #Library used to store dictionaries in a text file and read them from text files.
import random #Used for making random selections
from collections import defaultdict #Used for giving dictionary values default data types.
from collections import Counter #For counting elements in a list effieciently.
import threading #To allow for AI to think simultaneously while the GUI is coloring the board.



########################################################
#Class Definitions:
#####################################################
#There are three classes used in this program:
# 1. GamePosition - This class stores a chess position. A chess position constitutes several
# features that specify the state of the game, such as the the player that has to play next,
# castling rights of the players, number of irreversible moves played so far, the positions of
# pieces on the board, etc.
# 2. Shades - This is used for GUI. A shade is a transparent colored image that is displayed on
# a specific square of the chess board, in order to show various things to the user such as
# the squares to which a piece may move, the square that is currently selected, etc. The class
# stores a reference to the image that the instance of the class should display when needed. It
# also stores the coordinates at which the shade would be applied.
# 3. Piece - This is also used for GUI. A Piece object stores the information about the image
# that a piece should display (pawn, queen, etc.) and the coordinate at which it should be
# displayed on thee chess board.
##########################################################
class GamePosition:
    def __init__(self,board,player,castling_rights,EnP_Target,HMC,history = {}):
        self.board = board #A 2D array containing information about piece postitions. Check main
        #function to see an example of such a representation.
        self.player = player #Stores the side to move. If white to play, equals 0. If black to
        #play, stores 1.
        self.castling = castling_rights #A list that contains castling rights for white and
        #black. Each castling right is a list that contains right to castle kingside and queenside.
        self.EnP = EnP_Target #Stores the coordinates of a square that can be targeted by en passant capture.
        self.HMC = HMC #Half move clock. Stores the number of irreversible moves made so far, in order to help
        #detect draw by 50 moves without any capture or pawn movement.
        self.history = history #A dictionary that stores as key a position (hashed) and the value of each of
        #these keys represents the number of times each of these positions was repeated in order for this
        #position to be reached.
        
    def getboard(self):
        return self.board
    def setboard(self,board):
        self.board = board
    def getplayer(self):
        return self.player
    def setplayer(self,player):
        self.player = player
    def getCastleRights(self):
        return self.castling
    def setCastleRights(self,castling_rights):
        self.castling = castling_rights
    def getEnP(self):
        return self.EnP
    def setEnP(self, EnP_Target):
        self.EnP = EnP_Target
    def getHMC(self):
        return self.HMC
    def setHMC(self,HMC):
        self.HMC = HMC
    def checkRepition(self):
        #Returns True if any of of the values in the history dictionary is greater than 3.
        #This would mean a position had been repeated at least thrice in order to reach the
        #current position in this game.
        return any(value>=3 for value in self.history.itervalues())
    def addtoHistory(self,position):
        #Generate a unique key out of the current position:
        key = pos2key(position)
        #Add it to the history dictionary.
        self.history[key] = self.history.get(key,0) + 1
    def gethistory(self):
        return self.history
    def clone(self):
        #This method returns another instance of the current object with exactly the same
        #parameters but independent of the current object.
        clone = GamePosition(copy.deepcopy(self.board), #Independent copy
                             self.player,
                             copy.deepcopy(self.castling), #Independent copy
                             self.EnP,
                             self.HMC)
        return clone
class Shades:
    #Self explanatory:
    def __init__(self,image,coord):
        self.image = image
        self.pos = coord
    def getInfo(self):
        return [self.image,self.pos]
class Piece:
    def __init__(self,pieceinfo,chess_coord):
        #pieceinfo is a string such as 'Qb'. The Q represents Queen and b
        #shows the fact that it is black:
        piece = pieceinfo[0]
        color = pieceinfo[1]
        #Get the information about where the image for this piece is stored
        #on the overall sprite image with all the pieces. Note that
        #square_width and square_height represent the size of a square on the
        #chess board.
        if piece=='K':
            index = 0
        elif piece=='Q':
            index = 1
        elif piece=='B':
            index = 2
        elif piece == 'N':
            index = 3
        elif piece == 'R':
            index = 4
        elif piece == 'P':
            index = 5
        left_x = square_width*index
        if color == 'w':
            left_y = 0
        else:
            left_y = square_height
        
        self.pieceinfo = pieceinfo
        #subsection defines the part of the sprite image that represents our
        #piece:
        self.subsection = (left_x,left_y,square_width,square_height)
        #There are two ways that the position of a piece is defined on the
        #board. The default one used is the chess_coord, which stores something
        #like (3,2). It represents the chess coordinate where our piece image should
        #be blitted. On the other hand, is pos does not hold the default value
        #of (-1,-1), it will hold pixel coordinates such as (420,360) that represents
        #the location in the window that the piece should be blitted on. This is
        #useful for example if our piece is transitioning from a square to another:
        self.chess_coord = chess_coord
        self.pos = (-1,-1)

    #The methods are self explanatory:
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


########################################################
#Function Definitions:
#####################################################

#The functions in this file may be classified into three main groups:
# 1. Chess Processing Functions - these are the functions that work with variables
# that hold the information about gamestate.
# 2. GUI Functions - These are the functions that work together to display the
# chess board to the user and get the user's input as well, so that they may be
# passed on to the Chess Processing Functions.
# 3. AI related functions - These are the functions involved in helping the
# computer make decisions in terms of what should be played.

#CHESS PROCESSING FUNCTIONS////////////////////
# drawText(board) - This function is not called in this program. It is useful for 
#GUI FUNCTIONS////////////////////////////////
#AI RELATED FUNCTIONS////////////////////////


#CHESS PROCESSING FUNCTIONS////////////////////
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
#GUI FUNCTIONS////////////////////////////////
#AI RELATED FUNCTIONS////////////////////////

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
def isAttackedby(position,spec_x,spec_y,color):
    #This function checks if the square specified by (x,y) coordinate is being
    #attacked by any of a specific colored set of pieces
    board = position.getboard()
    color = color[0]
    listofAttackedSquares = []
    for x in range(8):
        for y in range(8):
            if board[y][x]!=0 and board[y][x][1]==color:
                listofAttackedSquares.extend(
                    findPossibleSquares(position,x,y,True))
    return (spec_x,spec_y) in listofAttackedSquares             
def findPossibleSquares(position,x,y,AttackSearch=False):
    #This function takes as its input the current state of the chessboard, and
    #a particular x and y coordinate. It will return for the piece on that board
    #a list of possible coordinates it could move to.
    board = position.getboard()
    player = position.getplayer()
    castling_rights = position.getCastleRights()
    EnP_Target = position.getEnP()
    #HMC = position.getHMC()
    if len(board[y][x])!=2: #Unexpected, return empty list.
        return [] 
    piece = board[y][x][0] #Pawn, rook, etc.
    color = board[y][x][1] #w or b.
    #Have the complimentary color stored for convenience:
    enemy_color = opp(color)
    
    listofTuples = [] #Holds list
    
    if piece == 'P': #The piece is a pawn.
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
            if EnP_Target!=-1: #There is a possible en pasant target:
                if EnP_Target == (x-1,y-1) or EnP_Target == (x+1,y-1):
                    #We're at the correct location to potentially perform en
                    #passant:
                    listofTuples.append(EnP_Target)
            
        elif color=='b': #The piece is black, same as above but opposite side.
            if not isOccupied(board,x,y+1) and not AttackSearch:
                listofTuples.append((x,y+1))
                if y == 1 and not isOccupied(board,x,y+2):
                    listofTuples.append((x,y+2))
            if x!=0 and isOccupiedby(board,x-1,y+1,'white'):
                listofTuples.append((x-1,y+1))
            if x!=7 and isOccupiedby(board,x+1,y+1,'white'):
                listofTuples.append((x+1,y+1))
            if EnP_Target == (x-1,y+1) or EnP_Target == (x+1,y+1):
                listofTuples.append(EnP_Target)

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
        list_rook = findPossibleSquares(position,x,y,True)
        #Temporarily pretend there is a bishop:
        board[y][x] = 'B' + color
        list_bishop = findPossibleSquares(position,x,y,True)
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
            #Kings can potentially castle:
            right = castling_rights[player]
            #Kingside
            if (right[0] and #has right to castle
            board[y][7]!=0 and #The rook square is not empty
            board[y][7][0]=='R' and #There is a rook at the appropriate place
            not isOccupied(board,x+1,y) and #The square on its right is empty
            not isOccupied(board,x+2,y) and #The second square beyond is also empty
            not isAttackedby(position,x,y,enemy_color) and #The king isn't under atack
            not isAttackedby(position,x+1,y,enemy_color) and #Or the path through which
            not isAttackedby(position,x+2,y,enemy_color)):#it will move
                listofTuples.append((x+2,y))
            #Queenside
            if (right[1] and #has right to castle
            board[y][0]!=0 and #The rook square is not empty
            board[y][0][0]=='R' and #The rook square is not empty
            not isOccupied(board,x-1,y)and #The square on its left is empty
            not isOccupied(board,x-2,y)and #The second square beyond is also empty
            not isOccupied(board,x-3,y) and #And the one beyond.
            not isAttackedby(position,x,y,enemy_color) and #The king isn't under atack
            not isAttackedby(position,x-1,y,enemy_color) and #Or the path through which
            not isAttackedby(position,x-2,y,enemy_color)):#it will move
                listofTuples.append((x-2,y)) #Let castling be an option.

    #Make sure the king is not under attack as a result of this move:
    if not AttackSearch:
        new_list = []
        for tupleq in listofTuples:
            x2 = tupleq[0]
            y2 = tupleq[1]
            temp_pos = position.clone()
            makemove(temp_pos,x,y,x2,y2)
            if not isCheck(temp_pos,color):
                new_list.append(tupleq)
        listofTuples = new_list
    return listofTuples

def makemove(position,x,y,x2,y2):
    #This function makes a move on the board and
    #returns the resultant board and game state.
    #Get piece and color of the one being moved:
    board = position.getboard()
    piece = board[y][x][0]
    color = board[y][x][1]
    #Get the individual game components:
    player = position.getplayer()
    castling_rights = position.getCastleRights()
    EnP_Target = position.getEnP()
    half_move_clock = position.getHMC()

    if isOccupied(board,x2,y2) or piece=='P':
        half_move_clock = 0
    else:
        half_move_clock += 1


    #Make the move:
    board[y2][x2] = board[y][x]
    board[y][x] = 0
    
    #Special piece requirements:
    #King:
    if piece == 'K':
        #Ensure that since a King is moved, the castling
        #rights are lost:
        castling_rights[player] = [False,False]
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
    if piece=='R':
        #The rook moved. Castling right for this rook must be removed.
        if x==0 and y==0:
            #Black queenside
            castling_rights[1][1] = False
        elif x==7 and y==0:
            #Black kingside
            castling_rights[1][0] = False
        elif x==0 and y==7:
            #White queenside
            castling_rights[0][1] = False
        elif x==7 and y==7:
            #White kingside
            castling_rights[0][0] = False
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
    #half_move_clock = half_move_clock + 1
    
    #Pack it back into one variable:       
    position.setplayer(player)
    position.setCastleRights(castling_rights)
    position.setEnP(EnP_Target)
    position.setHMC(half_move_clock)

def opp(color):
    color = color[0]
    if color == 'w':
        oppcolor = 'b'
    else:
        oppcolor = 'w'
    return oppcolor
def isCheck(position,color):
    #This function takes a board as its input and checks if the King of the
    #specified color is under attack.
    board = position.getboard()
    color = color[0]
    enemy = opp(color)
    piece = 'K' + color
    x,y = lookfor(board,piece)[0]

    return isAttackedby(position,x,y,enemy)

def isCheckmate(position,color=-1):
    #This function tells you if a position is a checkmate. Color is an
    #optional argument that may be passed to specifically check for mate
    #against a specific color.
    if color==-1:
        return isCheckmate(position,'white') or isCheckmate(position,'b')
    color = color[0]
    if isCheck(position,color) and allMoves(position,color)==[]:
            return True
    return False
def isStalemate(position):
    player = position.getplayer()
    if player==0:
        color = 'w'
    else:
        color = 'b'
    if not isCheck(position,color) and allMoves(position,color)==[]:
        return True
    return False
    

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


def chess_coord_to_pixels(chess_coord):
    #This function takes as input a chess coordinate such as (4,7) and
    #the size of the image of a chess piece. It returns the top left
    #corner pixel at which a piece of the given size should be placed
    #on the board for it to appear at the correct square.
    x,y = chess_coord
    if isAI:
        if AIPlayer==0:
            return ((7-x)*square_width, (7-y)*square_height)
        else:
            return (x*square_width, y*square_height)
    
    if not isFlip or player==0 ^ isTransition:
        return (x*square_width, y*square_height)
    else:
        return ((7-x)*square_width, (7-y)*square_height)

def pixel_coord_to_chess(pixel_coord):
    x,y = pixel_coord[0]/square_width, pixel_coord[1]/square_height
    if isAI:
        if AIPlayer==0:
            return (7-x,7-y)
        else:
            return (x,y)
    if not isFlip or player==0 ^ isTransition:
        return (x,y)
    else:
        return (7-x,7-y)

def drawBoard():
    screen.blit(background,(0,0))
    if player==1:
        order = [listofWhitePieces,listofBlackPieces]
    else:
        order = [listofBlackPieces,listofWhitePieces]
    if isTransition:
        order = list(reversed(order))
    if isDraw or chessEnded or isAIThink:
        #Shades
        for shade in listofShades:
            img,chess_coord = shade.getInfo()
            pixel_coord = chess_coord_to_pixels(chess_coord)
            screen.blit(img,pixel_coord)
    if prevMove[0]!=-1 and not isTransition:
        x,y,x2,y2 = prevMove
        screen.blit(yellowbox_image,chess_coord_to_pixels((x,y)))
        screen.blit(yellowbox_image,chess_coord_to_pixels((x2,y2)))
    #Pieces
    for piece in order[0]:
        
        chess_coord,subsection,pos = piece.getInfo()
        pixel_coord = chess_coord_to_pixels(chess_coord)
        if pos==(-1,-1):
            screen.blit(pieces_image,pixel_coord,subsection)
        else:
            screen.blit(pieces_image,pos,subsection)
    #Shades
    if not (isDraw or chessEnded or isAIThink):
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
    if isDraw:
        coord = lookfor(board,'Kw')[0]
        shade = Shades(circle_image_yellow,coord)
        listofShades.append(shade)
        coord = lookfor(board,'Kb')[0]
        shade = Shades(circle_image_yellow,coord)
        listofShades.append(shade)
        return
    if chessEnded:
        coord = lookfor(board,'K'+winner)[0]
        shade = Shades(circle_image_green_big,coord)
        listofShades.append(shade)
    if isCheck(position,'white'):
        coord = lookfor(board,'Kw')[0]
        shade = Shades(circle_image_red,coord)
        listofShades.append(shade)
    if isCheck(position,'black'):
        coord = lookfor(board,'Kb')[0]
        shade = Shades(circle_image_red,coord)
        listofShades.append(shade)
    #ACTUALLY DRAW
    for tupleq in listofTuples:
        if isOccupied(board,tupleq[0],tupleq[1]):
            img = circle_image_capture
        else:
            img = circle_image_green
        shade = Shades(img,tupleq)
        listofShades.append(shade)
    



def getallpieces(position,color):
    #This functin returns a list of postions of all the pieces on the
    #board of a particular color.
    board = position.getboard()
    listofpos = []
    for j in range(8):
        for i in range(8):
            if isOccupiedby(board,i,j,color):
                listofpos.append((i,j))
    return listofpos
def allMoves(position, color):
    if color==1:
        color = 'white'
    elif color ==-1:
        color = 'black'
    color = color[0]

    listofpieces = getallpieces(position,color)
    moves = []
    for pos in listofpieces:

        targets = findPossibleSquares(position,pos[0],pos[1])

        for target in targets:
             moves.append([pos,target])
    return moves

def negamax(position,depth,alpha,beta,colorsign,bestMoveReturn,root=True):
    if root:
        key = pos2key(position)
        if key in openings:
            bestMoveReturn[:] = random.choice(openings[key])
            return
    global searched
    if depth==0:
        return colorsign*evaluate(position)
    moves = allMoves(position, colorsign)
    if root:
        bestMove = moves[0]
    bestValue = -100000
    for move in moves:
        newpos = position.clone()
        makemove(newpos,move[0][0],move[0][1],move[1][0],move[1][1])
        key = pos2key(newpos)
        if key in searched:
            value = searched[key]
        else:
            value = -negamax(newpos,depth-1, -beta,-alpha,-colorsign,[],False)
            searched[key] = value
        if value>bestValue:
            bestValue = value
            
            if root:
                bestMove = move
        alpha = max(alpha,value)
        if alpha>=beta:
            break
    if root:
        searched = {}
        bestMoveReturn[:] = bestMove
        return
    return bestValue

def evaluate(position):
    #This function evaluates a position based on the point of view of
    #white.
    if isCheckmate(position,'white'):
        Kw = 0
    else:
        Kw = 1
    if isCheckmate(position,'black'):
        Kb = 0
    else:
        Kb = 1
    board = position.getboard()
    flatboard = [x for row in board for x in row]
    c = Counter(flatboard)
    Qw = c['Qw']
    Qb = c['Qb']
    Rw = c['Rw']
    Rb = c['Rb']
    Bw = c['Bw']
    Bb = c['Bb']
    Nw = c['Nw']
    Nb = c['Nb']
    Pw = c['Pw']
    Pb = c['Pb']
    whiteMaterial = 9*Qw + 5*Rw + 3*Nw + 3*Bw + 1*Pw
    blackMaterial = 9*Qb + 5*Rb + 3*Nb + 3*Bb + 1*Pb
    numofmoves = len(position.gethistory())
    gamephase = 'opening'
    if numofmoves>40 or (whiteMaterial<14 and blackMaterial<14):
        gamephase = 'ending'
    Dw = doubledPawns(board,'white')
    Db = doubledPawns(board,'black')
    Sw = blockedPawns(board,'white')
    Sb = blockedPawns(board,'black')
    Iw = isolatedPawns(board,'white')
    Ib = isolatedPawns(board,'black')
    evaluation = 20000*(Kw-Kb) + 900*(Qw - Qb) + 500*(Rw - Rb) +330*(Bw-Bb
                )+320*(Nw - Nb) +100*(Pw - Pb) +-30*(Dw-Db + Sw-Sb + Iw- Ib
                )
    evaluation2 = pieceSquareTable(flatboard,gamephase)
    evaluation = evaluation + evaluation2
    return evaluation


def pieceSquareTable(flatboard,gamephase):
    score = 0
    for i in range(64):
        if flatboard[i]==0:
            continue
        piece = flatboard[i][0]
        color = flatboard[i][1]
        sign = +1
        if color=='b':
            i = (7-i/8)*8 + i%8
            sign = -1
        if piece=='P':
            score += sign*pawn_table[i]
        elif piece=='N':
            score+= sign*knight_table[i]
        elif piece=='B':
            score+=sign*bishop_table[i]
        elif piece=='R':
            score+=sign*rook_table[i]
        elif piece=='Q':
            score+=sign*queen_table[i]
        elif piece=='K':
            if gamephase=='opening':
                score+=sign*king_table[i]
            else:
                score+=sign*king_endgame_table[i]
    return score

    
def doubledPawns(board,color):
    #This function counts the number of doubled pawns for a player.
    color = color[0]
    listofpawns = lookfor(board,'P'+color)
    repeats = 0
    temp = []
    for pawnpos in listofpawns:
        if pawnpos[0] in temp:
            repeats = repeats + 1
        else:
            temp.append(pawnpos[0])
    return repeats
def blockedPawns(board,color):
    #This function counts the number of blocekd pawns for a player.
    color = color[0]
    listofpawns = lookfor(board,'P'+color)
    blocked = 0
    for pawnpos in listofpawns:
        if ((color=='w' and isOccupiedby(board,pawnpos[0],pawnpos[1]-1,
                                       'black'))
            or (color=='b' and isOccupiedby(board,pawnpos[0],pawnpos[1]+1,
                                       'white'))):
            blocked = blocked + 1
    return blocked
def isolatedPawns(board,color):
    #This function counts the number of isolated pawns for a player.
    color = color[0]
    listofpawns = lookfor(board,'P'+color)
    xlist = [x for (x,y) in listofpawns]
    isolated = 0
    for x in xlist:
        if x!=0 and x!=7:
            if x-1 not in xlist and x+1 not in xlist:
                isolated+=1
        elif x==0 and 1 not in xlist:
            isolated+=1
        elif x==7 and 6 not in xlist:
            isolated+=1
    return isolated
        
def pos2key(position):
    board = position.getboard()
    boardTuple = []
    for row in board:
        boardTuple.append(tuple(row))
    boardTuple = tuple(boardTuple)
    rights = position.getCastleRights()
    tuplerights = (tuple(rights[0]),tuple(rights[1]))
    key = (boardTuple,position.getplayer(),
           tuplerights)
    return key


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
castling_rights = [[True, True],[True, True]]
#The above stores whether or not each of the players are permitted to castle on
#either side of the king. (Kingside, Queenside)
En_Passant_Target = -1 #This variable will store a coordinate if there is a square that can be
                       #en passant captured on. Otherwise it stores -1, indicating lack of en passant
                       #targets. 
half_move_clock = 0 #This variable stores the number of reversible moves that have been played so far.

position = GamePosition(board,player,castling_rights,En_Passant_Target
                        ,half_move_clock)
pawn_table = [  0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 30, 30, 20, 10, 10,
 5,  5, 10, 25, 25, 10,  5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5, -5,-10,  0,  0,-10, -5,  5,
 5, 10, 10,-20,-20, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]
knight_table = [-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-90,-30,-30,-30,-30,-90,-50]
bishop_table = [-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-90,-10,-10,-90,-10,-20]
rook_table = [0,  0,  0,  0,  0,  0,  0,  0,
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  0,  0,  5,  5,  0,  0,  0]
queen_table = [-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, 70, -5,-10,-10,-20]
king_table = [-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-20,-30,-30,-40,-40,-30,-30,-20,
-10,-20,-20,-20,-20,-20,-20,-10,
 20, 20,  0,  0,  0,  0, 20, 20,
 20, 30, 10,  0,  0, 10, 30, 20]
king_endgame_table = [-50,-40,-30,-20,-20,-30,-40,-50,
-30,-20,-10,  0,  0,-10,-20,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-30,  0,  0,  0,  0,-30,-30,
-50,-30,-30,-30,-30,-30,-30,-50]

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
circle_image_green = pygame.image.load('Media\\green_circle_small.png').convert_alpha()
circle_image_capture = pygame.image.load('Media\\green_circle_neg.png').convert_alpha()
circle_image_red = pygame.image.load('Media\\red_circle_big.png').convert_alpha()
greenbox_image = pygame.image.load('Media\\green_box.png').convert_alpha()
circle_image_yellow = pygame.image.load('Media\\yellow_circle_big.png').convert_alpha()
circle_image_green_big = pygame.image.load('Media\\green_circle_big.png').convert_alpha()
yellowbox_image = pygame.image.load('Media\\yellow_box.png').convert_alpha()
#Menu pictures:
withfriend_pic = pygame.image.load('Media\\withfriend.png').convert_alpha()
withAI_pic = pygame.image.load('Media\\withAI.png').convert_alpha()
playwhite_pic = pygame.image.load('Media\\playWhite.png').convert_alpha()
playblack_pic = pygame.image.load('Media\\playBlack.png').convert_alpha()
flipEnabled_pic = pygame.image.load('Media\\flipEnabled.png').convert_alpha()
flipDisabled_pic = pygame.image.load('Media\\flipDisabled.png').convert_alpha()

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
yellowbox_image = pygame.transform.scale(yellowbox_image,
                                      (square_width, square_height))
circle_image_yellow = pygame.transform.scale(circle_image_yellow,
                                             (square_width, square_height))
circle_image_green_big = pygame.transform.scale(circle_image_green_big,
                                             (square_width, square_height))
withfriend_pic = pygame.transform.scale(withfriend_pic,
                                      (square_width*4,square_height*4))
withAI_pic = pygame.transform.scale(withAI_pic,
                                      (square_width*4,square_height*4))
playwhite_pic = pygame.transform.scale(playwhite_pic,
                                      (square_width*4,square_height*4))
playblack_pic = pygame.transform.scale(playblack_pic,
                                      (square_width*4,square_height*4))
flipEnabled_pic = pygame.transform.scale(flipEnabled_pic,
                                      (square_width*4,square_height*4))
flipDisabled_pic = pygame.transform.scale(flipDisabled_pic,
                                      (square_width*4,square_height*4))



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
isDraw = False
chessEnded = False
isRecord = False
isAIThink = False
openings = defaultdict(list)
try:
    file_handle = open('openingTable.txt','r+')
    openings = pickle.loads(file_handle.read())
except:
    file_handle = open('openingTable.txt','w')
searched = {}
######INFINITE LOOP##########################################
#Allow loop to continue till game ends
gameEnded = False
ax,ay=0,0
numm = 0
isMenu = True
isAI = -1
isFlip = -1
AIPlayer = -1
prevMove = [-1,-1,-1,-1]
while not gameEnded:
    if isMenu:
        #Menu Stuff
        screen.blit(background,(0,0))
        if isAI==-1:
            #The user has not selected between playing against the AI
            #or playing against a friend.
            screen.blit(withfriend_pic,(0,square_height*2))
            screen.blit(withAI_pic,(square_width*4,square_height*2))
        elif isAI==True:
            screen.blit(playwhite_pic,(0,square_height*2))
            screen.blit(playblack_pic,(square_width*4,square_height*2))
        elif isAI==False:
            screen.blit(flipDisabled_pic,(0,square_height*2))
            screen.blit(flipEnabled_pic,(square_width*4,square_height*2))
        if isFlip!=-1:
            #All settings have already been specified.
            drawBoard()
            isMenu = False
            if isAI and AIPlayer==0:
                colorsign=1
                bestMoveReturn = []
                move_thread = threading.Thread(target = negamax,
                            args = (position,3,-1000000,1000000,colorsign,bestMoveReturn))
                move_thread.start()
                isAIThink = True
            continue
        for event in pygame.event.get():
            if event.type==QUIT:
                #Window was closed.
                gameEnded = True
                break
            if event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if (pos[0]<square_width*4 and
                pos[1]>square_height*2 and
                pos[1]<square_height*6):
                    #LEFT SIDE CLICKED
                    if isAI == -1:
                        isAI = False
                    elif isAI==True:
                        AIPlayer = 1
                        isFlip = False
                    elif isAI==False:
                        isFlip = False
                elif (pos[0]>square_width*4 and
                pos[1]>square_height*2 and
                pos[1]<square_height*6):
                    #RIGHT SIDE CLICKED
                    if isAI == -1:
                        isAI = True
                    elif isAI==True:
                        AIPlayer = 0
                        isFlip = False
                    elif isAI==False:
                        isFlip=True

        #Update the display:
        pygame.display.update()

        #Run at specific fps:
        clock.tick(60)
        continue
    numm+=1
    if isAIThink and numm%6==0:
        ax+=1
        if ax==8:
            ay+=1
            ax=0
        if ay==8:
            ax,ay=0,0
        if ax%4==0:
            createShades([])
        if AIPlayer==0:
            listofShades.append(Shades(greenbox_image,(7-ax,7-ay)))
        else:
            listofShades.append(Shades(greenbox_image,(ax,ay)))
        
    for event in pygame.event.get():
        
        if event.type==QUIT:
            #Window was closed.
            gameEnded = True
        
            break
        if chessEnded or isTransition or isAIThink:
            continue
        
        if not isDown and event.type == MOUSEBUTTONDOWN:
            #Mouse was pressed down.
            #Get the oordinates of the mouse
            pos = pygame.mouse.get_pos()
            
            chess_coord = pixel_coord_to_chess(pos)
            x = chess_coord[0]
            y = chess_coord[1]
            if not isOccupiedby(board,x,y,'wb'[player]):
                continue
            dragPiece = getPiece(chess_coord)
            listofTuples = findPossibleSquares(position,x,y)
            createShades(listofTuples)
            if ((dragPiece.pieceinfo[0]=='K') and
                (isCheck(position,'white') or isCheck(position,'black'))):
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
                            #User clicked on a square that is occupied by their
                            #own piece
                            isClicked = True
                            prevPos = (x2,y2) #Store it
                        else:
                            isClicked = False
                            createShades([])#FI this shit
                            isTransition = True #Possibly
                            

            if not (x2,y2) in listofTuples:
                isTransition = False
                continue
            
            if isRecord:
                key = pos2key(position)
                if [(x,y),(x2,y2)] not in openings[key]: 
                    openings[key].append([(x,y),(x2,y2)])
                

            makemove(position,x,y,x2,y2)
            prevMove = [x,y,x2,y2]
            
            player = position.getplayer()
            HMC = position.getHMC()
            position.addtoHistory(position)
            if HMC>=100 or isStalemate(position) or position.checkRepition():
                #There is a draw:
                isDraw = True
                chessEnded = True
            if isCheckmate(position,'white'):
                winner = 'b'
                chessEnded = True
            if isCheckmate(position,'black'):
                winner = 'w'
                chessEnded = True
            if isAI and not chessEnded:
                if player==0:
                    colorsign = 1
                else:
                    colorsign = -1
                bestMoveReturn = []
                move_thread = threading.Thread(target = negamax,
                            args = (position,3,-1000000,1000000,colorsign,bestMoveReturn))
                move_thread.start()
                isAIThink = True
        
            dragPiece.setcoord((x2,y2))
            if not isTransition:
                listofWhitePieces,listofBlackPieces = createPieces(board)
            else:
                movingPiece = dragPiece
                origin = chess_coord_to_pixels((x,y))
                destiny = chess_coord_to_pixels((x2,y2))
                movingPiece.setpos(origin)
                step = (destiny[0]-origin[0],destiny[1]-origin[1])
            
            
            createShades([])
    if isTransition:
        p,q = movingPiece.getpos()
        dx2,dy2 = destiny
        n= 30.0
        if abs(p-dx2)<=abs(step[0]/n) and abs(q-dy2)<=abs(step[1]/n):
            movingPiece.setpos((-1,-1))
            listofWhitePieces,listofBlackPieces = createPieces(board)
            isTransition = False
            createShades([])
        else:
            movingPiece.setpos((p+step[0]/n,q+step[1]/n))

    if isDown:
        #Mouse is held down and a pie
        m,k = pygame.mouse.get_pos()
        
        dragPiece.setpos((m-square_width/2,k-square_height/2))
    if isAIThink and not isTransition:
        if not move_thread.isAlive():
            isAIThink = False
            createShades([])
            ax,ay=0,0
            [x,y],[x2,y2] = bestMoveReturn
            makemove(position,x,y,x2,y2)
            prevMove = [x,y,x2,y2]
            player = position.getplayer()
            HMC = position.getHMC()
            position.addtoHistory(position)
            if HMC>=100 or isStalemate(position) or position.checkRepition():
                #There is a draw:
                isDraw = True
                chessEnded = True
            if isCheckmate(position,'white'):
                winner = 'b'
                chessEnded = True
            if isCheckmate(position,'black'):
                winner = 'w'
                chessEnded = True
            isTransition = True
            movingPiece = getPiece((x,y))
            origin = chess_coord_to_pixels((x,y))
            destiny = chess_coord_to_pixels((x2,y2))
            movingPiece.setpos(origin)
            step = (destiny[0]-origin[0],destiny[1]-origin[1])
    #Update positions of all images:
    drawBoard()
    #Update the display:
    pygame.display.update()

    #Run at specific fps:
    clock.tick(60)

#Out of loop. Quit pygame:
pygame.quit()
if isRecord:
    file_handle.seek(0)
    pickle.dump(openings,file_handle)
    file_handle.truncate()
    file_handle.close()

