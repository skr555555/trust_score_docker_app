
import streamlit as st
from real_time_trust import run_real_time_trust, get_latency_score, get_security_score, get_privacy_score
from fuzzy_inference_system import build_fuzzy_system

st.title("Real-Time Cloud Trust Score Evaluator")
st.markdown("Evaluate trustworthiness of a Cloud Service Provider using real-time security, privacy, and performance signals.")

ip = st.text_input("Enter IP address (e.g., 8.8.8.8)", "8.8.8.8")
domain = st.text_input("Enter domain (e.g., https://google.com)", "https://google.com")

if st.button("Evaluate Trust Score"):
    result = run_real_time_trust(ip, domain, log=True)
    st.success(f"Trust Score for {ip}: {result[-1]:.2f}")
    st.write({
        "Security": result[1],
        "Privacy": result[2],
        "Performance": result[3]
    })

if st.button("Compare AWS vs GCP vs Azure"):
    clouds = {
        "AWS": ("13.233.216.226", "https://aws.amazon.com"),
        "GCP": ("34.93.252.116", "https://cloud.google.com"),
        "Azure": ("20.204.56.10", "https://azure.microsoft.com")
    }

    results = []
    for name, (ip, url) in clouds.items():
        sec = get_security_score(ip)
        priv = get_privacy_score(url)
        perf = get_latency_score(ip)
        fuzzy = build_fuzzy_system()
        fuzzy.input['security'] = sec
        fuzzy.input['privacy'] = priv
        fuzzy.input['performance'] = perf
        fuzzy.compute()
        score = round(fuzzy.output['trust_score'], 2)
        results.append((name, sec, priv, perf, score))

    st.subheader("CSP Comparison Table")
    st.table(results)
