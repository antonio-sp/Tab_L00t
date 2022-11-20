from board import *

KING_ESCAPE = 400
KING_DANGER = 200
WEIGTH_WHITE = 140
WEIGTH_BLACK = 100
FLOW_WEIGTH_W = 3
FLOW_WEIGTH_B = 4

WHITE=0
KING=1
BLACK=2

KING_TABLE = (
                 (      0,   10000,   10000,       0,       0,       0,   10000,   10000,       0  ),       
                 (  10000,       0,       0,     -50,       0,     -50,       0,       0,   10000  ),       
                 (  10000,       0,      50,       0,       0,       0,      50,       0,   10000  ),       
                 (      0,   -1000,       0,       0,      10,       0,       0,   -1000,       0  ),       
                 (      0,       0,       0,      10,      20,      10,       0,       0,       0  ),       
                 (      0,   -1000,       0,       0,      10,       0,       0,   -1000,       0  ),       
                 (  10000,       0,      50,       0,       0,       0,      50,       0,   10000  ),       
                 (  10000,       0,       0,     -50,       0,     -50,       0,       0,   10000  ),       
                 (      0,   10000,   10000,       0,       0,       0,   10000,   10000,       0  )  )


TOP_R = ((0,5),(0,6),(0,7),(0,8),\
        (1,5),(1,6),(1,7),(1,8),\
        (2,5),(2,6),(2,7),(2,8),\
        (3,5),(3,6),(3,7),(3,8))
TOP_R = set(TOP_R)

TOP_L = ((0,0),(0,1),(0,2),(0,3),\
        (1,0),(1,1),(1,2),(1,3),\
        (2,0),(2,1),(2,2),(2,3),\
        (3,0),(3,1),(3,2),(3,3))
TOP_L = set(TOP_L)

BOT_R = ((5,5),(5,6),(5,7),(5,8),\
        (6,5),(6,6),(6,7),(6,8),\
        (7,5),(7,6),(7,7),(7,8),\
        (8,5),(8,6),(8,7),(8,8))
BOT_R = set(BOT_R)

BOT_L = ((5,0),(6,1),(7,2),(8,3),\
        (5,0),(6,1),(7,2),(8,3),\
        (5,0),(6,1),(7,2),(8,3),\
        (5,0),(6,1),(7,2),(8,3))
BOT_L = set(BOT_L)


walls =  (        (0,3), (0,5), (1,4), (0,4),
                  (3,0), (5,0), (4,1), (4,0),
                  (3,8), (5,8), (4,7), (4,8),
                  (7,4), (8,3), (8,5), (8,4),
                  (4,4)                     ) # throne


citadels   = (   (0,3),(0,4),(0,5),(1,4),   # upper-center citadel
                 (3,8),(4,8),(5,8),(4,7),   # right citadel
                 (8,3),(8,4),(8,5),(7,4),   # down-center citadel
                 (3,0),(4,0),(5,0),(4,1),   # left citadel
                                          ) # fake citadel to avoid a check

walls = set(walls)
citadels = set(citadels)


# evaluate future position
def heuristic_function(board):
    if   board.role == 'WHITE':
        return supremacy_white(board)
    elif board.role == 'BLACK':
        return ultimatum_black(board)

def ultimatum_black(board):
    result = 0

    win = board.check_win()
    if win is not None:
        if win:
            return  100000
        else:
            return -100000

    if(king_escape(board)):
        result += KING_ESCAPE

    if(king_danger(board)):
        result -= KING_DANGER

    result += eval_king(board)

    result += len(board.pawns[WHITE])*WEIGTH_WHITE
    result -= len(board.pawns[BLACK])*WEIGTH_BLACK

    return result



def supremacy_white(board):

    result = 0

    win = board.check_win()
    if win is not None:
        if win:
            return  100000
        else:
            return -100000

    if king_escape(board) :
        result += KING_ESCAPE + 1000

    if king_danger(board) :
        result -= KING_DANGER + 1200

    result += eval_king(board)

    result += len(board.pawns[WHITE])*(400)
    result -= len(board.pawns[BLACK])*(200)
    
    flow = number_flows(board)
    
    result += flow[0]*FLOW_WEIGTH_W
    result -= flow[1]*FLOW_WEIGTH_B

    return result



def king_escape(board):
    obstacle = False

    row = board.pawns[KING][0][ROW]
    column = board.pawns[KING][0][COLUMN]

    #Check right
    for i in range(column+1, 9):
        if (row, i) in board.pawns[WHITE] or (row,i) in board.pawns[BLACK]:
            obstacle = True
            break

    if not obstacle and not board.pawns[KING][0] in citadels:
        return True #(row, 8)


    obstacle = False
    #Check left
    for i in range(column-1, -1):
        if (row, i) in board.pawns[WHITE] or (row,i) in board.pawns[BLACK]:
            obstacle = True
            break

    if not obstacle and not board.pawns[KING][0] in citadels:
        return True #(row,0)


    obstacle = False
    #Check down
    for i in range(row+1, 9):
        if (i, column) in board.pawns[WHITE] or (i, column) in board.pawns[BLACK]:
            obstacle = True
            break

    if not obstacle and not board.pawns[KING][0] in citadels:
        return True #(8,column)


    obstacle = False
    #Check up
    for i in range(row-1, 0):
        if (i, column) in board.pawns[WHITE] or (i, column) in board.pawns[BLACK]:
            obstacle = True
            break

    if not obstacle and not board.pawns[KING][0] in citadels:
        return True #(0, column)

    #no king escape path found
    return False
    

def king_danger(board):

    row = board.pawns[KING][0][ROW]
    column = board.pawns[KING][0][COLUMN]

    capture = 0
    #right
    if (row,column+1) in board.pawns[BLACK]:
        capture+=1
    #left
    if (row,column-1) in board.pawns[BLACK]:
        capture+=1
    #top
    if (row+1,column) in board.pawns[BLACK]:
        capture+=1
    #under
    if (row-1,column) in board.pawns[BLACK]:
        capture+=1

    #controllo se è intrappolato nel trono o vicino
    if row == 4:
        if column == 4 and capture == 3:
            return True
        #se è adiacente al trono
        #left
        if column == 3 and capture == 2:
            return True
        #right
        if column == 5 and capture == 2:
            return True
    #se il re è nella colonna 4
    elif column == 4:
        #bottom
        if row == 3 and capture == 2:
            return True
        #top
        if row == 5 and capture == 2:
            return True
    
    if (row,column) in ((1,3),(1,5),(7,3),(7,5),(3,1),(5,1),(3,7),(5,7),(4,2),(4,6),(2,4),(2,6)):
        return True

    if capture == 1:
        return True

    return False

def number_flows(board):
    result = [0,0]

    if board.pawns[KING][0][ROW] < 4:
        if board.pawns[KING][0][COLUMN] < 4:
            #print(len(list( set(board.pawns[WHITE]) - BOT_R)))

            result[WHITE] = len(list( set(board.pawns[WHITE]) - BOT_R))
            result[BLACK-1] = len(list( set(board.pawns[BLACK]) - BOT_R))
        elif board.pawns[KING][0][COLUMN] > 4:
            result[WHITE] = len(list( set(board.pawns[WHITE]) - BOT_L))
            result[BLACK-1] = len(list( set(board.pawns[BLACK]) - BOT_L))
    elif board.pawns[KING][0][ROW] > 4:
        if board.pawns[KING][0][COLUMN] < 4:
            result[WHITE] = len(list( set(board.pawns[WHITE]) - TOP_R))
            result[BLACK-1] = len(list( set(board.pawns[BLACK]) - TOP_R))
        elif board.pawns[KING][0][COLUMN] > 4:
            result[WHITE] = len(list( set(board.pawns[WHITE]) - TOP_L))
            result[BLACK-1] = len(list( set(board.pawns[BLACK]) - TOP_L))
    else:
        return [0,0]
    #print(result)
    return result

def eval_king(board):
    row, column = board.pawns[KING][0]
    return KING_TABLE[row][column]




