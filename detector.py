import subprocess
from collections import defaultdict

failed_attempts = defaultdict(int)
THRESHOLD = 3

print("\n🔍 Analyzing system logs...\n")

# Run journalctl command
result = subprocess.run(
    ["journalctl"],
    capture_output=True,
    text=True
)

logs = result.stdout.split("\n")

for line in logs:
    if "Failed password" in line:
        try:
            ip = line.split()[-1]
            failed_attempts[ip] += 1
        except:
            continue

print("🚨 Suspicious IPs:\n")

found = False

for ip, count in failed_attempts.items():
    if count > THRESHOLD:
        print(f"⚠️  IP: {ip} | Attempts: {count}")
        found = True

if not found:
    print("✅ No brute-force attack detected.")

# Save attackers to file
with open("attackers.txt", "w") as f:
    for ip, count in failed_attempts.items():
        if count > THRESHOLD:
            f.write(f"{ip} - {count} attempts\n")

print("\n📁 Attackers saved to attackers.txt\n")
