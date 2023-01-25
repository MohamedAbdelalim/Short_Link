from flask import Flask, jsonify, request
import os
from firebase_admin import credentials, initialize_app, db, firestore
import random
import string

app = Flask(__name__)


cred = credentials.Certificate(os.environ.get("FIREBASE_CRED"))
initialize_app(cred)
db = firestore.client()

@app.route('/shortlinks', methods=['POST'])
def create_shortlink():
    if not request.is_json:
        return jsonify({"error": "Invalid Content-Type, expecting application/json"}), 400

    ios = request.json.get('ios')
    android = request.json.get('android')
    web = request.json.get('web')
    slug = request.json.get('slug')

    if ios is None or android is None or web is None:
        return jsonify({"error": "Missing required targets (ios, android, web) in request body"}), 400

    if slug is None:
        slug = generate_random_slug()
    else:
        if check_slug_exists(slug):
            return jsonify({"error": "Slug already taken"}), 404
        if not is_valid_slug(slug):
            return jsonify({"error": "Invalid slug, only alphanumeric characters are allowed"}), 400

    shortlink_ref = db.collection('shortlinks').document(slug)
    shortlink_ref.set({
        'ios': ios,
        'android': android,
        'web': web
    })

    return jsonify({"slug": slug}), 201

# Generate a random alphanumeric slug
def generate_random_slug():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Check if the slug is alphanumeric
def is_valid_slug(slug):
    return slug.isalnum()

def check_slug_exists(slug):
    shortlink_ref = db.collection('shortlinks').document(slug).get()
    return shortlink_ref.exists


if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)
    app.debug = False
    app.run(host='0.0.0.0', port=port)
