import os
import json
import flask
import nacl.signing
import nacl.exceptions

app = flask.Flask(__name__)

# Replace with your Discord public key from the Developer Portal
DISCORD_PUBLIC_KEY = "a940cde2195470fea81d21d9fa3be90c7c4ff0ad7e307a29cdc0b4e236b4ecfe"

@app.route("/", methods=["GET", "POST"])
def interactions():
    if flask.request.method == "GET":
        return "Flask is working!"

    # Verify the request signature
    signature = flask.request.headers.get("X-Signature-Ed25519")
    timestamp = flask.request.headers.get("X-Signature-Timestamp")
    body = flask.request.data.decode("utf-8")

    try:
        verify_key = nacl.signing.VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
    except nacl.exceptions.BadSignatureError:
        return "Invalid request signature", 401

    payload = flask.request.json

    # Respond to Discord's initial ping
    if payload["type"] == 1:
        return flask.jsonify({"type": 1})

    # Respond to /ping command
    if payload["type"] == 2 and payload["data"]["name"] == "whatvaradhan":
        return flask.jsonify({
            "type": 4,
            "data": {
                "content": "VARADHAN IS NOT OG " * 23
            }
        })

    return "Unhandled", 400

if __name__ == "__main__":
    app.run(port=5000)
