import pygame


pygame.init()
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
size = (700, 700)


class Square(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       self.color = color

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([60, 60])
       self.image.fill(self.color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       
       self.rect = self.image.get_rect()
       self.orig_color = color
       self.pos = [(self.rect.x - 40)/60, (self.rect.y-40)/60]
       self.occupied_color = -1
       
    def update(self, color):
        self.image = pygame.Surface([60, 60])
        if color == -1:
            self.image.fill(self.orig_color)
            self.color = self.orig_color
        else:
            self.image.fill(color)
            self.color = color
        
       
def select_image_file(team, form):
    filename = "Sprites/"
    if(team == 0):
        filename += "white"
    elif(team == 1):
        filename += "black"

    if (form == "K"):
        filename += "King"
    elif(form == "Q"):
        filename += "Queen"
    elif(form == "R"):
        filename += "Rook"
    elif(form == "B"):
        filename += "Bishop"
    elif(form == "N"):
        filename += "Knight"
    elif(form == "P"):
        filename += "Pawn"
    filename += ".png"      
    return filename;
        
        
class Piece(pygame.sprite.Sprite):
    #team is 0 or 1, for white or black
    #form is K, Q, R, B, N, P
    def __init__(self, team, form):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(select_image_file(team, form)).convert_alpha()
        self.rect = self.image.get_rect()
        self.name = select_image_file(team,form)[8:-4]
        self.team = team
        self.form = form
        self.loc = [(self.rect.x - 40)/60, (self.rect.y-40)/60]
        self.has_moved = False


#returns an list of positions a piece can move. A return to me hating my life.       
def can_move(piece, square_list):
    possible_locs = []
    cur_loc = piece.loc
    
    if(piece.form == "K"):
        for i in range(-1,2):
            for j in range(-1,2):
                loc = [(cur_loc[0]+ i), (cur_loc[1] +j)]
                possible_locs.append(loc)
                
    #queen is basically a combination of a bunch of different pieces
    if(piece.form == "Q"):
        #king
        for i in range(-1,2):
            for j in range(-1,1):
                loc = [cur_loc[0]+ i, cur_loc[1] +j]
                possible_locs.append(loc)
        #rook - remeber that we kick out positions that are out of range at the end
        for i in range(-8, 8): #either x or y can change, but not both.
            loc1 = [cur_loc[0]+ i, cur_loc[1]]
            loc2 = [cur_loc[0], cur_loc[1] +i]
            possible_locs.append(loc1)
            possible_locs.append(loc2)
        #bishop
        for i in range(-8,8):
            loc1 = [cur_loc[0]+ i, cur_loc[1]+i]
            loc2 = [cur_loc[0]+ i, cur_loc[1]-i]
            possible_locs.append(loc1)
            possible_locs.append(loc2)
    if(piece.form == "R"):
        for i in range(-8, 8): #either x or y can change, but not both.
            loc1 = [cur_loc[0]+ i, cur_loc[1]]
            loc2 = [cur_loc[0], cur_loc[1] +i]
            possible_locs.append(loc1)
            possible_locs.append(loc2)
    if(piece.form == "B"):
        for i in range(-8, 8): #Both x and y must change
            loc1 = [cur_loc[0]+ i, cur_loc[1]+i]
            loc2 = [cur_loc[0]+i, cur_loc[1] -i]
            possible_locs.append(loc1)
            possible_locs.append(loc2)

    if(piece.form == "N"):
        for i in range(-1, 2):
            for j in range(-1, 2):
                loc = [cur_loc[0] + (i*2), cur_loc[1]+(j*2)]
                possible_locs.append(loc)
    if(piece.form == "P"):
        if(piece.team == 0):
            if(not piece.has_moved):
                poss_loc1 = [cur_loc[0], cur_loc[1] -1]
                poss_loc2 = [cur_loc[0], cur_loc[1] -2]
                possible_locs.append(poss_loc1)
                possible_locs.append(poss_loc2)
            elif(piece.has_moved):
                poss_loc1 = [cur_loc[0], cur_loc[1] -1]
                possible_locs.append(poss_loc1)
        elif(piece.team == 1):
            if(not piece.has_moved):
                poss_loc1 = [cur_loc[0], cur_loc[1] +1]
                poss_loc2 = [cur_loc[0], cur_loc[1] +2]
                possible_locs.append(poss_loc1)
                possible_locs.append(poss_loc2)
            elif(piece.has_moved):
                poss_loc1 = [cur_loc[0], cur_loc[1] +1]
                possible_locs.append(poss_loc1)

         
    possible_locs = set(tuple(i) for i in possible_locs) #removes duplicates
    to_remove = [cur_loc]
    #remove locations that are invalid
    for loc in possible_locs:
        if(loc[0] < 0 or loc[1] < 0):
            to_remove.append(loc)
        elif (loc[0] > 7 or loc[1] > 7):
                to_remove.append(loc)

    to_remove = set(tuple(i) for i in to_remove)
    possible_locs = list(possible_locs - to_remove)
    
    to_remove = []
    #remove locations that are occupied by that teams own pieces
    for loc in possible_locs:
        if(square_list[loc[0]][loc[1]].occupied_color == piece.team):
            to_remove.append(loc);
    
    possible_locs = set(tuple(i) for i in possible_locs)
    to_remove = set(tuple(i) for i in to_remove)
    possible_locs = list(possible_locs - to_remove)
    
    #remove locations that would require hopping over other pieces
        
    
    return possible_locs
    
    

# Open a new window
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chess!")

running = True;
clock = pygame.time.Clock()

#init the chess board as an empty 8x8 2d array
board = [[""]*8 for i in range(8)]
all_squares = pygame.sprite.Group()

#set locations for all board square sprites
board_locs = [[[0 for k in xrange(2)] for j in xrange(8)] for i in xrange(8)]


for i in range(8):
    for j in range(8):
        board_locs[i][j][0] = (i*60) + 40
        board_locs[i][j][1] = (j*60) + 40

#create sprites for board squares
cur_color = RED
square_list = [[0 for i in xrange(8)] for j in xrange(8)]
color_change_cnt = 0
for i in range(8):
    if (cur_color == WHITE):
        cur_color = RED

    elif(cur_color == RED):
        cur_color = WHITE
    for j in range(8):
        square_list[i][j] = Square(cur_color)
        square_list[i][j].rect.x = board_locs[i][j][0]
        square_list[i][j].rect.y = board_locs[i][j][1]
        all_squares.add(square_list[i][j])
        
        if (cur_color == WHITE):
            cur_color = RED

        elif(cur_color == RED):
            cur_color = WHITE
            
#create sprites for pieces, and set starting positions
pieces = pygame.sprite.Group()
#Here is where hate my life...
#set starting squares to occupied
for i in range(8):
    for j in range(6,8): 
        square_list[i][j].occupied_color = 0
    for j in range(2): #black
        square_list[i][j].occupied_color = 1
        
white_pawn1 =  Piece(0, "P")
white_pawn1.rect.x = board_locs[0][6][0]
white_pawn1.rect.y = board_locs[0][6][1]
pieces.add(white_pawn1)

white_pawn2 =  Piece(0, "P")
white_pawn2.rect.x = board_locs[1][6][0]
white_pawn2.rect.y = board_locs[1][6][1]
pieces.add(white_pawn2)

white_pawn3 =  Piece(0, "P")
white_pawn3.rect.x = board_locs[2][6][0]
white_pawn3.rect.y = board_locs[2][6][1]
pieces.add(white_pawn3)

white_pawn4 =  Piece(0, "P")
white_pawn4.rect.x = board_locs[3][6][0]
white_pawn4.rect.y = board_locs[3][6][1]
pieces.add(white_pawn4)   

white_pawn5 =  Piece(0, "P")
white_pawn5.rect.x = board_locs[4][6][0]
white_pawn5.rect.y = board_locs[4][6][1]
pieces.add(white_pawn5)

white_pawn6 =  Piece(0, "P")
white_pawn6.rect.x = board_locs[5][6][0]
white_pawn6.rect.y = board_locs[5][6][1]
pieces.add(white_pawn6)             

white_pawn7 =  Piece(0, "P")
white_pawn7.rect.x = board_locs[6][6][0]
white_pawn7.rect.y = board_locs[6][6][1]
pieces.add(white_pawn7)     

white_pawn8 =  Piece(0, "P")
white_pawn8.rect.x = board_locs[7][6][0]
white_pawn8.rect.y = board_locs[7][6][1]
pieces.add(white_pawn8)    

white_rook1 = Piece(0, "R") 
white_rook1.rect.x = board_locs[0][7][0]
white_rook1.rect.y = board_locs[0][7][1]
pieces.add(white_rook1)

white_knight1 = Piece(0, "N")
white_knight1.rect.x = board_locs[1][7][0]
white_knight1.rect.y = board_locs[1][7][1]
pieces.add(white_knight1);

white_bishop1 = Piece(0, "B")
white_bishop1.rect.x = board_locs[2][7][0]
white_bishop1.rect.y = board_locs[2][7][1]
pieces.add(white_bishop1)


white_queen = Piece(0, "Q")
white_queen.rect.x = board_locs[3][7][0]
white_queen.rect.y = board_locs[3][7][1]
pieces.add(white_queen)

white_king = Piece(0, "K")
white_king.rect.x = board_locs[4][7][0]
white_king.rect.y = board_locs[4][7][1]
pieces.add(white_king)

white_bishop2 = Piece(0, "B")
white_bishop2.rect.x = board_locs[5][7][0]
white_bishop2.rect.y = board_locs[5][7][1]
pieces.add(white_bishop2)

white_knight2 = Piece(0, "N")
white_knight2.rect.x = board_locs[6][7][0]
white_knight2.rect.y = board_locs[6][7][1]
pieces.add(white_knight2);

white_rook2 = Piece(0, "R") 
white_rook2.rect.x = board_locs[7][7][0]
white_rook2.rect.y = board_locs[7][7][1]
pieces.add(white_rook2)

#black now
black_pawn1 =  Piece(1, "P")
black_pawn1.rect.x = board_locs[0][1][0]
black_pawn1.rect.y = board_locs[0][1][1]
pieces.add(black_pawn1)

black_pawn2 =  Piece(1, "P")
black_pawn2.rect.x = board_locs[1][1][0]
black_pawn2.rect.y = board_locs[1][1][1]
pieces.add(black_pawn2)

black_pawn3 =  Piece(1, "P")
black_pawn3.rect.x = board_locs[2][1][0]
black_pawn3.rect.y = board_locs[2][1][1]
pieces.add(black_pawn3)

black_pawn4 =  Piece(1, "P")
black_pawn4.rect.x = board_locs[3][1][0]
black_pawn4.rect.y = board_locs[3][1][1]
pieces.add(black_pawn4)   

black_pawn5 =  Piece(1, "P")
black_pawn5.rect.x = board_locs[4][1][0]
black_pawn5.rect.y = board_locs[4][1][1]
pieces.add(black_pawn5)

black_pawn6 =  Piece(1, "P")
black_pawn6.rect.x = board_locs[5][1][0]
black_pawn6.rect.y = board_locs[5][1][1]
pieces.add(black_pawn6)             

black_pawn7 =  Piece(1, "P")
black_pawn7.rect.x = board_locs[6][1][0]
black_pawn7.rect.y = board_locs[6][1][1]
pieces.add(black_pawn7)     

black_pawn8 =  Piece(1, "P")
black_pawn8.rect.x = board_locs[7][1][0]
black_pawn8.rect.y = board_locs[7][1][1]
pieces.add(black_pawn8)    

black_rook1 = Piece(1, "R") 
black_rook1.rect.x = board_locs[0][0][0]
black_rook1.rect.y = board_locs[0][0][1]
pieces.add(black_rook1)

black_knight1 = Piece(1, "N")
black_knight1.rect.x = board_locs[1][0][0]
black_knight1.rect.y = board_locs[1][0][1]
pieces.add(black_knight1);

black_bishop1 = Piece(1, "B")
black_bishop1.rect.x = board_locs[2][0][0]
black_bishop1.rect.y = board_locs[2][0][1]
pieces.add(black_bishop1)


black_queen = Piece(1, "Q")
black_queen.rect.x = board_locs[3][0][0]
black_queen.rect.y = board_locs[3][0][1]
pieces.add(black_queen)

black_king = Piece(1, "K")
black_king.rect.x = board_locs[4][0][0]
black_king.rect.y = board_locs[4][0][1]
pieces.add(black_king)

black_bishop2 = Piece(1, "B")
black_bishop2.rect.x = board_locs[5][0][0]
black_bishop2.rect.y = board_locs[5][0][1]
pieces.add(black_bishop2)

black_knight2 = Piece(1, "N")
black_knight2.rect.x = board_locs[6][0][0]
black_knight2.rect.y = board_locs[6][0][1]
pieces.add(black_knight2);

black_rook2 = Piece(1, "R") 
black_rook2.rect.x = board_locs[7][0][0]
black_rook2.rect.y = board_locs[7][0][1]
pieces.add(black_rook2)

found = False
pos = [0,0]
selected = None
in_square = False
found = False
while running:
    # --- Main event loop
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # If user clicked close
            running = False # Flag that we are done so we exit this loop
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if not (screen.get_at(pos)) == GREEN:
                selected = None
                found = False
                
        

   
     # --- Game logic should go here
    for piece in pieces:
        #let the piece know where it's current location is
        piece.loc = [(piece.rect.x - 40)/60, (piece.rect.y-40)/60]
        if (piece.rect.collidepoint(pos)):
            found = True
            selected = piece
            all_squares.update(-1) #remove all other highlighted squares
            #change the color of possible move squares
            possible_locs = can_move(piece, square_list)
            for loc in possible_locs:
                square_list[loc[0]][loc[1]].update(GREEN)
            break #we've found the selected piece. No need to loop through anymore
        if(not found): 
            selected = None
    if not ((screen.get_at(pos)) == GREEN) and not selected:
        all_squares.update(-1)
        
    #if a piece has been selected, then a player clicks a green square, move the piece there
    if(not selected is None):
        for square in all_squares:
            if square.rect.collidepoint(pos):
                found = True
                if(square.color == GREEN): #if it's a possible move
                    #move piece to that square
                    selected.rect.x = square.rect.x;
                    selected.rect.y = square.rect.y;
                    selected.pos = [(square.rect.x - 40)/60, (square.rect.y-40)/60]
                    selected = None
                    all_squares.update(-1)
                    pos = [0,0]
            
    
        



     
     
     # First, clear the screen to white. 
    screen.fill(WHITE)
    #draw board squares
    all_squares.draw(screen)
    #draw pieces
    pieces.draw(screen)
     
    #draw outline of board
    pygame.draw.line(screen, BLACK, [40, 40], [520, 40], 2)
    pygame.draw.line(screen, BLACK, [40, 520], [520, 520], 2)
    pygame.draw.line(screen, BLACK, [40, 40], [40, 520], 2)
    pygame.draw.line(screen, BLACK, [520, 40], [520, 520], 2)
    
 
 
     # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
     # --- Limit to 20 frames per second
    clock.tick(2)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()*7
