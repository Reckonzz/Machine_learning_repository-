import random
import numpy as np
from collections import defaultdict

class BoardPiece: 
    def __init__(self, name, code, pos): 
        self.name = name 
        self.code = code
        self.pos = pos 
    def addPos(self,pos): 
        self.pos = (self.pos[0] + pos[0], self.pos[1] + pos[1])
    def checkOverlap(self,pieces): 
        if type(pieces) != list: 
            return self.pos == pieces.pos 
        else: 
            flag = False
            for piece in pieces: 
                if self.pos == piece.pos: 
                    flag = True 
                    break 
            return flag 
    def __eq__(self, other): 
        return self.name == other.name and self.code == other.code and self.pos == other.pos

class Board: 
    def __init__(self, size):
        self.size = size 
        self.components = defaultdict(list) 
        
    def display(self): 
        board = np.zeros((self.size, self.size), dtype="<U2")
        board[:] = ' '
        for piece in self.components["All"]:
            x, y = piece.pos 
            code = piece.code 
            board[y][x] = code
        player = self.components["Player"][0]
        board[player.pos[1]][player.pos[0]] = player.code
        print(board)
        
    def clear_board(self): 
        self.components = defaultdict(list)
        
    def init_board(self, deterministic=True, n_walls=1, n_pits=1): 
        self.clear_board()
        if deterministic: 
            self.addPiece("Player", "P", (3,0))
            self.addPiece("Goal", "+", (0,0))
            self.addPiece('Pit', "-", (1,0))
            self.addPiece("Wall", "W", (1,1)) 
        else: 
            self.addPiece("Player","P")
            self.addPiece("Goal","+")
            for pit in range(n_pits):
                self.addPiece("Pit","-")
            for wall in range(n_walls): 
                self.addPiece("Wall","W") 
    
    def addPiece(self, name, code, pos=False): 
        piece = BoardPiece(name, code, pos) 
        if not pos: 
            piece = self.getPieceRandomPos(piece) 
        self.components[name].append(piece)
        self.components["All"].append(piece)
       
    def getPieceRandomPos(self, piece):
        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - 1)
        piece.pos = (x,y)
        while piece.checkOverlap(self.components["All"]): 
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            piece.pos = (x,y)
        return piece
    
    def reward(self): 
        if self.components["Player"][0].checkOverlap(self.components["Pit"]): 
            return -10 
        elif self.components["Player"][0].checkOverlap(self.components["Goal"][0]): 
            return 10 
        else: 
            return -1 
    
    def checkMove(self, pos): 
        player_pos = self.components["Player"][0].pos
        new_pos = (pos[0] + player_pos[0], pos[1] + player_pos[1])
        piece = BoardPiece("Player", "P", new_pos)
        #check if player lands outside of boundary or on wall, 
        return not (new_pos[0] < 0 or new_pos[0] >= self.size or new_pos[1] < 0 or new_pos[1] >= self.size or piece.checkOverlap(self.components["Wall"]))

    def makeMove(self, action): 
        if action == "u": 
            pos=(0,-1)
        elif action == "d": 
            pos=(0,1)
        elif action == "l": 
            pos=(-1,0) 
        elif action == "r": 
            pos=(1,0)
        if self.checkMove(pos): 
            self.components["Player"][0].addPos(pos)

    def board_to_matrix(self): 
        piece_names = list(self.components.keys())
        piece_names.remove("All") 
        np_board = np.zeros((len(piece_names), self.size, self.size))
        for i, name in enumerate(piece_names): 
            for piece in self.components[name]: 
                x, y = piece.pos
                np_board[i, y, x] = 1 
        return np_board
    