from models.etudiant import Etudiant
from models.cours import Cours
from models.inscription import Inscription
from models.note import Note

def afficher_titre(titre):
    print("\n" + "=" * 60)
    print(f"  {titre}")
    print("=" * 60)

def menu_etudiants():
    while True:
        afficher_titre("GESTION DES ÉTUDIANTS")
        print("1. Lister les étudiants")
        print("2. Ajouter un étudiant")
        print("3. Modifier un étudiant")
        print("4. Supprimer un étudiant")
        print("5. Retour")
        choix = input("Choix : ")
        if choix == "1":
            etudiants = Etudiant.tous()
            if not etudiants:
                print("Aucun étudiant trouvé.")
            else:
                print(f"\n{'ID':<26} {'Matricule':<12} {'Nom':<15} {'Prénom':<15} {'Email':<25} {'Téléphone':<15}")
                print("-" * 110)
                for e in etudiants:
                    print(f"{str(e['_id']):<26} {e['matricule']:<12} {e['nom']:<15} {e['prenom']:<15} {e['email']:<25} {e['telephone']:<15}")
        elif choix == "2":
            matricule = input("Matricule : ")
            nom = input("Nom : ")
            prenom = input("Prénom : ")
            email = input("Email : ")
            telephone = input("Téléphone : ")
            date_naissance = input("Date de naissance (AAAA-MM-JJ) : ")
            adresse = input("Adresse : ")
            Etudiant.creer(matricule, nom, prenom, email, telephone, date_naissance, adresse)
        elif choix == "3":
            id_ = input("ID de l'étudiant à modifier : ")
            etudiant = Etudiant.chercher_par_id(id_)
            if not etudiant:
                print("Étudiant non trouvé.")
                continue
            print("Laissez vide pour ne pas modifier.")
            nom = input(f"Nom [{etudiant['nom']}] : ") or etudiant['nom']
            prenom = input(f"Prénom [{etudiant['prenom']}] : ") or etudiant['prenom']
            email = input(f"Email [{etudiant['email']}] : ") or etudiant['email']
            telephone = input(f"Téléphone [{etudiant['telephone']}] : ") or etudiant['telephone']
            adresse = input(f"Adresse [{etudiant['adresse']}] : ") or etudiant['adresse']
            Etudiant.modifier(id_, {"nom": nom, "prenom": prenom, "email": email, "telephone": telephone, "adresse": adresse})
        elif choix == "4":
            id_ = input("ID de l'étudiant à supprimer : ")
            Etudiant.supprimer(id_)
        elif choix == "5":
            break

def menu_cours():
    while True:
        afficher_titre("GESTION DES COURS")
        print("1. Lister les cours")
        print("2. Ajouter un cours")
        print("3. Modifier un cours")
        print("4. Supprimer un cours")
        print("5. Retour")
        choix = input("Choix : ")
        if choix == "1":
            cours_list = Cours.tous()
            if not cours_list:
                print("Aucun cours trouvé.")
            else:
                print(f"\n{'ID':<26} {'Code':<10} {'Intitulé':<35} {'Crédit':<8} {'Enseignant':<20}")
                print("-" * 100)
                for c in cours_list:
                    print(f"{str(c['_id']):<26} {c['code']:<10} {c['intitule']:<35} {c['credit']:<8} {c['enseignant']:<20}")
        elif choix == "2":
            code = input("Code du cours : ")
            intitule = input("Intitulé : ")
            credit = int(input("Crédit : "))
            enseignant = input("Enseignant : ")
            Cours.creer(code, intitule, credit, enseignant)
        elif choix == "3":
            id_ = input("ID du cours à modifier : ")
            cours = Cours.chercher_par_id(id_)
            if not cours:
                print("Cours non trouvé.")
                continue
            print("Laissez vide pour ne pas modifier.")
            intitule = input(f"Intitulé [{cours['intitule']}] : ") or cours['intitule']
            credit = input(f"Crédit [{cours['credit']}] : ")
            credit = int(credit) if credit else cours['credit']
            enseignant = input(f"Enseignant [{cours['enseignant']}] : ") or cours['enseignant']
            Cours.modifier(id_, {"intitule": intitule, "credit": credit, "enseignant": enseignant})
        elif choix == "4":
            id_ = input("ID du cours à supprimer : ")
            Cours.supprimer(id_)
        elif choix == "5":
            break

def menu_inscriptions():
    while True:
        afficher_titre("GESTION DES INSCRIPTIONS")
        print("1. Lister les inscriptions")
        print("2. Inscrire un étudiant à un cours")
        print("3. Inscriptions par étudiant")
        print("4. Inscriptions par cours")
        print("5. Supprimer une inscription")
        print("6. Retour")
        choix = input("Choix : ")
        if choix == "1":
            inscriptions = Inscription.tous()
            if not inscriptions:
                print("Aucune inscription trouvée.")
            else:
                print(f"\n{'ID':<26} {'ID Étudiant':<26} {'ID Cours':<26} {'Année Acad.':<15} {'Date Insc.':<15}")
                print("-" * 110)
                for ins in inscriptions:
                    print(f"{str(ins['_id']):<26} {str(ins['id_etudiant']):<26} {str(ins['id_cours']):<26} {ins['annee_academique']:<15} {ins['date_inscription']:<15}")
        elif choix == "2":
            id_etudiant = input("ID de l'étudiant : ")
            id_cours = input("ID du cours : ")
            annee = input("Année académique (ex: 2025-2026) : ")
            Inscription.creer(id_etudiant, id_cours, annee)
        elif choix == "3":
            id_etudiant = input("ID de l'étudiant : ")
            inscriptions = Inscription.chercher_par_etudiant(id_etudiant)
            if not inscriptions:
                print("Aucune inscription trouvée pour cet étudiant.")
            else:
                for ins in inscriptions:
                    cours = Cours.chercher_par_id(ins['id_cours'])
                    nom_cours = cours['intitule'] if cours else "Inconnu"
                    print(f"  Cours : {nom_cours} | Année : {ins['annee_academique']} | Date : {ins['date_inscription']}")
        elif choix == "4":
            id_cours = input("ID du cours : ")
            inscriptions = Inscription.chercher_par_cours(id_cours)
            if not inscriptions:
                print("Aucune inscription trouvée pour ce cours.")
            else:
                for ins in inscriptions:
                    etu = Etudiant.chercher_par_id(ins['id_etudiant'])
                    nom_etu = f"{etu['prenom']} {etu['nom']}" if etu else "Inconnu"
                    print(f"  Étudiant : {nom_etu} | Année : {ins['annee_academique']}")
        elif choix == "5":
            id_ = input("ID de l'inscription à supprimer : ")
            Inscription.supprimer(id_)
        elif choix == "6":
            break

def menu_notes():
    while True:
        afficher_titre("GESTION DES NOTES")
        print("1. Lister toutes les notes")
        print("2. Ajouter une note")
        print("3. Notes d'un étudiant")
        print("4. Notes d'un cours")
        print("5. Moyenne d'un étudiant par cours")
        print("6. Moyenne générale d'un étudiant")
        print("7. Modifier une note")
        print("8. Supprimer une note")
        print("9. Retour")
        choix = input("Choix : ")
        if choix == "1":
            notes = Note.tous()
            if not notes:
                print("Aucune note trouvée.")
            else:
                print(f"\n{'ID':<26} {'ID Étudiant':<26} {'ID Cours':<26} {'Note':<6} {'Type':<12} {'Date':<15}")
                print("-" * 115)
                for n in notes:
                    print(f"{str(n['_id']):<26} {str(n['id_etudiant']):<26} {str(n['id_cours']):<26} {n['valeur']:<6} {n['type_note']:<12} {n['date_evaluation']:<15}")
        elif choix == "2":
            id_etudiant = input("ID de l'étudiant : ")
            id_cours = input("ID du cours : ")
            valeur = float(input("Note (0-20) : "))
            type_note = input("Type (examen, devoir, tp) [examen] : ") or "examen"
            Note.ajouter(id_etudiant, id_cours, valeur, type_note)
        elif choix == "3":
            id_etudiant = input("ID de l'étudiant : ")
            notes = Note.chercher_par_etudiant(id_etudiant)
            if not notes:
                print("Aucune note trouvée pour cet étudiant.")
            else:
                for n in notes:
                    cours = Cours.chercher_par_id(n['id_cours'])
                    nom_cours = cours['intitule'] if cours else "Inconnu"
                    print(f"  {nom_cours} | Note : {n['valeur']}/20 | Type : {n['type_note']} | Date : {n['date_evaluation']}")
        elif choix == "4":
            id_cours = input("ID du cours : ")
            notes = Note.chercher_par_cours(id_cours)
            if not notes:
                print("Aucune note trouvée pour ce cours.")
            else:
                for n in notes:
                    etu = Etudiant.chercher_par_id(n['id_etudiant'])
                    nom_etu = f"{etu['prenom']} {etu['nom']}" if etu else "Inconnu"
                    print(f"  {nom_etu} | Note : {n['valeur']}/20 | Type : {n['type_note']}")
        elif choix == "5":
            id_etudiant = input("ID de l'étudiant : ")
            id_cours = input("ID du cours : ")
            moyenne = Note.moyenne_etudiant_par_cours(id_etudiant, id_cours)
            print(f"Moyenne : {moyenne:.2f}/20")
        elif choix == "6":
            id_etudiant = input("ID de l'étudiant : ")
            moyenne = Note.moyenne_generale_etudiant(id_etudiant)
            print(f"Moyenne générale : {moyenne:.2f}/20")
        elif choix == "7":
            id_ = input("ID de la note à modifier : ")
            valeur = float(input("Nouvelle note (0-20) : "))
            Note.modifier(id_, valeur)
        elif choix == "8":
            id_ = input("ID de la note à supprimer : ")
            Note.supprimer(id_)
        elif choix == "9":
            break

def menu_principal():
    while True:
        afficher_titre("SYSTÈME DE GESTION DES ÉTUDES")
        print("1. Gérer les étudiants")
        print("2. Gérer les cours")
        print("3. Gérer les inscriptions")
        print("4. Gérer les notes")
        print("5. Quitter")
        choix = input("Choix : ")
        if choix == "1":
            menu_etudiants()
        elif choix == "2":
            menu_cours()
        elif choix == "3":
            menu_inscriptions()
        elif choix == "4":
            menu_notes()
        elif choix == "5":
            print("Au revoir!")
            break

if __name__ == "__main__":
    from db import connect, disconnect
    connect()
    try:
        menu_principal()
    finally:
        disconnect()
