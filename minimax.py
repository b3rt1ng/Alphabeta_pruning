class mima:
    def __init__(self):
        self.count=0

    def minimax(self,next,ask,d=2):
        self.count+=1
        if d==0 or next.is_over()[0]==True:
            return next.get_score(next.player)
        else:
            if next.player==ask: #alors le joueur actuel est celui qui à appellé minimax, c'est donc un noeud max
                b=float('-inf')
                for i in next.get_moves():
                    m=self.minimax(next.play(i),ask,d-1) #0
                    if b < m:
                        b=m
            else:
                b=float('+inf')
                for i in next.get_moves():
                    m=self.minimax(next.play(i),ask,d-1) #1
                    if b > m:
                        b=m
            return b
