import move as mv
import copy
mask_diag=((-2,-2),(-2,0),(-2,2),(0,-2),(0,2),(2,-2),(2,0),(2,2))
mask_cube=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))


class State:
    def __init__(self):
        self.board={False:[(0,0),(6,6)],True:[(0,6),(6,0)]}
        self.player=False
        self.turn=1
        self.haspassed=[False,False]

    def __hash__(self):
        # retourne une version hashée de board
        return hash(tuple(self.board[False])+(tuple(self.board[True])))

    def __eq__(self,autre):
        return (self.board == autre.board and self.player == autre.player)

    def get_score(self,player):
        return len(self.board[player])/(len(self.board[not player])+len(self.board[player]))

    def is_over(self,statelist=[]):
        if len(self.board[False])==0:
            return (True,"le joueur rouge à gagné.")
        elif len(self.board[True])==0:
            return (True,"le joueur bleu à gagné.")
        elif self in statelist:
            return (True,"boucle, l'état est déjà arrivé.")
        elif False not in self.haspassed:
            return (True,"les deux joeurs passent leur tour.")
        else:
            return (False,"le nombre max de tour est atteint.")

    def get_moves(self,player=None):
        if player==None:
            player=self.player
        moves=[]
        for i in range(len(self.board[player])):
            current = self.board[player]
            temp=[]
            for j in range(16):
                dumb = (current[i][0]-(mask_cube+mask_diag)[j][0],current[i][1]-(mask_cube+mask_diag)[j][1])
                if dumb not in self.board[player] and 0<=dumb[0]<=6 and 0<=dumb[1]<=6:
                    moves.append(mv.Move(self.board[player][i],dumb))
        return moves

    def play(self,move):
        n = copy.deepcopy(self)
        def passing(classe,queue):
            classe.haspassed=classe.haspassed[-1:]
            classe.haspassed.append(queue)
        if move.next != None:
            n.board[n.player].append(move.next)
            if move.next in n.board[not n.player]:
                n.board[not n.player].remove(move.next)
            for i in range(len(mask_cube)):
                r = (move.next[0]-mask_cube[i][0],move.next[1]-mask_cube[i][1])
                if r in n.board[not n.player]:
                    n.board[not n.player].remove(r)
                    n.board[n.player].append(r)
            if ((move.current[0]-move.next[0])**2+(move.current[1]-move.next[1])**2)**0.5>=2: #sqrt((x2-x1)²-(y2-y1)²)
                n.board[n.player].remove(move.current)
            n.player=not n.player
            n.turn+=1
            passing(n,False)
            return n
        else:
            n.player=not n.player
            n.turn+=1
            passing(n,True)
            return n
