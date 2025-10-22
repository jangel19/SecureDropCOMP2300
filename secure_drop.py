import os, json, hashlib, base64
#i have this for now there are some issues with the directories but nothing too major you have
#to run the file from user-reg was in an src dir but had issues with user_data displaying yall
#are more than welcome to add or fix anything
#i also noticed rn that there is a bug that wont let me run it unless the user info json is empty
#i will try to work on that later this week maybeee

USER_DB = "user_data/user_info.json"

def getUsers():
    #lods the user db from json file
    #if its empty it js returns the empty struct
    if not os.path.exists(USER_DB):
        return{"users": []}
    with open(USER_DB, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    #this saves teh users info to the json indent is js aesthetics lol
    with open(USER_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def make_salt(length = 16):
    #thisll just make a random salt val for the pwd hashing
    #each user gets a diff salt we use base64 for the encoding (go into json)
    return base64.b64encode(os.urandom(length)).decode("utf-8")

def simple_hash(salt, pwd):
    #combine th esalt and pwd into a string then hash it
    combo = (salt + pwd).encode("utf-8")
    return hashlib.sha256(combo).hexdigest()

def findeusr(users, email):
    #will go through json and return the user that matchs
    for u in users:
        if u["email"].lower() == email.lower():
            return u
    return None




def register_user(db):
    #now we get user input abotu registersting

    print("Do you want to register a new user (y/n)? ", end="")
    if input().strip().lower() != "y":
        print("Exiting SecureDrop.")
        return db

    full_name = input("Enter Full Name: ").strip()
    email = input("Enter Email Address: ").strip().lower()
    pwd1 = input("Enter Password: ").strip()
    pwd2 = input("Re-enter Password: ").strip()

    if pwd1 != pwd2:
        print("Passwords do not match.")
        print("Exiting SecureDrop.")
        return db

    salt = make_salt()
    pwd_hash = simple_hash(salt, pwd1)

    user = {
        "full_name": full_name,
        "email": email,
        "password_salt": salt,
        "password_hash": pwd_hash,
    }

    db["users"] = [u for u in db["users"] if u["email"].lower() != email]

    db["users"].append(user)
    save_users(db)

    print("Passwords Match.")
    print("User Registered.")
    print("Exiting SecureDrop.")
    return db

def main():

    db = getUsers()

    if len(db["users"]) == 0:
        print("No users are registered with this client.")
        db = register_user(db)
    else:
        print("A user is already registered with this client.")
        return

if __name__ == "__main__":
    main()
