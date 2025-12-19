import os, json, hashlib, base64, time, subprocess
from milestone4_network import NetworkDiscovery, list_contacts

# Note: the json file can't be all empty it has to have the structure {"users": []} even if there are no users
# that is probably why it wasn't working before.

USER_DB = "user_data/user_info.json"

def getUsers():
    """Loads the user db from json file
    If it's empty it just returns the empty struct"""
    if not os.path.exists(USER_DB):
        os.makedirs("user_data", exist_ok=True)
        return {"users": []}
    with open(USER_DB, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    """This saves the users info to the json. indent is just aesthetics lol"""
    os.makedirs("user_data", exist_ok=True)
    with open(USER_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def make_salt(length=16):
    """This'll just make a random salt val for the pwd hashing
    Each user gets a diff salt. We use base64 for the encoding (go into json)"""
    return base64.b64encode(os.urandom(length)).decode("utf-8")

def simple_hash(salt, pwd):
    """Combine the salt and pwd into a string then hash it"""
    combo = (salt + pwd).encode("utf-8")
    return hashlib.sha256(combo).hexdigest()

def findeusr(users, email):
    """Will go through json and return the user that matches"""
    for u in users:
        if u["email"].lower() == email.lower():
            return u
    return None

def register_user(db):
    """Now we get user input about registering"""
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
        "contacts": []  # Initialize empty contacts list
    }

    # Remove any existing user with same email
    db["users"] = [u for u in db["users"] if u["email"].lower() != email]

    db["users"].append(user)
    save_users(db)

    print("Passwords Match.")
    print("User Registered.")
    print("Exiting SecureDrop.")
    return db

def login(db):
    """Handle user login"""
    print("Enter Email Address: ", end="")
    email = input().strip().lower()

    print("Enter Password: ", end="")
    pwd = input().strip()

    # Find the user in DB
    users = db.get("users", [])
    user = findeusr(users, email)

    if user is None:
        print("Email and Password Combination Invalid.\n")
        return False

    # Re-hash the input password using stored salt
    salt = user["password_salt"]
    expected_hash = user["password_hash"]
    given_hash = simple_hash(salt, pwd)

    if given_hash != expected_hash:
        print("Email and Password Combination Invalid.\n")
        return False

    # LOGIN SUCCESSFUL
    print("Welcome to SecureDrop.")
    print('Type "help" For Commands.')
    return user

def start_receiver_server():
    try:
        subprocess.Popen(
            ["./server"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("[Receiver server running]")
        time.sleep(1)
    except Exception as e:
        print(f"Could not start receiver server: {e}")

def add_contact(current_user, db):
    """Add a new contact (Milestone 3)"""
    print("\nEnter Full Name: ", end="")
    full_name = input().strip()

    print("Enter Email Address: ", end="")
    email = input().strip().lower()

    # Ensure contacts list exists
    if "contacts" not in current_user:
        current_user["contacts"] = []

    # Check if contact already exists - remove to overwrite
    current_user["contacts"] = [
        c for c in current_user.get("contacts", []) if c["email"].lower() != email
    ]

    # Add new contact
    contact = {
        "full_name": full_name,
        "email": email
    }
    current_user["contacts"].append(contact)

    # Save entire DB to JSON file
    # (current_user is a reference to the user object in db["users"])
    save_users(db)
    print("Contact Added.\n")

def shell(current_user, db, discovery):
    """Main command shell (secure_drop>)"""
    while True:
        try:
            cmd = input("secure_drop> ").strip().lower()

            if cmd == "add":
                add_contact(current_user, db)

            elif cmd == "list":
                # Milestone 4: List online contacts
                list_contacts(discovery)

            elif cmd == "send":
                online = discovery.get_online_contacts()

                if not online:
                    print("No online connections are available right now.")
                    continue

                print("\nSelect a contact:")
                for i, c in enumerate(online):
                    print(f"{i+1}) {c['full_name']} <{c['email']}>")

                try:
                    choice = int(input("Enter a number: ")) - 1
                    if choice < 0 or choice >= len(online):
                        raise ValueError
                    contact = online[choice]
                except:
                    print("Invalid selection.")
                    continue

                filename = input("Enter filename to send: ").strip()
                if not os.path.exists(filename):
                    print("File does not exist.")
                    continue

                ip = contact["ip"]

                print("\nSecureDrop file transfer starting...")
                print("Make sure the receiver is running the server.")

                time.sleep(1)

                print("Sending encrypted file...")
                subprocess.run(["./client", ip, "6767", filename])

                print("Secure transfer completed.")

            elif cmd == "help":
                print('"add"  -> Add a new contact')
                print('"list" -> List all online contacts')
                print('"send" -> Transfer file to contact')
                print('"exit" -> Exit SecureDrop')

            elif cmd == "exit":
                print("Exiting SecureDrop.")
                discovery.stop()
                return

            else:
                print('Unknown command. Type "help".')

        except KeyboardInterrupt:
            print("\nExiting SecureDrop.")
            discovery.stop()
            return
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main application entry point"""
    db = getUsers()

    # If there are no users we have to register one
    if len(db["users"]) == 0:
        print("No users are registered with this client.")
        db = register_user(db)
        return

    # Otherwise, we can try to login
    user = login(db)
    if user:
        #added so i dont need to run ./server every time
        start_receiver_server()
        # Start network discovery (Milestone 4)
        discovery = NetworkDiscovery(user, db)
        discovery.start()

        # Give discovery a moment to initialize
        import time
        time.sleep(1)

        # Enter main shell
        shell(user, db, discovery)


if __name__ == "__main__":
    main()
