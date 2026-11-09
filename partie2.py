
T = []
nb_g = 0
nb_d = 0


def ligne_tab(nb: int) -> int:
    """Renvoie le niveau local ( borne inférieur de notre intervalle )"""
    res = 0                       # niveau trouvé
    i = 1                         # puissance de deux en cour
    if nb == 0:
        return -1                 
    while i * 2 <= nb:            # tant que la puissance de deux est dans nb
        i *= 2
        res += 1
    return res



def existe(i: int) -> bool:
    """Vrai si la case i contient un element"""
    return 2 <= i < len(T) and T[i] is not None


def parent(i: int) -> int:
    return i // 2                


def dans_sg(i: int) -> bool:
    """Vrai si i est dans le sous arbre gauche"""
    d = ligne_tab(i)              # niveau global
    return i < 2 ** d + 2 ** (d - 1)   # moitié gauche du niveau d


def miroir(i: int) -> int:
    """Indice de la case au meme emplacement dans l'autre arbre"""
    d = ligne_tab(i)
    h = 2 ** (d - 1)              # decalage entre sg et sd 
    if dans_sg(i):
        return i + h
    return i - h


def echanger(i: int, j: int):
    temp = T[i]
    T[i] = T[j]
    T[j] = temp

def remonter(i: int):
    if dans_sg(i):
        # miroir de i s'il existe sinon celui du parent
        m = miroir(i)
        if not existe(m):
            p = parent(i)
            if p >= 2:
                m = miroir(p)
            else:
                m = -1            # parent = racine : pas de test
        if existe(m) and T[i] > T[m]:
            echanger(i, m)
            remonter_sd(m)        # n est maintenant dans le tas inverse
            return
        remonter_sg(i)
    else:
        m = miroir(i)             # existe toujours
        if T[i] < T[m]:
            echanger(i, m)
            remonter_sg(m)        # n est maintenant dans le tas
            return
        remonter_sd(i)


def remonter_sg(i: int):
    """ Etape de mise a jour du tas avec le mini en haut"""
    p = parent(i)
    if p >= 2 and T[i] < T[p]:
        echanger(i, p)
        remonter(p)


def remonter_sd(i: int):
    """Etape de mise a jour du tas avec le max en haut"""
    p = parent(i)
    if p >= 2 and T[i] > T[p]:
        echanger(i, p)
        remonter(p)




def inserer(x: int):
    global nb_g, nb_d

    # On cherche a trouver la nouvelle position

    if nb_g == nb_d:                  #meme taille on insere a gauche
        j = nb_g + 1                  # rang du nouveau nœud dans Sg 
        l = ligne_tab(j)
        p = 2 ** (l + 1) + (j - 2 ** l)
        nb_g += 1
    else:                             # sinon droite
        j = nb_d + 1
        l = ligne_tab(j)
        p = 2 ** (l + 1) + 2 ** l + (j - 2 ** l)   
        nb_d += 1

    # Le tableau a des trous
    while len(T) <= p:
        T.append(None)

    T[p] = x

    remonter(p)

    return None





def affiche_arbre(i=1, c=""):
    
    if i >= len(T) or (T[i] is None and i != 1):
        return

    affiche_arbre(2 * i + 1, c + "\t")
    print(c + ("•" if T[i] is None else str(T[i])))
    affiche_arbre(2 * i, c + "\t")



T = [None, None]  # On commence avec T[1]
nb_g = nb_d = 0
for x in [15, 3, 40, 8, 27, 1, 60, 5, 41, 21, 11, 71, 111, 152, 634, 85, 47, 14, 21, 100, 99]:
    inserer(x)
affiche_arbre()













