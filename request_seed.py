import requests
import json

# ===============================
# CONFIGURATION
# ===============================
STUDENT_ID = "23P31A12B0"
GITHUB_REPO_URL = "https://github.com/N-Haritha16/HarithaNallamilli_PKI_2FA_Microservice"
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"  # Replace with actual API URL

# Public key in a single-line string with \n for newlines
PUBLIC_KEY = (
    "-----BEGIN PUBLIC KEY-----\n"
    "MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAuoHwzhrj5mJwTKiczMkmdCTTe2FdqzovavMq2+G7VR+io3FGGeiprZ8or3vA1DIPtICo9y32d8Je+MdJ9q2F9EztbKn/sYZAPW8fgF97GXTCxM9KIXG4SqjtEjdKl3yCLwlKJ0CMzQV2Wn5n5ovtu19zMPAPDpKutEd2E2k8rkMamtqwPrL8n3GG1NBWSlWBmvfmoTqaAtw9eqJsUky7N7KliyUWB46FYjwtvnXAIdV4Iz0LT/XWhKOADxoWZ7071sxLP9DKe3QDpwR47mQ9WQJUHvmGNBTgMflgn0SPDpT/HKHXjmfP6E7gRR470TQHLc1jP1xcw0WkoxHoY2n2vBarZu9CFo+X12zbO0jbvH4sco+FQHn2Au4apPvX3tmKCqkQ+iIVsD+FwVoMydcWfy/wTA5fiqyW9Q8TtP9BTGGtMpJuYU30/lUx16xKoMz7C0h0GK18oF1aipOlbU3Gsp70JNnbosRASh09A0zQslmvkVhDGBQjwhLs7O6HuJzeaGeeH6mPZquromF9RWg55yQWIM9TWaAksgT2W5UxfzR39irwRof1xYvaZdJqUI0SLfke2GD8t7xjItnDLsnBMsb9zkZzh4EX7essjcrCZXRb/cl0kOBax4JwaDdlaN8EwcDKywv/fiousOHHgTGKse5o6P4FPqvwyYPPRWgalgMCAwEAAQ==\n"
    "-----END PUBLIC KEY-----"
)

# ===============================
# FUNCTION TO REQUEST ENCRYPTED SEED
# ===============================
def request_seed(student_id: str, github_repo_url: str, public_key: str, api_url: str):
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    print("===== DEBUGGING PAYLOAD =====")
    print(json.dumps(payload, indent=2))
    print("=============================")

    try:
        response = requests.post(api_url, json=payload, timeout=10)

        print("\n===== RESPONSE =====")
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")
        print("===================")

        if response.status_code == 200:
            data = response.json()
            if "encrypted_seed" in data:
                with open("encrypted_seed.txt", "w") as f:
                    f.write(data["encrypted_seed"])
                print("Encrypted seed saved to 'encrypted_seed.txt'.")
            else:
                print("Error: 'encrypted_seed' not found in response.")
        else:
            print("Error: Server returned", response.status_code)
            print("Check API key, student ID, GitHub repo URL, and public key format.")

    except requests.RequestException as e:
        print("Request failed:", e)


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    print("Sending request to instructor API...")
    request_seed(STUDENT_ID, GITHUB_REPO_URL, PUBLIC_KEY, API_URL)
