import numpy as np
import random


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

    def GetScore(self, verbose=False, player=0):
        if self.score1 == 0 : self.score2 = 100
        if self.score2 == 0 : self.score1 = 100
        if verbose : print(f"score {self.score1} - {self.score2}")
        if player == 1 : return self.score1 - self.score2
        elif player == -1 : return self.score2 - self.score1
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
    
    def GetFeatures(self, player, verbose=False):
        features = np.zeros(9)
        metrics = np.zeros(6)
        # 0 est qu'on a gagné
        # 1 nombre de piece blanche
        # 2 nombre de dame blanche
        # 3 nombre de piece noir
        # 4 nombre de dame noir
        # 5 nombre de piece blanche loin
        # 6 nombre de piece noir loin
        # 7 nombre de piece blanche au milieu
        # 8 nombre de piece noir au milieu


        end = self.EndGame()
        if end == player : features[0] = 1
        for i in range(10):
            for j in range(10):
                pawn = self.board[i][j]
                if pawn == 1 : features[1] += 1
                elif pawn == 2 : features[2] += 1
                elif pawn == -1 : features[3] += 1
                elif pawn == -2 : features[4] += 1
                if i < 4 and pawn > 0 : features[5] += 1
                if i > 5 and pawn < 0 : features[6] += 1
                if i < 6 and i > 3 and pawn > 0 : features[7] += 1
                if i < 6 and i > 3 and pawn < 0 : features[8] += 1
        if player < 0 : 
            metrics[0] = 100*features[0]
            metrics[1] = -(features[1] - features[3])
            metrics[2] = -(features[2] - features[4])
            metrics[3] = -(features[5] - features[6])
            metrics[4] = -(features[7] - features[8])
            score = 100*metrics[0] + metrics[1] + 3*metrics[2] + 2*metrics[3] + 1*metrics[4]
            if score >= 0 : metrics[5] = 1
            else : metrics[5] = -1
        
        if player > 0 : 
            metrics[0] = 100*features[0]
            metrics[1] = (features[1] - features[3])
            metrics[2] = (features[2] - features[4])
            metrics[3] = (features[5] - features[6])
            metrics[4] = (features[7] - features[8])
            score = 100*metrics[0] + metrics[1] + 3*metrics[2] + 2*metrics[3] + 1*metrics[4]
            if score >= 0 : metrics[5] = 1
            else : metrics[5] = -1

        if verbose : print(player, metrics)

        return metrics

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
        return (a < 0 and b <0) or (a > 0 and b > 0)
    
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
        
    def GetValidMoves(self, player=1,Filter=True, verbose=False):
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
        liste = self.MergeList(moves, moves2)
        return liste
    
    def CompareBoard(self, a, b):
        for i in range(10):
            for j in range(10):
                if a[i][j] != b[i][j] : return False
        return True

    def CopyBoard(self):
        tab = np.zeros((10,10))
        for i in range(10):
            for j in range(10):
                tab[i][j] = self.board[i][j]
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

    def playrandom(self, verbose=False, GetFeatures=False, ArrayFeatures=[]):
        if verbose : self.Show()
        player = -1
        while True :
            a = self.CopyBoard()
            player = -player
            moves = self.GetValidMoves(player, Filter=True)
            if len(moves) == 0 : 
                if verbose : print(f"player {player} lose")
                if GetFeatures : return player, ArrayFeatures
                return player
            move = random.choice(moves)
            self.PushMove(move)
            if self.CompareBoard(a, self.board) :
                print(f"move did not play {move}")
                print(self.board)
                break
            if verbose :
                print(move)
                self.GetScore(verbose=True)
                self.GetFeatures(player, verbose=True)
                self.Show()
            
            if GetFeatures : ArrayFeatures.append(self.CopyBoard(), self.GetFeatures(player))
            end = self.EndGame()
            if (end == 2) : 
                if verbose : print("draw")
                if GetFeatures : return 0, ArrayFeatures
                return 0
            elif (end == 1) :
                if verbose : print("white win")
                if GetFeatures : return 1, ArrayFeatures
                return 1
            elif (end == -1) : 
                if verbose : print("black win")
                if GetFeatures : return -1, ArrayFeatures
                return -1

    def SetBoard(self, tab):
        for i in range(10):
            for j in range(10):
                self.board[i][j] = tab[i][j]

    def minmax(self, player, RL=False, verbose=False):
        Leafs = []
        FinalMoves = []
        b1 = self.CopyBoard() 
        s1 = self.score1
        s2 = self.score2          
        moves = self.GetValidMoves(player, Filter=True)
        for m1 in moves :
            self.SetBoard(b1)
            self.score1 = s1
            self.score2 = s2
            self.PushMove(m1)
            b2 = self.CopyBoard()
            s21 = self.score1
            s22 = self.score2
            Moves = self.GetValidMoves(-player, Filter=True)
            if len(Moves) == 0 : Leafs.append((m1, 100, self.GetFeatures(player)))
            for m2 in Moves:
                self.SetBoard(b2)
                self.score1 = s21
                self.score2 = s22
                self.PushMove(m2)
                Leafs.append((m1, self.GetScore(verbose=False, player=player),self.GetFeatures(player)))
        self.board = b1
        self.score1 = s1
        self.score2 = s2
        maximum = -200
        for leaf in Leafs:
            if leaf[1] > maximum :
                maximum = leaf[1]
                FinalMoves.clear()
                if not self.CheckIfInside(leaf[0][0], leaf[0][1], FinalMoves) : FinalMoves.append(leaf[0])
            elif leaf[1] == maximum :
                if not self.CheckIfInside(leaf[0][0], leaf[0][1], FinalMoves) : FinalMoves.append(leaf[0])
        
        if verbose : print(FinalMoves) ; print(Leafs)
        if RL : return Leafs
        return FinalMoves

    def PlayMinMax(self, player, verbose=False, GetFeatures=False, ArrayFeatures=[]):
        a = self.CopyBoard()
        moves = self.GetValidMoves(player, Filter=True)
        if len(moves) == 0 : 
            if verbose : print(f"player {player} lose")
            if GetFeatures : return -player, ArrayFeatures
            return -player
        move = random.choice(self.minmax(player))
        self.PushMove(move)
        if self.CompareBoard(a, self.board) :
            print(f"move did not play {move}")
            print(self.board)
        if verbose :
            print(move)
            self.GetScore(verbose=True)
            self.GetFeatures(player, verbose=True)
            self.Show()
        if GetFeatures : ArrayFeatures.append((self.CopyBoard(), self.GetFeatures(player)))
        end = self.EndGame()
        if (end == 1) :
            if verbose : print("white win")
            if GetFeatures : return 1, ArrayFeatures
            return 1
        elif (end == -1) : 
            if verbose : print("black win")
            if GetFeatures : return -1, ArrayFeatures
            return -1   

    def playRandomMinMax(self, Bot1="random", Bot2="random", verbose=False, GetFeatures=False, ArrayFeatures=[]):
        if verbose : self.Show()
        player = -1
        NumberOfMoves = 0
        while True :
            player = -player
            if (player == 1):
                a = self.CopyBoard()
                moves = self.GetValidMoves(player, Filter=True)
                if len(moves) == 0 : 
                    if verbose : print(f"player {player} lose")
                    if GetFeatures : return -player, ArrayFeatures
                    return -player
                if Bot1 == "random" : move = random.choice(moves)
                elif Bot1 == "minmax" : move = random.choice(self.minmax(1))
                else : raise(f"Do not know the type of bot {Bot1}")
                self.PushMove(move)
                if self.CompareBoard(a, self.board) :
                    print(f"move did not play {move}")
                    print(self.board)
                    break
                if GetFeatures : ArrayFeatures.append(self.GetFeatures(player))
                if verbose :
                    print(move)
                    self.GetScore(verbose=True)
                    self.GetFeatures(player, verbose=True)
                    self.Show()
                end = self.EndGame()
                if (end == 1) :
                    if verbose : print("white win")
                    if GetFeatures : return 1, ArrayFeatures
                    return 1
                elif (end == -1) : 
                    if verbose : print("black win")
                    if GetFeatures : return -1, ArrayFeatures
                    return -1
            elif player == -1:
                a = self.CopyBoard()
                moves = self.GetValidMoves(player, Filter=True)
                if len(moves) == 0 : 
                    if verbose : print(f"player {player} lose")
                    if GetFeatures : return -player, ArrayFeatures
                    return -player
                if Bot2 == "random" : move = random.choice(moves)
                elif Bot2 == "minmax" : move = random.choice(self.minmax(-1))
                else : raise(f"Do not know the type of bot {Bot2}")
                self.PushMove(move)
                if self.CompareBoard(a, self.board) :
                    print(f"move did not play {move}")
                    print(self.board)
                    break
                if GetFeatures : ArrayFeatures.append(self.GetFeatures(player))
                if verbose :
                    print(move)
                    self.GetScore(verbose=True)
                    self.GetFeatures(player, verbose=True)
                    self.Show()
                end = self.EndGame()
                if (end == 1) :
                    if verbose : print("white win")
                    if GetFeatures : return 1, ArrayFeatures
                    return 1
                elif (end == -1) : 
                    if verbose : print("black win")
                    if GetFeatures : return -1, ArrayFeatures
                    return -1    
            NumberOfMoves += 2   
            if (NumberOfMoves > 1000):
                return 0, ArrayFeatures   

    def GetNextBoards(self, player, verbose=False):
        b = self.CopyBoard()
        boards = []
        moves = self.GetValidMoves(player)
        for m in moves:
            self.PushMove(m)
            boards.append(self.CopyBoard())
            self.SetBoard(b)
        if verbose : print(boards)
        return boards, moves
    
    def CompressBoard(self, player, board,  verbose=False):
        tab = np.zeros((10,5))
        tab2 = np.zeros((1,50))
        if player == 1:
            for i in range(10):
                for j in range(5):
                    tab[i][j] = board[i][2*j+((i+1)%2)]
        
        elif player == -1:
            for i in range(10):
                for j in range(5):
                    tab[9-i][4-j] = -board[i][2*j+((i+1)%2)]

        for i in range(len(tab)):
            for j in range(len(tab[0])):
                tab2[0][i*5+j] = tab[i][j]
        if verbose : 
            print(tab2)
            print(tab)
        return tab

def main():
    game = Checkers()
    game.minmax(1, RL=True, verbose=True)

def main2():
    game = Checkers()
    game.CompressBoard(-1,game.board, verbose=True)
    



if "__main__" == __name__:
    main()
    