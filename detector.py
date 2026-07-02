import re
print("====================================")
print("     PHISHING URL DETECTOR")
print("====================================")

url = input("Enter a URL: ")
risk_score = 0
https_status = "✅ Yes"
ip_status = "✅ No"
length_status = "✅ Normal"
extension_status = "✅ Normal"
keyword_count = 0

# List of suspicious words
suspicious_words = [
    "login",
    "verify",
    "update",
    "account",
    "secure",
    "bank",
    "paypal",
    "password"
]
suspicious_extensions = [
    ".xyz",
    ".top",
    ".tk",
    ".ml",
    ".cf",
    ".gq"
]
print("\nChecking for suspicious keywords...")
keyword_count = 0
for word in suspicious_words:
    if word in url.lower():
        print("⚠️ Suspicious keyword:", word)
        keyword_count += 1
        risk_score += 1
print("\nChecking URL...")
print("Checking for IP address...")

if re.search(r"\d+\.\d+\.\d+\.\d+", url):
    ip_status = "⚠️ Yes"
    risk_score += 1
print("\nChecking URL length...")

if len(url) > 50:
    length_status = "⚠️ Long"
    risk_score += 1
print("\nChecking domain extension...")

for ext in suspicious_extensions:
    if url.lower().endswith(ext):
        extension_status = "⚠️ Suspicious"
        print("⚠️ Suspicious domain extension:", ext)
        risk_score += 1
# Check whether the URL uses HTTPS
if not url.startswith("https://"):
    https_status = "❌ No"
    risk_score += 1
print("\n====================================")
print("      PHISHING URL REPORT")
print("====================================")

print(f"URL                 : {url}")
print(f"HTTPS               : {https_status}")
print(f"IP Address          : {ip_status}")
print(f"URL Length          : {length_status}")
print("Domain Extension    :", extension_status)
print(f"Keywords Found      : {keyword_count}")

print("------------------------------------")
print(f"Risk Score          : {risk_score}")

if risk_score == 0:
    print("Risk Level          : 🟢 LOW")
elif risk_score <= 2:
    print("Risk Level          : 🟡 MEDIUM")
else:
    print("Risk Level          : 🔴 HIGH")

print("------------------------------------")
print("Analysis Complete!")
if risk_score == 0:
    risk_level = "LOW"
elif risk_score <= 2:
    risk_level = "MEDIUM"
else:
    risk_level = "HIGH"
with open("report.txt", "w", encoding="utf-8") as file:
    file.write("PHISHING URL REPORT\n")
    file.write("=========================\n")
    file.write(f"URL: {url}\n")
    file.write(f"HTTPS: {https_status}\n")
    file.write(f"IP Address: {ip_status}\n")
    file.write(f"URL Length: {length_status}\n")
    file.write(f"Domain Extension: {extension_status}\n")
    file.write(f"Keywords Found: {keyword_count}\n")
    file.write(f"Risk Score: {risk_score}\n")
    file.write(f"Risk Level: {risk_level}\n")

print("📄 Report saved as report.txt")
