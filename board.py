import json

UTF8  = True

WHITE = 0
KING = 1
BLACK = 2

ROW = 0
COLUMN =1


walls =  set((    (0,3), (0,5), (1,4),# (0,4),
                  (3,0), (5,0), (4,1),# (4,0),
                  (3,8), (5,8), (4,7),# (4,8),
                  (7,4), (8,3), (8,5),# (8,4),
                  (4,4)                     )) # throne


citadels   = (   set(((0,3),(0,4),(0,5),(1,4))),   # upper-center citadel
                 set(((3,8),(4,8),(5,8),(4,7))),   # right citadel
                 set(((8,3),(8,4),(8,5),(7,4))),   # down-center citadel
                 set(((3,0),(4,0),(5,0),(4,1))),   # left citadel
                 set(())                         ) # fake citadel to avoid a check

class Board:
    def __init__(self,data_from_server):
        data = json.loads(data_from_server)
        # 0,1 -> white + king
        # 2   -> black
        self.pawns = [[],[],[]]
        self.role = data['turn']
        
        for row in range(0,9):
            for column in range(0,9):
                if data['board'][row][column] == 'WHITE':
                    self.pawns[WHITE].append((row,column))
                    continue
                if data['board'][row][column] == 'KING':
                    self.pawns[KING].append((row,column))
                    continue
                if data['board'][row][column] == 'BLACK':
                    self.pawns[BLACK].append((row,column))
                    continue


    # the color needs to be a boolean
    def generate_moves(self, color):
        result        = []
        current_pawns = []
        opponent     = []
        if color:
            current_pawns = self.pawns[WHITE] + self.pawns[KING]
            opponent      = self.pawns[BLACK]
        else:
            current_pawns = self.pawns[BLACK]
            opponent      = self.pawns[WHITE] + self.pawns[KING]


        ###############
        #### WHITE ####
        ###############
        # if color == WHITE:
        if color:
            for pawn in current_pawns:
                row    = pawn[0]
                column = pawn[1]
                #### horizonal moves ####
                # right #
                for i in range(column+1, 9):
                    # check if movment is possible
                    if (row,i) not in walls and (row,i) not in current_pawns + opponent:
                        result.append((row,column,row,i))
                    else:
                        break
                # left #
                for i in range(column-1, -1, -1):
                    # check if movment is possible
                    if (row,i) not in walls and (row,i) not in current_pawns + opponent:
                        result.append((row,column,row,i))
                    else:
                        break
                #########################

                #### vertical moves ####
                # up #
                for i in range(row+1, 9):
                    # check if movment is possible
                    if (i, column) not in walls and (i, column) not in current_pawns + opponent:
                        result.append((row,column,i,column))
                    else:
                        break
                # down #
                for i in range(row-1, -1, -1):
                    # check if movment is possible
                    if (i, column) not in walls and (i, column) not in current_pawns + opponent:
                        result.append((row,column,i,column))
                    else:
                        break
                #########################

        ###############
        #### BLACK ####
        ###############
        else:
            for pawn in current_pawns:
                row    = pawn[0]
                column = pawn[1]
                # check if the pawn is a citadel:
                # in that case the movement inside
                # the same citadel is possible
                citadel = 4
                for i in range(4):
                    if (i,column) in citadels[i]:
                        citadel = i
                        break
                #### horizonal moves ####
                # on right #
                for i in range(column+1, 9):
                    # check if movment is possible
                    if  (row,i) not in walls - citadels[citadel] \
                            and (row,i) not in current_pawns + opponent:
                        result.append((row,column,row,i))
                    else:
                        break
                # on left #
                for i in range(column-1, -1, -1):
                    # check if movment is possible
                    if (row,i) not in walls - citadels[citadel] \
                            and (row,i) not in current_pawns + opponent:
                        result.append((row,column,row,i))
                    else:
                        break
                #########################

                #### vertical moves ####
                # up #
                for i in range(row+1, 9):
                    # check if movment is possible
                    if (i, column) not in walls - citadels[citadel] \
                            and (i, column) not in current_pawns + opponent:
                        result.append((row,column,i,column))
                    else:
                        break
                # down #
                for i in range(row-1, -1, -1):
                    # check if movment is possible
                    if (i, column) not in walls - citadels[citadel] \
                            and (i, column) not in current_pawns + opponent:
                        result.append((row,column,i,column))
                    else:
                        break
                #########################
        return result

        
    def __str__(self):
        board = []
        for _ in range(0,9):
            board.append(['.','.','.','.','.','.','.','.','.'])
        for w in self.pawns[0]:
            board[w[0]][w[1]] = 'W'
        for k in self.pawns[1]:
            board[k[0]][k[1]] = 'K'
        for b in self.pawns[2]:
            board[b[0]][b[1]] = 'B'

        res = ''
        index = 0
        res += '┌───┬───┬───┬───┬───┬───┬───┬───┬───┐\n'
        for l in board:
            iindex = 0
            for p in l:
                if p == '.':
                    res += '│   '
                elif p == 'B':
                    if UTF8:
                        res += '│⚫ '
                    else:
                        res += '│ \x1b[1;37;40m' + 'X' + '\x1b[0m '
                elif p == 'W':
                    if UTF8:
                        res += '│⚪ '
                    else:
                        res += '│ \x1b[0;30;47m' + 'X' + '\x1b[0m '
                elif p == 'K':
                    if UTF8:
                        res += '│♔  '
                    else:
                        res += '│ \x1b[0;30;47m' + 'O' + '\x1b[0m '
                if iindex == 8:
                    res += f'│ {index+1}'
                iindex += 1
            if index == 8:
                res += '\n└───┴───┴───┴───┴───┴───┴───┴───┴───┘\n'
                res += '  A   B   C   D   E   F   G   H   I  \n'
            else:
                res += '\n├───┼───┼───┼───┼───┼───┼───┼───┼───┤\n'
            index += 1
        return res


    def gen_state_string(self):
        board = []
        for row in range(0,9):
            board.append(['.','.','.','.','.','.','.','.','.'])
        for w in self.pawns[0]:
            board[w[0]][w[1]] = 'W'
        for k in self.pawns[1]:
            board[k[0]][k[1]] = 'K'
        for b in self.pawns[2]:
            board[b[0]][b[1]] = 'B'
        return ''.join([''.join(x) for x in board])


    def check_capture(self, current_pos, color):
        captures = []
        whites = self.pawns[WHITE] + self.pawns[KING]
        if color == True: #white case
            if (current_pos[0]-1,current_pos[1]) in self.pawns[BLACK]:
                if (current_pos[0]-2,current_pos[1]) in whites or (current_pos[0]-2,current_pos[1]) in walls:
                    captures.append((current_pos[0]-1,current_pos[1]))

            if (current_pos[0]+1,current_pos[1]) in self.pawns[BLACK]:
                if (current_pos[0]+2,current_pos[1]) in whites or (current_pos[0]+2,current_pos[1]) in walls:
                    captures.append((current_pos[0]+1,current_pos[1]))

            if (current_pos[0],current_pos[1]-1) in self.pawns[BLACK]:
                if (current_pos[0],current_pos[1]-2) in whites or (current_pos[0],current_pos[1]-2) in walls:
                    captures.append((current_pos[0],current_pos[1]-1))

            if (current_pos[0],current_pos[1]+1) in self.pawns[BLACK]:
                if (current_pos[0],current_pos[1]+2) in whites or (current_pos[0],current_pos[1]+2) in walls:
                    captures.append((current_pos[0],current_pos[1]+1))

        else:
            if (current_pos[0]-1,current_pos[1]) in whites:
                if (current_pos[0]-2,current_pos[1]) in self.pawns[BLACK] or (current_pos[0]-2,current_pos[1]) in walls:
                    captures.append((current_pos[0]-1,current_pos[1]))

            if (current_pos[0]+1,current_pos[1]) in whites:
                if (current_pos[0]+2,current_pos[1]) in self.pawns[BLACK] or (current_pos[0]+2,current_pos[1]) in walls:
                    captures.append((current_pos[0]+1,current_pos[1]))

            if (current_pos[0],current_pos[1]-1) in whites:
                if (current_pos[0],current_pos[1]-2) in self.pawns[BLACK] or (current_pos[0],current_pos[1]-2) in walls:
                    captures.append((current_pos[0],current_pos[1]-1))

            if (current_pos[0],current_pos[1]+1) in whites:
                if (current_pos[0],current_pos[1]+2) in self.pawns[BLACK] or (current_pos[0],current_pos[1]+2) in walls:
                    captures.append((current_pos[0],current_pos[1]+1))

        return captures

            

    def move(self, move, color):
        row_from, column_from, row_to, column_to = move
        if color == True: #white case
            if (row_from,column_from) == self.pawns[KING][0]:
                self.pawns[KING].remove((row_from, column_from))
                self.pawns[KING].append((row_to, column_to))
                captures = self.check_capture((row_to,column_to), color)
                for c in captures:
                    self.pawns[BLACK].remove(c)
            else:
                self.pawns[WHITE].remove((row_from, column_from))
                self.pawns[WHITE].append((row_to, column_to))
                captures = self.check_capture((row_to,column_to), color)
                for c in captures:
                    self.pawns[BLACK].remove(c)

        else:
            self.pawns[BLACK].remove((row_from, column_from))
            self.pawns[BLACK].append((row_to, column_to))
            captures = self.check_capture((row_to,column_to), color)
            for c in captures:
                if c not in self.pawns[KING]:
                    self.pawns[WHITE].remove(c)
                else:
                    if self.pawns[KING][0] not in ((4,4),(3,4),(5,4),(4,3),(4,5)):
                        self.pawns[KING].remove(c)
        return self
        


    def check_win(self):
        if len(self.pawns[KING]) == 0:
            return False
        # check if white or black are 0
        if len(self.pawns[BLACK]) == 0:
            return True

        if len(self.pawns[WHITE]) + len(self.pawns[KING]) == 0:
            return False


        
        if self.pawns[KING][0][0] == 0 or self.pawns[KING][0][0] == 8 \
                or self.pawns[KING][0][1] == 0 or self.pawns[KING][0][1] == 8:
            return True

        if self.pawns[KING][0] == (4,4) and \
                (3,4) in self.pawns[BLACK] and (5,4) in self.pawns[BLACK] and \
                (4,3) in self.pawns[BLACK] and (4,5) in self.pawns[BLACK]:
            return False

        if (self.pawns[KING][0] == (3,4) and \
                (2,4) in self.pawns[BLACK] and (3,5) in self.pawns[BLACK] and \
                (3,3) in self.pawns[BLACK] ) or \
                (self.pawns[KING][0] == (5,4) and \
                (5,5) in self.pawns[BLACK] and (6,4) in self.pawns[BLACK] and \
                (5,3) in self.pawns[BLACK] ) or \
                (self.pawns[KING][0] == (4,3) and \
                (4,2) in self.pawns[BLACK] and (3,3) in self.pawns[BLACK] and \
                (5,3) in self.pawns[BLACK] ) or \
                (self.pawns[KING][0] == (4,5) and \
                (3,5) in self.pawns[BLACK] and (5,5) in self.pawns[BLACK] and \
                (4,6) in self.pawns[BLACK] ):
            return False
        




        return None

        

