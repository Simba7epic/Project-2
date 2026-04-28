# ──────────────────────────────────────────────
#  Common / Blacklisted Passwords
# ──────────────────────────────────────────────
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
 
 
# ──────────────────────────────────────────────
#  Core Checker
# ──────────────────────────────────────────────
def check_password(password):
    issues      = []
    suggestions = []
    checks      = {}
    score       = 0
 
    # ── 1. Blacklist check ──────────────────────────────────────
    is_blacklisted = password.lower() in BLACKLISTED_PASSWORDS
    checks["not_blacklisted"] = not is_blacklisted
    if is_blacklisted:
        issues.append("Password is in the list of commonly used / breached passwords")
        suggestions.append("Choose a unique password not based on common words or patterns")
    else:
        score += 10
 
    # ── 2. Minimum length (12 chars) ────────────────────────────
    has_min_length = len(password) >= 12
    checks["min_length_12"] = has_min_length
    if not has_min_length:
        issues.append(f"Too short — {len(password)} character(s), minimum is 12")
        suggestions.append("Use at least 12 characters; longer is always better")
    else:
        score += 20
        if len(password) >= 16:
            score += 10
        if len(password) >= 20:
            score += 5
 
    # ── 3. Uppercase letters ────────────────────────────────────
    has_upper = any(c.isupper() for c in password)
    checks["has_uppercase"] = has_upper
    if not has_upper:
        issues.append("No uppercase letters")
        suggestions.append("Add at least one uppercase letter (A-Z)")
    else:
        score += 15
 
    # ── 4. Lowercase letters ────────────────────────────────────
    has_lower = any(c.islower() for c in password)
    checks["has_lowercase"] = has_lower
    if not has_lower:
        issues.append("No lowercase letters")
        suggestions.append("Add at least one lowercase letter (a-z)")
    else:
        score += 15
 
    # ── 5. Numbers ──────────────────────────────────────────────
    has_digit = any(c.isdigit() for c in password)
    checks["has_number"] = has_digit
    if not has_digit:
        issues.append("No numbers")
        suggestions.append("Include at least one number (0-9)")
    else:
        score += 15
 
    # ── 6. Special characters ───────────────────────────────────
    has_special = any(c in SPECIAL_CHARACTERS for c in password)
    checks["has_special_char"] = has_special
    if not has_special:
        issues.append("No special characters")
        suggestions.append("Add symbols like !@#$%^&*")
    else:
        score += 15
 
    # ── 7. No repeating characters (e.g. aaa, 111) ─────────────
    has_repeats = False
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            has_repeats = True
            break
    checks["no_repeating_chars"] = not has_repeats
    if has_repeats:
        issues.append("Contains 3+ repeated characters in a row (e.g. 'aaa', '111')")
        suggestions.append("Avoid repeating the same character multiple times")
    else:
        score += 10
 
    # ── Clamp score ─────────────────────────────────────────────
    score = min(score, 100)
 
    # ── Strength label ──────────────────────────────────────────
    if score <= 20:
        strength = "Very Weak"
    elif score <= 40:
        strength = "Weak"
    elif score <= 60:
        strength = "Fair"
    elif score <= 80:
        strength = "Strong"
    else:
        strength = "Very Strong"
 
    passed = strength in ("Strong", "Very Strong") and not is_blacklisted
 
    return {
        "password":    password,
        "score":       score,
        "strength":    strength,
        "passed":      passed,
        "checks":      checks,
        "issues":      issues,
        "suggestions": suggestions,
    }
 
 
# ──────────────────────────────────────────────
#  Display Result
# ──────────────────────────────────────────────
def print_result(result):
    pw       = result["password"]
    score    = result["score"]
    strength = result["strength"]
    passed   = result["passed"]
    checks   = result["checks"]
    issues   = result["issues"]
    tips     = result["suggestions"]
 
    # Strength bar using simple characters
    filled = round(score / 5)
    bar    = "[" + "#" * filled + "-" * (20 - filled) + "]"
 
    print()
    print("=" * 58)
    print("  PEOPLE'S PRODUCE - PASSWORD STRENGTH REPORT")
    print("=" * 58)
    print(f"  Password : {'*' * len(pw)}  ({len(pw)} characters)")
    print(f"  Score    : {score}/100  {bar}")
    print(f"  Strength : {strength}")
    print(f"  Status   : {'ACCEPTED' if passed else 'REJECTED'}")
 
    # ── Checklist ────────────────────────────────────────────
    print()
    print("  Security Checks:")
    labels = {
        "not_blacklisted":    "Not a commonly breached password",
        "min_length_12":      "Minimum 12 characters",
        "has_uppercase":      "Contains uppercase letter",
        "has_lowercase":      "Contains lowercase letter",
        "has_number":         "Contains number",
        "has_special_char":   "Contains special character",
        "no_repeating_chars": "No repeated character sequences",
    }
    for key, label in labels.items():
        tick = "  [PASS]" if checks.get(key) else "  [FAIL]"
        print(f"{tick}  {label}")
 
    # ── Issues ───────────────────────────────────────────────
    if issues:
        print()
        print("  Issues Found:")
        for issue in issues:
            print(f"    - {issue}")
 
    # ── Suggestions ──────────────────────────────────────────
    if tips:
        print()
        print("  How to improve:")
        for tip in tips:
            print(f"    -> {tip}")
 
    print()
    print("=" * 58)
 
 
# ──────────────────────────────────────────────
#  Demo — shows multiple example passwords
# ──────────────────────────────────────────────
DEMO_PASSWORDS = [
    ("123456",             "Blacklisted + very short"),
    ("password123",        "Common pattern, blacklisted"),
    ("Produce99",          "Short, missing special char"),
    ("MyGr0cery!",         "Close but under 12 chars"),
    ("Fr3sh!Produce#2024", "Strong - meets all criteria"),
    ("T^9kL#mQz@2Xw!pN",  "Very Strong - random and long"),
]
 
def run_demo():
    print()
    print("=" * 58)
    print("  DEMO: People's Produce Password Vulnerability Examples")
    print("=" * 58)
    print("  Showing how passwords the site currently accepts")
    print("  would be rated under a proper security policy.")
    print()
 
    for pw, description in DEMO_PASSWORDS:
        result = check_password(pw)
        status = "ACCEPTED" if result["passed"] else "REJECTED"
        filled = round(result["score"] / 5)
        bar    = "[" + "#" * filled + "-" * (20 - filled) + "]"
        print(f"  {pw:<25}  {bar}  {result['strength']:<12}  [{status}]")
        print(f"  {'':25}  -> {description}")
        print()
 
    print("=" * 58)
    print("  Type a password in interactive mode to test your own.")
    print("=" * 58)
 
 
# ──────────────────────────────────────────────
#  Interactive Mode
# ──────────────────────────────────────────────
def interactive_mode():
    print()
    print("=" * 58)
    print("  People's Produce - Interactive Password Checker")
    print("=" * 58)
    print("  Type a password to check its strength.")
    print("  Type 'demo' to see examples, or 'quit' to exit.")
    print()
 
    while True:
        pw = input("  Enter password: ").strip()
 
        if not pw:
            print("  No password entered. Try again.\n")
            continue
        if pw.lower() == "quit":
            print("\n  Exiting. Stay secure!\n")
            break
        if pw.lower() == "demo":
            run_demo()
            continue
 
        result = check_password(pw)
        print_result(result)
 
 
# ──────────────────────────────────────────────
#  Entry Point
# ──────────────────────────────────────────────
interactive_mode()