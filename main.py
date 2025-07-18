import os
import json
import flask
import nacl.signing
import nacl.exceptions

app = flask.Flask(__name__)
DISCORD_PUBLIC_KEY = "a940cde2195470fea81d21d9fa3be90c7c4ff0ad7e307a29cdc0b4e236b4ecfe"

@app.route("/", methods=["GET", "POST"])
def interactions():
    if flask.request.method == "GET":
        return "Render Flask is working!", 200

    # Step 1: Capture headers
    signature = flask.request.headers.get("X-Signature-Ed25519")
    timestamp = flask.request.headers.get("X-Signature-Timestamp")

    if not signature or not timestamp:
        return "Missing signature headers", 400

    # Step 2: Get raw body
    body = flask.request.data.decode("utf-8")

    # Step 3: Verify signature
    try:
        verify_key = nacl.signing.VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
    except nacl.exceptions.BadSignatureError:
        return "Invalid request signature", 401

    # Step 4: Parse payload
    try:
        payload = flask.request.json
    except Exception:
        return "Invalid JSON", 400

    # Step 5: Handle Discord handshake
    if payload.get("type") == 1:
        return flask.jsonify({"type": 1}), 200

    # Step 6: Respond to slash command
    if payload.get("type") == 2 and payload.get("data", {}).get("name") == "whatvaradhan":
        return flask.jsonify({
            "type": 4,
            "data": {
                "content": "VARADHAN IS NOT OG " * 23
            }
        }), 200

    return "Unhandled", 400

# ✅ Render's port config — this line is key!
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
