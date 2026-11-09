import random
T = []
dernier_libre = 2


def init_T(): 
    T = [None, None]

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
                m = -1 
            if existe(m) and T[i] > T[m]: 
                echanger(i, m)
                organise_sd(m)
            else: 
                remonter_sg(i)

            
        elif T[i] > T[m]:        # parent = racine : pas de test
            echanger(i, m)
            remonter_sd(m)        # n est maintenant dans le tas inverse
        else: 
            remonter_sg(i)
    else:
        m = miroir(i)             # existe toujours
        if T[i] < T[m]:
            echanger(i, m)
            remonter_sg(m)        # n est maintenant dans le tas
        else:
            remonter_sd(i)


# def organise_sg(i : int): 
#     p = parent(i)
#     if p >= 2 and T[i] < T[p]:
#         echanger(i, p)
#         organise_sg(p)

def organise_sd(i : int): 
    """Réorganisation correcte de notre tas avec le max en haut"""
    p = parent(i)
    if p >= 2 and T[i] > T[p]:
        echanger(i, p)
        organise_sd(p)

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

    

def test(born_inf : int, born_sup: int, nb):



    for i in range(0,nb): 
        v = random.randint(born_inf, born_sup)
        inserer(v)
        print("\n\n")
        affiche_arbre()
        print("\n\n")
    
    print("Vérification de la propriété e : ", verifier_prop_e())
    print("Vérification de la proppriété arbre parfait : ", verifier_arbre_parfait())
    print("Vérification de la propriété de nos deux tas, premier tas normal second tas inversé : ", verifier_tas())

T = [None, None]  # On commence avec T[1]





# for i in range(0, 50): 
#     test(0, 10000)


# for t in [2, 11, 7, 30, 20, 50, 10, 11, 7]: 
#     inserer(t) 
#     print("\n\n\n")
#     affiche_arbre()
#     print(verifier_prop_e())
#     print(verifier_arbre_parfait())
#     print(verifier_tas())



def affiche_menu(): 
    print("\n")
    print("Veuillez choisir une de ces options : ")
    print("1 - Test automatique")
    print("2 - Test Manuelle")
    print("3 - Quitter")
    val = 0
    while (val not in [1,2,3]): 

        val = int(input("Veuillez choisir la valeur souhaité : "))
    return val

def test_auto():
    print("\n\nTest de notre arbre de tas Hybride en automatique \n")
    val = int(input("Veuillez choisir le nombre de test que vous voulez effectuer : ")) 
    val2= int(input("Veuillez choisir la valeur minimum pouvant etre inséré dans l'arbre : "))
    val3 = int(input("Veuillez choisir la valeur maximum pouvant etre inséré dans l'arbre : "))
    
    print("\nLes paramètres sélectionné de ce test automatique sont : ")
    print("Nombre de test : ", val)
    print("Valeur minimum : ", val2)
    print("Valeur maximum : ", val3)
    print("\n")

    return [val, val2, val3]




def menu_test_manuel(): 
    print("\n")
    print("Menu test manuelle")
    print("Veuillez choisir une de ces options : ")
    print("1 - Ajout nombre aléatoire")
    print("2 - Ajout nombre choisis")
    print("3 - Tester la propriété e")
    print("4 - Tester si l'arbre est parfait")
    print("5 - Test si l'organisation des deux tas son correcte")
    print("6 - Tester l'ensemble des propriété")
    print("7 - Arreter le test")
    val = 0
    while (val not in [1,2,3,4,5,6,7]): 

        val = int(input("Veuillez choisir la valeur souhaité : "))
    return val


def test_interactif(): 
    global T, dernier_libre
    print("Test : ")
    val = 0
    while ( val != 3): 
        val = affiche_menu()


        if val == 1 : 
            param = test_auto()
            print(param)
            for i in range(1, param[0] +1 ): 
                print("Test numéro : ", i)
                nb_valeur = int(input("Veuillez chosir le nombre de valeur dans votre arbre numéro " + str(i) + ": "))
                test(param[1], param[2], nb_valeur)
                T = [None, None]
                dernier_libre = 2

        if val == 2: 
            param_act = False
            choix = 0
            while (choix != 7): 
                choix = menu_test_manuel()

                if choix == 1 and not param_act: 
                    param1= int(input("Veuillez choisir la valeur minimum pouvant etre inséré dans l'arbre : "))
                    param2= int(input("Veuillez choisir la valeur maximum pouvant etre inséré dans l'arbre : "))
                    
                    print("\nLes paramètres sélectionné de ce test automatique sont : ")
                    print("Valeur minimum : ", param1)
                    print("Valeur maximum : ", param2)
                    print("\n")
                    
                    param_act = True

                if choix == 1: 
                    inserer(random.randint(param1, param2))
                    affiche_arbre()
                elif choix == 2: 
                    nb = int(input("Veuillez choisir la valeur que vous voulez ajouter dans l'arbre : "))
                    inserer(nb)
                    affiche_arbre()
                elif choix == 3:
                        print("Vérification de la propriété e : ", verifier_prop_e())
                elif choix == 4: 

                    print("Vérification de la proppriété arbre parfait : ", verifier_arbre_parfait())
                elif choix == 5: 

                    print("Vérification de la propriété de nos deux tas, premier tas normal second tas inversé : ", verifier_tas())
                elif choix == 6: 
                        print("Vérification de la propriété e : ", verifier_prop_e())
                        print("Vérification de la proppriété arbre parfait : ", verifier_arbre_parfait())
                        print("Vérification de la propriété de nos deux tas, premier tas normal second tas inversé : ", verifier_tas())
                
            print("Vous avez quitter l'arbre actuelle")
            T = [None, None]
            dernier_libre = 2
                    
test_interactif()









