import numpy as np


class Checkers:
    def __init__(self, clear=False) -> None:
        self.board = np.zeros((10,10))
        if (not clear):
            for i in [0, 2]:
                for j in range(0,9,2):
                    self.board[i+1][j] = 1
                    self.board[9-i][j] = -1
            for i in [0, 2]:
                for j in range(1,10,2):
                    self.board[i][j] = 1
                    self.board[9-i-1][j] = -1

    def reverse(self):
        tab = np.zeros((10,10))
        for i in range(10):
            for j in range(10):
                tab[i][j] = self.board[9-i][9-j]
        return tab

    def Show(self, reverse=False):
        if reverse :
            print(self.reverse())
        else :
            print(self.board)
    
    def IsWinning(self, x):
        player = False
        for line in self.board:
            for case in line:
                if case == -x:
                    return False
                elif case == x:
                    player = True
        return player
    
    def IsEmpty(self, x, y):
        return (self.board[x][y] == 0)
    
    def IsOnBoard(self, x, y):
        return (x >= 0 and x < 10) and (y >= 0 and y < 10)

    def CanEat(self, x, y, OldPawn, path=None):
        child = []
        moves = []
        if self.IsOnBoard(x, y) and self.IsEmpty(x, y):
            child.append(self.GetValidMoveFromPawn(x, y, OnlyEat=True,  OldPawn=OldPawn, path=path))
        for c in child:
            if len(c) != 0 : moves = child
        if (len(moves) == 0):
            #return (x, y)
            return path
        elif (len(moves) == 1):
            return moves[0]
        return moves
    
    def CheckIfInside(self,x, y, array):
        for tab in array:
            if tab[0] == x and tab[1] == y:
                return True
        return False

            
        
    
    def GetValidMoveFromPawn(self, x, y, OnlyEat=False, OldPawn=None, path = []):
        pawn = int(self.board[x][y])
        if OnlyEat : pawn = OldPawn
        if len(path) == 0 : path.append((x, y))
        moves = []
        if abs(pawn) == 1: # In case of a pawn
            # Forward
            if self.IsOnBoard(x-pawn, y+1) and self.IsEmpty(x-pawn, y+1):
                if not OnlyEat : moves.append(((x, y), (x-pawn, y+1)))
            elif self.IsOnBoard(x-pawn, y+1) and self.IsOnBoard(x+2*(-pawn), y+2):
                if not self.CheckIfInside(x+2*(-pawn), y+2, path):
                    path2 = path.copy()
                    path2.append((x+2*(-pawn), y+2))
                    #moves.append(((x, y),self.CanEat(x+2*(-pawn), y+2, pawn, path=path)))
                    moves.append(self.CanEat(x+2*(-pawn), y+2, pawn, path=path2))
            if self.IsOnBoard(x-pawn, y-1) and self.IsEmpty(x-pawn, y-1):
                if not OnlyEat : moves.append(((x, y), (x-pawn, y-1)))
            elif self.IsOnBoard(x-pawn, y+1) and self.IsOnBoard(x+2*(-pawn), y-2):
                if not self.CheckIfInside(x+2*(-pawn), y-2, path):
                    path2 = path.copy()
                    path2.append((x+2*(-pawn), y-2))
                    #moves.append(((x, y),self.CanEat(x+2*(-pawn), y-2, pawn, path=path)))
                    moves.append(self.CanEat(x+2*(-pawn), y-2, pawn, path=path2))

            # Backward
            if self.IsOnBoard(x+pawn, y+1) and self.IsEmpty(x+pawn, y+1):
                pass
            elif self.IsOnBoard(x+pawn, y+1) and self.IsOnBoard(x+2*pawn, y+2):
                if not self.CheckIfInside(x+2*pawn, y+2, path):
                    path2 = path.copy()
                    path2.append((x+2*pawn, y+2))
                    #moves.append(((x, y),self.CanEat(x+2*pawn, y+2, pawn, path=path)))
                    moves.append(self.CanEat(x+2*pawn, y+2, pawn, path=path2))
            if self.IsOnBoard(x+pawn, y-1) and self.IsEmpty(x+pawn, y-1):
                pass
            elif self.IsOnBoard(x+pawn, y+1) and self.IsOnBoard(x+2*pawn, y-2):
                if not self.CheckIfInside(x+2*pawn, y-2, path):
                    path2 = path.copy()
                    path2.append((x+2*pawn, y-2))
                    #moves.append(((x, y),self.CanEat(x+2*pawn, y-2, pawn, path=path)))
                    moves.append(self.CanEat(x+2*pawn, y-2, pawn, path=path2))

        elif abs(pawn) == 2: # In case of a queen
            for i in range(-9,10,1):
                if self.IsOnBoard(x+i, y+i) and self.IsEmpty(x+i, y+i):
                    if not OnlyEat : moves.append(((x, y), (x+i, y+i)))
                if self.IsOnBoard(x+i, y-i) and self.IsEmpty(x+i, y-i):
                    if not OnlyEat : moves.append(((x, y), (x+i, y-i)))
        if len(moves) == 1 : return moves[0]
        return moves
    
    def FilterMoves(self, moves):
        Moves = []
        def loop(moves, array, FromArray=False):
            for i in range(len(array)):
                if isinstance(array[i], tuple) and not FromArray : 
                    Moves.append(array[i])
                elif isinstance(array[i], tuple):
                    Moves.append(array)
                    break
                elif isinstance(array[i], list) : 
                    loop(moves, array[i], FromArray=True)
        loop(Moves, moves)

        FinalMoves = []
        count = 0
        for i in range (len(Moves)):
            c = 0
            if isinstance(Moves[i], list) : c += 1
            c += len(Moves[i])
            if c > count :
                count = c
                FinalMoves = []
                FinalMoves.append(Moves[i])
            elif c == count :
                FinalMoves.append(Moves[i])
                
        
        return FinalMoves
    

    
    def GetValidMoves(self, player=1, verbose=False):
        moves = []
        for i in range(10):
            for j in range(10):
                if (self.board[i][j] == player or self.board[i][j] == 2*player):
                    for move in self.GetValidMoveFromPawn(i, j):
                        moves.append(move)

        moves = self.FilterMoves(moves)
        if verbose:
            print(moves)
        return moves
    


def main():
    game = Checkers(clear=True)
    game.board[6][5] = 1
    game.GetValidMoves(player=1, verbose=True)
    game.Show()

if "__main__" == __name__:
    main()