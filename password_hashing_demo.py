import hashlib
import os

# ==============================
# BASIC HASH FUNCTION
# ==============================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ==============================
# HASH WITH SALT
# ==============================
def hash_with_salt(password):
    salt = os.urandom(16)
    hashed = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt, hashed

# ==============================
# SIMULATED DATABASE
# ==============================
users = {}

def register(username, password):
    salt, hashed = hash_with_salt(password)
    users[username] = (salt, hashed)
    print(f"[REGISTERED] {username}")

def login(username, password):
    if username not in users:
        print("[FAILED] User not found")
        return

    salt, stored_hash = users[username]
    test_hash = hashlib.sha256(salt + password.encode()).hexdigest()

    if test_hash == stored_hash:
        print("[SUCCESS] Login successful")
    else:
        print("[FAILED] Incorrect password")

# ==============================
# DEMO
# ==============================
def demo():
    password = "Password123"

    print("\n=== PLAINTEXT STORAGE (INSECURE) ===")
    print("Stored password:", password)

    print("\n=== WITHOUT SALT ===")
    h1 = hash_password(password)
    h2 = hash_password(password)

    print("Hash 1:", h1)
    print("Hash 2:", h2)

    print("\nSame password → same hash\n")

    print("=== WITH SALT ===")
    salt1, hs1 = hash_with_salt(password)
    salt2, hs2 = hash_with_salt(password)

    print("Hash 1:", hs1)
    print("Hash 2:", hs2)

    print("\nSalt 1:", salt1.hex())
    print("Salt 2:", salt2.hex())

    print("\nSame password → different hashes")

    print("\n=== AUTHENTICATION DEMO ===")
    register("sam", "Password123")

    print(f"[DEBUG] Stored entry: {users['sam']}")

    login("sam", "wrongpass")
    login("sam", "Password123")


if __name__ == "__main__":
    demo()
