import random
double_tas = [None, None]   # indice 0 inutilisé, indice 1 = racine (vide)
                            # chaque case : {"valeur": int, "hauteur": int}


def reinitialiser_double_tas():
    """Remet le double-tas à zéro"""
    global double_tas
    double_tas = [None, None]


# Acces aux cases

def case_occupee(indice: int) -> bool:
    """Vrai si la case contient un élément"""
    return 2 <= indice < len(double_tas) and double_tas[indice] is not None


def valeur_de(indice: int) -> int:
    """Valeur stockée dans la case"""
    return double_tas[indice]["valeur"]


def indice_parent(indice: int) -> int:
    """Indice du parent"""
    return indice // 2


def est_dans_tas_min(indice: int) -> bool:
    """Vrai si la case est dans le sous-arbre gauche (tas min)"""
    h = double_tas[indice]["hauteur"]
    return indice < 2 ** h + 2 ** (h - 1)      # moitié gauche du niveau h


def indice_miroir(indice: int) -> int:
    """Indice de la case au même emplacement dans l'autre sous-arbre"""
    decalage = 2 ** (double_tas[indice]["hauteur"] - 1)

    res = indice - decalage 
    if est_dans_tas_min(indice):
        res = indice + decalage
    return res


def indice_miroir_tas_min(indice: int) -> int:
    """
    Case a comparer avec indice pour la propriété  (e)
    Son miroir si il existe sinon sinon le miroir de son parent. 
    On renvoie -1 si nous n'avons aucune comparaisons nécessaire
    """
    res = -1
    miroir = indice_miroir(indice)
    if case_occupee(miroir):
        res = miroir
    else : 
        parent = indice_parent(indice)
        if parent >= 2:
            res = indice_miroir(parent)           # existe forcément d'après (d)
    return res


def echanger_valeurs(i: int, j: int):
    """Échange les VALEURS (la hauteur appartient à la position, elle ne bouge pas)"""
    temp = double_tas[i]["valeur"]
    double_tas[i]["valeur"] = double_tas[j]["valeur"]
    double_tas[j]["valeur"] = temp


# Remonté dans chacun des tas

def remonter_dans_tas_min(indice: int):
    """Remontée classique dans le tas min (sous-arbre gauche)"""
    parent = indice_parent(indice)
    print("DEBUG sous arbre gauche : On compare l'élement courant avec son père  il doit être supérieur")
    if parent >= 2 and valeur_de(indice) < valeur_de(parent):
        print("DEBUG sous arbre gauche : ", valeur_de(indice), " < ", valeur_de(parent), "on échange donc")
        affiche_arbre()
        echanger_valeurs(indice, parent)
        
        remonter_dans_tas_min(parent)


def remonter_dans_tas_max(indice: int):
    """Remontée classique dans le tas max (sous-arbre droit)"""
    print("DEBUG sous arbre gauche : On compare l'élement courant avec son père  il doit être inférieur")
    parent = indice_parent(indice)
    if parent >= 2 and valeur_de(indice) > valeur_de(parent):
        print("DEBUG sous arbre gauche : ", valeur_de(indice), " > ", valeur_de(parent), "on échange donc")
        affiche_arbre()
        echanger_valeurs(indice, parent)
        
        remonter_dans_tas_max(parent)


def placer_nouvel_element(indice: int):
    """Vérifie la propriété (e) pour le nouvel élément, puis le fait remonter
    dans le bon tas"""
    if est_dans_tas_min(indice):
        miroir = indice_miroir_tas_min(indice)
        if miroir != -1 and valeur_de(indice) > valeur_de(miroir):
            if miroir >0: 

                print("DEBUG sous arbre gauche: Nous échangeons les valeur entre l'élément venant d'etre ajouter et son miroir car", valeur_de(indice), ">", valeur_de(miroir))
            else:
                print("DEBUG sous arbre gauche : Aucun changement car il n'existe pas de valeur miroir")
            affiche_arbre()
            echanger_valeurs(indice, miroir)
            
            remonter_dans_tas_max(miroir)
        else:
            print("DEBUG sous arbre gauche: Nous n'échangeons pas les valeur entre l'élément venant d'etre ajouter et son miroir car",valeur_de(indice), "<", valeur_de(miroir))

            remonter_dans_tas_min(indice)
    else:
        miroir = indice_miroir(indice)         # existe toujours
        if valeur_de(indice) < valeur_de(miroir):
            print("DEBUG sous arbre gauche: Nous échangeons les valeur entre l'élément venant d'etre ajouter et son miroir car", valeur_de(indice), "<", valeur_de(miroir))
            affiche_arbre()
            echanger_valeurs(indice, miroir)
            remonter_dans_tas_min(miroir)
        else:
            print("DEBUG sous arbre gauche: Nous n'échangeons pas les valeur entre l'élément venant d'etre ajouter et son miroir car",valeur_de(indice), ">", valeur_de(miroir))

            remonter_dans_tas_max(indice)


#Insertion 

def inserer(valeur: int):
    """Insère une valeur dans le double-tas"""
    indice = len(double_tas)   # prochaine case libre

    # Hauteur de la nouvelle case ajouté. On la déduit de la case précédente
    if indice == 2:
        print("DEBUG insertion : premier élément ajouté")
        hauteur = 1
    else:
        
        hauteur_precedente = double_tas[indice - 1]["hauteur"]
        if indice == 2 ** (hauteur_precedente + 1):    # le niveau précédent est plein
            print("DEBUG insertion :  Le niveau est plein la hauteur va donc augmenter de 1")
            hauteur = hauteur_precedente + 1
        else:
            print("DEBUG insertion : Le niveau n'est pas plein la hauteur et donc la même que celui de l'élément précédent")
            hauteur = hauteur_precedente

    double_tas.append({"valeur": valeur, "hauteur": hauteur})
    placer_nouvel_element(indice)




#Affichage

def affiche_arbre(indice=1, indentation=""):
    """Affiche l'arbre (sous-arbre droit en haut)"""
    if indice >= len(double_tas) or (double_tas[indice] is None and indice != 1):
        return
    affiche_arbre(2 * indice + 1, indentation + "\t")
    print(indentation + ("•" if double_tas[indice] is None else str(valeur_de(indice))))
    affiche_arbre(2 * indice, indentation + "\t")
    print("-"*25)



#Vérification 

def verifier_tas() -> bool:
    """Vérifie les propriétés (b) et (c) : le sous-arbre gauche est un tas min
    et le sous-arbre droit est un tas max"""
    for indice in range(2, len(double_tas)):
        for fils in (2 * indice, 2 * indice + 1):
            if case_occupee(fils):
                if est_dans_tas_min(indice):
                    if valeur_de(fils) < valeur_de(indice):
                        return False
                else:
                    if valeur_de(fils) > valeur_de(indice):
                        return False
    return True


def verifier_arbre_parfait() -> bool:
    """On vérifie que la proprité (d) soit respecter donc que l'arbre soit parfait"""
    hauteur_max_gauche = 0
    hauteur_max_droite = 0

    for indice in range(2, len(double_tas)):
        if double_tas[indice] is None:
            return False                                   # trou dans le tableau

        hauteur_stockee = double_tas[indice]["hauteur"]
    

        if est_dans_tas_min(indice):
            hauteur_max_gauche = max(hauteur_max_gauche, hauteur_stockee)
        else:
            hauteur_max_droite = max(hauteur_max_droite, hauteur_stockee)

    # (d) : hauteur droite = hauteur gauche ou hauteur gauche - 1
    return hauteur_max_droite in (hauteur_max_gauche, hauteur_max_gauche - 1)


def propriete_e_valide(indice: int) -> bool:
    """Vérifie la propriété (e) pour une case du tas min"""
    if not case_occupee(indice) or not est_dans_tas_min(indice):
        return True

    miroir = indice_miroir_tas_min(indice)
    if miroir == -1:
        return True
    if not case_occupee(miroir):
        return False                                       
    return valeur_de(indice) <= valeur_de(miroir)


def verifier_propriete_e() -> bool:
    """Vérifie la propriété (e) sur tout l'arbre"""
    for indice in range(2, len(double_tas)):
        if not propriete_e_valide(indice):
            return False
    return True


def afficher_verifications():
    """Affiche le résultat de toutes les vérifications"""
    print("Vérification de la propriété e : ", verifier_propriete_e())
    print("Vérification de l'arbre parfait (hauteurs et propriété d) : ", verifier_arbre_parfait())
    print("Vérification des deux tas (gauche min, droit max) : ", verifier_tas())


#Test automatique

def test_automatique(borne_inf: int, borne_sup: int, nb_valeurs: int):
    """Insère nb_valeurs valeurs aléatoires en affichant l'arbre à chaque étape
    puis vérifie toutes les propriétés"""
    for _ in range(nb_valeurs):
        valeur = random.randint(borne_inf, borne_sup)
        inserer(valeur)
        print("\n\n")
        affiche_arbre()
        print("\n\n")

    afficher_verifications()


#Menu

def demander_choix(options_valides: list) -> int:
    """Redemande un entier tant qu'il n'est pas dans options_valides"""
    choix = 0
    while choix not in options_valides:
        try:
            choix = int(input("Veuillez choisir la valeur souhaitée : "))
        except ValueError:
            choix = 0
    return choix


def afficher_menu_principal() -> int:
    """Affiche le menu principal et renvoie le choix"""
    print("\n")
    print("Veuillez choisir une de ces options : ")
    print("1 - Test automatique")
    print("2 - Test manuel")
    print("3 - Test en masse")
    print("4 - Quitter")
    return demander_choix([1, 2, 3, 4])


def demander_parametres_test_auto() -> list:
    """Demande et affiche les paramètres du test automatique"""
    print("\n\nTest de notre arbre de tas hybride en automatique \n")
    nb_tests = int(input("Veuillez choisir le nombre de tests que vous voulez effectuer : "))
    valeur_min = int(input("Veuillez choisir la valeur minimum pouvant être insérée dans l'arbre : "))
    valeur_max = int(input("Veuillez choisir la valeur maximum pouvant être insérée dans l'arbre : "))

    print("\nLes paramètres sélectionnés de ce test automatique sont : ")
    print("Nombre de tests : ", nb_tests)
    print("Valeur minimum : ", valeur_min)
    print("Valeur maximum : ", valeur_max)
    print("\n")

    return [nb_tests, valeur_min, valeur_max]


def afficher_menu_test_manuel() -> int:
    """Affiche le menu du test manuel et renvoie le choix"""
    print("\n")
    print("Menu test manuel")
    print("Veuillez choisir une de ces options : ")
    print("1 - Ajout d'un nombre aléatoire")
    print("2 - Ajout d'un nombre choisi")
    print("3 - Tester la propriété e")
    print("4 - Tester si l'arbre est parfait")
    print("5 - Tester si l'organisation des deux tas est correcte")
    print("6 - Tester l'ensemble des propriétés")
    print("7 - Arrêter le test")
    return demander_choix([1, 2, 3, 4, 5, 6, 7])


#test interactifs

def lancer_tests_automatiques():
    """Enchaîne plusieurs tests automatiques, chacun sur un arbre neuf"""
    nb_tests, valeur_min, valeur_max = demander_parametres_test_auto()

    for numero in range(1, nb_tests + 1):
        print("Test numéro : ", numero)
        nb_valeurs = int(input("Veuillez choisir le nombre de valeurs dans votre arbre numéro "
                               + str(numero) + " : "))
        test_automatique(valeur_min, valeur_max, nb_valeurs)
        reinitialiser_double_tas()


def lancer_test_manuel():
    """Permet d'insérer des valeurs et de tester les propriétés à la demande"""
    valeur_min = None
    valeur_max = None       # demandées au premier ajout aléatoire

    choix = 0
    while choix != 7:
        choix = afficher_menu_test_manuel()

        if choix == 1:
            if valeur_min is None:
                valeur_min = int(input("Veuillez choisir la valeur minimum pouvant être insérée dans l'arbre : "))
                valeur_max = int(input("Veuillez choisir la valeur maximum pouvant être insérée dans l'arbre : "))
                print("\nLes paramètres sélectionnés de ce test manuel sont : ")
                print("Valeur minimum : ", valeur_min)
                print("Valeur maximum : ", valeur_max)
                print("\n")
            inserer(random.randint(valeur_min, valeur_max))
            affiche_arbre()

        elif choix == 2:
            valeur = int(input("Veuillez choisir la valeur que vous voulez ajouter dans l'arbre : "))
            inserer(valeur)
            affiche_arbre()

        elif choix == 3:
            print("Vérification de la propriété e : ", verifier_propriete_e())

        elif choix == 4:
            print("Vérification de l'arbre parfait (hauteurs et propriété d) : ", verifier_arbre_parfait())

        elif choix == 5:
            print("Vérification des deux tas (gauche min, droit max) : ", verifier_tas())

        elif choix == 6:
            afficher_verifications()

    print("Vous avez quitté l'arbre actuel")
    reinitialiser_double_tas()


def lancer_tests_interactifs():
    """Point d'entrée des tests"""
    print("Test : ")
    choix = 0
    while choix != 4:
        choix = afficher_menu_principal()
        if choix == 1:
            lancer_tests_automatiques()
        elif choix == 2:
            lancer_test_manuel()
        elif choix == 3: 
            test_en_masse()


def test_en_masse(nb_arbres=500, taille_max=60):
    """Construit plein d'arbres aléatoires et vérifie toutes les propriétés"""
    for _ in range(nb_arbres):
        reinitialiser_double_tas()
        for _ in range(random.randint(1, taille_max)):
            inserer(random.randint(0, 20))      # petite plage = beaucoup de doublons
        assert verifier_tas() and verifier_propriete_e() and verifier_arbre_parfait()
    print("Tous les arbres sont valides")

lancer_tests_interactifs()