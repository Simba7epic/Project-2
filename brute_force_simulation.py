import time
from collections import defaultdict
import random

# ==============================
# CONFIGURATION
# ==============================
CORRECT_PASSWORD = "Password123"
MAX_ACCOUNT_ATTEMPTS = 5
MAX_IP_ATTEMPTS = 10

# ==============================
# GLOBAL STATE
# ==============================
ip_attempts = defaultdict(int)
account_attempts = defaultdict(int)
locked_accounts = set()
blocked_ips = set()

# ==============================
# RESET FUNCTION
# ==============================
def reset_system():
    ip_attempts.clear()
    account_attempts.clear()
    locked_accounts.clear()
    blocked_ips.clear()
    print("[RESET] System cleared.\n")

# ==============================
# BASELINE (NO PROTECTION)
# ==============================
def baseline_demo():
    print("\n=== BASELINE: No Protection ===")
    print("Type 'exit' to stop\n")

    correct_password = "Password123"

    while True:
        attempt = input("Enter password: ")

        if attempt.lower() == "exit":
            break

        if attempt == correct_password:
            print("[SUCCESS] Access granted (no protection!)\n")
            break
        else:
            print("[FAILED] Try again (unlimited attempts)")

# ==============================
# DELAY DEMO
# ==============================
def delay_demo():
    print("\n=== DELAY DEMO ===")
    print("Type 'exit' to stop\n")

    correct_password = "Password123"
    attempts = 0

    while True:
        attempt = input("Enter password: ")

        if attempt.lower() == "exit":
            break

        attempts += 1
        delay = min(2 ** attempts, 8)

        if attempt == correct_password:
            print("[SUCCESS] Access granted\n")
            break
        else:
            print(f"[FAILED] Attempt {attempts}")

        print(f"[DELAY] Waiting {delay}s...")
        time.sleep(delay)



# ==============================
# CAPTCHA DEMO
# ==============================
def captcha_demo():
    print("\n=== CAPTCHA DEMO ===")
    print("Type 'exit' to stop\n")

    correct_password = "Password123"
    attempts = 0

    while True:
        attempt = input("Enter password: ")

        if attempt.lower() == "exit":
            break

        attempts += 1

        if attempts >= 3:
            print("[CAPTCHA REQUIRED]")

            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            total = str(num1 + num2)
            ans = input(f"Solve {num1} + {num2}: ")

            if ans != str(total):
                print("[FAILED] CAPTCHA failed — attack stopped\n")
                break

        if attempt == correct_password:
            print("[SUCCESS] Access granted\n")
            break
        else:
            print(f"[FAILED] Attempt {attempts}")

# ==============================
# ACCOUNT LOCK DEMO
# ==============================
def lockout_demo():
    print("\n=== ACCOUNT LOCKOUT DEMO ===")
    print("Type 'exit' to stop\n")

    correct_password = "Password123"
    attempts = 0
    MAX_ATTEMPTS = 5

    while True:
        if attempts >= MAX_ATTEMPTS:
            print("[LOCKED] Account locked after too many attempts\n")
            break

        attempt = input("Enter password: ")

        if attempt.lower() == "exit":
            break

        attempts += 1

        if attempt == correct_password:
            print("[SUCCESS] Access granted\n")
            break
        else:
            print(f"[FAILED] Attempt {attempts}/{MAX_ATTEMPTS}")

# ==============================
# IP BLOCK DEMO
# ==============================
def ip_block_demo():
    print("\n=== IP BLOCKING DEMO ===")
    print("Type 'exit' to stop\n")

    correct_password = "Password123"
    ip_attempts = {}
    MAX_IP_ATTEMPTS = 10

    ip = input("Enter IP address: ")

    while True:
        if ip_attempts.get(ip, 0) >= MAX_IP_ATTEMPTS:
            print(f"[BLOCKED] IP {ip} blocked\n")
            break

        attempt = input("Enter password: ")

        if attempt.lower() == "exit":
            break

        ip_attempts[ip] = ip_attempts.get(ip, 0) + 1

        if attempt == correct_password:
            print("[SUCCESS] Access granted\n")
            break
        else:
            print(f"[FAILED] Attempt {ip_attempts[ip]}")

# ==============================
# COMBINED SYSTEM
# ==============================
def apply_delay(attempts):
    delay = min(2 ** attempts, 8)
    print(f"[DELAY] {delay}s")
    time.sleep(delay)

def require_captcha(username):
    return account_attempts[username] >= 3

def captcha_challenge():
    print("[CAPTCHA REQUIRED]")
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    total = str(num1 + num2)
    ans = input(f"Solve {num1} + {num2}: ")
    
    return ans == str(total)

def combined_login():
    print("\n=== COMBINED REAL-WORLD SYSTEM ===")
    print("Type 'exit' at any time to stop\n")

    ip = input("Enter IP: ")
    username = input("Enter username: ")

    while True:
        # Check if already blocked/locked BEFORE input
        if ip in blocked_ips:
            print(f"[BLOCKED IP] {ip}")
            break

        if username in locked_accounts:
            print(f"[LOCKED ACCOUNT] {username}")
            break

        password = input("Enter password: ")

        if password.lower() == "exit":
            break

        # Increment counters
        ip_attempts[ip] += 1
        account_attempts[username] += 1

        print(f"\n[ATTEMPT #{account_attempts[username]}]")

        # 1. IP BLOCKING (strongest → check early)
        if ip_attempts[ip] > MAX_IP_ATTEMPTS:
            blocked_ips.add(ip)
            print("[SECURITY] IP BLOCKED due to excessive attempts")
            break

        # 2. ACCOUNT LOCKOUT
        if account_attempts[username] > MAX_ACCOUNT_ATTEMPTS:
            locked_accounts.add(username)
            print("[SECURITY] ACCOUNT LOCKED due to repeated failures")
            break

        # 3. CAPTCHA
        # 3. CAPTCHA (must be solved before continuing)
        if require_captcha(username):
            print("[SECURITY] CAPTCHA TRIGGERED")

            while True:
                success = captcha_challenge()

                if success:
                    print("[CAPTCHA PASSED]")
                    break  # exit CAPTCHA loop and continue login flow

                print("[FAILED] CAPTCHA incorrect")

                retry = input("Try again CAPTCHA? (y/exit): ").lower()

                if retry == "exit":
                    print("[ABORTED] User exited CAPTCHA challenge")
                    return  # clean exit from entire login attempt

        # 4. DELAY (always applied)
        apply_delay(account_attempts[username])

        # 5. PASSWORD CHECK
        if password == CORRECT_PASSWORD:
            print(f"[SUCCESS] Welcome {username}")
            
            # Reset on success (real systems do this)
            account_attempts[username] = 0
            ip_attempts[ip] = 0
            break
        else:
            print("[FAILED] Incorrect password")

# ==============================
# MAIN MENU
# ==============================
def main():
    while True:
        print("\n===== SECURITY SIMULATION MENU =====")
        print("1. Baseline (No Protection)")
        print("2. Delay Demo")
        print("3. CAPTCHA Demo")
        print("4. Account Lockout Demo")
        print("5. IP Blocking Demo")
        print("6. Combined System")
        print("7. Reset System")
        print("8. Exit")

        choice = input("Select option: ")

        if choice == "1":
            baseline_demo()
        elif choice == "2":
            delay_demo()
        elif choice == "3":
            captcha_demo()
        elif choice == "4":
            lockout_demo()
        elif choice == "5":
            ip_block_demo()
        elif choice == "6":
            combined_login()
        elif choice == "7":
            reset_system()
        elif choice == "8":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()