"""
================================================================
  People's Produce - Password Strength Checker
  Cybersecurity Group Project | Authentication Vulnerability Demo
================================================================
"""

# ── CONFIG ──
MIN_LENGTH       = 12
MAX_REPEATS      = 3
PASS_THRESHOLD   = 80

# ── BLACKLIST ──
BLACKLISTED_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345",
    "1234567", "qwerty", "abc123", "111111", "123123",
    "admin", "letmein", "welcome", "monkey", "dragon",
    "master", "login", "pass", "test", "user",
    "iloveyou", "sunshine", "princess", "football",
    "password1", "password123", "qwerty123", "1q2w3e4r",
    "passw0rd", "p@ssword", "p@ssw0rd", "admin123",
    "peoplesproduce", "produce123", "grocery", "fresh123"
}

# ── CHARACTER SETS ───
SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{}';:\",./<>?\\|`~"

# ── SEQUENCE DETECTION ──
# Number sequences (ascending and descending)
NUMBER_SEQUENCES = [
    "01234", "12345", "23456", "34567", "45678", "56789",
    # "98765", "87654", "76543", "65432", "54321", "43210"
]

# Keyboard row sequences
KEYBOARD_SEQUENCES = [
    "qwerty", "wertyu", 
    # "ertyui", "rtyuio", "tyuiop",
    # "asdfgh", "sdfghj", "dfghjk", "fghjkl",
    # "zxcvbn", "xcvbnm"
]


ALL_SEQUENCES = NUMBER_SEQUENCES + KEYBOARD_SEQUENCES


# ── CORE CHECKER ──────────────────────────────────────────────
def check_password(password):
    checks = {}
    issues = []
    score  = 0

    pw_lower = password.lower()

    # 1. Blacklist — HARD REQUIREMENT
    is_blacklisted = pw_lower in BLACKLISTED_PASSWORDS
    checks["Not a commonly breached password"] = not is_blacklisted
    if is_blacklisted:
        issues.append("Commonly breached password")

    # 2. Minimum length — HARD REQUIREMENT
    has_min_length = len(password) >= MIN_LENGTH
    checks[f"Minimum {MIN_LENGTH} characters"] = has_min_length
    if not has_min_length:
        issues.append(f"Too short ({len(password)} chars, need {MIN_LENGTH})")

    # 3. Uppercase
    has_upper = any(c.isupper() for c in password)
    checks["Contains uppercase letter"] = has_upper
    if not has_upper:
        issues.append("No uppercase letter")
    else:
        score += 15

    # 4. Lowercase
    has_lower = any(c.islower() for c in password)
    checks["Contains lowercase letter"] = has_lower
    if not has_lower:
        issues.append("No lowercase letter")
    else:
        score += 15

    # 5. Number
    has_digit = any(c.isdigit() for c in password)
    checks["Contains number"] = has_digit
    if not has_digit:
        issues.append("No number")
    else:
        score += 15

    # 6. Special character
    has_special = any(c in SPECIAL_CHARACTERS for c in password)
    checks["Contains special character"] = has_special
    if not has_special:
        issues.append("No special character")
    else:
        score += 15

    # 7. No repeated characters (e.g. aaa, 111)
    has_repeats = False
    for i in range(len(password) - (MAX_REPEATS - 1)):
        if len(set(password[i:i + MAX_REPEATS])) == 1:
            has_repeats = True
            break
    checks["No repeated character sequences"] = not has_repeats
    if has_repeats:
        issues.append(f"Contains {MAX_REPEATS}+ repeated characters in a row (e.g. aaa, 111)")
    else:
        score += 20

    # 8. No predictable sequences (e.g. 1234, qwerty, abcd)
    has_sequence = any(seq in pw_lower for seq in ALL_SEQUENCES)
    checks["No predictable sequences (e.g. 1234, qwerty, abcd)"] = not has_sequence
    if has_sequence:
        issues.append("Contains a predictable sequence (e.g. 1234, qwerty, abcd)")
    else:
        score += 20

    # ── Hard requirements ──────────────────────────────────────
    has_keyboard_seq = any(seq in pw_lower for seq in KEYBOARD_SEQUENCES)
    has_number_seq   = any(seq in pw_lower for seq in NUMBER_SEQUENCES)
    hard_fail = is_blacklisted or not has_min_length or has_keyboard_seq or has_number_seq

    if hard_fail:
        strength = "Weak"
        passed   = False
    else:
        score = min(score, 100)
        if score <= 40:
            strength = "Weak"
        elif score <= 60:
            strength = "Fair"
        elif score < 100:
            strength = "Strong"
        else:
            strength = "Very Strong"
        passed = score >= PASS_THRESHOLD

    return {
        "password": password,
        "score":    score if not hard_fail else 0,
        "strength": strength,
        "passed":   passed,
        "checks":   checks,
        "issues":   issues,
    }


# ── DISPLAY ───────────────────────────────────────────────────
def print_result(result):
    pw     = result["password"]
    score  = result["score"]
    passed = result["passed"]
    checks = result["checks"]
    issues = result["issues"]

    filled = round(score / 5)
    bar    = "[" + "#" * filled + "-" * (20 - filled) + "]"
    status = "ACCEPTED" if passed else "REJECTED"

    print()
    print("=" * 58)
    print("  PASSWORD STRENGTH REPORT — PEOPLE'S PRODUCE")
    print("=" * 58)
    print(f"  Password : {'*' * len(pw)}  ({len(pw)} chars)")
    print(f"  Score    : {score}/100  {bar}")
    print(f"  Status   : {status}")
    print()
    print("  Checks:")
    for label, ok in checks.items():
        tag = "[PASS]" if ok else "[FAIL]"
        print(f"    {tag}  {label}")
    if issues:
        print()
        print("  Issues:")
        for issue in issues:
            print(f"    - {issue}")
    print("=" * 58)


# ── DEMO ──────────────────────────────────────────────────────
DEMO_PASSWORDS = [
    ("123456",             "Blacklisted + very short"),
    ("password123",        "Common pattern, blacklisted"),
    ("HelloWor!d",         "Too short, missing number"),
    ("Abcdefgh2024!@",     "Contains alphabet sequence"),
    ("Fr3sh!Produce#2024", "Strong - meets all criteria"),
    ("T^9kL#mQz@2Xw!pN",  "Very Strong - random and long"),
]

def run_demo():
    print()
    print("=" * 58)
    print("  DEMO — Password Vulnerability Examples")
    print("=" * 58)
    for pw, description in DEMO_PASSWORDS:
        result = check_password(pw)
        status = "ACCEPTED" if result["passed"] else "REJECTED"
        filled = round(result["score"] / 5)
        bar    = "[" + "#" * filled + "-" * (20 - filled) + "]"
        print(f"  {pw:<24}  {bar}  [{status}]")
        print(f"  {'':24}  {description}")
        print()
    print("=" * 58)


# ── INTERACTIVE ───────────────────────────────────────────────
def interactive_mode():
    print()
    print("=" * 58)
    print("  People's Produce - Password Checker")
    print("  Type 'demo' for examples, 'quit' to exit")
    print("=" * 58)

    while True:
        pw = input("\n  Enter password: ").strip()
        if not pw:
            continue
        if pw.lower() == "quit":
            print("\n  Exiting.\n")
            break
        if pw.lower() == "demo":
            run_demo()
            continue
        print_result(check_password(pw))


interactive_mode()