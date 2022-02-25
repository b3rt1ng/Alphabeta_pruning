def negamax(next,ask,d=2):
    if d==0 or next.is_over()[0]==True:
        if next.player==ask:
            return next.get_score(next.player)
        else:
            return -next.get_score(next.player)
    else:
        m=float('-inf')
        for i in next.get_moves():
            m=max(m,-negamax(next.play(i),ask,d-1))
        return m
    return None
