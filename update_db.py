import sys
sys.path.insert(0, r'C:\Users\no-enter\OneDrive\Desktop\GestionEtude')
from db import connect, get_collection, disconnect
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from datetime import date
import random

connect()

# --- NETTOYAGE ---
print("--- Nettoyage ---")
get_collection("cours").delete_many({})
get_collection("inscriptions").delete_many({})
get_collection("notes").delete_many({})
get_collection("annonces").delete_many({})
print("  Cours, inscriptions, notes, annonces vidés")

# --- RECREER LES CHEFS (inchangés) ---
print("\n--- Chefs ---")
users = get_collection("users")
chefs_data = [
    {"email": "chef.info@gestionetude.com", "nom": "KOUASSI", "prenom": "Jean", "departement": "Informatique"},
    {"email": "chef.gestion@gestionetude.com", "nom": "TRAORE", "prenom": "Fatou", "departement": "Gestion"},
    {"email": "chef.geniecivil@gestionetude.com", "nom": "DIALLO", "prenom": "Moussa", "departement": "Genie Civil"},
    {"email": "chef.communication@gestionetude.com", "nom": "KONE", "prenom": "Aminata", "departement": "Communication"},
]
chefs_ids = {}
for c in chefs_data:
    existing = users.find_one({"email": c["email"]})
    if existing:
        chefs_ids[c["departement"]] = existing["_id"]
        print(f"  {c['departement']}: déjà existant (id préservé)")
    else:
        result = users.insert_one({
            "email": c["email"],
            "password": generate_password_hash("admin123"),
            "role": "head",
            "nom": c["nom"],
            "prenom": c["prenom"],
            "departement": c["departement"],
            "matricule": f"CHEF-{c['departement'][:4].upper()}",
        })
        chefs_ids[c["departement"]] = result.inserted_id
        print(f"  {c['departement']}: créé")

# --- COURS ---
print("\n--- Cours ---")
cours_col = get_collection("cours")
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
cours_ids = {}
for dept, clist in COURS_PAR_DEPT.items():
    cours_ids[dept] = []
    for c in clist:
        doc = {**c, "departement": dept}
        result = cours_col.insert_one(doc)
        cours_ids[dept].append(result.inserted_id)
        print(f"  {dept}: {c['code']} - {c['intitule']}")

# --- INSCRIPTIONS POUR LES ÉTUDIANTS EXISTANTS ---
print("\n--- Inscriptions ---")
inscriptions = get_collection("inscriptions")
etudiants_col = get_collection("etudiants")
all_etudiants = list(etudiants_col.find({}))
count_ins = 0
for etu in all_etudiants:
    dept = etu.get("departement")
    for c_id in cours_ids.get(dept, []):
        inscriptions.insert_one({
            "id_etudiant": etu["_id"],
            "id_cours": c_id,
            "annee_academique": "2025-2026",
            "date_inscription": str(date.today()),
        })
        count_ins += 1
print(f"  {count_ins} inscriptions créées")

# --- NOTES ALÉATOIRES ---
print("\n--- Notes ---")
notes = get_collection("notes")
count_notes = 0
for etu in all_etudiants:
    dept = etu.get("departement")
    for c_id in cours_ids.get(dept, []):
        for ntype in ("cc", "examen"):
            valeur = round(random.uniform(8, 18), 2)
            notes.insert_one({
                "id_etudiant": etu["_id"],
                "id_cours": c_id,
                "valeur": valeur,
                "type_note": ntype,
                "date_evaluation": str(date.today()),
            })
            count_notes += 1
print(f"  {count_notes} notes créées")

# --- ANNONCES ---
print("\n--- Annonces ---")
annonces = get_collection("annonces")
count_ann = 0
for dept, chef_id in chefs_ids.items():
    annonces.insert_one({
        "titre": f"Bienvenue au departement {dept}",
        "contenu": f"Nous sommes ravis de vous accueillir dans le departement {dept}. Les cours debutent le 15 Septembre 2025.",
        "departement": dept,
        "auteur": chef_id,
        "date_creation": str(date.today()),
        "publie": True,
        "visibilite": "departement",
    })
    annonces.insert_one({
        "titre": f"Calendrier des examens {dept}",
        "contenu": f"Les examens du premier semestre auront lieu du 15 au 30 Janvier 2026.",
        "departement": dept,
        "auteur": chef_id,
        "date_creation": str(date.today()),
        "publie": True,
        "visibilite": "departement",
    })
    count_ann += 2
print(f"  {count_ann} annonces créées")

# --- RÉCAPITULATIF ---
print("\n========== RÉCAPITULATIF ==========")
for col_name in ["users", "etudiants", "cours", "inscriptions", "notes", "annonces", "messages"]:
    count = get_collection(col_name).count_documents({})
    print(f"{col_name}: {count}")

print("\nComptes chefs : chef.*@gestionetude.com / admin123")
print("Étudiants : emails existants / mot de passe = etudiant123")

disconnect()
