import random
T = []
dernier_libre = 2


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
    global dernier_libre

    # On cherche a trouver la nouvelle position

    while  dernier_libre < len(T) and T[dernier_libre] is not None: 
        dernier_libre = dernier_libre + 1

    if dernier_libre == len(T): 
        T.append(None)
    T[dernier_libre] = x

    remonter(dernier_libre)

    return None





def affiche_arbre(i=1, c=""):
    
    if i >= len(T) or (T[i] is None and i != 1):
        return

    affiche_arbre(2 * i + 1, c + "\t")
    print(c + ("•" if T[i] is None else str(T[i])))
    affiche_arbre(2 * i, c + "\t")

def sup(v1: int, v2: int)->bool: 
    return v1 >= v2

def inf(v1: int, v2: int)->bool: 
    return v1 <= v2

def compare_fils(i: int, compare)->bool: 
    if not existe(i):
        return True
    fg, fd = 2 * i, 2 * i + 1
    res = True
    if existe(fg):
        res = compare(T[i], T[fg])
    if res and existe(fd):
        res = compare(T[i], T[fd])
    return res


def verifier_tas(): 
    res = True
    niveau_g = ligne_tab(len(T))
    i = 1
    while res and i < niveau_g: 
        j = 0
        while res and j < (2**i) //2 : 
            res = compare_fils(2**i + j, inf)
            j+=1

        while res and j >= (2**i) // 2 and j < 2**i: 
            res = compare_fils(2**i +j, sup)
            j+=1
        i +=1

    
    return res



def verifier_arbre_parfait(): 
    i = 2
    none_act = False
    res = True

    while i < len(T) and res: 
        if T[i] is None: 
            none_act = True
        elif T[i] is not None and none_act: 
            res = False

        i = i + 1

    return res
    
def prop_e(index: int)-> bool:
    res = True 
    if existe(index): 

        m = miroir(index)
        if existe(m): 
            res = T[index] <= T[m]
        else: 
            res= T[index] <= T[parent(m)]
    return res



def verifier_prop_e()->bool: 
    taille = ligne_tab(dernier_libre)

    for i in range(1, taille +1): 

        for j in range(2**i, 2**(i+1) // 2): 
            if not prop_e(2**i+j): 
                return False

    return True

    

def test(born_inf : int, born_sup: int):

    nb = random.randint(born_inf, born_sup)


    for i in range(0,nb): 
        v = random.randint(born_inf, born_sup)
        inserer(v)
    print(verifier_prop_e())
    print(verifier_arbre_parfait())
    print(verifier_tas())

T = [None, None]  # On commence avec T[1]





for i in range(0, 50): 
    test(0, 10000)


# for t in [2, 11, 7, 30]: 
#     inserer(t) 
#     print("\n\n\n")
#     affiche_arbre()


# print(verifier_prop_e())
# print(verifier_arbre_parfait())
# print(verifier_tas())











