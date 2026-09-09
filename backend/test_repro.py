import requests

url = "http://localhost:8001/api/v1/analyze"
with open("data/pmay/RevisedFAQ_PMAY.pdf", "rb") as f:
    files = {"file": ("RevisedFAQ_PMAY.pdf", f, "application/pdf")}
    data = {"lang": "en", "provider": "ollama"}
    resp = requests.post(url, files=files, data=data)

print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")
