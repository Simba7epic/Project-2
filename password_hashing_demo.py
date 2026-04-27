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
# DEMO
# ==============================
def demo():
    password = "Password123"

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

    print("\nSalt 1:", salt1)
    print("Salt 2:", salt2)

    print("\nSame password → different hashes")


if __name__ == "__main__":
    demo()
