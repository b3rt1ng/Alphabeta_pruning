def alphabeta(next,ask,alpha,beta,d=2):
    if d==0 or next.is_over()[0]==True:
        return next.get_score(next.player)
    else:
        if next.player==ask:
            for i in next.get_moves():
                alpha=max(alpha,alphabeta(next.play(i),ask,alpha,beta,d-1))
                if alpha>=beta:
                    return alpha
            return alpha
        else:
            for i in next.get_moves():
                beta=min(beta,alphabeta(next.play(i),ask,alpha,beta,d-1))
                if alpha>=beta:
                    return beta
            return beta
