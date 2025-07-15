
import subprocess
import re
import sys
import csv
from fuzzy_inference_system import build_fuzzy_system

# 🟢 Dynamic latency-to-performance scoring using ping
def get_latency_score(host="8.8.8.8"):
    try:
        output = subprocess.check_output(["ping", "-c", "4", host], universal_newlines=True)
        avg_line = [line for line in output.split("\n") if "avg" in line or "rtt" in line][0]
        avg_ms = float(re.findall(r'=\s[\d\.]+/([\d\.]+)', avg_line)[0])
    except Exception as e:
        print(f"⚠️ Ping failed for {host}: {e}")
        avg_ms = 1000  # fallback value
    return max(100 - avg_ms / 5, 10)  # linear inverse scoring (higher latency = lower score)

# 🔐 Basic security scoring using nmap
def get_security_score(host="8.8.8.8"):
    try:
        result = subprocess.run(["nmap", "-F", host], capture_output=True, text=True)
        open_ports = result.stdout.count("/open/")
        total_ports = result.stdout.count("tcp")
        score = max(min(100 - (open_ports * 5 + total_ports * 2), 100), 10)
        return score
    except Exception as e:
        print(f"⚠️ nmap failed: {e}")
        return 50

# 🔏 Privacy score using headers from curl
def get_privacy_score(host="https://google.com"):
    try:
        result = subprocess.run(["curl", "-sI", host], capture_output=True, text=True)
        headers = result.stdout.lower()
        score = 0
        if "strict-transport-security" in headers: score += 30
        if "x-frame-options" in headers: score += 30
        if "x-xss-protection" in headers: score += 30
        return score if score > 0 else 10
    except Exception as e:
        print(f"⚠️ curl failed: {e}")
        return 10

# 🧠 Full real-time pipeline
def run_real_time_trust(ip="8.8.8.8", web="https://google.com", log=False):
    performance_score = get_latency_score(ip)
    security_score = get_security_score(ip)
    privacy_score = get_privacy_score(web)

    trust_score = 50
    try:
        fuzzy = build_fuzzy_system()
        fuzzy.input['security'] = security_score
        fuzzy.input['privacy'] = privacy_score
        fuzzy.input['performance'] = performance_score
        fuzzy.compute()
        trust_score = fuzzy.output['trust_score']
    except Exception as e:
        print(f"⚠️ Fuzzy system failed: {e}")

    row = [ip, security_score, privacy_score, performance_score, round(trust_score, 2)]
    if log:
        with open("trust_scores.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)
    return row
