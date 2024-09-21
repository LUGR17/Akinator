import json

# Charger la base de données JSON
def charger_donnees():
    with open('personnalites.json', 'r') as file:
        return json.load(file)

def sauvegarder_donnees(personnalites):
    with open('personnalites.json', 'w') as file:
        json.dump(personnalites, file, indent=4)

def choisir_meilleure_question(candidats, questions_posees):
    meilleure_question = None
    meilleur_score = float('inf')  # On cherche à minimiser la différence

    for question in list(candidats[0].keys())[1:]:  # Ignorer la première clé (nom)
        if question in questions_posees:  # Ignorer les questions déjà posées
            continue
        
        oui_count = sum(1 for c in candidats if c.get(question, False))
        non_count = len(candidats) - oui_count

        # Ne pas compter si la question n'est pas présente
        if oui_count + non_count > 0:
            difference = abs(oui_count - non_count)
            if difference < meilleur_score:
                meilleur_score = difference
                meilleure_question = question

    return meilleure_question

def poser_questions(personnalites):
    candidats = personnalites
    questions_posees = []  # Liste pour garder trace des questions posées
    reponses_utilisateur = {}  # Dictionnaire pour stocker les réponses de l'utilisateur

    while len(candidats) > 1:
        question = choisir_meilleure_question(candidats, questions_posees)
        
        if question is None:  # Si aucune question valable n'est trouvée
            print("Je ne peux plus poser de questions.")
            break
        
        reponse_utilisateur = input(f"{question} (oui/non): ").strip().lower()
        questions_posees.append(question)  # Ajouter la question à la liste
        
        # Stocker la réponse de l'utilisateur
        reponses_utilisateur[question] = reponse_utilisateur in ['oui', 'o']
        
        if reponse_utilisateur in ['oui', 'o']:
            candidats = [c for c in candidats if c.get(question, False)]
        else:
            candidats = [c for c in candidats if not c.get(question, False)]

    # Annonce le résultat
    if candidats:
        print(f"Je pense que le personnage est: {candidats[0]['nom']}")
        reponse_correcte = input("Est-ce correct ? (oui/non): ").strip().lower()

        if reponse_correcte not in ['oui', 'o']:
            nom_personnage = input("Quel est le nom du personnage ? ").strip()
            if any(c['nom'].lower() == nom_personnage.lower() for c in personnalites):
                print("Ce personnage est déjà dans la base de données.")
                # Mettre à jour les informations ici
            else:
                print("Ajout du personnage à la base de données.")
                # Créer le nouveau personnage basé sur les réponses
                nouveau_personnage = {"nom": nom_personnage}

                # Remplir les caractéristiques basées sur les réponses précédentes
                for question in questions_posees:
                    nouveau_personnage[question] = reponses_utilisateur[question]

                personnalites.append(nouveau_personnage)
                sauvegarder_donnees(personnalites)

    else:
        print("Je n'ai pas pu trouver de personnage.")

# Appel de la fonction
personnalites = charger_donnees()
poser_questions(personnalites)
