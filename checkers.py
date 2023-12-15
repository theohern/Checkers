import numpy as np
import random
from time import sleep


class Checkers:
    def __init__(self, clear=False) -> None:
        self.board = np.zeros((10,10))
        if (not clear):
            for i in [0, 2]:
                for j in range(0,9,2):
                    self.board[i+1][j] = -1
                    self.board[9-i][j] = 1
            for i in [0, 2]:
                for j in range(1,10,2):
                    self.board[i][j] = -1
                    self.board[9-i-1][j] = 1

        self.score1 = 20
        self.score2 = 20

    def GetScore(self, verbose):
        if verbose : print(f"score {self.score1} - {self.score2}")
        return self.score1, self.score2

    def CheckScore(self):
        count1 = 0
        count2 = 0
        for i in range(10):
            for j in range(10):
                if self.board[i][j] > 0 : count1 += self.board[i][j]
                elif self.board[i][j] < 0 : count2 -= self.board[i][j]
        return count1 == self.score1 and count2 == self.score2
    
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
    
    def EndGame(self):
        player1 = 0
        player2 = 0
        for line in self.board:
            for case in line:
                if case > 0:
                    player1 += case
                elif case < 0:
                    player2 -= case
        if player1 == 0 and player2 == 0 : return 2
        elif player2 == 0 : return 1
        elif player1 == 0 : return -1
        else : return 0

    def IsEmpty(self, x, y):
        return self.board[x][y] == 0
    
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
        SimpleMoves = []
        if not OnlyEat : path = []; AllPath = [];
        eat = False
        DRContinue, DLContinue, URContinue, ULContinue = True, True, True, True
        path.append((x, y))
        for i in range(1,10):
            if self.IsOnBoard(x+i, y+i) and self.IsEmpty(x+i, y+i) and DRContinue  :
                if not OnlyEat : SimpleMoves.append(((x, y), (x+i, y+i)))
            elif self.IsOnBoard(x+i+1, y+i+1) and DRContinue and self.IsEmpty(x+i+1, y+i+1) and not ((x+i, y+i) in eatten) :
                DRContinue = False
                if  not self.IsSameSign(pawn, self.board[x+i][y+i]) : 
                    eat = True
                    eatten2 = eatten.copy()
                    eatten2.append((x+i, y+i))
                    self.MoveQueen(x+i+1, y+i+1,pawn, OnlyEat=True, eatten=eatten2, AllPath=AllPath, path=path.copy())
            if self.IsOnBoard(x-i, y-i) and self.IsEmpty(x-i, y-i) and ULContinue  :
                if not OnlyEat : SimpleMoves.append(((x, y), (x-i, y-i)))
            elif self.IsOnBoard(x-i-1, y-i-1) and ULContinue and self.IsEmpty(x-i-1, y-i-1) and not ((x-i, y-i) in eatten) :
                ULContinue = False
                if  not self.IsSameSign(pawn, self.board[x-i][y-i]) :
                    eat = True 
                    eatten2 = eatten.copy()
                    eatten2.append((x-i, y-i))
                    self.MoveQueen(x-i-1, y-i-1, pawn, OnlyEat=True, eatten=eatten2, AllPath=AllPath, path=path.copy())
            if self.IsOnBoard(x+i, y-i) and self.IsEmpty(x+i, y-i) and DLContinue  :
                if not OnlyEat : SimpleMoves.append(((x, y), (x+i, y-i)))
            elif self.IsOnBoard(x+i+1, y-i-1) and DLContinue and self.IsEmpty(x+i+1, y-i-1) and not ((x+i, y-i) in eatten) :
                DLContinue = False
                if  not self.IsSameSign(pawn, self.board[x+i][y-i]) :
                    eat = True 
                    eatten2 = eatten.copy()
                    eatten2.append((x+i, y-i))
                    self.MoveQueen(x+i+1, y-i-1, pawn, OnlyEat=True, eatten=eatten2, AllPath=AllPath, path=path.copy())
            if self.IsOnBoard(x-i, y+i) and self.IsEmpty(x-i, y+i) and URContinue  :
                if not OnlyEat : SimpleMoves.append(((x, y), (x-i, y+i)))
            elif self.IsOnBoard(x-i-1, y+i+1) and URContinue and self.IsEmpty(x-i-1, y+i+1) and not ((x-i, y+i) in eatten) :
                URContinue = False
                if  not self.IsSameSign(pawn, self.board[x-i][y+i]) : 
                    eat = True
                    eatten2 = eatten.copy()
                    eatten2.append((x-i, y+i))
                    self.MoveQueen(x-i-1, y+i+1, pawn, OnlyEat=True, eatten=eatten2, AllPath=AllPath, path=path.copy())

        if not eat and len(path) > 1: AllPath.append(path)
        
        return SimpleMoves, AllPath
 
    def MovePawn(self, x, y, pawn, OnlyEat=False, eatten=[], AllPath = [], path=[]):
        SimpleMoves = []
        eat = False
        if not OnlyEat : path = []; AllPath = []
        path.append((x, y))
        if self.IsOnBoard(x-pawn, y+1) and self.IsEmpty(x-pawn, y+1):
            if not OnlyEat : SimpleMoves.append(((x, y), (x-pawn, y+1)))
        elif self.IsOnBoard(x-pawn, y+1) and self.IsOnBoard(x+2*(-pawn), y+2) and self.IsEmpty(x+2*(-pawn), y+2) and not((x-pawn, y+1) in eatten):
            if not self.IsSameSign(pawn, self.board[x-pawn][y+1]) : 
                eatten2 = eatten.copy()
                eatten2.append((x-pawn, y+1))
                self.MovePawn(x+2*(-pawn), y+2, pawn, eatten=eatten2, OnlyEat=True, AllPath=AllPath, path=path.copy())
                eat = True
        if self.IsOnBoard(x-pawn, y-1) and self.IsEmpty(x-pawn, y-1):
            if not OnlyEat : SimpleMoves.append(((x, y), (x-pawn, y-1)))
        elif self.IsOnBoard(x-pawn, y-1) and self.IsOnBoard(x+2*(-pawn), y-2) and self.IsEmpty(x+2*(-pawn), y-2) and not((x-pawn, y-1) in eatten):
            if not self.IsSameSign(pawn, self.board[x-pawn][y-1]) : 
                eatten2 = eatten.copy()
                eatten2.append((x-pawn, y-1))
                self.MovePawn(x+2*(-pawn), y-2, pawn, eatten=eatten2, OnlyEat=True, AllPath=AllPath, path=path.copy())
                eat = True
        # Backward
        if self.IsOnBoard(x+pawn, y+1) and self.IsEmpty(x+pawn, y+1):
            pass
        elif self.IsOnBoard(x+pawn, y+1) and self.IsOnBoard(x+2*pawn, y+2) and self.IsEmpty(x+2*pawn, y+2) and not((x+pawn, y+1) in eatten):
            if not self.IsSameSign(pawn, self.board[x+pawn][y+1]) : 
                eatten2 = eatten.copy()
                eatten2.append((x+pawn, y+1))
                self.MovePawn(x+2*pawn, y+2, pawn, eatten=eatten2, OnlyEat=True, AllPath=AllPath, path=path.copy())
                eat = True

        if self.IsOnBoard(x+pawn, y-1) and self.IsEmpty(x+pawn, y-1):
            pass
        elif self.IsOnBoard(x+pawn, y-1) and self.IsOnBoard(x+2*pawn, y-2) and self.IsEmpty(x+2*pawn, y-2) and not((x+pawn, y-1) in eatten):
            if not self.IsSameSign(pawn, self.board[x+pawn][y-1]) : 
                eatten2 = eatten.copy()
                eatten2.append((x+pawn, y-1))
                self.MovePawn(x+2*pawn, y-2, pawn, eatten=eatten2, OnlyEat=True, AllPath=AllPath, path=path.copy())
                eat = True
        
        if not eat and len(path) > 1 : AllPath.append(path)

        return SimpleMoves, AllPath

    def GetValidMoveFromPawn(self, x, y):
        moves = []
        pawn = int(self.board[x][y])
        if abs(pawn) == 1: # In case of a pawn
            Moves, Eat = self.MovePawn(x, y, pawn)
            for m in Moves : moves.append(m)
            for e in Eat : moves.append(e)
        return moves
    
    def GetValidMoveFromQueen(self, x, y):
        moves = []
        queen = self.board[x][y]
        if abs(queen) == 2: # In case of a queen
            Moves, Eat = self.MoveQueen(x, y, queen)
            for m in Moves : moves.append(m)
            for e in Eat : moves.append(e)
        return moves

    def FilterMovesPawn(self, moves):
        FinalMoves = []
        maximum = 0
        for m in moves :
            count = 0
            if isinstance(m, list) : count += 1
            count += len(m)
            if count > maximum:
                maximum = count
                FinalMoves.clear()
                FinalMoves.append(m)
            elif count == maximum:
                FinalMoves.append(m)
        return FinalMoves
    
    def FilterMovesQueen(self, moves):
        maximum = 0
        FinalMoves = []
        for m in moves :
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
        
    def GetValidMoves(self, player=1,Filter=False, verbose=False):
        moves = []
        moves2 = []
        for i in range(10):
            for j in range(10):
                if self.board[i][j] == player:
                    for move in self.GetValidMoveFromPawn(i, j):
                        moves.append(move)
                elif self.board[i][j] == 2*player:
                    for move in self.GetValidMoveFromQueen(i, j):
                        moves2.append(move)

        if Filter  : 
            moves = self.FilterMovesPawn(moves)
            moves2 = self.FilterMovesQueen(moves2)


        if verbose:
            print(moves)
            print(moves2)
        return moves, moves2
    
    def CompareBoard(self, a, b):
        for i in range(10):
            for j in range(10):
                if a[i][j] != b[i][j] : return False
        return True

    def CopyBoard(self):
        tab = []
        for i in range(10):
            tab.append([])
            for j in range(10):
                tab[i].append(self.board[i][j])
        return tab  
    
    def MergeList(self, a, b):
        liste = []
        for i in a :
            liste.append(i)
        for i in b:
            liste.append(i)
        return liste
    
    def PushMove(self, move):
        score = 0
        pawn  = self.board[move[0][0]][move[0][1]]
        xx = move[0][0] - move[1][0]
        if abs(xx) == 1 : 
            self.board[move[1][0]][move[1][1]] = pawn
            self.board[move[0][0]][move[0][1]] = 0
        
        elif abs(xx) > 1:
            start = move[0]
            for m in move:
                deltax = m[0] - start[0]
                deltay = m[1] - start[1]
                if deltax > 0 and deltay > 0 : 
                    if self.board[m[0]-1][m[1]-1] != 0:
                        score += self.board[m[0]-1][m[1]-1]
                        self.board[m[0]-1][m[1]-1] = 0
                elif deltax > 0 and deltay < 0 : 
                    if self.board[m[0]-1][m[1]+1] != 0 :
                        score += self.board[m[0]-1][m[1]+1]
                        self.board[m[0]-1][m[1]+1] = 0
                elif deltax < 0 and deltay > 0 : 
                    if self.board[m[0]+1][m[1]-1] != 0:
                        score += self.board[m[0]+1][m[1]-1]
                        self.board[m[0]+1][m[1]-1] = 0
                elif deltax < 0 and deltay < 0 : 
                    if self.board[m[0]+1][m[1]+1] != 0:
                        score += self.board[m[0]+1][m[1]+1]
                        self.board[m[0]+1][m[1]+1] = 0

                start = m
            self.board[move[-1][0]][move[-1][1]] = pawn
            self.board[move[0][0]][move[0][1]] = 0

        if pawn > 0 : 
            self.score2 -= abs(score)
            if move[-1][0] == 0: 
                self.board[move[-1][0]][move[-1][1]] = 2
                if pawn == 1 : self.score1 += 1

        elif pawn < 0 :
            self.score1 -= abs(score)
            if move[-1][0] == 9: 
                self.board[move[-1][0]][move[-1][1]] = -2
                if pawn == -1 : self.score2 += 1

    def play(self, verbose=True):
        if verbose : self.Show()
        player = -1
        while True :
            a = self.CopyBoard()
            player = -player
            moves, moves2 = self.GetValidMoves(player, Filter=True)
            moves = self.MergeList(moves, moves2)
            if len(moves) == 0 : 
                print(f"player {player} lose")
                break
            move = random.choice(moves)
            self.PushMove(move)
            if self.CompareBoard(a, self.board) :
                print(f"move did not play {move}")
                print(self.board)
                break
            if verbose :
                print(move)
                self.GetScore(verbose=True)
                self.Show()
                if not self.CheckScore() : raise ("probleme de score")
            end = self.EndGame()
            if (end == 2) : 
                print("draw")
                break
            elif (end == 1) :
                print("white win")
                break
            elif (end == -1) : 
                print("black win")
                break


def main():
    game = Checkers()
    game.play(verbose=True)

def main2():
    game = Checkers(clear=True)
    game.board[0][9] = 2
    game.board[1][8] = -2
    game.GetValidMoves(1, Filter=False, verbose=True)
    game.Show()

if "__main__" == __name__:
    main()
    