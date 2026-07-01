import tkinter as tk
import re
from tkinter import ttk
from tkinter import messagebox



# ---------------- WINDOW ----------------
window = tk.Tk()
#window.iconbitmap("logo.ico")
window.title("PhishGuard - Phishing URL Detection System")
#window.state("zoomed")
window.geometry("1200x800")
window.configure(bg="#0b0f1a")


# ---------------- STYLE ----------------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "green.Horizontal.TProgressbar",
    troughcolor="#1f2937",
    background="#00ff88",
    thickness=20
)


# ---------------- TITLE ----------------
title = tk.Label(
    window,
    text="🛡 PhishGuard",
    font=("Segoe UI", 26, "bold"),
    bg="#0b0f1a",
    fg="#00ff88"
)
title.pack(pady=(15,5))


subtitle = tk.Label(
    window,
    text="Phishing URL Detection System",
    font=("Segoe UI",12),
    fg="#94a3b8",
    bg="#0b0f1a"
)
subtitle.pack()

# ---------------- INPUT FRAME ----------------
input_frame = tk.Frame(
    window,
    bg="#111827",
    padx=20,
    pady=20,
    relief="ridge",
    bd=2
)
input_frame.pack(pady=20)

url_label = tk.Label(
    input_frame,
    text="Enter Website URL",
    font=("Segoe UI",13,"bold"),
    bg="#111827",
    fg="white"
)
url_label.pack()

url_entry = tk.Entry(
    input_frame,
    width=60,
    font=("Segoe UI",12),
    bg="#1e293b",
    fg="white",
    insertbackground="white",
    relief="flat",
    bd=8
)
url_entry.pack(pady=10)

# ---------------- BUTTON FRAME ----------------
button_frame = tk.Frame(window, bg="#0b0f1a")
button_frame.pack()

# ---------------- PROGRESS BAR ----------------
progress = ttk.Progressbar(
    window,
    style="green.Horizontal.TProgressbar",
    length=500,
    mode="determinate"
)
progress.pack(pady=20)

# ---------------- RESULT BOX ----------------
result_box = tk.Text(
    window,
    width=90,
    height=18,
    bg="#111827",
    fg="white",
    font=("Consolas",11),
    relief="flat",
    padx=15,
    pady=15
)
result_box.pack(pady=10)

result_box.tag_config("blue", foreground="#38bdf8")
result_box.tag_config("green", foreground="#22c55e")
result_box.tag_config("red", foreground="#ef4444")
result_box.tag_config("yellow", foreground="#facc15")

# ---------------- STATUS ----------------
status = tk.Label(
    window,
    text="Status : Ready",
    bg="#111827",
    fg="#9ca3af",
    anchor="w"
)
status.pack(fill="x", side="bottom")

# ---------------- ANALYZE FUNCTION ----------------
def analyze():

    url = url_entry.get().strip()

    result_box.delete(1.0, tk.END)

    if url == "":
        messagebox.showwarning(
            "Input Required",
            "Please enter a URL."
        )
        return

    risk_score = 0

    https_status = "✅ Secure"
    ip_status = "✅ No"
    length_status = "✅ Normal"
    extension_status = "✅ Safe"
    keyword_status = "None"

    reasons = []
    found_keywords = []

    keywords = [
        "login",
        "verify",
        "update",
        "account",
        "bank",
        "secure",
        "password",
        "paypal",
        "free"
    ]

    suspicious_tlds = [
        ".xyz",
        ".tk",
        ".top",
        ".click",
        ".loan",
        ".gq",
        ".ml"
    ]

    # HTTPS
    if not url.startswith("https://"):
        risk_score += 1
        https_status = "❌ Not Secure"
        reasons.append("Website does not use HTTPS")

    # IP Address
    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        risk_score += 1
        ip_status = "⚠ Yes"
        reasons.append("Contains an IP address")

    # URL Length
    if len(url) > 60:
        risk_score += 1
        length_status = f"⚠ Long ({len(url)} chars)"
        reasons.append("URL is unusually long")
        # Suspicious Keywords
    for word in keywords:
        if word in url.lower():
            risk_score += 1
            found_keywords.append(word)

    if found_keywords:
        keyword_status = ", ".join(found_keywords)
        reasons.append("Contains suspicious keywords")

    # Suspicious Domain Extension
    for ext in suspicious_tlds:
        if url.lower().endswith(ext):
            risk_score += 1
            extension_status = ext
            reasons.append("Uses suspicious domain extension")

    # Progress Bar
    progress["value"] = min(risk_score * 20, 100)

    # Risk Level
    if risk_score == 0:
        risk = "🟢 LOW"
    elif risk_score <= 2:
        risk = "🟡 MEDIUM"
    else:
        risk = "🔴 HIGH"

    # Status
    status.config(text="Status : Analysis Completed")

    # ---------------- REPORT ----------------
    result_box.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", "blue")
    result_box.insert(tk.END, "🛡 PHISHGUARD SECURITY REPORT\n","blue")
    result_box.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n", "blue")

    result_box.insert(tk.END, f"🔗 URL\n{url}\n\n")

    result_box.insert(tk.END, "✔ SECURITY CHECKS\n", "green")
    result_box.insert(tk.END, "----------------------------------------------\n")

    result_box.insert(tk.END, f"HTTPS Connection : {https_status}\n")
    result_box.insert(tk.END, f"IP Address Used  : {ip_status}\n")
    result_box.insert(tk.END, f"URL Length       : {length_status}\n")
    result_box.insert(tk.END, f"Domain Extension : {extension_status}\n")
    result_box.insert(tk.END, f"Keywords Found   : {keyword_status}\n\n")

    result_box.insert(tk.END, "📊 RISK ANALYSIS\n", "yellow")
    result_box.insert(tk.END, "----------------------------------------------\n")

    result_box.insert(tk.END, f"Risk Score : {risk_score}\n")
    result_box.insert(tk.END, f"Risk Level : {risk}\n\n")

    result_box.insert(tk.END, "⚠ REASONS\n", "red")
    result_box.insert(tk.END, "----------------------------------------------\n")

    if reasons:
        for reason in reasons:
            result_box.insert(tk.END, "• " + reason + "\n")
    else:
        result_box.insert(tk.END, "No suspicious indicators found.\n")

    result_box.insert(tk.END, "\n💡 RECOMMENDATION\n", "green")
    result_box.insert(tk.END, "----------------------------------------------\n")

    if risk_score == 0:
        result_box.insert(tk.END, "✔ URL appears safe.\n")
        result_box.insert(tk.END, "✔ Continue browsing carefully.\n")

    elif risk_score <= 2:
        result_box.insert(tk.END, "⚠ Verify the website before logging in.\n")
        result_box.insert(tk.END, "⚠ Double-check the domain name.\n")

    else:
        result_box.insert(tk.END, "❌ Do NOT enter passwords.\n")
        result_box.insert(tk.END, "❌ Avoid sharing personal information.\n")
        result_box.insert(tk.END, "✔ Visit the official website directly.\n")

    messagebox.showinfo(
        "Analysis Complete",
        f"Risk Level : {risk}"
    )


# ---------------- CLEAR FUNCTION ----------------
def clear():
    url_entry.delete(0, tk.END)
    result_box.delete(1.0, tk.END)
    progress["value"] = 0
    status.config(text="Status : Ready")
def save_report():
    report = result_box.get("1.0", tk.END)

    with open("report.txt", "w", encoding="utf-8") as file:
        file.write(report)

    messagebox.showinfo(
        "Saved",
        "Report saved successfully as report.txt"
    )


# ---------------- BUTTONS ----------------
analyze_button = tk.Button(
    button_frame,
    text="🔍 ANALYZE",
    width=18,
    bg="#00e676",
    fg="black",
    font=("Segoe UI", 12, "bold"),
    cursor="hand2",
    command=analyze
)

clear_button = tk.Button(
    button_frame,
    text="🗑 CLEAR",
    width=18,
    bg="#374151",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    cursor="hand2",
    command=clear
)
save_button = tk.Button(
    button_frame,
    text="SAVE REPORT",
    width=15,
    font=("Segoe UI", 12, "bold"),
    bg="#2563eb",
    fg="white",
    cursor="hand2",
    command=save_report
)

save_button.pack(pady=5)

analyze_button.pack(side="left", padx=10)
clear_button.pack(side="left", padx=10)

# ---------------- RUN ----------------
window.mainloop()
