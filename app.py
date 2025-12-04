from flask import Flask, request, jsonify
import pyotp
from totp_utils import generate_totp_code, verify_totp_code

app = Flask(__name__)

# Store user secrets in memory (for demo; production → database)
user_secrets = {}

@app.route('/generate-totp', methods=['POST'])
def generate_totp_endpoint():
    data = request.get_json()

    if not data or 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400

    user_id = data["user_id"]

    # Generate or fetch secret
    if user_id not in user_secrets:
        secret = pyotp.random_base32()
        user_secrets[user_id] = secret
    else:
        secret = user_secrets[user_id]

    # Generate TOTP
    totp = pyotp.TOTP(secret)
    otp = totp.now()

    return jsonify({
        'user_id': user_id,
        'otp': otp,
        'secret': secret
    })


@app.route('/verify-totp', methods=['POST'])
def verify_totp_endpoint():
    data = request.get_json()
    if not data or 'user_id' not in data or 'otp' not in data:
        return jsonify({'error': 'user_id and otp are required'}), 400

    user_id = data['user_id']
    code = data['otp']

    if user_id not in user_secrets:
        return jsonify({'error': 'User not found'}), 404

    secret = user_secrets[user_id]

    totp = pyotp.TOTP(secret)
    is_valid = totp.verify(code, valid_window=1)

    return jsonify({
        'user_id': user_id,
        'otp': code,
        'valid': is_valid
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
