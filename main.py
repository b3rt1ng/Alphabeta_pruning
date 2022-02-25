import os,sys,random,time,argparse,copy
import state as st
import move as mv
import negamax,alphabeta
import minimax as mm
import matplotlib.pyplot as plt

# ---------------- quelques constantes rapides -----------------
BLEU, ROUGE, VERT, MAGENTA, BLANC = '\33[94m', '\033[91m', '\033[1;32m', '\033[1;35m', '\33[97m' #attention, cette méthode d'affichage fonctione sous linux (ANSI escape codes) mais ne marche pas sous tout les os windows ou OSX
grid=[[0 for i in range(7)] for j in range(7)]
state=st.State()
data=[[],[]]
data_turn=[[],[]]

# ---------------------- Argument Parser ----------------------
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,help='Montre une aide aux arguments.')
parser.add_argument('-dr', '--deepness_red', type=int, required=False, default=2, help="Initialisé à 2 s'il n'est pas spécifié. Détermine la profondeur de raisonement des pions rouges.")
parser.add_argument('-db', '--deepness_blue', type=int, required=False, default=2, help="Initialisé à 2 s'il n'est pas spécifié. Détermine la profondeur de raisonement des pions bleus.")
parser.add_argument('-m', '--mode', type=str, required=False, default='minimax', help="Séléctione l'algorythme de jeu. Initialisé sur minimax par défaut.['random','minimax','negamax','alphabeta']")
parser.add_argument('--maxturn', type=int, required=False, default=-1, help="Permet de définir le nombre de tours maximums du jeu. Nombre infini par défaut.")
args = parser.parse_args()
deep={False:args.deepness_red,True:args.deepness_blue}

def show_grid(stat):
    """
    Les pions sont représentés par leur couleurs respectives.
    La couleur verte sert à montrer où le joueur actuel peut se déplacer.
    La couleur magenta signifie que le déplacement mangerais un pion adverse.
    """
    os.system('clear')
    n=[i.next for i in stat.get_moves(stat.player)]
    for i in range(len(grid)):
        for j in range(len(grid)):
            if (i,j) in stat.board[not stat.player] and (i,j) in n:
                sys.stdout.write(MAGENTA+'■ '+BLANC)
            elif (i,j) in stat.board[False]:
                sys.stdout.write(ROUGE+'■ '+BLANC)
            elif (i,j) in stat.board[True]:
                sys.stdout.write(BLEU+'■ '+BLANC)
            elif(i,j) in n:
                sys.stdout.write(VERT+'■ '+BLANC)
            else:
                print('■',end=' ')
        print()
    print('tour:',stat.turn)
    print('score rouge:',stat.get_score(False))
    print('score bleu:',stat.get_score(True))
    time.sleep(.01)

def getBestMove(etat,d=2):
    bestaction=None
    bestvalue=float('-inf')
    c=0
    for i in etat.get_moves():
        next=etat.play(i)
        if args.mode =='minimax':
            minimax=mm.mima()
            value=minimax.minimax(next,next.player,d)
            c+=minimax.count
        elif args.mode =='negamax':
            value=negamax.negamax(next,next.player,d)
        elif args.mode =='alphabeta':
            value=alphabeta.alphabeta(next,next.player,-1,2,d)
        else:
            print("erreur: le mode choisi n'existe pas");exit()
        if value > bestvalue:
            bestvalue=value
            bestaction=i
    if next.player==False:
        data[0].append(c)
        data_turn[0].append(next.turn-1)
    else:
        data[1].append(c)
        data_turn[1].append(next.turn-1)
    return bestaction


def jeu(etat):
    tempo={False:[],True:[]}
    memory=[]
    max_tour=args.maxturn
    while etat.is_over(memory)[0]!=True:
        memory.append(etat)
        n=etat.get_moves(etat.player)
        start=time.time()
        if args.mode =='random':
            etat = etat.play(n[random.randint(0,len(n)-1)])
        else:
            etat = etat.play(getBestMove(etat,deep[etat.player]))
        show_grid(etat)
        if etat.turn == max_tour:
            break
        tempo[etat.player].append(time.time()-start)
    return (etat.is_over(memory)[1],etat)

start = time.time()
try:
    show_grid(state)
    result = jeu(state)
    stop=time.time()
    if result[1].get_score(False)>0.5:
        print("le joueur rouge gagne")
    elif result[1].get_score(True)>0.5:
        print("le joueur bleu gagne")
    else:
        print("égalité")
    print("\nexec time:",time.time()-start,"seconds")
    plt.plot(data_turn[0],data[0],"b--o",label='bleus, deepness='+str(args.deepness_blue))
    plt.plot(data_turn[1],data[1],"r--o",label='rouges, deepness='+str(args.deepness_red))
    plt.title("algorythme: "+args.mode+" sur "+str((result[1].turn if args.maxturn==-1 else args.maxturn-1))+" tours\nexécuté en "+str(round(stop-start,1))+" secondes")
    plt.legend()
    plt.show()
except KeyboardInterrupt:
    print("intrrompu")
    print("\nexec time:",time.time()-start,"seconds")
