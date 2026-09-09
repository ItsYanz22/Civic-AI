import requests
from PIL import Image

# Create a dummy image
img = Image.new('RGB', (100, 30), color = (73, 109, 137))
img.save('test_img.png')

url = "http://localhost:8001/api/v1/analyze"
with open("test_img.png", "rb") as f:
    files = {"file": ("test_img.png", f, "image/png")}
    data = {"lang": "en", "provider": "ollama"}
    resp = requests.post(url, files=files, data=data)

print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")
