from flask import Flask, request, jsonify
import base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA

app = Flask(__name__)

# 🔹 Chaves RSA geradas automaticamente
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# Chave AES
AES_KEY = b"SuaChaveSecreta1"

# Funções de Criptografia AES
def encrypt_AES(text):
    cipher = AES.new(AES_KEY, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    return base64.b64encode(bytes(iv) + encrypted_bytes).decode()

def decrypt_AES(encrypted_text):
    encrypted_data = base64.b64decode(encrypted_text)
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    decrypted_bytes = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)
    return decrypted_bytes.decode()

# Funções de Criptografia RSA
def encrypt_RSA(text):
    recipient_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(recipient_key)
    encrypted_bytes = cipher.encrypt(text.encode())
    return base64.b64encode(encrypted_bytes).decode()

def decrypt_RSA(encrypted_text):
    private_key_obj = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(private_key_obj)
    encrypted_data = base64.b64decode(encrypted_text)
    decrypted_bytes = cipher.decrypt(encrypted_data)
    return decrypted_bytes.decode()

@app.route("/send_message", methods=["POST"])
def send_message():
    """Usuário envia uma mensagem criptografada"""
    data = request.json
    if not data or "message" not in data or "method" not in data:
        return jsonify({"error": "JSON inválido ou campos ausentes"}), 400

    method = data["method"]

    if method == "AES":
        encrypted_text = encrypt_AES(data["message"])
    elif method == "RSA":
        encrypted_text = encrypt_RSA(data["message"])
    else:
        return jsonify({"error": "Método de criptografia inválido"}), 400

    return jsonify({"encrypted_message": encrypted_text})

@app.route("/receive_message", methods=["POST"])
def receive_message():
    """Usuário recebe a mensagem e a descriptografa automaticamente"""
    data = request.json
    if not data or "encrypted_message" not in data or "method" not in data:
        return jsonify({"error": "JSON inválido ou campo 'encrypted_message' ausente"}), 400

    method = data["method"]

    if method == "AES":
        decrypted_text = decrypt_AES(data["encrypted_message"])
    elif method == "RSA":
        decrypted_text = decrypt_RSA(data["encrypted_message"])
    else:
        return jsonify({"error": "Método de criptografia inválido"}), 400

    return jsonify({"decrypted_message": decrypted_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
