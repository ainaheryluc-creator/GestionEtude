from db import connect, disconnect, get_collection
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from datetime import date

CHEFS = [
    {"email": "chef.info@gestionetude.com", "nom": "KOUASSI", "prenom": "Jean", "departement": "Informatique", "password": "admin123"},
    {"email": "chef.gestion@gestionetude.com", "nom": "TRAORE", "prenom": "Fatou", "departement": "Gestion", "password": "admin123"},
    {"email": "chef.geniecivil@gestionetude.com", "nom": "DIALLO", "prenom": "Moussa", "departement": "Genie Civil", "password": "admin123"},
    {"email": "chef.communication@gestionetude.com", "nom": "KONE", "prenom": "Aminata", "departement": "Communication", "password": "admin123"},
]

SAMPLE_ETUDIANTS = {
    "Informatique": [
        {"nom": "KOFFI", "prenom": "Amadou", "email": "amadou.koffi@etudiant.com"},
        {"nom": "BAMBA", "prenom": "Mariam", "email": "mariam.bamba@etudiant.com"},
        {"nom": "SILUE", "prenom": "Lucas", "email": "lucas.silue@etudiant.com"},
    ],
    "Gestion": [
        {"nom": "TOURE", "prenom": "Aicha", "email": "aicha.toure@etudiant.com"},
        {"nom": "COULIBALY", "prenom": "Oumar", "email": "oumar.coulibaly@etudiant.com"},
    ],
    "Genie Civil": [
        {"nom": "FOFANA", "prenom": "Salim", "email": "salim.fofana@etudiant.com"},
        {"nom": "GUEYE", "prenom": "Rokia", "email": "rokia.gueye@etudiant.com"},
    ],
    "Communication": [
        {"nom": "DIOP", "prenom": "Fatoumata", "email": "fatoumata.diop@etudiant.com"},
        {"nom": "KEITA", "prenom": "Mamadou", "email": "mamadou.keita@etudiant.com"},
        {"nom": "SISSOKO", "prenom": "Aminata", "email": "aminata.sissoko@etudiant.com"},
    ],
}

COURS_PAR_DEPT = {
    "Informatique": [
        {"code": "INF101", "intitule": "Algorithmique et Programmation", "credit": 5, "enseignant": "Dr. Konate", "semestre": "S1", "code_ue": "U001"},
        {"code": "INF102", "intitule": "Systemes d'Exploitation", "credit": 4, "enseignant": "Dr. Yapi", "semestre": "S1", "code_ue": "U001"},
        {"code": "INF201", "intitule": "Bases de Donnees", "credit": 5, "enseignant": "Dr. N'Guessan", "semestre": "S2", "code_ue": "U002"},
        {"code": "INF202", "intitule": "Reseaux", "credit": 4, "enseignant": "Dr. Kouame", "semestre": "S2", "code_ue": "U002"},
        {"code": "INF301", "intitule": "Intelligence Artificielle", "credit": 5, "enseignant": "Pr. Yao", "semestre": "S3", "code_ue": "U003"},
        {"code": "INF302", "intitule": "Genie Logiciel", "credit": 4, "enseignant": "Dr. Angora", "semestre": "S3", "code_ue": "U003"},
        {"code": "INF401", "intitule": "Projet de Fin d'Etudes", "credit": 6, "enseignant": "Pr. Yao", "semestre": "S4", "code_ue": "U004"},
    ],
    "Gestion": [
        {"code": "GES101", "intitule": "Comptabilite Generale", "credit": 5, "enseignant": "Dr. Kone", "semestre": "S1", "code_ue": "U001"},
        {"code": "GES102", "intitule": "Microeconomie", "credit": 4, "enseignant": "Dr. Diarra", "semestre": "S1", "code_ue": "U001"},
        {"code": "GES201", "intitule": "Marketing Fondamental", "credit": 5, "enseignant": "Dr. Bamba", "semestre": "S2", "code_ue": "U002"},
        {"code": "GES202", "intitule": "Gestion Financiere", "credit": 4, "enseignant": "Dr. Traore", "semestre": "S2", "code_ue": "U002"},
    ],
    "Genie Civil": [
        {"code": "GC101", "intitule": "Mecanique des Sols", "credit": 5, "enseignant": "Pr. Diallo", "semestre": "S1", "code_ue": "U001"},
        {"code": "GC102", "intitule": "Resistance des Materiaux", "credit": 4, "enseignant": "Dr. Doumbia", "semestre": "S1", "code_ue": "U001"},
        {"code": "GC201", "intitule": "Hydraulique", "credit": 5, "enseignant": "Dr. Kamagate", "semestre": "S2", "code_ue": "U002"},
        {"code": "GC202", "intitule": "Topographie", "credit": 4, "enseignant": "Dr. Soro", "semestre": "S2", "code_ue": "U002"},
    ],
    "Communication": [
        {"code": "COM101", "intitule": "Theories de la Communication", "credit": 5, "enseignant": "Dr. Kouyate", "semestre": "S1", "code_ue": "U001"},
        {"code": "COM102", "intitule": "Expression Orale et Ecrite", "credit": 4, "enseignant": "Dr. Fadiga", "semestre": "S1", "code_ue": "U001"},
        {"code": "COM201", "intitule": "Communication Digitale", "credit": 5, "enseignant": "Dr. Cisse", "semestre": "S2", "code_ue": "U002"},
        {"code": "COM202", "intitule": "Relations Publiques", "credit": 4, "enseignant": "Dr. Dembele", "semestre": "S2", "code_ue": "U002"},
    ],
}

def init_chefs():
    users = get_collection("users")
    chefs_ids = {}
    for chef in CHEFS:
        existing = users.find_one({"email": chef["email"]})
        if existing:
            chefs_ids[chef["departement"]] = existing["_id"]
            print(f"  [OK] Chef {chef['departement']} existe deja.")
        else:
            result = users.insert_one({
                "email": chef["email"],
                "password": generate_password_hash(chef["password"]),
                "role": "head",
                "nom": chef["nom"],
                "prenom": chef["prenom"],
                "departement": chef["departement"],
                "matricule": f"CHEF-{chef['departement'][:4].upper()}",
            })
            chefs_ids[chef["departement"]] = result.inserted_id
            print(f"  [OK] Chef {chef['departement']} cree : {chef['email']} / {chef['password']}")
    return chefs_ids

def init_etudiants():
    users = get_collection("users")
    etudiants = get_collection("etudiants")
    prefix_map = {"Informatique": "INF", "Gestion": "GES", "Genie Civil": "GC", "Communication": "COM"}
    created = {}
    for dept, etus in SAMPLE_ETUDIANTS.items():
        prefix = prefix_map[dept]
        for i, etu in enumerate(etus, 1):
            email = etu["email"]
            if users.find_one({"email": email}):
                print(f"  [OK] Etudiant {etu['prenom']} {etu['nom']} ({dept}) existe deja.")
                existing = users.find_one({"email": email})
                created.setdefault(dept, []).append(existing["_id"])
                continue
            matricule = f"{prefix}{i:03d}"
            password = "etudiant123"
            user_result = users.insert_one({
                "email": email,
                "password": generate_password_hash(password),
                "role": "student",
                "nom": etu["nom"],
                "prenom": etu["prenom"],
                "departement": dept,
                "matricule": matricule,
            })
            etudiants.insert_one({
                "matricule": matricule,
                "nom": etu["nom"],
                "prenom": etu["prenom"],
                "email": email,
                "telephone": "",
                "date_naissance": "2000-01-01",
                "adresse": f"Adresse de {etu['prenom']} {etu['nom']}",
                "departement": dept,
            })
            created.setdefault(dept, []).append(user_result.inserted_id)
            print(f"  [OK] Etudiant cree : {email} / {password} (matricule: {matricule})")
    return created

def init_cours():
    cours_col = get_collection("cours")
    created = {}
    for dept, cours_list in COURS_PAR_DEPT.items():
        created[dept] = []
        for c in cours_list:
            if cours_col.find_one({"code": c["code"]}):
                existing = cours_col.find_one({"code": c["code"]})
                created[dept].append(existing["_id"])
                continue
            doc = {**c, "departement": dept}
            result = cours_col.insert_one(doc)
            created[dept].append(result.inserted_id)
            print(f"  [OK] Cours cree : {c['code']} - {c['intitule']}")
    return created

def init_inscriptions(etudiants_by_dept, cours_by_dept):
    inscriptions = get_collection("inscriptions")
    count = 0
    for dept in etudiants_by_dept:
        for e_id in etudiants_by_dept[dept]:
            etu = get_collection("etudiants").find_one({"_id": e_id})
            if not etu:
                continue
            for c_id in cours_by_dept.get(dept, []):
                existing = inscriptions.find_one({"id_etudiant": e_id, "id_cours": c_id})
                if existing:
                    continue
                inscriptions.insert_one({
                    "id_etudiant": e_id,
                    "id_cours": c_id,
                    "annee_academique": "2025-2026",
                    "date_inscription": str(date.today()),
                })
                count += 1
    if count:
        print(f"  [OK] {count} inscriptions creees.")

def init_notes(etudiants_by_dept, cours_by_dept):
    notes = get_collection("notes")
    import random
    count = 0
    for dept in etudiants_by_dept:
        for e_id in etudiants_by_dept[dept]:
            etu = get_collection("etudiants").find_one({"_id": e_id})
            if not etu:
                continue
            for c_id in cours_by_dept.get(dept, []):
                for ntype in ("cc", "examen"):
                    existing = notes.find_one({"id_etudiant": e_id, "id_cours": c_id, "type_note": ntype})
                    if existing:
                        continue
                    valeur = round(random.uniform(8, 18), 2)
                    notes.insert_one({
                        "id_etudiant": e_id,
                        "id_cours": c_id,
                        "valeur": valeur,
                        "type_note": ntype,
                        "date_evaluation": str(date.today()),
                    })
                    count += 1
    if count:
        print(f"  [OK] {count} notes creees.")

def init_annonces(chefs_ids):
    annonces = get_collection("annonces")
    count = 0
    for dept, chef_id in chefs_ids.items():
        existing = annonces.find_one({"departement": dept, "titre": f"Bienvenue au departement {dept}"})
        if existing:
            continue
        annonces.insert_one({
            "titre": f"Bienvenue au departement {dept}",
            "contenu": f"Nous sommes ravis de vous accueillir dans le departement {dept}. "
                       f"Les cours debutent le 15 Septembre 2025. Consultez votre emploi du temps sur le portail etudiant.",
            "departement": dept,
            "auteur": chef_id,
            "date_creation": str(date.today()),
            "publie": True,
            "visibilite": "departement",
        })
        annonces.insert_one({
            "titre": f"Calendrier des examens {dept}",
            "contenu": f"Les examens du premier semestre auront lieu du 15 au 30 Janvier 2026. "
                       f"Les notes seront publiees dans les deux semaines suivant les epreuves.",
            "departement": dept,
            "auteur": chef_id,
            "date_creation": str(date.today()),
            "publie": True,
            "visibilite": "departement",
        })
        count += 2
    if count:
        print(f"  [OK] {count} annonces creees.")

def init():
    connect()
    print("\n--- Chefs de departement ---")
    chefs_ids = init_chefs()
    print("\n--- Etudiants ---")
    etudiants_ids = init_etudiants()
    etudiants_by_dept = {}
    for dept, ids in etudiants_ids.items():
        etudiants_by_dept[dept] = [ObjectId(str(e_id)) for e_id in ids]
    print("\n--- Cours ---")
    cours_ids = init_cours()
    cours_by_dept = {}
    for dept, ids in cours_ids.items():
        cours_by_dept[dept] = [ObjectId(str(c_id)) for c_id in ids]
    print("\n--- Inscriptions ---")
    init_inscriptions(etudiants_by_dept, cours_by_dept)
    print("\n--- Notes ---")
    init_notes(etudiants_by_dept, cours_by_dept)
    print("\n--- Annonces ---")
    init_annonces(chefs_ids)
    disconnect()

if __name__ == "__main__":
    print("Initialisation de la base de donnees...")
    init()
    print("\nTerminé.")
    print("\nComptes chefs :")
    for chef in CHEFS:
        print(f"  {chef['email']} / {chef['password']} ({chef['departement']})")
    print("\nComptes etudiants : mot de passe = 'etudiant123'")
