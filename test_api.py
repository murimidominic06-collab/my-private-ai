import requests

r = requests.post("http://127.0.0.1:5000/api/chat",
  headers={"x-api-key": "nairobi-ai-2024-secret-xyz"},
  json={"message": "nipe code ya snake game"})

print(r.json())