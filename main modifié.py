import os

commande = ''

#default values
param = {'bdd': [(1,3,10, "2024-05-11"),(2,1,13,"2024-05-13"), (3,2,6, "2024-05-15"), (3,1,8, "2024-05-17") ],
         'nages': [(1, "Brasse"), (2, "Dos"), (3, "Crawl")],
         'nageurs': [(1, "Pierre"), (2, "Paul"), (3, "Léa")]
        }


def reset(param):
    '''réinitialise la bdd'''
    param.clear()
    param['bdd'] = []
    param['nages'] = []
    param['nageurs'] = []


def get_str_from_num_in_list(num, liste):
    """Return str from num into liste"""
    for elt in liste:
        if elt[0]==num:
            return elt[1]
    #la ligne suivante ne devrait jamais être exécutée
    return "unknown"


def cmd_individu(param):
    """Ajoute un nouveau najeur"""
    prénom = input("Prénom du nouveau nageur ? ")
    id = len(param['nageurs'])+1
    param['nageurs'].append( (id,prénom ))
    print(param['nageurs'])


def cmd_nouvelle_nage(param):
    """Ajoute une nouvelle nage au logiciel"""
    nage = input("Quelle nage enregistrer ? ")
    id = len(param['nages'])+1
    param['nages'].append( (id,nage ))
    print(param['nages'])


def cmd_ajout(param):
    """Ajoute un évènement à la liste"""
    for elt in param['nageurs']:
        print(f"{elt[0]:5} : {elt[1]}")
    a = int(input("Nageur n° ? "))
    for elt in param['nages']:
        print(f"{elt[0]:5} : {elt[1]}")
    b = int(input("Nage n° ? "))
    c = int(input("combien de longueur ? "))
    param['bdd'].append((a,b,c))


def cmd_liste(param):
    """Affiche toutes les performances des nageurs"""
    print("Prénom      |  nage   |  longueur |  date")
    print("---------------------------------")
    for elt in param['bdd']:
        nageur = get_str_from_num_in_list(elt[0], param['nageurs'])
        nage = get_str_from_num_in_list(elt[1], param['nages'])
        print(f" {nageur:11}| {nage:8}|  {elt[2]}| {elt[3]}")


def cmd_nageur(param):
    """Affiche toutes les performances d'un nageur"""
    for elt in param['nageurs']:
        print(f"{elt[0]:5} : {elt[1]}")
    tmp = int(input("Quel numéro de nageur ? "))
    print("Performances de ", tmp)
    print("  nage   |  longueur |  date")
    print("--------------------")
    for elt in param['bdd']:
        if elt[0]== tmp:
            nage = get_str_from_num_in_list(elt[1], param['nages'])
            print(f" {nage:8}|  {elt[2]}|  {elt[3]}")


def cmd_nage(param):
    """Affiche toutes les performances suivant une nage donnée"""
    for elt in param['nages']:
        print(f"{elt[0]:5} : {elt[1]}")
    tmp = int(input("Quel numéro de nage ? "))
    print("Nage ", tmp)
    print(" Nageur     |  longueur |  date")
    print("------------------------")
    for elt in param['bdd']:
        if elt[1]== tmp:
            nageur = get_str_from_num_in_list(elt[0], param['nageurs'])
            print(f" {nageur:11}|  {elt[2]}|{elt[3]}")


def cmd_exit(param):
    tmp = input("En êtes-vous sûr ? (o)ui/(n)on ")
    if tmp == 'o':
        cmd_save(param, 'save.backup')
        return False
    else:
        return True


def cmd_save(param, filename = 'save.csv'):
    '''sauvegarde complète de la BDD'''
    fichier = open(filename, 'w')
    # sauvegarde des nageurs
    fichier.write('@ nageurs\n')
    for elt in param['nageurs']:
        fichier.write(str(elt[0])+','+str(elt[1])+"\n")
    # sauvegarde des nages
    fichier.write('@ nages\n')
    for elt in param['nages']:
        fichier.write(str(elt[0])+','+str(elt[1])+"\n")
    # sauvegarde des données
    fichier.write('@ bdd\n')
    for elt in param['bdd']:
        fichier.write(str(elt[0])+','+str(elt[1])+','+str(elt[2])+','+str(elt[3])+"\n")
    fichier.close()


def cmd_load(param, filename = 'save.csv'):
    '''chargement complet la BDD avec réinitialisation'''
    reset(param)
    key = ''
    fichier = open(filename, 'r')
    for line in fichier:
        line.strip()
        if line[-1] == '\n':
            line = line[:-1]
        if line[0]=='#':
            continue
        if line[0]=='@':
            key = line[2:]
            continue
        if key =='':
            continue
        tmp = line.split(',')
        # convertion en int de ce qui doit l'être
        if key == 'bdd':
            for i in range(len(tmp)):
                tmp[i] = int(tmp[i])
        if key == 'nages' or key == 'nageurs':
            tmp[0] = int(tmp[0])
        param[key].append(tuple(tmp))
    fichier.close()


#
#   Programme principal
#
isAlive = True
if os.path.exists('save.backup'):
    cmd_load(param, 'save.backup')
while isAlive:
    commande = input("Que faut-il faire ? ")
    print(" 1: ajout d'une performance")
    print(" 2: ajout d'un individu")
    print(" 3: ajout d'une nouvelle nage")
    print(" 4: liste toutes les performances")
    print(" 5: liste les performances d'un nageur")
    print(" 6: liste tous les nageurs pratiquants une nage")
    print(" 7: sauvegarde les données utilisateurs")
    print(" 8: charge les données utilisateurs")
    print(" 0: quitte le logiciel")
    if commande == '1':
        cmd_ajout(param)
        continue
    if commande == '2':
        cmd_individu(param)
        continue

    if commande == '3':
        cmd_nouvelle_nage(param)
        continue

    if commande == '4':
        cmd_liste(param)
        continue

    if commande == '5':
        cmd_nageur(param)
        continue

    if commande == '6':
        cmd_nage(param)
        continue

    if commande == '7':
        cmd_save(param)
        continue

    if commande == '8':
        cmd_load(param)
        continue

    if commande == '0':
        isAlive = cmd_exit(param)
        continue

    print(f"Commande {commande} inconnue")