"""
MFA Demo — The People's Produce
Authenticator app (TOTP) login demo.
"""

import pyotp
import qrcode
import time

# ── Fake user ──────────────────────────────────────────
EMAIL    = "customer@example.com"
PASSWORD = "password123"

# ── Step 1: Generate a secret and show the QR code ────
print("\n=== The People's Produce — MFA Setup ===\n")

secret = pyotp.random_base32()
totp   = pyotp.TOTP(secret)
uri    = totp.provisioning_uri(name=EMAIL, issuer_name="The People's Produce")

print("Scan this QR code with your authenticator app")
print("(Google Authenticator, Authy, etc.)\n")

qr = qrcode.QRCode(border=2)
qr.add_data(uri)
qr.make(fit=True)
qr.print_ascii(invert=True)

print(f"\nOr enter this key manually: {secret}\n")

# ── Step 2: Confirm setup ──────────────────────────────
print("=== Confirm Setup ===\n")
for _ in range(3):
    code = input("Enter the 6-digit code from your app: ").strip()
    if totp.verify(code, valid_window=1):
        print("✔ MFA setup complete!\n")
        break
    print("✘ Incorrect code, try again.")
else:
    print("Setup failed. Exiting.")
    exit()

# ── Step 3: Live code viewer ──────────────────────────
print("=== Live Code Viewer ===\n")
print("Watch your code refresh every 30 seconds.")
print("Press Ctrl+C when you're ready to log in.\n")

try:
    while True:
        code      = totp.now()
        remaining = 30 - int(time.time()) % 30
        filled    = int(remaining / 30 * 20)
        bar       = "█" * filled + "░" * (20 - filled)
        print(f"\r  Code: {code}   [{bar}] {remaining:2d}s ", end="", flush=True)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n")

# ── Step 4: Simulate login with MFA ───────────────────
print("=== Login ===\n")

entered_password = input("Password: ").strip()
if entered_password != PASSWORD:
    print("✘ Wrong password.")
    exit()

for _ in range(3):
    code = input("Authenticator code: ").strip()
    if totp.verify(code, valid_window=1):
        print("\n✔ Login successful! Welcome to The People's Produce.\n")
        break
    remaining = 30 - int(time.time()) % 30
    print(f"✘ Incorrect code. (refreshes in {remaining}s)")
else:
    print("✘ Too many attempts. Access denied.")