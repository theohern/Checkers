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
    
    def IsSameSign(self, a, b):
        return (a <= 0 and b <=0) or (a >= 0 and b >= 0)
    
    def MoveQueen(self, x, y , pawn, OnlyEat=False, eatten=[], AllPath=[], path=[]):
        path.append((x, y))
        SimpleMoves = []
        EatMoves = []
        eat = False
        if OnlyEat : EatMoves.append((x, y))
        DRContinue, DLContinue, URContinue, ULContinue = True, True, True, True
        for i in range(1,10):
            if self.IsOnBoard(x+i, y+i) and self.IsEmpty(x+i, y+i) and DRContinue  :
                if not OnlyEat : SimpleMoves.append(((x, y), (x+i, y+i)))
            elif self.IsOnBoard(x+i+1, y+i+1) and DRContinue and self.IsEmpty(x+i+1, y+i+1) and not ((x+i, y+i) in eatten) :
                DRContinue = False
                if  not self.IsSameSign(pawn, self.board[x+i][y+i]) : 
                    eat = True
                    eatten2 = eatten.copy()
                    eatten2.append((x+i, y+i))
                    EatMoves.append(self.MoveQueen(x+i+1, y+i+1,pawn, OnlyEat=True, eatten=eatten2, AllPath=AllPath, path=path.copy()))
            if self.IsOnBoard(x-i, y-i) and self.IsEmpty(x-i, y-i) and ULContinue  :
                if not OnlyEat : SimpleMoves.append(((x, y), (x-i, y-i)))
            elif self.IsOnBoard(x-i-1, y-i-1) and ULContinue and self.IsEmpty(x-i-1, y-i-1) and not ((x-i, y-i) in eatten) :
                ULContinue = False
                if  not self.IsSameSign(pawn, self.board[x-i][y-i]) :
                    eat = True 
                    eatten2 = eatten.copy()
                    eatten2.append((x-i, y-i))
                    EatMoves.append(self.MoveQueen(x-i-1, y-i-1, pawn, OnlyEat=True, eatten=eatten2, AllPath=AllPath, path=path.copy()))
            if self.IsOnBoard(x+i, y-i) and self.IsEmpty(x+i, y-i) and DLContinue  :
                if not OnlyEat : SimpleMoves.append(((x, y), (x+i, y-i)))
            elif self.IsOnBoard(x+i+1, y-i-1) and DLContinue and self.IsEmpty(x+i+1, y-i-1) and not ((x+i, y-i) in eatten) :
                DLContinue = False
                if  not self.IsSameSign(pawn, self.board[x+i][y-i]) :
                    eat = True 
                    eatten2 = eatten.copy()
                    eatten2.append((x+i, y-i))
                    EatMoves.append(self.MoveQueen(x+i+1, y-i-1, pawn, OnlyEat=True, eatten=eatten2, AllPath=AllPath, path=path.copy()))
            if self.IsOnBoard(x-i, y+i) and self.IsEmpty(x-i, y+i) and URContinue  :
                if not OnlyEat : SimpleMoves.append(((x, y), (x-i, y+i)))
            elif self.IsOnBoard(x-i-1, y+i+1) and URContinue and self.IsEmpty(x-i-1, y+i+1) and not ((x-i, y+i) in eatten) :
                URContinue = False
                if  not self.IsSameSign(pawn, self.board[x-i][y+i]) : 
                    eat = True
                    eatten2 = eatten.copy()
                    eatten2.append((x-i, y+i))
                    EatMoves.append(self.MoveQueen(x-i-1, y+i+1, pawn, OnlyEat=True, eatten=eatten2, AllPath=AllPath, path=path.copy()))

        if not eat : 
            AllPath.append(path)
        #if OnlyEat : return EatMoves
        return SimpleMoves, AllPath
 
    def MovePawn(self, x, y, pawn, OnlyEat=False, eatten=[], AllPath = [], path=[]):
        moves = []
        SimpleMoves = []
        if not OnlyEat : path = []; AllPath = []; eatten = []
        eat = False
        path.append((x, y))
        if self.IsOnBoard(x-pawn, y+1) and self.IsEmpty(x-pawn, y+1):
            if not OnlyEat : SimpleMoves.append(((x, y), (x-pawn, y+1)))
        elif self.IsOnBoard(x-pawn, y+1) and self.IsOnBoard(x+2*(-pawn), y+2) and not((x-pawn, y+1) in eatten):
            if not self.IsSameSign(pawn, self.board[x-pawn][y+1]) : 
                eatten2 = eatten.copy()
                eatten2.append((x-pawn, y+1))
                moves.append(self.MovePawn(x+2*(-pawn), y+2, pawn, eatten=eatten2, OnlyEat=True, AllPath=AllPath, path=path.copy()))
                eat = True
        if self.IsOnBoard(x-pawn, y-1) and self.IsEmpty(x-pawn, y-1):
            if not OnlyEat : SimpleMoves.append(((x, y), (x-pawn, y-1)))
        elif self.IsOnBoard(x-pawn, y-1) and self.IsOnBoard(x+2*(-pawn), y-2) and not((x-pawn, y-1) in eatten):
            if not self.IsSameSign(pawn, self.board[x-pawn][y-1]) : 
                eatten2 = eatten.copy()
                eatten2.append((x-pawn, y-1))
                moves.append(self.MovePawn(x+2*(-pawn), y-2, pawn, eatten=eatten2, OnlyEat=True, AllPath=AllPath, path=path.copy()))
                eat = True
        # Backward
        if self.IsOnBoard(x+pawn, y+1) and self.IsEmpty(x+pawn, y+1):
            pass
        elif self.IsOnBoard(x+pawn, y+1) and self.IsOnBoard(x+2*pawn, y+2) and not((x+pawn, y+1) in eatten):
            if not self.IsSameSign(pawn, self.board[x+pawn][y+1]) : 
                eatten2 = eatten.copy()
                eatten2.append((x+pawn, y+1))
                moves.append(self.MovePawn(x+2*pawn, y+2, pawn, eatten=eatten2, OnlyEat=True, AllPath=AllPath, path=path.copy()))
                eat = True

        if self.IsOnBoard(x+pawn, y-1) and self.IsEmpty(x+pawn, y-1):
            pass
        elif self.IsOnBoard(x+pawn, y+1) and self.IsOnBoard(x+2*pawn, y-2) and not((x+pawn, y-1) in eatten):
            if not self.IsSameSign(pawn, self.board[x+pawn][y-1]) : 
                eatten2 = eatten.copy()
                eatten2.append((x+pawn, y-1))
                moves.append(self.MovePawn(x+2*pawn, y+2, pawn, eatten=eatten2, OnlyEat=True, AllPath=AllPath, path=path.copy()))
                eat = True
        
        if not eat : AllPath.append(path)

        return SimpleMoves, AllPath

    def GetValidMoveFromPawn(self, x, y):
        pawn = int(self.board[x][y])
        if abs(pawn) == 1: # In case of a pawn
            return self.MovePawn(x, y, pawn)
    
    def GetValidMoveFromQueen(self, x, y, OnlyEat=False, OldPawn=None, path=[]):
        moves = []
        queen = self.board[x][y]
        if abs(queen) == 2: # In case of a queen
            Moves, Eat = self.MoveQueen(x, y, queen)
            for m in Moves : moves.append(m)
            for e in Eat : moves.append(e)
        return moves

    def FilterMovesPawn(self, moves):
        Moves = []
        FinalMoves = []
        for move in moves :
            if len(move[1]) == 0:
                for m in move[0]:
                    Moves.append(m)
            else :
                for m in move[1]:
                    Moves.append(m)
        maximum = 0
        for m in Moves :
            count = 0
            if isinstance(m, list) : count += 1
            count += len(m)
            if count > maximum:
                maximum = count
                FinalMoves = []
                FinalMoves.append(m)
            elif count == maximum:
                FinalMoves.append(m)
        return FinalMoves
    
    def FilterMovesQueen(self, moves):
        def loop(FinalMoves, moves):
            pass
        
    def GetValidMoves(self, player=1, verbose=False):
        moves = []
        moves2 = []
        for i in range(10):
            for j in range(10):
                if self.board[i][j] == player:
                    moves.append(self.GetValidMoveFromPawn(i, j))
                elif self.board[i][j] == 2*player:
                    for move in self.GetValidMoveFromQueen(i, j):
                        moves2.append(move)

        moves = self.FilterMovesPawn(moves)

        if verbose:
            print(moves)
            print(moves2)
        return moves, moves2
    


def main():
    game = Checkers(clear=True)
    #game.board[5][4] = 2
    game.board[4][3] = 0
    game.board[7][4] = 1
    game.board[3][2] = 1
    game.board[6][5] = -1
    game.board[8][7] = -1
    game.board[4][3] = -1
    game.board[2][3] = -1
    game.board[5][8] = -1
    game.GetValidMoves(player=1, verbose=True)
    game.Show()

if "__main__" == __name__:
    main()
    a =[[(5, 4), (7, 6), (9, 8)], [(5, 4), (7, 6), (4, 9)], [(5, 4), (1, 0), (7, 6), (9, 8)], [(5, 4), (1, 0), (7, 6), (4, 9)]]
    