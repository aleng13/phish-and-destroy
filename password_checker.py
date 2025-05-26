import re

# Common passwords list
common_passwords = ["123456", "password", "123456789", "qwerty", "abc123"]

# Function to evaluate password with visual feedback and score
def check_password_strength_advanced(password):
    tips = []
    passed_checks = 0
    total_checks = 6

    print("\n🔍 Password Rule Check:")

    # 1. Length Check
    if len(password) >= 8:
        print("✅ Length is 8+ characters")
        passed_checks += 1
    else:
        print("❌ Password is too short (< 8)")
        tips.append("🔴 Make it at least 8 characters long")

    # 2. Digit Check
    if re.search(r"\d", password):
        print("✅ Contains a digit")
        passed_checks += 1
    else:
        print("❌ No digit found")
        tips.append("🔴 Add at least one digit (0–9)")

    # 3. Uppercase Check
    if re.search(r"[A-Z]", password):
        print("✅ Contains an uppercase letter")
        passed_checks += 1
    else:
        print("❌ No uppercase letter found")
        tips.append("🔴 Add an uppercase letter (A–Z)")

    # 4. Lowercase Check
    if re.search(r"[a-z]", password):
        print("✅ Contains a lowercase letter")
        passed_checks += 1
    else:
        print("❌ No lowercase letter found")
        tips.append("🔴 Add a lowercase letter (a–z)")

    # 5. Symbol Check
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        print("✅ Contains a special symbol")
        passed_checks += 1
    else:
        print("❌ No symbol found")
        tips.append("🔴 Include at least one symbol (e.g., @, #, !)")

    # 6. Common Password Check
    if password.lower() not in common_passwords:
        print("✅ Not a common password")
        passed_checks += 1
    else:
        print("❌ Common password detected")
        tips.append("🔴 Avoid common passwords like '123456' or 'password'")

    # Calculate strength score
    score = int((passed_checks / total_checks) * 100)

    # Categorize strength
    if score == 100:
        strength = "🟩 Strong"
    elif score >= 60:
        strength = "🟨 Moderate"
    else:
        strength = "🟥 Weak"

    return strength, tips, score

# 🔁 Keep asking until password is strong
while True:
    test_pw = input("\n🔑 Enter a password to test: ")

    strength, suggestions, score = check_password_strength_advanced(test_pw)

    print(f"\n🔐 Password Strength: {strength} ({score}%)")

    if strength == "🟩 Strong":
        print("✅ Your password is solid! Well done.")
        break
    else:
        print("\n💡 Suggestions to improve:")
        for tip in suggestions:
            print("-", tip)
        print("\n⚠️ Try again.\n")
