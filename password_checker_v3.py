"""
================================================================
  People's Produce - Password Strength Checker
  Cybersecurity Group Project | Authentication Vulnerability Demo
================================================================
"""

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

SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{}';:\",./<>?\\|`~"


def check_password(password):
    checks = {}
    issues = []
    score  = 0

    # 1. Blacklist
    is_blacklisted = password.lower() in BLACKLISTED_PASSWORDS
    checks["Not a commonly breached password"] = not is_blacklisted
    if is_blacklisted:
        issues.append("Commonly breached password")

    # 2. Minimum length
    has_min_length = len(password) >= 12
    checks["Minimum 12 characters"] = has_min_length
    if not has_min_length:
        issues.append(f"Too short ({len(password)} chars, need 12)")

    # 3. Uppercase
    has_upper = any(c.isupper() for c in password)
    checks["Contains uppercase letter"] = has_upper
    if not has_upper:
        issues.append("No uppercase letter")
    else:
        score += 20

    # 4. Lowercase
    has_lower = any(c.islower() for c in password)
    checks["Contains lowercase letter"] = has_lower
    if not has_lower:
        issues.append("No lowercase letter")
    else:
        score += 20

    # 5. Number
    has_digit = any(c.isdigit() for c in password)
    checks["Contains number"] = has_digit
    if not has_digit:
        issues.append("No number")
    else:
        score += 20

    # 6. Special character
    has_special = any(c in SPECIAL_CHARACTERS for c in password)
    checks["Contains special character"] = has_special
    if not has_special:
        issues.append("No special character")
    else:
        score += 20

    # 7. No repeated chars
    has_repeats = False
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            has_repeats = True
            break
    checks["No repeated character sequences"] = not has_repeats
    if has_repeats:
        issues.append("Repeated characters (e.g. aaa, 111)")
    else:
        score += 20

    # Hard requirements — if blacklisted OR too short, force reject
    hard_fail = is_blacklisted or not has_min_length

    if hard_fail:
        strength = "Weak"
        passed   = False
    else:
        score = min(score, 100)
        if score <= 40:
            strength = "Weak"
        elif score <= 60:
            strength = "Fair"
        elif score <= 80:
            strength = "Strong"
        else:
            strength = "Very Strong"
        passed = score == 100   # must pass all optional checks too

    return {
        "password": password,
        "score":    score if not hard_fail else 0,
        "strength": strength,
        "passed":   passed,
        "checks":   checks,
        "issues":   issues,
    }


def print_result(result):
    pw      = result["password"]
    score   = result["score"]
    passed  = result["passed"]
    checks  = result["checks"]
    issues  = result["issues"]

    filled = round(score / 5)
    bar    = "[" + "#" * filled + "-" * (20 - filled) + "]"
    status = "ACCEPTED" if passed else "REJECTED"

    print()
    print("=" * 54)
    print("  PASSWORD STRENGTH REPORT — PEOPLE'S PRODUCE")
    print("=" * 54)
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
    print("=" * 54)


DEMO_PASSWORDS = [
    ("123456",             "Blacklisted + very short"),
    ("password123",        "Common pattern, blacklisted"),
    ("HelloWor!d",         "Short, missing number"),
    ("helloworld2024!",    "No uppercase letter"),
    ("Fr3sh!Produce#2024", "Strong - meets all criteria"),
    ("T^9kL#mQz@2Xw!pN",  "Very Strong - random and long"),
]

def run_demo():
    print()
    print("=" * 54)
    print("  DEMO — Password Vulnerability Examples")
    print("=" * 54)
    for pw, description in DEMO_PASSWORDS:
        result = check_password(pw)
        status = "ACCEPTED" if result["passed"] else "REJECTED"
        filled = round(result["score"] / 5)
        bar    = "[" + "#" * filled + "-" * (20 - filled) + "]"
        print(f"  {pw:<22}  {bar}  [{status}]")
        print(f"  {'':22}  {description}")
        print()
    print("=" * 54)


def interactive_mode():
    print()
    print("=" * 54)
    print("  People's Produce - Password Checker")
    print("  Type 'demo' for examples, 'quit' to exit")
    print("=" * 54)

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