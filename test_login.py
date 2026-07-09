from db import connect, disconnect, get_collection
from werkzeug.security import check_password_hash

connect()
user = get_collection("users").find_one({"email": "chef.info@gestionetude.com"})
if user:
    print("User found:", user["email"])
    pw_ok = check_password_hash(user["password"], "admin123")
    print("Password check:", pw_ok)
else:
    print("User NOT found")
disconnect()
