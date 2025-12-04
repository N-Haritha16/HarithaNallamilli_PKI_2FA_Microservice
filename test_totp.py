import requests

# Flask endpoint
url = "http://127.0.0.1:5000/generate-totp"

# Data to send
data = {"user_id": "23P31A12B0"}

# Make POST request
response = requests.post(url, json=data)

# Print the JSON response
print(response.json())
